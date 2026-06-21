import { Injectable } from '@angular/core';
import { HttpClient } from '@angular/common/http';
import { Router } from '@angular/router';
import { Observable, take } from 'rxjs';
import { LoginRequest, LoginResponse } from '../../models/models';

@Injectable({
  providedIn: 'root'
})
export class AuthService {
  url = '/api'

  constructor(
    private httpClient: HttpClient,
    private router: Router
  ) { }

  login(dataLogin: LoginRequest) : Observable<LoginResponse> {
    return this.httpClient.post<LoginResponse>(this.url + '/auth/login', dataLogin).pipe(take(1))
  }

  logout() {
    localStorage.removeItem('token');
    localStorage.removeItem('token_rol')
    localStorage.removeItem('user_id')
    this.router.navigateByUrl("login")
  }
}
