import { Component, OnInit } from '@angular/core';
import { MatDialog } from '@angular/material/dialog';
import { CrearResenaComponent } from '../../components/modals/user-modals/crear-resena/crear-resena.component';
import { AbmModalComponent } from '../../components/modals/abm-modal/abm-modal.component';
import { PrestamosService } from '../../services/loans/prestamos.service';
import { ReseñasService } from '../../services/reviews/reseñas.service';
import { SysNotificationService } from '../../services/sys-notifications/sys-notification.service';
import { ActivatedRoute } from '@angular/router';


@Component({
  selector: 'app-prestamo',
  templateUrl: './prestamo.component.html',
  styleUrl: './prestamo.component.css'
})
export class PrestamoComponent implements OnInit{

  constructor(
    private dialog: MatDialog,
    private loanService: PrestamosService,
    private reviewService: ReseñasService,
    private sysNotificationService: SysNotificationService,
    private route: ActivatedRoute

  ) {}

  loanList:any[] = []
  filteredLoans:any[] = []
  currentPage: number = 1;
  totalPages: number = 1;

  currentFilter: { type: string, value: string } | null = null;
  baseParams: any = {};

  ngOnInit(): void {
    const tokenRol = localStorage.getItem('token_rol');
    const tokenUserId = localStorage.getItem('user_id');
    const routeUserId = this.route.snapshot.queryParamMap.get('idUsuario');

    this.baseParams = tokenRol === 'Usuario' && tokenUserId ? { idUsuario: tokenUserId } : routeUserId ? { idUsuario: routeUserId } : {};
    this.fetchLoans(1, this.baseParams);
    }

    fetchLoans(page: number, extraParams: any = {}): void {
      const params = {...this.baseParams, ...extraParams}
      this.loanService.getLoans(page, params).subscribe((rta: any) => {
        this.loanList = rta.prestamos || [];
        this.filteredLoans = [...this.loanList];
        this.totalPages = rta.pages;
      });
    }

  //areglar
  handleSearch(query: string) {
    if (query) {
      this.filteredLoans = this.loanList.filter(loan =>
        loan.titulo.toLowerCase().includes(query.toLowerCase()) ||
        loan.usuario.user.toLowerCase().includes(query.toLowerCase())      ||
        loan.inicio_fecha.toLowerCase().includes(query.toLowerCase())  ||
        loan.fin_fecha.toLowerCase().includes(query.toLowerCase())
      );
    } else {
      this.filteredLoans = [...this.loanList];
    }
  }

  handleActionEvent(event: { action: string, loan: any }) {
    if (event.action === 'accept') {
      this.acceptLoan(event.loan);
    } else if (event.action === '') {
      this.refreshLoanList()
    } else if (event.action === 'edit') {
      this.openABMLoanModal(event.loan, 'edit');
    } else if (event.action === 'delete' || event.action === 'decline') {
      this.loanService.deleteLoan(event.loan.id).subscribe({
        next: () => {
          this.sysNotificationService.showSuccess('Prestamo eliminado correctamente')
          this.refreshLoanList();
        },
        error: (err) => {
          console.error('Error al eliminar el prestamo', err)
          this.sysNotificationService.showError('Error al eliminar el préstamo')
        }
      })
    }
  }

  openABMLoanModal(loanData: any, operation: string): void {
    const dialogRef = this.dialog.open(AbmModalComponent, {
      width: '500px',
      data: {
        formType: 'loan',
        formOperation: operation,
        ...loanData
      }
    });
    dialogRef.afterClosed().subscribe(result => {
      console.log('El modal se cerró', result); 
      if (result) {
        if (operation === 'create') {
          this.loanService.postLoan(result).subscribe({
            next: () => {
              this.sysNotificationService.showSuccess('Préstamo creado correctamente')
              this.refreshLoanList();
            },
            error: () => {
              this.sysNotificationService.showError('Error al crear el préstamo')
            }
          });
        } else if (operation === 'edit') {
          this.loanService.updateLoan(loanData.id, result).subscribe({
            next: () => {
              this.sysNotificationService.showSuccess('Préstamo editado correctamente')
              this.refreshLoanList();
            },
            error: () => {
              this.sysNotificationService.showError('Error al editar el préstamo')
            }
          });
        }
      }
    })
  }

  refreshLoanList(): void {
    const filterParams = this.currentFilter ? { [this.currentFilter.type]: this.currentFilter.value } : {};
    this.fetchLoans(this.currentPage, filterParams)
  }

  changePage(newPage: number): void {
    if (newPage >= 1 && newPage <= this.totalPages) {
      this.currentPage = newPage;
      const filterParams = this.currentFilter ? { [this.currentFilter.type]: this.currentFilter.value } : {};
      this.fetchLoans(this.currentPage, filterParams);
    }
  }

    handleFilterChange(option: { type: string, value: string }): void {
    this.currentPage = 1;

    if (option.value === '') {
      this.currentFilter = null;
      this.fetchLoans(this.currentPage);
    } else {
      this.currentFilter = { type: option.type, value: option.value };
      const filterParams = { [option.type]: option.value };
      this.fetchLoans(this.currentPage, filterParams);
    }
  }

  openRealizarResena(loan: any): void {
    if (!loan || !loan.libro || loan.libro.length === 0) {
        console.error("El objeto loan o loan.libro es undefined o está vacío", loan);
        return;
    }

    const params = { idLibro: loan.libro[0].id };
    this.reviewService.getReviews(1, params).subscribe(reviewsResponse => {
        const dialogRef = this.dialog.open(CrearResenaComponent, {
            width: '500px',
            data: {
                loan: loan,
                reviews: (reviewsResponse as any).reseñas
            }
        });
    });
}

  acceptLoan(loan: any) {
    this.loanService.updateLoan(loan.id, { estado: 'Activo' }).subscribe({
      next: () => {
        loan.estado = 'Activo';
        this.sysNotificationService.showSuccess('Préstamo aceptado correctamente');
      },
      error: (error) => {
        console.error('Error al aceptar el préstamo', error);
        this.sysNotificationService.showError('Error al aceptar el préstamo');
      }
    });
  }

  actualizarPrestamosVencidos(): void {
  this.loanService.patchLoans().subscribe({
    next: (res: any) => {
      this.sysNotificationService.showSuccess(res.message);
      this.refreshLoanList()
    },
    error: () => {
      this.sysNotificationService.showError("Error al actualizar préstamos");
    }
  });
}
  isAdmin() { 
    const tokenRol = localStorage.getItem('token_rol');
  if (tokenRol && tokenRol.includes("Admin")) {
    return true;
  } else {
    return false;
  }
}
}
