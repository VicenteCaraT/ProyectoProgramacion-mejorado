import { TestBed } from '@angular/core/testing';

import { GuardadosService } from './guardados.service';

describe('GuardadosService', () => {
  let service: GuardadosService;

  beforeEach(() => {
    TestBed.configureTestingModule({});
    service = TestBed.inject(GuardadosService);
  });

  it('should be created', () => {
    expect(service).toBeTruthy();
  });
});
