import { Component, EventEmitter, Output } from '@angular/core';
import { AuthService } from '../../services/auth/auth.service';

@Component({
  selector: 'app-add-icon',
  templateUrl: './add-icon.component.html',
  styleUrl: './add-icon.component.css'
})
export class AddIconComponent {
  @Output() addEvent = new EventEmitter<void>();

  constructor(
    private authService: AuthService
  ) { }

  isAdmin() { return this.authService.isAdmin() }

  addClick() {
    this.addEvent.emit();
  }
}