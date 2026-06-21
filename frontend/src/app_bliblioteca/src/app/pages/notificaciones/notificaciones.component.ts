import { Component, OnInit } from '@angular/core';
import { NotificacionesService } from '../../services/notifications/notificaciones.service';
import { Notificacion, NotificacionesResponse } from '../../models/models';

@Component({
  selector: 'app-notificaciones',
  templateUrl: './notificaciones.component.html',
  styleUrl: './notificaciones.component.css'
})
export class NotificacionesComponent implements OnInit {
  notifications: Notificacion[] = []; 
  userID: string = '';
  currentPage: number = 1;
  totalPages: number = 1;

  constructor(private notificationService: NotificacionesService) {}

  ngOnInit(): void {
    this.userID = localStorage.getItem('user_id') || '';
    this.getNotifications(this.currentPage);
  }

  getNotifications(page: number) {
    this.notificationService.getNotifications(page, { usuario: this.userID })
      .subscribe((rta: NotificacionesResponse) => {
        this.notifications = rta.notificaciones || [];
        this.totalPages = rta.pages || 1;
      });
  }

  changePage(newPage: number) {
    if (newPage >= 1 && newPage <= this.totalPages) {
      this.currentPage = newPage;
      this.getNotifications(this.currentPage);
    }
  }

  deleteNotification(id: number) {
    this.notificationService.deleteNotification(id).subscribe({
      next: () => this.getNotifications(this.currentPage),
      error: (error) => console.error('Error al eliminar la notificación', error)
    });
  }
}