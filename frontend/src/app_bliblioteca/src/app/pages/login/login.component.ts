import { Component } from '@angular/core';
import { AuthService } from '../../services/auth/auth.service'
import { Router } from '@angular/router';
import { FormBuilder, FormGroup, Validators } from '@angular/forms';
import { jwtDecode } from 'jwt-decode';
import { LoginResponse, JwtPayload } from '../../models/models';

@Component({
  selector: 'app-login',
  templateUrl: './login.component.html',
  styleUrl: './login.component.css'
})
export class LoginComponent {
  loginForm!: FormGroup;

  constructor(
      private authService: AuthService,
      private router: Router,
      private formBuilder: FormBuilder
  ) {
    this.loginForm = this.formBuilder.group({
      email: ['', Validators.required],
      contraseña: ['', Validators.required]
    })
  }

  irLogin(dataLogin: any) {
    this.authService.login(dataLogin).subscribe({
      next: (rta: LoginResponse) => {
        console.log('Exito: ', rta);

        localStorage.setItem('token', rta.access_token);

        let tokenPayload: JwtPayload = jwtDecode<JwtPayload>(rta.access_token);
        localStorage.setItem('token_rol', tokenPayload.rol);
        localStorage.setItem('user_id', tokenPayload.id);
        localStorage.setItem('estado_user', String(tokenPayload.estado))

        // Si el usuario tiene rol "Pendiente" no puede entrar a la pagina
        if (tokenPayload.rol === 'Pendiente' || tokenPayload.estado === true) {
          alert(tokenPayload.rol === 'Pendiente'
            ? 'Su usuario debe ser aceptado por un administrador.'
            : 'Su usuario se encuentra bloqueado.');
          
          localStorage.removeItem('token');
          localStorage.removeItem('token_rol');
          localStorage.removeItem('user_id');
          localStorage.removeItem('estado_user');
        } else {
          this.router.navigateByUrl('home');
        }
      }, error: (err) => {
        alert('Usuario o constraseña Incorrecta');
        console.log('Error: ' + err);
        localStorage.removeItem('token');
      }, complete: () => {
        console.log('Finalizo');
      }
    })
  }

  submit() { 
    if(this.loginForm.valid) {
      console.log('Dato del formulario: ', this.loginForm.value);
      this.irLogin(this.loginForm.value);
    } else {
      alert('Los valores son requeridos');
    }   
  }
}
