import { Component, Inject } from '@angular/core';
import { MatDialogRef, MAT_DIALOG_DATA } from '@angular/material/dialog';
import { FormBuilder, FormGroup, Validator, Validators, ValidatorFn } from '@angular/forms';

const onlyLetters: ValidatorFn = Validators.pattern(/^[a-zA-ZáéíóúÁÉÍÓÚñÑ\s]+$/);
const onlyNumbers: ValidatorFn = Validators.pattern(/^\d+$/);

@Component({
  selector: 'app-abm-modal',
  templateUrl: './abm-modal.component.html',
  styleUrl: './abm-modal.component.css'
})
export class AbmModalComponent {
  formEntity!: FormGroup;
  formTitle: string = '';
  formOperation: string = '';

  constructor(
    private formBuilder: FormBuilder,
    public dialogRef: MatDialogRef<AbmModalComponent>,
    @Inject(MAT_DIALOG_DATA) public data: any
  ) {
    this.formOperation = this.data.formOperation || 'create';
    this.formControl(this.data.formType);
  }

  formControl(formType: string): void {
    switch (formType) {
      case 'book':
        this.formTitle = this.formOperation === 'edit' ? 'Editar Libro' : 'Agregar Libro';
        this.formEntity = this.formBuilder.group({
          img: [this.data.img || '', Validators.required],
          titulo: [this.data.titulo || '', Validators.required],
          cantidad: [this.data.cantidad || '', [Validators.required, onlyNumbers]],
          autor: [this.formOperation === 'edit' ? this.data.autor[0].id : '', [Validators.required, onlyNumbers]],
          editorial: [this.data.editorial || '', Validators.required],
          genero: [this.data.genero || '', Validators.required],
          sinopsis: [this.data.sinopsis || '', Validators.required],
        });
        break;
      case 'loan':
        this.formTitle = this.formOperation === 'edit' ? 'Editar Préstamo' : 'Crear Prestamo';
        this.formEntity = this.formBuilder.group({
          usuario: [this.formOperation === 'edit' ? this.data.usuario.id : '', [Validators.required, onlyNumbers]],
          libro: [this.formOperation === 'edit' ? this.data.libro[0].id : '', [Validators.required, onlyNumbers]],
          inicio_prestamo: [this.formatDate(this.data.inicio_prestamo) || '', Validators.required],
          fin_prestamo: [this.formatDate(this.data.fin_prestamo) || '', Validators.required],
          estado: [this.data.estado || '', Validators.required]
        })
        break;
      case 'user':
        this.formTitle = this.formOperation === 'edit' ? 'Editar Usuario' : 'Agregar Usuario';
        this.formEntity = this.formBuilder.group({
          user: [this.data.user || '', Validators.required],
          ...(this.formOperation !== 'edit' && {contraseña: ['', Validators.required]}),
          nombre: [this.data.nombre || '', [Validators.required, onlyLetters]],
          apellido: [this.data.apellido || '', [Validators.required, onlyLetters]],
          dni: [this.data.dni || '', [Validators.required, onlyNumbers]],
          telefono: [this.data.telefono || '', [Validators.required, onlyNumbers]],
          email: [this.data.email || '', Validators.required],
          rol: [this.data.rol || '', Validators.required],
          img: [this.data.img || '', Validators.required],
          estado: [this.data.estado || '', Validators.required],
        })
        break;
      case 'review':
        if (this.formOperation === 'edit') {
          this.formTitle = 'Editar Reseña';
          const valoracionNum = this.data.valoracion ? parseInt(this.data.valoracion.split('/')[0]) : '';
          // Define el formulario solo para editar reseña
          this.formEntity = this.formBuilder.group({
        usuario: [this.data.usuario?.id || '', [Validators.required, onlyNumbers]],
        libro: [this.data.libro?.id || '', [Validators.required, onlyNumbers]],
        descripcion: [this.data.descripcion || '', Validators.required],
        valoracionNum: [valoracionNum, [Validators.required, Validators.min(1), Validators.max(5), onlyNumbers]]
          });
        } else {
          throw new Error('Solo se permite editar reseñas');
        }
        break;
        case 'autor':
          this.formTitle = this.formOperation === 'edit' ? 'Editar Autor' : 'Agregar Autor';
          this.formEntity = this.formBuilder.group({
            nombre: [this.data.nombre || '', [Validators.required, onlyLetters]],
            apellido: [this.data.apellido || '', [Validators.required, onlyLetters]],
            apodo: [this.data.apodo || '', Validators.required]
          });
        break;

      default:
        throw new Error('Tipo de formulario desconocido');
    }
  }

  isAdmin() { 
    const tokenRol = localStorage.getItem('token_rol');
  if (tokenRol && tokenRol.includes("Admin")) {
    return true;
  } else {
    return false;
  }
  }

  closeModal(): void {
    this.dialogRef.close(null);
  }

  handleSave(formData: any): void {
    this.dialogRef.close(formData);
  }

  formatDate(dateString: string | undefined): string {
    if (!dateString || !dateString.includes('-')) return '';
    const [day, month, year] = dateString.split('-');
    return `${year}-${month}-${day}`;
  }

  saveChanges(): void {
    if (this.formEntity.valid) {
      const formData = { ...this.formEntity.value };

      if (this.data.formType === 'loan') {
        formData.inicio_prestamo = this.formatDate(formData.inicio_prestamo);
        formData.fin_prestamo = this.formatDate(formData.fin_prestamo);

        formData.libro = [formData.libro];
      }

      console.log('Formulario enviado:', formData);
      this.handleSave(formData);
    }
  }

  allowOnlyLetters(event: KeyboardEvent) {
    const pattern = /^[a-zA-ZáéíóúÁÉÍÓÚñÑ\s]*$/;
    const inputChar = String.fromCharCode(event.keyCode || event.which);
    if (!pattern.test(inputChar)) {
      event.preventDefault();
    }
  }

  allowOnlyNumbers(event: KeyboardEvent) {
    const pattern = /^[0-9]*$/;
    const inputChar = String.fromCharCode(event.keyCode || event.which);
    if (!pattern.test(inputChar)) {
      event.preventDefault();
    }
  }
}
