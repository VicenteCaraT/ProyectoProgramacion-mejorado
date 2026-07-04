import { Component, Inject } from '@angular/core';
import { MAT_DIALOG_DATA, MatDialogRef } from '@angular/material/dialog';
import { FormBuilder, FormGroup, Validators } from '@angular/forms';
import { AuthService } from '../../../../services/auth/auth.service';

@Component({
  selector: 'app-editar-perfil',
  templateUrl: './editar-perfil.component.html',
  styleUrl: './editar-perfil.component.css'
})
export class EditarPerfilComponent {
  formPerfil!: FormGroup;
  
  constructor(
    private formBuilder: FormBuilder,
    public dialogRef: MatDialogRef<EditarPerfilComponent>,
    @Inject(MAT_DIALOG_DATA) public data: any,
    private authService: AuthService
  ) {
    this.formPerfil = this.formBuilder.group({
      user: ['', Validators.required],
      contraseña: ['', Validators.required],
      nombre: ['', Validators.required],
      apellido: ['', Validators.required],
      dni: ['', Validators.required],
      telefono: ['', Validators.required],
      email: ['', Validators.required],
      rol: ['', Validators.required],
    })
  }

  isAdmin() { return this.authService.isAdmin() }
  
  closeModal(): void {
    this.dialogRef.close()
  }

  handleSave(formData: any): void {
    this.dialogRef.close(formData);
  }

  saveChanges(): void {
    if (this.formPerfil.valid) {
      this.handleSave(this.formPerfil.value)
    }
  }
}
