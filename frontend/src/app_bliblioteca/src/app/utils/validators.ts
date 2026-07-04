import { ValidatorFn, Validators } from '@angular/forms';

export const onlyLetters: ValidatorFn = Validators.pattern(/^[a-zA-ZáéíóúÁÉÍÓÚñÑ\s]+$/);
export const onlyNumbers: ValidatorFn = Validators.pattern(/^\d+$/);

export function allowOnlyLetters(event: KeyboardEvent): void {
  const pattern = /^[a-zA-ZáéíóúÁÉÍÓÚñÑ\s]*$/;
  const inputChar = String.fromCharCode(event.keyCode || event.which);
  if (!pattern.test(inputChar)) {
    event.preventDefault();
  }
}

export function allowOnlyNumbers(event: KeyboardEvent): void {
  const pattern = /^[0-9]*$/;
  const inputChar = String.fromCharCode(event.keyCode || event.which);
  if (!pattern.test(inputChar)) {
    event.preventDefault();
  }
}
