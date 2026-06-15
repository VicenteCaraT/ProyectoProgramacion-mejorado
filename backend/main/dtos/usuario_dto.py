class UsuarioDTO:
    @staticmethod
    def full(usuario):
        return {
            "id": usuario.idUser,
            "user": usuario.user,
            "nombre": usuario.nombre,
            "apellido": usuario.apellido,
            "dni": usuario.dni,
            "telefono": usuario.telefono,
            "email": usuario.email,
            "rol": usuario.rol,
            "img": usuario.profile_img,
            "estado": str(usuario.estado)
        }

    @staticmethod
    def short(usuario):
        return {
            "id": usuario.idUser,
            "user": usuario.user,
            "nombre": usuario.nombre,
            "apellido": usuario.apellido
        }
