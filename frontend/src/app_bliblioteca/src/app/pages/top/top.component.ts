import { Component, OnInit } from '@angular/core';
import { LibrosService } from '../../services/books/libros.service';
import { Router } from '@angular/router';

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

  bookList:any[] = []
  filteredBook:any = []

  ngOnInit(): void {
    this.bookService.getBooks(1, { orden: 'ranking'}).subscribe((rta: any) => {
      console.log("Libros Api: ", rta);
      this.bookList = rta.libros || [];
      this.filteredBook = [...this.bookList]
    })
  }
    goToBook(bookID: string) {
    this.router.navigate(['/libro', bookID])
  }
}
