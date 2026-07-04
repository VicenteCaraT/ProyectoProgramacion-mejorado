import { HttpClient, HttpParams } from '@angular/common/http';
import { Injectable } from '@angular/core';
import { first } from 'rxjs';
import { Guardado, GuardadoResponse, GuardadosResponse } from '../../models/models';
import { environment } from '../../../environments/environment';
import { buildParams } from '../../utils/http-params';

@Injectable({
  providedIn: 'root'
})
export class GuardadosService {
  url = environment.apiUrl

  constructor(
    private httpClient: HttpClient,
  ) { }

  getSaves(page: number, params?: {idUsuario?: string, libro_id?: string}) {
    const httpParams = buildParams(page, params);
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
