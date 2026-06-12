import { Component, EventEmitter, Input, Output } from '@angular/core';

@Component({
  selector: 'app-edit-delete',
  templateUrl: './edit-delete.component.html',
  styleUrl: './edit-delete.component.css'
})
export class EditDeleteComponent {
  @Input() userRol: string = '';
  @Input() loanStatus: string = '';
  @Input() isReviewPage: boolean = false;
  @Output() editDelete = new EventEmitter<string>();


  isAdminOrReview() {
    const tokenRol = localStorage.getItem('token_rol');

    // Mostrar botones si es Admin o si es la página de reseñas
    if ((tokenRol && tokenRol.includes("Admin")) || this.isReviewPage) {
      return true;
    } else {
      return false;
    }
  }

  isPending() {
    return this.userRol === 'Pendiente' || this.loanStatus === 'Pendiente';
  }

  emitEditClick(){
    this.editDelete.emit('edit')
  }

  emitDeleteClick() {
    this.editDelete.emit('delete')
  }

  emitAcceptClick() {
    this.editDelete.emit('accept')
  }

  emitDeclineClick() {
    this.editDelete.emit('decline')
  }

}
