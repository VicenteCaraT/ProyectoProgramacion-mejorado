import { HttpClient, HttpParams } from '@angular/common/http';
import { Injectable } from '@angular/core';
import { Observable, first } from 'rxjs';
import { Usuario, UsuarioResponse, UsuariosResponse } from '../../models/models';

@Injectable({
  providedIn: 'root'
})
export class UsuariosService {
  url = '/api'

  constructor(
    private httpClient: HttpClient
  ) { }

  getUsers(page: number, params?: {rol?:string, nombre?:string, dni?:string, telefono?:string, email?:string, estado?: string}) {
    let httpParams = new HttpParams().set('page', page.toString());

    if (params) {
      if (params.rol) {
        httpParams = httpParams.set('rol', params.rol)
      }
    }
    if (params) {
      if (params.nombre) {
        httpParams = httpParams.set('nombre', params.nombre)
      }
    }
    if (params) {
      if (params.dni) {
        httpParams = httpParams.set('dni', params.dni)
      }
    }
    if (params) {
      if (params.telefono) {
        httpParams = httpParams.set('telefono', params.telefono)
      }
    }
    if (params) {
      if (params.email) {
        httpParams = httpParams.set('email', params.email)
      }
    }
    if (params) {
      if (params.estado) {
        httpParams = httpParams.set('estado', params.estado)
      }
    }
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
