import { Component, OnInit } from '@angular/core';
import { GuardadosService } from '../../services/saves/guardados.service';
import { Router } from '@angular/router';

@Component({
  selector: 'app-save',
  templateUrl: './save.component.html',
  styleUrl: './save.component.css'
})
export class SaveComponent implements OnInit{
  bookList: any[] = [];
  filteredBook: any[] = [];

  constructor(
    private guardadosService: GuardadosService,
    private router: Router
  ) {}

  ngOnInit(): void {
    const userId = localStorage.getItem('user_id') ?? undefined;
    this.guardadosService.getSaves(1, { idUsuario: userId }).subscribe({
      next: (res: any) => {
        console.log("Guardados:", res);
        this.bookList = res.guardados.map((item: any) => item.libro);
        this.filteredBook = [...this.bookList];
      },
      error: (err) => {
        console.error("Error al obtener guardados:", err);
      }
    });
  }

    goToBook(bookID: string) {
    this.router.navigate(['/libro', bookID])
  }
}
