import { Component, EventEmitter, Input, Output } from '@angular/core';
import { AuthService } from '../../services/auth/auth.service';

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

  constructor(private authService: AuthService) {}

  isAdminOrReview() {
    return this.authService.isAdmin() || this.isReviewPage;
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
