import { TestBed } from '@angular/core/testing';

import { SysNotificationService } from './sys-notification.service';

describe('SysNotificationService', () => {
  let service: SysNotificationService;

  beforeEach(() => {
    TestBed.configureTestingModule({});
    service = TestBed.inject(SysNotificationService);
  });

  it('should be created', () => {
    expect(service).toBeTruthy();
  });
});
