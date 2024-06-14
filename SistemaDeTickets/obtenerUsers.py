# Mostrar todos los usuarios
from django.contrib.auth import get_user_model

User = get_user_model()

print(User.objects.all())  # Verifica que los usuarios se han creado correctamente

# Mostrar el role de un usuario
from django.contrib.auth.models import Group
from venta.models import CustomUser

# Obtener el usuario que acabas de crear
user = CustomUser.objects.get(username="someuser")

# Obtener el grupo 'Editors'
editors_group = Group.objects.get(name="Editors")

# Añadir el usuario al grupo 'Editors'
user.groups.add(editors_group)

# Verificar que el usuario ha sido añadido al grupo
print(user.groups.all())  # Deberías ver el grupo 'Editors' en la salida
