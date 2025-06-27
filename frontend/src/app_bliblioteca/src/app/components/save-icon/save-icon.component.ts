import { Component, Input, OnInit } from '@angular/core';
import { GuardadosService } from '../../services/saves/guardados.service';

@Component({
  selector: 'app-save-icon',
  templateUrl: './save-icon.component.html',
  styleUrl: './save-icon.component.css'
})
export class SaveIconComponent implements OnInit {
  @Input() libroID!: number;
  isSaved = false;
  savedID: number | null = null;

  constructor(
    private saveService: GuardadosService
  ) {}

  ngOnInit(): void {
    const userId = localStorage.getItem('user_id');   
    if (userId) {
      this.checkIfSaved(userId);
    }
  }

  checkIfSaved(userId: string): void {
    this.saveService.getSaves(1, {
      idUsuario: userId,
      libro_id: this.libroID.toString()
    }).subscribe((rta: any) => {
      const guardado = rta.guardados?.[0];
      if (guardado) {
        this.isSaved = true;
        this.savedID = guardado.id;
      } else {
        this.isSaved = false;
        this.savedID = null;
      }
    });
  }
  
  toggleSave(): void {
    if (this.isSaved && this.savedID !== null) {
      this.saveService.deleteSave(this.savedID).subscribe(() => {
        this.isSaved = false;
        this.savedID = null;
      });
    } else {
      this.saveService.postSaves({ libro: this.libroID }).subscribe((rta: any) => {
        this.isSaved = true;
        this.savedID = rta.id;
      });
    }
  }
}
