import { Component } from '@angular/core';
import { LibrosService } from '../../services/books/libros.service';
import { Router } from '@angular/router';

@Component({
  selector: 'app-search',
  templateUrl: './search.component.html',
  styleUrl: './search.component.css'
})
export class SearchComponent {
  showDropdown: boolean = false;
  searchResults: any[] = [];

  constructor(private bookService: LibrosService, private router: Router) {}

  goToBook(bookID: string) {
    this.router.navigate(['/libro', bookID])
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

      const allResults: any[] = [];
      const seenIds = new Set();
      let pending = paramsList.length;

      for (const params of paramsList) {
        this.bookService.getBooks(1, params).subscribe(
          (response: any) => {
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
}
