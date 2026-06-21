import { Injectable } from '@angular/core';
import { HttpClient } from '@angular/common/http';
import { Router } from '@angular/router';
import { Observable, take } from 'rxjs';
import { Usuario } from '../../models/models';

@Injectable({
  providedIn: 'root'
})
export class RegisterService {
  url = '/api'
  constructor(
    private httpClient: HttpClient,
    private router: Router
  ) { }

  register (dataRegister: any): Observable<Usuario>{
    return this.httpClient.post<Usuario>(this.url + '/auth/register', dataRegister).pipe(take(1))
  }
}
