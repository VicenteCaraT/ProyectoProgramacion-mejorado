import { HttpClient, HttpParams } from '@angular/common/http';
import { Injectable } from '@angular/core';
import { first } from 'rxjs';
import { Guardado, GuardadoResponse, GuardadosResponse } from '../../models/models';

@Injectable({
  providedIn: 'root'
})
export class GuardadosService {
  url = '/api'

  constructor(
    private httpClient: HttpClient,
  ) { }

  getSaves(page: number, params?: {idUsuario?: string, libro_id?: string}) {
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
    return this.httpClient.get<GuardadosResponse>(`${this.url}/guardados`, {params:httpParams}).pipe(first())
  }

  getSavesById(id: number) {
    return this.httpClient.get<Guardado>(`${this.url}/guardado/${id}`).pipe(first())
  }

  postSaves(saveData: any) {
    return this.httpClient.post<GuardadoResponse>(`${this.url}/guardados`, saveData).pipe(first())
  }

  deleteSave(id: number) {
    return this.httpClient.delete<void>(`${this.url}/guardado/${id}`).pipe(first())
  }
}
