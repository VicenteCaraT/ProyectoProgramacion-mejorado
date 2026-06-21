import { HttpClient, HttpHeaders, HttpParams } from '@angular/common/http';
import { Injectable } from '@angular/core';
import { Observable, first } from 'rxjs';
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
    let auth_token = localStorage.getItem('token')
    const headers = new HttpHeaders({
      'Content-Type': 'application/json',
      'Authorization': `Bearer ${auth_token}`
    })
    let httpParams = new HttpParams().set('page', page.toString());

    if (params?.usuario) {
      httpParams = httpParams.set('usuario', params.usuario);
    }

    return this.httpClient.get<NotificacionesResponse>(`${this.url}/notificaciones`, {headers: headers, params: httpParams})
  }

  getNotificationByIs(id: number) {
    let auth_token = localStorage.getItem('token')
    const headers = new HttpHeaders({
      'Content-Type': 'application/json',
      'Authorization': `Bearer ${auth_token}`
    })
    return this.httpClient.get<Notificacion>(`${this.url}/notificacion/${id}`, {headers: headers}).pipe(first())
  }

  deleteNotification(id: number) {
    let auth_token = localStorage.getItem('token')
    const headers = new HttpHeaders({
      'Content-Type': 'application/json',
      'Authorization': `Bearer ${auth_token}`
    })
    return this.httpClient.delete<void>(`${this.url}/notificacion/${id}`, {headers: headers}).pipe(first())
  }

}
