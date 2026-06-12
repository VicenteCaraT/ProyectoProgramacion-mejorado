import { Injectable } from '@angular/core';
import { MatSnackBar } from '@angular/material/snack-bar';

@Injectable({
  providedIn: 'root'
})
export class SysNotificationService {

  constructor(private snackBar: MatSnackBar) { }

  showSuccess(message: string): void {
    this.snackBar.open(message, 'Cerrar', {
      duration:3000,
      panelClass: ['snackbar-success']
    });
  }

  showError(message: string): void {
    this.snackBar.open(message, 'Cerrar', {
      duration: 4000,
      panelClass: ['snackbar-error']
    })
  }
}
