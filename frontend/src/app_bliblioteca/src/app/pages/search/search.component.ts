import { Component } from '@angular/core';
import { LibrosService } from '../../services/books/libros.service';
import { Router } from '@angular/router';
import { Libro, LibrosResponse } from '../../models/models';
import { dedupSearch } from '../../utils/search';

@Component({
  selector: 'app-search',
  templateUrl: './search.component.html',
  styleUrl: './search.component.css'
})
export class SearchComponent {
  showDropdown: boolean = false;
  searchResults: Libro[] = [];

  constructor(private bookService: LibrosService, private router: Router) {}

  goToBook(bookID: number) {
    this.router.navigate(['/libro', String(bookID)])
  }

  handleSearch(query: string) {
    if (query) {
      const queries = [
        this.bookService.getBooks(1, { titulo: query }),
        this.bookService.getBooks(1, { autor: query }),
        this.bookService.getBooks(1, { genero: query }),
        this.bookService.getBooks(1, { editorial: query })
      ];
      dedupSearch(queries, r => (r as LibrosResponse).libros || [], results => {
        this.searchResults = results;
        this.showDropdown = results.length > 0;
      });
    } else {
      this.showDropdown = false;
      this.searchResults = [];
    }
  }

  filterByGenre(genero: string) {
  this.bookService.getBooks(1, { genero }).subscribe(
    (response: LibrosResponse) => {
      this.searchResults = response.libros || [];
      this.showDropdown = this.searchResults.length > 0;
    },
    (error) => {
      console.error('Error al filtrar por género:', error);
      this.searchResults = [];
      this.showDropdown = false;
    }
  );
}

filterByAuthor(autor: string) {
  this.bookService.getBooks(1, { autor }).subscribe(
    (response: LibrosResponse) => {
      this.searchResults = response.libros || [];
      this.showDropdown = this.searchResults.length > 0;
    },
    (error) => {
      console.error('Error al filtrar por autor:', error);
      this.searchResults = [];
      this.showDropdown = false;
    }
  );
}
}
