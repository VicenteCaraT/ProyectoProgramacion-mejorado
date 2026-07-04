import { Component, OnInit } from '@angular/core';
import { AuthService } from '../../services/auth/auth.service';
import { UsuariosService } from '../../services/users/usuarios.service';
import { RegisterModalComponent } from '../modals/register-modal/register-modal.component';
import { MatDialog } from '@angular/material/dialog';
import { Router } from '@angular/router';
import { Usuario } from '../../models/models';

@Component({
  selector: 'app-navbar',
  templateUrl: './navbar.component.html',
  styleUrl: './navbar.component.css'
})
export class NavbarComponent implements OnInit{
  user: Usuario | null = null;

  constructor(
    private authService: AuthService,
    private usuarioService: UsuariosService,
    private dialog: MatDialog, 
    private router: Router
  ) { }

  ngOnInit(): void {
      this.loadUserData();
  }

  loadUserData(){
    const userId = this.authService.getUserId();
    if (userId) {
      this.usuarioService.getUserById(Number(userId)).subscribe({
        next: (userData) => {
          this.user = userData;
        },
        error: () => {}
      });
    }
  }

  isAdmin() { return this.authService.isAdmin() }

  isUser() { return this.authService.isUser() }

  checkUser(event: Event): void {
    const tokenJWT = this.authService.getToken();

    if (tokenJWT) {
      // Si hay un token, redirigir a /perfil
      this.router.navigate(['/perfil']);
    } else {
      // Evitar el comportamiento por defecto del enlace
      event.preventDefault();
      
      // Mostrar un modal para registrarse
      const dialogRef = this.dialog.open(RegisterModalComponent, {
        width: '400px',
        data: { message: 'Debe registrarse o iniciar sesión para acceder a su perfil.' }
      });

      dialogRef.afterClosed().subscribe(result => {
        if (result === 'signup') {
          // Redirigir al formulario de registro
          this.router.navigate(['/signup']);
        }
      });
    }
  }
}