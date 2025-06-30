import { Component, OnInit } from '@angular/core';
import { ReseñasService } from '../../services/reviews/reseñas.service';
import { SysNotificationService } from '../../services/sys-notifications/sys-notification.service';
import { ActivatedRoute } from '@angular/router';
import { MatDialog } from '@angular/material/dialog';
import { AbmModalComponent } from '../../components/modals/abm-modal/abm-modal.component';

@Component({
  selector: 'app-review',
  templateUrl: './review.component.html',
  styleUrl: './review.component.css'
})
export class ReviewComponent implements OnInit{

  constructor(
    private reviewService: ReseñasService,
    private sysNotificationService: SysNotificationService,
    private route: ActivatedRoute,
    private dialog: MatDialog
  ) {}

  reviewList: any[] = [];
  filteredReviews: any[] = [];
  currentPage: number = 1;
  totalPages: number = 1;

  currentFilter: { type: string, value: string } | null = null;
  baseParams: any = {};

  
  ngOnInit(): void {
    const tokenRol = localStorage.getItem('token_rol');
    const tokenUserId = localStorage.getItem('user_id');
    const routeUserId = this.route.snapshot.queryParamMap.get('idUsuario')

    this.baseParams = tokenRol === 'Usuario' && tokenUserId ? { idUserPost: tokenUserId }: routeUserId ? { idUserPost: routeUserId }: {};
    this.fetchReviews(1, this.baseParams);
  }

  fetchReviews(page: number, extraParams: any = {}): void {
    const params = {...this.baseParams, ...extraParams}
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
      const filterParams =this.currentFilter ? { [this.currentFilter.type]: this.currentFilter.value }: {};
      this.fetchReviews(this.currentPage, filterParams);
    }
  }

  handleActionEvent(event: { action: string, review: any }) {
    if (event.action === 'edit') {
      this.openABMReviewModal(event.review, 'edit');
    } else if (event.action === 'delete') {
      this.reviewService.deleteReview(event.review.id).subscribe({
        next: () => {
          this.sysNotificationService.showSuccess('Libro eliminado correctamente')
          this.fetchReviews(this.currentPage, this.currentFilter);
        },
        error: (err) => {
          console.error('Error al eliminar el libro', err)
          this.sysNotificationService.showError('Error al eliminar el libro')
        }
      })
    }
  }

  openABMReviewModal(reviewData: any, operation: string): void {
      const dialogRef = this.dialog.open(AbmModalComponent, {
        width: '500px',
        data: {
          formType: 'review',
          formOperation: operation,
          ...reviewData
        } 
      });
      dialogRef.afterClosed().subscribe(result => {
        console.log('El modal se cerro', result);

        if (result && operation === 'edit') {
          const valoracionFinal = `${result.valoracionNum}/5`;
          const payload = {
            ...result,
            valoracion: valoracionFinal
          };
          delete payload.valoracionNum;
          this.reviewService.updateReview(reviewData.id, payload).subscribe({
            next: () => {
              this.sysNotificationService.showSuccess('Reseña editada correctamente')
              this.fetchReviews(this.currentPage, this.currentFilter);
            },
            error: () => {
              this.sysNotificationService.showError('Error al editar la reseña')
            }
          });
        }
      });
    }
}
