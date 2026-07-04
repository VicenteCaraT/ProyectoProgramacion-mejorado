import { Component, OnInit } from '@angular/core';
import { MatDialog } from '@angular/material/dialog';
import { AutorService } from '../../services/autor/autor.service';
import { AbmModalComponent } from '../../components/modals/abm-modal/abm-modal.component';
import { SysNotificationService } from '../../services/sys-notifications/sys-notification.service';
import { Autor, AutoresResponse } from '../../models/models';
import { dedupSearch } from '../../utils/search';

@Component({
  selector: 'app-autor',
  templateUrl: './autor.component.html',
  styleUrl: './autor.component.css'
})
export class AutorComponent implements OnInit{

  constructor(
    private dialog: MatDialog,
    private autorService: AutorService,
    private sysNotificationService: SysNotificationService
  ) {}

  autorList: Autor[] = [];
  filteredAutor: Autor[] = [];
  currentPage: number = 1;
  totalPages: number = 1;

  currentFilter: { type: string, value: string } | null = null;
  baseParam: any = {};

  ngOnInit(): void {
    this.fetchAutores(1, this.baseParam)
  }

  fetchAutores(page: number, extraParams: any = {}): void {
    const params = {...this.baseParam, ...extraParams}
    this.autorService.getAutores(page, params).subscribe((rta: AutoresResponse) => {
      this.autorList = rta.autores || [];
      this.filteredAutor = [...this.autorList];
      this.totalPages = rta.pages;
    })
  }

  handleSearch(query: string) {
    if (query) {
      const queries = [
        this.autorService.getAutores(1, { nombre: query }),
        this.autorService.getAutores(1, { apellido: query }),
        this.autorService.getAutores(1, { apodo: query }),
      ];
      dedupSearch(queries, r => (r as AutoresResponse).autores || [], results => this.filteredAutor = results);
    } else {
      this.filteredAutor = [...this.autorList];
    }
  }

  handleActionEvent(event: { action: string, autor: any }) {
    if (event.action === 'edit') {
      this.openABMautorModal(event.autor, 'edit');
    } else if (event.action === 'delete') {
      this.autorService.deleteAutor(event.autor.id).subscribe({
        next: () => {
          this.sysNotificationService.showSuccess('Autor eliminado correctamente')
          this.refreshAutorList();
        },
        error: (err) => {
          console.error('Error al eliminar el autor', err)
          this.sysNotificationService.showError('Error al eliminar el autor')
        }
      })
    }
  }

  openABMautorModal(autorData: any, operation: string): void {
      const dialogRef = this.dialog.open(AbmModalComponent, {
        width: '500px',
        data: {
          formType: 'autor',
          formOperation: operation,
          ...autorData
        } 
      });
      dialogRef.afterClosed().subscribe( result => {
        if(result) {
          if (operation == 'create') {
            this.autorService.postAutor(result).subscribe({
              next: () => {
                this.sysNotificationService.showSuccess('Autor creado correctamente')
                this.refreshAutorList();
              },
              error: () => {
                this.sysNotificationService.showError('Error al crear el autor')
              }
            });
          } else if (operation === 'edit') {
            this.autorService.updateAutor(autorData.id, result).subscribe({
              next: () => {
                this.sysNotificationService.showSuccess('Autor editado correctamente')
                this.refreshAutorList();
              },
              error: () => {
                this.sysNotificationService.showError('Error al editar el autor')
              }
            });
          }
        }
      });
    }

    refreshAutorList(): void {
      const filterParams = this.currentFilter ? { [this.currentFilter.type]: this.currentFilter.type }: {};
      this.fetchAutores(this.currentPage, filterParams);
  }

  changePage(newPage: number): void {
    if (newPage >= 1 && newPage <= this.totalPages) {
      this.currentPage = newPage;
      const filterParams = this.currentFilter ? { [this.currentFilter.type]: this.currentFilter.type }: {};
      this.fetchAutores(this.currentPage, filterParams);
    }
  }

}
