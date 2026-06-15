from main.repositories import PrestamoRepository, LibroRepository, UsuarioRepository
from main.models import PrestamoModel
from .. import db
from datetime import datetime, timedelta

class PrestamoService:
    @staticmethod
    def get_by_id(id):
        return PrestamoRepository.get_by_id(id)

    @staticmethod
    def get_all(filters):
        return PrestamoRepository.get_all(
            page=filters.pop("page", 1),
            per_page=filters.pop("per_page", 10),
            filters=filters
        )

    @staticmethod
    def create(data):
        user_id = data.get("usuario")
        if UsuarioRepository.get_by_id(user_id) is None:
            raise ValueError(f"El usuario ID {user_id} no existe")

        libro_ids = data.get("libro")
        if not isinstance(libro_ids, list):
            libro_ids = [libro_ids]

        libros = []
        for lib_id in libro_ids:
            libro = LibroRepository.get_by_id(lib_id)
            if libro is None:
                raise ValueError(f"El libro ID {lib_id} no existe")
            if libro.cantidad <= 0:
                raise ValueError(f"Sin stock para el libro ID {libro.idLibro}")
            libros.append(libro)

        if "inicio_prestamo" not in data or "fin_prestamo" not in data:
            hoy = datetime.today()
            data["inicio_prestamo"] = hoy.strftime("%d-%m-%Y")
            data["fin_prestamo"] = (hoy + timedelta(days=30)).strftime("%d-%m-%Y")

        prestamo = PrestamoModel.from_json(data)
        prestamo.estado = "Pendiente"
        for libro in libros:
            prestamo.fk_idLibro.append(libro)
        return PrestamoRepository.save(prestamo)

    @staticmethod
    def update(id, data):
        prestamo = PrestamoRepository.get_by_id(id)
        if "inicio_prestamo" in data:
            prestamo.inicio_prestamo = datetime.strptime(data["inicio_prestamo"], "%d-%m-%Y")
        if "fin_prestamo" in data:
            prestamo.fin_prestamo = datetime.strptime(data["fin_prestamo"], "%d-%m-%Y")
        if "estado" in data:
            estado_anterior = prestamo.estado
            prestamo.estado = data["estado"]
            if data["estado"] == "Activo" and estado_anterior != "Activo":
                for libro in prestamo.fk_idLibro:
                    if libro.cantidad > 0:
                        libro.cantidad -= 1
                    else:
                        raise ValueError(f"No hay cantidad disponible para el libro ID {libro.idLibro}")
            elif data["estado"] == "Desactivado" and estado_anterior == "Activo":
                for libro in prestamo.fk_idLibro:
                    libro.cantidad += 1
        if "libro" in data:
            ids_libros = data["libro"]
            if isinstance(ids_libros, int):
                ids_libros = [ids_libros]
            nuevos = []
            for lib_id in ids_libros:
                libro = LibroRepository.get_by_id(lib_id)
                if libro is None:
                    raise ValueError(f"El libro ID {lib_id} no existe")
                nuevos.append(libro)
            prestamo.fk_idLibro = nuevos
        return PrestamoRepository.save(prestamo)

    @staticmethod
    def delete(id):
        prestamo = PrestamoRepository.get_by_id(id)
        for libro in prestamo.fk_idLibro:
            libro.cantidad += 1
        PrestamoRepository.delete(prestamo)

    @staticmethod
    def expire_overdue():
        hoy = datetime.today()
        prestamos = PrestamoRepository._apply_filters(
            db.session.query(PrestamoModel), {"estado": "Activo"}
        ).all()
        cambios = 0
        for prestamo in prestamos:
            if prestamo.fin_prestamo < hoy:
                prestamo.estado = "Terminado"
                for libro in prestamo.fk_idLibro:
                    libro.cantidad += 1
                cambios += 1
        db.session.commit()
        return cambios
