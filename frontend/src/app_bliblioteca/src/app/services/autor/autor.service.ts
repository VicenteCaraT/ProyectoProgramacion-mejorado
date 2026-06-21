import { HttpClient, HttpParams } from '@angular/common/http';
import { Injectable } from '@angular/core';
import { first } from 'rxjs';
import { Autor, AutorResponse, AutoresResponse } from '../../models/models';

@Injectable({
  providedIn: 'root'
})
export class AutorService {
  url = '/api'

  constructor(
    private httpClient: HttpClient
  ) { }

  getAutores(page: number, params?: {nombre?:string, apellido?:string, apodo?:string}) {
    let httpParams = new HttpParams().set('page', page.toString());

    if (params) {
      if (params.nombre) {
        httpParams = httpParams.set('nombre', params.nombre)
      }
    }
    
    if (params) {
      if (params.apellido) {
        httpParams = httpParams.set('apellido', params.apellido)
      }
    }

    if (params) {
      if (params.apodo) {
        httpParams = httpParams.set('apodo', params.apodo)
      }
    }
    return this.httpClient.get<AutoresResponse>(`${this.url}/autores`, {params:httpParams}).pipe(first())
  }

  getAutorById(id: number) {
    return this.httpClient.get<AutorResponse>(`${this.url}/autor/${id}`).pipe(first())
  } 

  postAutor(autorData:any) {
    return this.httpClient.post<AutorResponse>(`${this.url}/autores`, autorData).pipe(first())
  }

  updateAutor(id: number, autorData: any) {
    return this.httpClient.put<AutorResponse>(`${this.url}/autor/${id}`, autorData).pipe(first())
  }

  deleteAutor(id: number) {
    return this.httpClient.delete<void>(`${this.url}/autor/${id}`).pipe(first())
  }
}
