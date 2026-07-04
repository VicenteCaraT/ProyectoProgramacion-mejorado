import { HttpClient, HttpParams } from '@angular/common/http';
import { Injectable } from '@angular/core';
import { first } from 'rxjs';
import { Prestamo, PrestamoResponse, PrestamosResponse } from '../../models/models';
import { environment } from '../../../environments/environment';
import { buildParams } from '../../utils/http-params';

@Injectable({
  providedIn: 'root'
})
export class PrestamosService {
  url = environment.apiUrl

  constructor(
    private httpClient: HttpClient,
  ) { }

  getLoans(page: number, params?: {idUsuario?:string, nombre_usuario?:string, inicio_prestamo?:string, fin_prestamo?:string, cant_libros?:string, libro_id?:string, cant_prestamos?:string, estado?:string, orden?:string, titulo_libro?:string}) {
    const httpParams = buildParams(page, params, { titulo_libro: 'titulo' });
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
