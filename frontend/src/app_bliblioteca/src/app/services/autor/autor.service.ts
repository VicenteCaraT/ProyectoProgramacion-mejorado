import { HttpClient, HttpHeaders, HttpParams } from '@angular/common/http';
import { Injectable } from '@angular/core';
import { Observable, first } from 'rxjs';

@Injectable({
  providedIn: 'root'
})
export class AutorService {
  url = '/api'

  constructor(
    private httpClient: HttpClient
  ) { }

  getAutores(page: number, params?: {nombre?:string, apellido?:string, apodo?:string}) {
    let auth_token = localStorage.getItem('token')
    const headers = new HttpHeaders({
      'Content-Type': 'application/json',
      'Authorization': `Bearer ${auth_token}`
    })
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
    return this.httpClient.get(`${this.url}/autores`, {headers: headers, params:httpParams}).pipe(first())
  }

  getAutorById(id: number) {
    let auth_token = localStorage.getItem('token')
    const headers = new HttpHeaders({
      'Content-Type': 'application/json',
      'Authorization': `Bearer ${auth_token}`
    })
    return this.httpClient.get(`${this.url}/autor/${id}`, {headers: headers}).pipe(first())
  } 

  postAutor(autorData:any) {
    let auth_token = localStorage.getItem('token')
    const headers = new HttpHeaders({
      'Content-Type': 'application/json',
      'Authorization': `Bearer ${auth_token}`
    })
    console.log(autorData)
    return this.httpClient.post(`${this.url}/autores`, autorData, {headers: headers}).pipe(first())
  }

  updateAutor(id: number, autorData: any) {
    let auth_token = localStorage.getItem('token')
    const headers = new HttpHeaders({
      'Content-Type': 'application/json',
      'Authorization': `Bearer ${auth_token}`
    })
    console.log(autorData)
    return this.httpClient.put(`${this.url}/autor/${id}`, autorData, {headers: headers}).pipe(first())
  }

  deleteAutor(id: number) {
    let auth_token = localStorage.getItem('token')
    const headers = new HttpHeaders({
      'Content-Type': 'application/json',
      'Authorization': `Bearer ${auth_token}`
    })
    return this.httpClient.delete(`${this.url}/autor/${id}`, {headers: headers}).pipe(first())
  }
}
