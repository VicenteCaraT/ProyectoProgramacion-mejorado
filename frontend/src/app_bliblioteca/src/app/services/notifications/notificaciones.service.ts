import { HttpClient, HttpParams } from '@angular/common/http';
import { Injectable } from '@angular/core';
import { first } from 'rxjs';
import { Notificacion, NotificacionesResponse } from '../../models/models';

@Injectable({
  providedIn: 'root'
})
export class NotificacionesService {
  url = '/api'

  constructor(
    private httpClient: HttpClient,
  ) { }

  getNotifications(page: number, params?: {usuario:string}) {
    let httpParams = new HttpParams().set('page', page.toString());

    if (params?.usuario) {
      httpParams = httpParams.set('usuario', params.usuario);
    }

    return this.httpClient.get<NotificacionesResponse>(`${this.url}/notificaciones`, {params: httpParams})
  }

  getNotificationByIs(id: number) {
    return this.httpClient.get<Notificacion>(`${this.url}/notificacion/${id}`).pipe(first())
  }

  deleteNotification(id: number) {
    return this.httpClient.delete<void>(`${this.url}/notificacion/${id}`).pipe(first())
  }

}
