import { Component, EventEmitter, Input, OnChanges, Output } from '@angular/core';
import { Location } from '@angular/common';

@Component({
  selector: 'app-searchbar',
  templateUrl: './searchbar.component.html',
  styleUrl: './searchbar.component.css'
})
export class SearchbarComponent implements OnChanges{
  @Output() searchEvent = new EventEmitter<string>();
  @Input() currentPage: string = '';
  searchQuery: string = '';
  @Output() filterChange = new EventEmitter<{ type: string, value: string }>();
  filterOptions: Array<{ type?:string, value: string, label: string}> = [];

  constructor (
    private location: Location,
  ) {}

  isAdmin() { 
    const tokenRol = localStorage.getItem('token_rol');
  if (tokenRol && tokenRol.includes("Admin")) {
    return true;
  } else {
    return false;
  }
  }

  ngOnChanges() {
    this.setFilterOptions();
  }

  onSearch() {
    console.log('buscar: ', this.searchQuery);
    this.searchEvent.emit(this.searchQuery)
  }

  goBack() {
    this.location.back()
  }

  setFilterOptions() {
    const clearFilterOption = { value: '', label: 'Quitar filtros' };

    switch (this.currentPage) {
      case 'catalogo':
        this.filterOptions = [
          clearFilterOption,
          {value: 'user', label: 'Usuarios'},
          {value: 'book', label: 'Libros'},
          {value: 'status', label: 'Estado'}
        ];
        break;
      case 'prestamo':
        this.filterOptions = [
          clearFilterOption,
          { type: 'estado', value: 'Pendiente', label: 'Pendiente' },
          { type: 'estado', value: 'Activo', label: 'Activos' },
          { type: 'fecha_proxima', value: '1', label: 'Fechas Próximas' }
        ];
        break;
        case 'usuarios':
          this.filterOptions = [
            clearFilterOption,
            { type: 'rol', value: 'Pendiente', label: 'Pendiente' },
            { type: 'rol', value: 'Usuario', label: 'Usuarios' },
            { type: 'rol', value: 'Admin', label: 'Administradores' },
            { type: 'rol', value: 'Bibliotecario', label: 'Bibliotecarios' },
            { type: 'estado', value: '0', label: 'Desbloqueado' },
            { type: 'estado', value: '1', label: 'Bloqueado' }
          ];
          break;
      default:
        this.filterOptions = [];
    }
  }

  onFilterChange(option: { type?: string, value: string }) {
    console.log('Filter changed:', option);
    this.filterChange.emit({ type: option.type || '', value: option.value });
  }

}
