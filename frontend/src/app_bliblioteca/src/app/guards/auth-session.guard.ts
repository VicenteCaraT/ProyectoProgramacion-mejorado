import { CanActivateFn, Router } from '@angular/router';
import { inject } from '@angular/core';

export const authSessionGuard: CanActivateFn = (route, state) => {

  const router = inject(Router);
  const token = localStorage.getItem('token');

  if(!token) {
    router.navigateByUrl('login');
    return false;
  } else {
    return true;
  }
};
