import { Component, OnInit, TemplateRef } from '@angular/core';
import { BookModalComponent } from '../../components/modals/book-modal/book-modal.component';
import { MatDialog } from '@angular/material/dialog';
import { LibrosService } from '../../services/books/libros.service';
import { Libro, LibrosResponse } from '../../models/models';


@Component({
  selector: 'app-home',
  templateUrl: './home.component.html',
  styleUrl: './home.component.css'
})
export class HomeComponent implements OnInit{
  
  constructor(
    public dialog: MatDialog,
    private bookService: LibrosService,

  ) {}

  bookList: Libro[] = []
  harryPotterBooks: Libro[] = [];
  fantasyBooks: Libro[] = [];

  filteredBooks: Libro[] = []

  ngOnInit(): void {
    this.bookService.getBooks(1).subscribe((rta: LibrosResponse) => {
      this.bookList = rta.libros || [];
      this.filteredBooks = [...this.bookList]
    })
    this.bookService.getBooks(1, {titulo:'Harry'}).subscribe((rta: LibrosResponse) => {
      this.harryPotterBooks = rta.libros || []
    })
    this.bookService.getBooks(1, {genero:'Fanta'}).subscribe((rta: LibrosResponse) => {
      this. fantasyBooks= rta.libros || []
    })
}

  openBookModal(book: Libro): void {
    this.dialog.open(BookModalComponent, {
      width: '500px',
      data: book
    }
    )
  }
}