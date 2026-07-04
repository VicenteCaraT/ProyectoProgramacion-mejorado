import { HttpParams } from '@angular/common/http';

export function buildParams(
  page: number,
  filters?: Record<string, string | undefined>,
  keyMap?: Record<string, string>
): HttpParams {
  let params = new HttpParams().set('page', page.toString());
  if (filters) {
    Object.entries(filters).forEach(([key, value]) => {
      if (value) {
        params = params.set(keyMap?.[key] ?? key, value);
      }
    });
  }
  return params;
}
