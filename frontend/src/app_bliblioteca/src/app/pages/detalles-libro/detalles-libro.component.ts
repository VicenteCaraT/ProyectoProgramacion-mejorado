import { Component, Input, OnInit } from '@angular/core';
import { LibrosService } from '../../services/books/libros.service';
import { ActivatedRoute, Router } from '@angular/router';
import { PrestamosService } from '../../services/loans/prestamos.service';
import { ReseñasService } from '../../services/reviews/reseñas.service';
import { RegisterModalComponent } from '../../components/modals/register-modal/register-modal.component';
import { MatDialog } from '@angular/material/dialog';
import { SysNotificationService } from '../../services/sys-notifications/sys-notification.service';
import { Location } from '@angular/common';

@Component({
  selector: 'app-detalles-libro',
  templateUrl: './detalles-libro.component.html',
  styleUrl: './detalles-libro.component.css'
})
export class DetallesLibroComponent implements OnInit{
  book: any; 
  reviews: any[] = [];
  currentPage: number = 1;
  totalPages: number = 1;

  constructor(
    private bookService: LibrosService,
    private loanService: PrestamosService,
    private reviewService: ReseñasService,
    private route: ActivatedRoute,
    private router: Router,
    private dialog: MatDialog,
    private location: Location,
    private sysNotificationService: SysNotificationService
  ) {}

  ngOnInit(): void {
    const bookId = this.route.snapshot.paramMap.get('id');

    if (bookId) {
      this.bookService.getBooksById(Number(bookId)).subscribe(
        (data) => {
          this.book = data;
          this.getBookReviews(Number(bookId));
        },
        (error) => {
          console.log('Error al obtener los detalles del libro: ', error);
        }
      );
    }
  }

  getBookReviews(id: number): void {
    const params = { idLibro: this.book.id };
    this.reviewService.getReviews(1, params).subscribe(
      (reviewsResponse) => {
        this.reviews = (reviewsResponse as any).reseñas;
      },
      (error) => {
        console.error('Error al obtener las reseñas del libro: ', error);
      }
    );
  }

  solicitarPrestamo(): void {
    const tokenUserId = localStorage.getItem('user_id');
    const tokenJWT = localStorage.getItem('token');

    if (!tokenUserId || !tokenJWT) {
      const dialogRef = this.dialog.open(RegisterModalComponent, {
        width: '400px',
      });

      dialogRef.afterClosed().subscribe(result => {
        if (result === 'signup') {
          this.router.navigate(['/signup']);
        }
      });
      return;
    }

    const prestamoData = {
      usuario: tokenUserId,
      libro: [this.book.id]
    };

    this.loanService.postLoan(prestamoData).subscribe({
      next: (response) => {
        this.sysNotificationService.showSuccess('Préstamo solicitado con éxito');
      },
      error: (error) => {
        const msg = error?.error?.message || 'Error al solicitar el préstamo';
        this.sysNotificationService.showError(msg);
      }
    });
  }
  goBack() {
    this.location.back()
  }

  changePage(newPage: number): void {
    if (newPage >= 1 && newPage <= this.totalPages) {
      this.currentPage = newPage;
      this.getBookReviews(this.currentPage);
    }
  }

}
