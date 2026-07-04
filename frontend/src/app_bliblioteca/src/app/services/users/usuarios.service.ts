import { HttpClient, HttpParams } from '@angular/common/http';
import { Injectable } from '@angular/core';
import { Observable, first } from 'rxjs';
import { Usuario, UsuarioResponse, UsuariosResponse } from '../../models/models';
import { environment } from '../../../environments/environment';
import { buildParams } from '../../utils/http-params';

@Injectable({
  providedIn: 'root'
})
export class UsuariosService {
  url = environment.apiUrl

  constructor(
    private httpClient: HttpClient
  ) { }

  getUsers(page: number, params?: {rol?:string, nombre?:string, dni?:string, telefono?:string, email?:string, estado?: string}) {
    const httpParams = buildParams(page, params);
    return this.httpClient.get<UsuariosResponse>(`${this.url}/usuarios`, {params: httpParams}).pipe(first())
  }

  getUserById(id: number) {
    return this.httpClient.get<Usuario>(`${this.url}/usuario/${id}`).pipe(first())
  }

  postUser(userData:any) {
    return this.httpClient.post<UsuarioResponse>(`${this.url}/usuarios`, userData)
  }

  updateUser(id: number, userData: any) {
    return this.httpClient.put<UsuarioResponse>(`${this.url}/usuario/${id}`, userData).pipe(first())
  }

  deleteUser(id: number) {
    return this.httpClient.delete<void>(`${this.url}/usuario/${id}`).pipe(first())
  }

}
