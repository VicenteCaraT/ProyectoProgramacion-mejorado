import { Component, OnInit } from '@angular/core';
import { LibrosService } from '../../services/books/libros.service';
import { Router } from '@angular/router';
import { Libro, LibrosResponse } from '../../models/models';

@Component({
  selector: 'app-top',
  templateUrl: './top.component.html',
  styleUrl: './top.component.css'
})
export class TopComponent implements OnInit{

  constructor(
    private bookService: LibrosService,
    private router: Router
  ) {}

  bookList: Libro[] = [];
  filteredBook: Libro[] = [];
  currentPage: number = 1;
  totalPages: number = 1;

  ngOnInit(): void {
    this.fetchTopBooks(1);
  }

  fetchTopBooks(page: number): void {
    this.bookService.getBooks(page, { orden: 'ranking' }).subscribe((rta: LibrosResponse) => {
      console.log("Libros API:", rta);
      this.bookList = rta.libros || [];
      this.filteredBook = [...this.bookList];
      this.totalPages = rta.pages;
    });
  }

  changePage(newPage: number): void {
    if (newPage >= 1 && newPage <= this.totalPages) {
      this.currentPage = newPage;
      this.fetchTopBooks(this.currentPage);
    }
  }

  goToBook(bookID: number): void {
    this.router.navigate(['/libro', String(bookID)]);
  }
}
