import { Component, OnInit } from '@angular/core';
import { ReseñasService } from '../../services/reviews/reseñas.service';
import { SysNotificationService } from '../../services/sys-notifications/sys-notification.service';
import { ActivatedRoute } from '@angular/router';

@Component({
  selector: 'app-review',
  templateUrl: './review.component.html',
  styleUrl: './review.component.css'
})
export class ReviewComponent implements OnInit{

  constructor(
    private reviewService: ReseñasService,
    private sysNotificationService: SysNotificationService,
    private route: ActivatedRoute
  ) {}

  reviewList: any[] = [];
  filteredReviews: any[] = [];
  currentPage: number = 1;
  totalPages: number = 1;
  
  ngOnInit(): void {
    const tokenRol = localStorage.getItem('token_rol');
    const tokenUserId = localStorage.getItem('user_id');
    const routeUserId = this.route.snapshot.queryParamMap.get('idUsuario')

    const params = tokenRol === 'Usuario' && tokenUserId ? { idUserPost: tokenUserId } : routeUserId ? { idUserPost: routeUserId } : {};    
    this.fetchReviews(this.currentPage, params);
  }

  fetchReviews(page: number, params?: { idUserPost?: string, idLibro?: string }): void {
    this.reviewService.getReviews(page, params).subscribe((rta: any) => {
      console.log('Reseñas API: ', rta);
      this.reviewList = rta.reseñas || [];
      this.filteredReviews = [...this.reviewList];
      this.totalPages = rta.pages;
    });
  }

  changePage(page: number): void {
    if (page >= 1 && page <= this.totalPages) {
      this.currentPage = page;
      this.fetchReviews(this.currentPage);
    }
  }

  handleActionEvent(event: { action: string, review: any }) {
    if (event.action === 'delete') {
      this.reviewService.deleteReview(event.review.id).subscribe({
        next: () => {
          this.sysNotificationService.showSuccess('Usuario eliminado correctamente')
          this.fetchReviews(this.currentPage)
        },
        error: (err) => {
          console.error('Error al eliminar el usuario', err)
          this.sysNotificationService.showError('Error al eliminar el usuario')
        }
      });
    }   
  }
}
