import { HttpClient, HttpParams } from '@angular/common/http';
import { Injectable } from '@angular/core';
import { first } from 'rxjs';
import { Reseña, ReseñaResponse, ReseñasResponse } from '../../models/models';
import { environment } from '../../../environments/environment';
import { buildParams } from '../../utils/http-params';

@Injectable({
  providedIn: 'root'
})
export class ReseñasService {
  url = environment.apiUrl

  constructor(
    private httpClient: HttpClient
  ) { }

  getReviews(page: number, params?: {nroValoracion?:string, ordenValoracion?:string, idUserPost?:string, fechaReseña?:string, Valoraciones_desc?:string, Valoraciones_asc?:string, idLibro?: string, titulo_libro?:string, nombre_usuario?:string}){
    const httpParams = buildParams(page, params);
    return this.httpClient.get<ReseñasResponse>(`${this.url}/reseñas`, {params: httpParams}).pipe(first())
  }

  getReviewById(id: number) {
    return this.httpClient.get<Reseña>(`${this.url}/reseña/${id}`).pipe(first())
  }

  postReview(reviewData:any) {
    return this.httpClient.post<ReseñaResponse>(`${this.url}/reseñas`, reviewData).pipe(first())
  }

  updateReview(id: number, reviewData: any) {
    return this.httpClient.put<ReseñaResponse>(`${this.url}/reseña/${id}`, reviewData).pipe(first())
  }

  deleteReview(id: number) {
    return this.httpClient.delete<void>(`${this.url}/reseña/${id}`).pipe(first())
  }
}
