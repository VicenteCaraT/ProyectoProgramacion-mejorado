// ─── Autor ───────────────────────────────────────────────

export interface Autor {
  id: number;
  nombre: string;
  apellido: string;
  apodo: string;
}

export interface AutorShort {
  apodo: string;
}

// ─── Usuario ─────────────────────────────────────────────

export interface Usuario {
  id: number;
  user: string;
  nombre: string;
  apellido: string;
  dni: number;
  telefono: string;
  email: string;
  rol: string;
  img: string | null;
  estado: string;
}

export interface UsuarioShort {
  id: number;
  user: string;
  nombre: string;
  apellido: string;
}

// ─── Libro ───────────────────────────────────────────────

export interface Libro {
  id: number;
  img: string;
  titulo: string;
  cantidad: number;
  autor: Autor[];
  editorial: string;
  genero: string;
  sinopsis: string;
  total_reseñas: number;
  promedio_valoracion: number;
}

export interface LibroShort {
  id: number;
  img: string;
  titulo: string;
  autor: AutorShort[];
  editorial: string;
  genero: string;
  sinopsis: string;
}

// ─── Prestamo ────────────────────────────────────────────

export interface Prestamo {
  id: number;
  usuario: Usuario;
  libro: Libro[];
  inicio_prestamo: string;
  fin_prestamo: string;
  estado: string;
}

// ─── Reseña ──────────────────────────────────────────────

export interface Reseña {
  id: number;
  usuario: Usuario;
  libro: Libro;
  fecha: string;
  descripcion: string;
  valoracion: string;
}

// ─── Notificacion ────────────────────────────────────────

export interface Notificacion {
  id: number;
  usuario: Usuario;
  descripcion: string;
}

// ─── Guardado ────────────────────────────────────────────

export interface Guardado {
  id: number;
  usuario: Usuario;
  libro: Libro;
}

// ─── Paginated Response ──────────────────────────────────

export interface PaginatedResponse<T> {
  total: number;
  pages: number;
  page: number;
}

export interface LibrosResponse extends PaginatedResponse<Libro> {
  libros: Libro[];
}

export interface UsuariosResponse extends PaginatedResponse<Usuario> {
  usuarios: Usuario[];
}

export interface PrestamosResponse extends PaginatedResponse<Prestamo> {
  prestamos: Prestamo[];
}

export interface AutoresResponse extends PaginatedResponse<Autor> {
  autores: Autor[];
}

export interface ReseñasResponse extends PaginatedResponse<Reseña> {
  reseñas: Reseña[];
}

export interface NotificacionesResponse extends PaginatedResponse<Notificacion> {
  notificaciones: Notificacion[];
}

export interface GuardadosResponse extends PaginatedResponse<Guardado> {
  guardados: Guardado[];
}

// ─── API Single-Entity Wrappers ──────────────────────────

export interface MessageResponse {
  message: string;
}

export interface AutorResponse extends MessageResponse {
  autor: Autor;
}

export interface LibroResponse extends MessageResponse {
  libro: Libro;
}

export interface UsuarioResponse extends MessageResponse {
  usuario: Usuario;
}

export interface PrestamoResponse extends MessageResponse {
  prestamo: Prestamo;
}

export interface ReseñaResponse extends MessageResponse {
  reseña: Reseña;
}

export interface NotificacionResponse extends MessageResponse {
  notificacion: Notificacion;
}

export interface GuardadoResponse extends MessageResponse {
  guardado: Guardado;
}

// ─── Auth ────────────────────────────────────────────────

export interface LoginRequest {
  email: string;
  contraseña: string;
}

export interface LoginResponse {
  id: string;
  email: string;
  access_token: string;
}

export interface JwtPayload {
  rol: string;
  id: string;
  estado: boolean;
  [key: string]: unknown;
}

// ─── Error ───────────────────────────────────────────────

export interface ApiError {
  message: string;
  error?: string;
  errors?: Record<string, string[]>;
}
