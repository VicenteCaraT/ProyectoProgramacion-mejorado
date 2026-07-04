import { HttpClient, HttpParams } from '@angular/common/http';
import { Injectable } from '@angular/core';
import { Observable, first } from 'rxjs';
import { Libro, LibroResponse, LibrosResponse } from '../../models/models';
import { environment } from '../../../environments/environment';
import { buildParams } from '../../utils/http-params';

@Injectable({
  providedIn: 'root'
})
export class LibrosService {
  url = environment.apiUrl

  constructor(
    private httpClient: HttpClient
  ) { }

  getBooks(page: number, params?: {genero?:string, autor?:string, titulo?:string, editorial?:string, orden?:string, sin_stock?:string}) {
    const httpParams = buildParams(page, params);
    return this.httpClient.get<LibrosResponse>(`${this.url}/libros`, {params: httpParams}).pipe(first())
  }

  getBooksById(id : number)  {
    return this.httpClient.get<Libro>(`${this.url}/libro/${id}`).pipe(first())
  }

  postBook(bookData:any) {
    return this.httpClient.post<LibroResponse>(`${this.url}/libros`, bookData).pipe(first())
  }

  updateBook(id: number, bookData: any) {
    return this.httpClient.put<LibroResponse>(`${this.url}/libro/${id}`, bookData).pipe(first())
  }

  deleteBook(id: number) {
    return this.httpClient.delete<void>(`${this.url}/libro/${id}`).pipe(first())
  }
}
