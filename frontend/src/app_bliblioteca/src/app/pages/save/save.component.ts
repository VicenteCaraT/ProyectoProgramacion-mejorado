import { Component, OnInit } from '@angular/core';
import { GuardadosService } from '../../services/saves/guardados.service';
import { Router } from '@angular/router';

@Component({
  selector: 'app-save',
  templateUrl: './save.component.html',
  styleUrl: './save.component.css'
})
export class SaveComponent implements OnInit{
  bookList: any[] = [];
  filteredBook: any[] = [];
  currentPage: number = 1;
  totalPages: number = 1;
  userId: string | undefined;

  constructor(
    private guardadosService: GuardadosService,
    private router: Router
  ) {}

  ngOnInit(): void {
    this.userId = localStorage.getItem('user_id') ?? undefined;
    this.fetchSaves(this.currentPage);
  }

    fetchSaves(page: number): void {
      if (!this.userId) return;
      this.guardadosService.getSaves(page, { idUsuario: this.userId }).subscribe({
        next: (res: any) => {
          console.log("Guardados:", res);
          this.bookList = res.guardados.map((item: any) => item.libro);
          this.filteredBook = [...this.bookList];
          this.totalPages = res.pages || 1;
        },
        error: (err) => {
          console.error("Error al obtener guardados:", err);
        }
      });
  }

    goToBook(bookID: string) {
    this.router.navigate(['/libro', bookID])
  }

    changePage(newPage: number): void {
    if (newPage >= 1 && newPage <= this.totalPages) {
      this.currentPage = newPage;
      this.fetchSaves(this.currentPage);
    }
  }
}
