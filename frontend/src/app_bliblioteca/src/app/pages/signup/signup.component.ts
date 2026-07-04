import { Component } from '@angular/core';
import { FormBuilder, FormGroup, Validators } from '@angular/forms';
import { Router } from '@angular/router';
import { AuthService } from '../../services/auth/auth.service';
import { RegisterService } from '../../services/auth/register.service';
import { Usuario } from '../../models/models';
import { onlyLetters, onlyNumbers, allowOnlyLetters, allowOnlyNumbers } from '../../utils/validators';

@Component({
  selector: 'app-signup',
  templateUrl: './signup.component.html',
  styleUrl: './signup.component.css'
})
export class SignupComponent {
  signInForm!: FormGroup;

  constructor(
      private authService: AuthService,
      private registerService: RegisterService,
      private router: Router,
      private formBuilder: FormBuilder
  ) {
    this.signInForm = this.formBuilder.group({
      user: ['', Validators.required],
      contraseña: ['', Validators.required],
      nombre: ['', [Validators.required, onlyLetters]],
      apellido: ['', [Validators.required, onlyLetters]],
      dni: ['', [Validators.required, onlyNumbers]],
      telefono: ['', [Validators.required, onlyNumbers]],
      email: ['', Validators.required],
    })
  }

  register(registerData: any) {
    this.registerService.register(registerData).subscribe({
      next: (rta: Usuario) => {
        alert('Registro Exitoso');
        this.router.navigateByUrl('login')
      }, error: (err) => {
        alert('Error al Registrarse');
      }
    })
  }

  submit() { 
    if (this.signInForm.valid) {
      const registerData = {
        ...this.signInForm.value,
        img: 'assets/user.jpeg',
        rol: 'Pendiente',
        estado: false
      };
      this.register(registerData);
    } else {
      alert('Todos los campos son requeridos');
    }   
  }

  allowOnlyLetters = allowOnlyLetters;

  allowOnlyNumbers = allowOnlyNumbers;
}
