import { Component, OnInit } from '@angular/core';
import { MatDialog } from '@angular/material/dialog';
import { AbmModalComponent } from '../../components/modals/abm-modal/abm-modal.component';
import { UsuariosService } from '../../services/users/usuarios.service';
import { SysNotificationService } from '../../services/sys-notifications/sys-notification.service';
import { Usuario, UsuariosResponse } from '../../models/models';

@Component({
  selector: 'app-users',
  templateUrl: './users.component.html',
  styleUrl: './users.component.css'
})
export class UsersComponent implements OnInit{

  constructor(
    private dialog: MatDialog,
    private usuarioService: UsuariosService,
    private sysNotificationService: SysNotificationService
  ) {}

  usersList: Usuario[] = [];
  filteredUsers: Usuario[] = [];
  currentPage: number = 1;
  totalPages: number = 1;

  currentFilter: { type: string, value: string } | null = null;
  baseParams: any = {};

  ngOnInit(): void {
    this.fetchUsers(1, this.baseParams)
  }

  fetchUsers(page: number, extraParams: any = {}): void {
    const params = {...this.baseParams, ...extraParams}
    this.usuarioService.getUsers(page, params).subscribe((rta: UsuariosResponse) => {
      this.usersList = rta.usuarios || [];
      this.filteredUsers = [...this.usersList];
      this.totalPages = rta.pages;
    });
  }

  handleSearch(query: string) {
    if (query) {
      this.usuarioService.getUsers(1, { nombre: query }).subscribe(
        (response: UsuariosResponse) => {
          if (response && response.usuarios) {
            this.filteredUsers = response.usuarios;
          } else {
            this.filteredUsers = [...this.usersList];
          }
        }
      )
    }
  }


  handleActionEvent(event: { action: string, user: any }) {
    if (event.action === 'accept') {
      this.acceptUser(event.user)
    } else if (event.action === '') {
      this.refreshUserList()
    } else if (event.action === 'edit') {
      this.openABMUserModal(event.user, 'edit');
    } else if (event.action === 'delete' || event.action === 'decline') {
      this.usuarioService.deleteUser(event.user.id).subscribe({
        next: () => {
          this.sysNotificationService.showSuccess('Usuario eliminado correctamente')
          this.refreshUserList();
        },
        error: (err) => {
          console.error('Error al eliminar el usuario', err)
          this.sysNotificationService.showError('Error al eliminar el usuario')
        }
      });
    }
  }

  openABMUserModal(userData: any, operation: string): void {
    const dialogRef = this.dialog.open(AbmModalComponent, {
      width: '500px',
      data: {
        formType: 'user',
        formOperation: operation,
        ...userData
      }
    });
    dialogRef.afterClosed().subscribe(result => {
      if (result) {
        if (operation === 'create') {
          this.usuarioService.postUser(result).subscribe({
            next: () => {
              this.sysNotificationService.showSuccess('Usuario creado correctamente')
              this.refreshUserList();
            },
            error: () => {
              this.sysNotificationService.showError('Error al crear el usuario')
            }
          });
        } else if (result) {
          if (operation === 'edit') {
            this.usuarioService.updateUser(userData.id, result).subscribe({
              next: () => {
                this.sysNotificationService.showSuccess('Usuario editado correctamente')
                this.refreshUserList();
              },
              error: () => {
                this.sysNotificationService.showError('Error al editar el usuario')
              }
            });
          }
        }
      }
    });
  }

  refreshUserList(): void {
    const filterParams = this.currentFilter ? { [this.currentFilter.type]: this.currentFilter.value }: {};
    this.fetchUsers(this.currentPage, filterParams)
  }

  changePage(newPage: number): void {
    if (newPage >= 1 && newPage <= this.totalPages) {
      this.currentPage = newPage;
      const filterParams = this.currentFilter ? { [this.currentFilter.type]: this.currentFilter.type }: {};
      this.fetchUsers(this.currentPage, filterParams);
    }
  }

  handleFilterChange(option: { type: string, value: string }): void {
    this.currentPage = 1;

    if (option.value === '') {
      this.currentFilter = null;
      this.fetchUsers(this.currentPage);
    } else {
      this.currentFilter = { type: option.type, value: option.value };
      const filterParams = { [option.type]: option.value };
      this.fetchUsers(this.currentPage, filterParams);
    }
  }
  
  acceptUser(user: any) {
    this.usuarioService.updateUser(user.id, { rol: 'Usuario' }).subscribe({
      next: () => {
        user.rol = 'Usuario';
      },
      error: (error) => {
        console.error('Error al aceptar usuario', error);
      },
      complete: () => undefined
    })
  }
}
