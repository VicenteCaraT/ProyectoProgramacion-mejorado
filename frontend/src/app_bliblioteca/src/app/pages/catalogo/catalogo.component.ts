import { Component, OnInit } from '@angular/core';
import { MatDialog } from '@angular/material/dialog';
import { AbmModalComponent } from '../../components/modals/abm-modal/abm-modal.component';
import { LibrosService } from '../../services/books/libros.service';
import { SysNotificationService } from '../../services/sys-notifications/sys-notification.service';
import { Libro, LibrosResponse } from '../../models/models';

@Component({
  selector: 'app-catalogo',
  templateUrl: './catalogo.component.html',
  styleUrl: './catalogo.component.css'
})
export class CatalogoComponent implements OnInit{

  constructor(
    private dialog: MatDialog,
    private bookService: LibrosService,
    private sysNotificationService: SysNotificationService
  ) {}

  bookList: Libro[] = []
  filteredBook: Libro[] = []
  currentPage: number = 1;
  totalPages: number = 1;

  currentFilter: { type: string, value: string } | null = null;
  baseParam: any = {};

  ngOnInit(): void {
    this.fetchBooks(1, this.baseParam);
  }

  fetchBooks(page: number, extraParams: any = {}): void {
    const params = {...this.baseParam, ...extraParams}
    this.bookService.getBooks(page, params).subscribe((rta: LibrosResponse) => {
      this.bookList = rta.libros || [];
      this.filteredBook = [...this.bookList];
      this.totalPages = rta.pages;
    })
  }

  // ARREGLAR ya que no filtra
  handleSearch(query: string) {
    if (query) {
      const paramsList = [
        { titulo: query },
        { autor: query },
        { genero: query },
        { editorial: query }
      ];

      const allResults: Libro[] = [];
      const seenIds = new Set<number>();
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
              this.filteredBook = allResults;
            }
          },
          (error) => {
            console.error('Error en búsqueda:', error);
            pending--;
            if (pending === 0) {
              this.filteredBook = allResults;
            }
          }
        );
      }
    } else {
      this.filteredBook = [...this.bookList];
    }
  }

  
  handleActionEvent(event: { action: string, book: any }) {
    if (event.action === 'edit') {
      this.openABMbookModal(event.book, 'edit');
    } else if (event.action === 'delete') {
      this.bookService.deleteBook(event.book.id).subscribe({
        next: () => {
          this.sysNotificationService.showSuccess('Libro eliminado correctamente')
          this.refreshBookList();
        },
        error: (err) => {
          console.error('Error al eliminar el libro', err)
          this.sysNotificationService.showError('Error al eliminar el libro')
        }
      })
    }
  }

  openABMbookModal(bookData: any, operation: string): void {
    const dialogRef = this.dialog.open(AbmModalComponent, {
      width: '500px',
      data: {
        formType: 'book',
        formOperation: operation,
        ...bookData
      } 
    });
    dialogRef.afterClosed().subscribe( result => {
      if(result) {
        if (operation == 'create') {
          this.bookService.postBook(result).subscribe({
            next: () => {
              this.sysNotificationService.showSuccess('Libro creado correctamente')
              this.refreshBookList();
            },
            error: () => {
              this.sysNotificationService.showError('Error al crear el libro')
            }
          });
        } else if (operation === 'edit') {
          this.bookService.updateBook(bookData.id, result).subscribe({
            next: () => {
              this.sysNotificationService.showSuccess('Libro editado correctamente')
              this.refreshBookList();
            },
            error: () => {
              this.sysNotificationService.showError('Error al editar el libro')
            }
          });
        }
      }
    });
  }
  
  refreshBookList(): void {
    const filterParams = this.currentFilter ? { [this.currentFilter.type]: this.currentFilter.type }: {};
    this.fetchBooks(this.currentPage, filterParams);
  }

  changePage(newPage: number): void {
    if (newPage >= 1 && newPage <= this.totalPages) {
      this.currentPage = newPage;
      const filterParams = this.currentFilter ? { [this.currentFilter.type]: this.currentFilter.type }: {};
      this.fetchBooks(this.currentPage, filterParams);
    }
  }

    handleFilterChange(option: { type: string, value: string }): void {
    this.currentPage = 1;

    if (option.value === '') {
      this.currentFilter = null;
      this.fetchBooks(this.currentPage);
    } else {
      this.currentFilter = { type: option.type, value: option.value };
      const filterParams = { [option.type]: option.value };
      this.fetchBooks(this.currentPage, filterParams);
    }
  }
}
