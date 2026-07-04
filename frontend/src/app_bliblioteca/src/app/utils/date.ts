export function formatToIso(dateStr: string | undefined): string {
  if (!dateStr || !dateStr.includes('-')) return '';
  const [day, month, year] = dateStr.split('-');
  return `${year}-${month}-${day}`;
}

export function formatToday(): string {
  const fecha = new Date();
  const dia = String(fecha.getDate()).padStart(2, '0');
  const mes = String(fecha.getMonth() + 1).padStart(2, '0');
  const anio = fecha.getFullYear();
  return `${dia}-${mes}-${anio}`;
}
