import { Component } from '@angular/core';
import { LibrosService } from '../../services/books/libros.service';
import { Router } from '@angular/router';
import { Libro, LibrosResponse } from '../../models/models';

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
      const lowerQuery = query.toLowerCase();

      const paramsList = [
        { titulo: query },
        { autor: query },
        { genero: query },
        { editorial: query }
      ];

      const allResults: Libro[] = [];
      const seenIds = new Set();
      let pending = paramsList.length;

      for (const params of paramsList) {
        this.bookService.getBooks(1, params).subscribe(
          (response: LibrosResponse) => {
            if (response && response.libros) {
              for (const libro of response.libros) {
                if (!seenIds.has(libro.id)) {
                  seenIds.add(libro.id);
                  allResults.push(libro);
                }
              }
            }

            pending--;
            if (pending === 0) {
              this.searchResults = allResults;
              this.showDropdown = this.searchResults.length > 0;
            }
          },
          (error) => {
            console.error('Error al buscar libros:', error);
            pending--;
            if (pending === 0) {
              this.searchResults = allResults;
              this.showDropdown = this.searchResults.length > 0;
            }
          }
        );
      }
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
