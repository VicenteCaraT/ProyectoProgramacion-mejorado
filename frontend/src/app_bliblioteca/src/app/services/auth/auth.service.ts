import { Injectable } from '@angular/core';
import { HttpClient } from '@angular/common/http';
import { Router } from '@angular/router';
import { Observable, first } from 'rxjs';
import { LoginRequest, LoginResponse } from '../../models/models';
import { environment } from '../../../environments/environment';

@Injectable({
  providedIn: 'root'
})
export class AuthService {
  url = environment.apiUrl

  constructor(
    private httpClient: HttpClient,
    private router: Router
  ) { }

  login(dataLogin: LoginRequest) : Observable<LoginResponse> {
    return this.httpClient.post<LoginResponse>(this.url + '/auth/login', dataLogin).pipe(first())
  }

  logout() {
    localStorage.removeItem('token');
    localStorage.removeItem('token_rol')
    localStorage.removeItem('user_id')
    this.router.navigateByUrl("login")
  }
}
