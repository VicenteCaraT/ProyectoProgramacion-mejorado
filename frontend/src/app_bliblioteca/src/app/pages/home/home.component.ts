import { Component, OnInit, TemplateRef } from '@angular/core';
import { BookModalComponent } from '../../components/modals/book-modal/book-modal.component';
import { MatDialog } from '@angular/material/dialog';
import { LibrosService } from '../../services/books/libros.service';


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

  bookList:any[] = []
  harryPotterBooks:any[] = [];
  fantasyBooks:any[] = [];

  filteredBooks:any = []

  ngOnInit(): void {
    this.bookService.getBooks(1).subscribe((rta: any) => {
      console.log("Libros Api: ", rta);
      this.bookList = rta.libros || [];
      this.filteredBooks = [...this.bookList]
    })
    //libros Harry Potter
    this.bookService.getBooks(1, {titulo:'Harry'}).subscribe((rta: any) => {
      console.log("Harry Potter Libros:", rta);
      this.harryPotterBooks = rta.libros || []
    })
    //libros de Fantasía
        this.bookService.getBooks(1, {genero:'Fanta'}).subscribe((rta: any) => {
      console.log("Fantasy Books:", rta);
      this. fantasyBooks= rta.libros || []
    })
}

  openBookModal(book: any): void {
    this.dialog.open(BookModalComponent, {
      width: '500px',
      data: book
    }
    )
  }
}