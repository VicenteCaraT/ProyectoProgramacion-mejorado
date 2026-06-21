import { HttpClient, HttpParams } from '@angular/common/http';
import { Injectable } from '@angular/core';
import { first } from 'rxjs';
import { Prestamo, PrestamoResponse, PrestamosResponse } from '../../models/models';

@Injectable({
  providedIn: 'root'
})
export class PrestamosService {
  url = '/api'

  constructor(
    private httpClient: HttpClient,
  ) { }

  getLoans(page: number, params?: {idUsuario?:string, nombre_usuario?:string, inicio_prestamo?:string, fin_prestamo?:string, cant_libros?:string, libro_id?:string, cant_prestamos?:string, estado?:string, orden?:string, titulo_libro?:string}) {
    let httpParams = new HttpParams().set('page', page.toString());

    if (params) {
      if (params.idUsuario) {
        httpParams = httpParams.set('idUsuario', params.idUsuario)
      }
    }

    if (params) {
      if (params.nombre_usuario) {
        httpParams = httpParams.set('nombre_usuario', params.nombre_usuario)
      }
    }

    if (params) {
      if (params.inicio_prestamo) {
        httpParams = httpParams.set('inicio_prestamo', params.inicio_prestamo)
      }
    }

    if (params) {
      if (params.fin_prestamo) {
        httpParams = httpParams.set('fin_prestamo', params.fin_prestamo)
      }
    }

    if (params) {
      if (params.cant_libros) {
        httpParams = httpParams.set('cant_libros', params.cant_libros)
      }
    }

    if (params) {
      if (params.libro_id) {
        httpParams = httpParams.set('libro_id', params.libro_id)
      }
    }

    if (params) {
      if (params.titulo_libro) {
        httpParams = httpParams.set('titulo', params.titulo_libro)
      }
    }

    if (params) {
      if (params.cant_prestamos) {
        httpParams = httpParams.set('cant_prestamos', params.cant_prestamos)
      }
    }

    if (params) {
      if (params.estado) {
        httpParams = httpParams.set('estado', params.estado)
      }
    }

    if (params) {
      if (params.orden) {
        httpParams = httpParams.set('orden', params.orden)
      }
    }
    return this.httpClient.get<PrestamosResponse>(`${this.url}/prestamos`, {params:httpParams}).pipe(first())
  }

  getLoanById(id: number) {
    return this.httpClient.get<Prestamo>(`${this.url}/prestamo/${id}`).pipe(first())
  } 

  postLoan(loanData:any) {
    return this.httpClient.post<PrestamoResponse>(`${this.url}/prestamos`, loanData).pipe(first())
  }

  updateLoan(id: number, loanData: any) {
    return this.httpClient.put<PrestamoResponse>(`${this.url}/prestamo/${id}`, loanData).pipe(first())
  }

  deleteLoan(id: number) {
    return this.httpClient.delete<void>(`${this.url}/prestamo/${id}`).pipe(first())
  }

  patchLoans() {
  return this.httpClient
    .patch<{message: string}>(`${this.url}/prestamos`, {})
    .pipe(first());
}
}
