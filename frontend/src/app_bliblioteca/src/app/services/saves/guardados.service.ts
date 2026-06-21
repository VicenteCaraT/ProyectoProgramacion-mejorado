import { HttpClient, HttpHeaders, HttpParams } from '@angular/common/http';
import { Injectable } from '@angular/core';
import { first } from 'rxjs';
import { Guardado, GuardadoResponse, GuardadosResponse } from '../../models/models';

@Injectable({
  providedIn: 'root'
})
export class GuardadosService {
  url = '/api'
  private guardadosLibroIds: number[] = [];

  constructor(
    private httpClient: HttpClient,
  ) { }

  getSaves(page: number, params?: {idUsuario?: string, libro_id?: string}) {
    let auth_token = localStorage.getItem('token')
    const headers = new HttpHeaders({
      'Content-Type': 'application/json',
      'Authorization': `Bearer ${auth_token}`
    })
    let httpParams = new HttpParams().set('page', page.toString());

    if(params) {
      if(params.idUsuario) {
        httpParams = httpParams.set('idUsuario', params.idUsuario)
      }
    }
    if(params) {
      if(params.libro_id) {
        httpParams = httpParams.set('libro_id', params.libro_id)
      }
    }
    return this.httpClient.get<GuardadosResponse>(`${this.url}/guardados`, {headers: headers, params:httpParams}).pipe(first())
  }

  getSavesById(id: number) {
    let auth_token = localStorage.getItem('token')
    const headers = new HttpHeaders({
      'Content-Type': 'application/json',
      'Authorization': `Bearer ${auth_token}`
    })
    return this.httpClient.get<Guardado>(`${this.url}/guardado/${id}`, {headers: headers}).pipe(first())
  }

  postSaves(saveData: any) {
        let auth_token = localStorage.getItem('token')
    const headers = new HttpHeaders({
      'Content-Type': 'application/json',
      'Authorization': `Bearer ${auth_token}`
    })
    return this.httpClient.post<GuardadoResponse>(`${this.url}/guardados`, saveData, {headers: headers}).pipe(first())
  }

  deleteSave(id: number) {
    let auth_token = localStorage.getItem('token')
    const headers = new HttpHeaders({
      'Content-Type': 'application/json',
      'Authorization': `Bearer ${auth_token}`
    })
    return this.httpClient.delete<void>(`${this.url}/guardado/${id}`, {headers: headers}).pipe(first())
  }
}
