import { Observable } from 'rxjs';

export function dedupSearch<T extends { id: number }>(
  queries: Observable<any>[],
  extractFn: (response: any) => T[],
  onComplete: (results: T[]) => void
): void {
  const allResults: T[] = [];
  const seenIds = new Set<number>();
  let pending = queries.length;

  if (pending === 0) {
    onComplete([]);
    return;
  }

  for (const obs of queries) {
    obs.subscribe({
      next: (response) => {
        const items = extractFn(response);
        for (const item of items) {
          if (!seenIds.has(item.id)) {
            seenIds.add(item.id);
            allResults.push(item);
          }
        }
        pending--;
        if (pending === 0) onComplete(allResults);
      },
      error: () => {
        pending--;
        if (pending === 0) onComplete(allResults);
      }
    });
  }
}
