import { Component, OnInit } from '@angular/core';
import { ReseñasService } from '../../services/reviews/reseñas.service';
import { SysNotificationService } from '../../services/sys-notifications/sys-notification.service';
import { ActivatedRoute } from '@angular/router';
import { MatDialog } from '@angular/material/dialog';
import { AbmModalComponent } from '../../components/modals/abm-modal/abm-modal.component';
import { Reseña, ReseñasResponse } from '../../models/models';

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

  reviewList: Reseña[] = [];
  filteredReviews: Reseña[] = [];
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
    this.reviewService.getReviews(page, params).subscribe((rta: ReseñasResponse) => {
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
          this.sysNotificationService.showSuccess('Reseña eliminada correctamente')
          this.fetchReviews(this.currentPage, this.currentFilter);
        },
        error: (err) => {
          console.error('Error al eliminar el libro', err)
          this.sysNotificationService.showError('Error al eliminar la reseña')
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

  handleSearch(query:string) {
    if (query) {
      const lowerQuery = query.toLowerCase();

      const paramsList = [
        { titulo_libro: query },
        { nombre_usuario: query }
      ];

      const allResults: Reseña[] = [];
      const seenIds = new Set<number>();
      let pending = paramsList.length;

      for ( const params of paramsList) {
        this.reviewService.getReviews(1, params).subscribe(
          (response: ReseñasResponse) => {
            if (response && response.reseñas) {
              for (const reseña of response.reseñas) {
                if(!seenIds.has(reseña.id)) {
                  seenIds.add(reseña.id);
                  allResults.push(reseña)
                }
              }
            }
            pending--;
            if(pending === 0) {
              this.filteredReviews = allResults;
            }
          },
          (error) => {
            console.error('Error de búsqueda', error);
            pending--;
            if (pending === 0) {
              this.filteredReviews = allResults;
            }
          }
        );
      }
    } else {
      this.filteredReviews = [...this.reviewList]
    }
  }

  handleFilterChange(option: { type: string, value: string }): void {
    this.currentPage = 1;

    if (option.value === '') {
      this.currentFilter = null;
      this.fetchReviews(this.currentPage);
    } else {
      this.currentFilter = { type: option.type, value: option.value };
      const filterParams = { [option.type]: option.value };
      this.fetchReviews(this.currentPage, filterParams);
    }
  }
}
