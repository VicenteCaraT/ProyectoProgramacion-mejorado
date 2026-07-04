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
          { type: 'orden', value: 'mayor_stock', label: 'Mayor stock' },
          { type: 'sin_stock', value: 'true', label: 'Sin stock' },
          { type: 'orden', value: 'ranking', label: 'Ranking' },
        ];
        break;
      case 'prestamo':
        this.filterOptions = [
          clearFilterOption,
          { type: 'estado', value: 'Pendiente', label: 'Pendiente' },
          { type: 'estado', value: 'Activo', label: 'Activos' },
          { type: 'estado', value: 'Terminado', label: 'Terminados' },
          { type: 'orden', value: 'proximos', label: 'Próximos a Terminar' }
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
        case 'reseñas':
          this.filterOptions = [
            clearFilterOption,
            { type: 'ordenValoracion', value: 'Valoraciones_desc', label: 'Reseñas + a -' },
            { type: 'ordenValoracion', value: 'Valoraciones_asc', label: 'Reseñas - a +' },
          ];
        break;
      default:
        this.filterOptions = [];
    }
  }

  onFilterChange(option: { type?: string, value: string }) {
    this.filterChange.emit({ type: option.type || '', value: option.value });
  }

}
