import { HttpClient, HttpParams } from '@angular/common/http';
import { Injectable } from '@angular/core';
import { first } from 'rxjs';
import { Notificacion, NotificacionesResponse } from '../../models/models';
import { environment } from '../../../environments/environment';
import { buildParams } from '../../utils/http-params';

@Injectable({
  providedIn: 'root'
})
export class NotificacionesService {
  url = environment.apiUrl

  constructor(
    private httpClient: HttpClient,
  ) { }

  getNotifications(page: number, params?: {usuario:string}) {
    const httpParams = buildParams(page, params);
    return this.httpClient.get<NotificacionesResponse>(`${this.url}/notificaciones`, {params: httpParams}).pipe(first())
  }

  getNotificationByIs(id: number) {
    return this.httpClient.get<Notificacion>(`${this.url}/notificacion/${id}`).pipe(first())
  }

  deleteNotification(id: number) {
    return this.httpClient.delete<void>(`${this.url}/notificacion/${id}`).pipe(first())
  }

}
