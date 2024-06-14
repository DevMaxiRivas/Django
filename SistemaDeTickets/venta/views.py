from django.contrib.auth.forms import UserCreationForm
from django.shortcuts import render, redirect
from django.contrib.auth import login

# Gestion de Permisos
from django.contrib.auth.decorators import permission_required

# Proteccion de Vistas
from django.contrib.auth.decorators import login_required, user_passes_test

# Asignacion de Roles

from django.contrib.auth.models import Group
from django.http import HttpResponse
from venta.models import CustomUser


def register(request):
    if request.method == "POST":
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect(
                "home"
            )  # Asegúrate de que 'home' esté definido o usa la URL que prefieras
    else:
        form = UserCreationForm()
    return render(request, "register.html", {"form": form})


@permission_required("venta.can_publish", raise_exception=True)
def publish_article(request):
    # Lógica para publicar un artículo
    return render(request, "publish_article.html")


@login_required
@user_passes_test(lambda user: user.is_superuser)
def superuser_only_view(request):
    return render(request, "superuser_only.html")


def assign_role_to_user(request, username):
    try:
        user = CustomUser.objects.get(username=username)

        # Obtener el grupo 'Editors'
        editors_group = Group.objects.get(name="Editors")

        # Añadir el usuario al grupo 'Editors'
        user.groups.add(editors_group)

        # Guardar el usuario
        user.save()

        return HttpResponse("Successfully assigned user to group")

    except CustomUser.DoesNotExist:
        return HttpResponse("User does not exist")
    except Group.DoesNotExist:
        return HttpResponse("Group does not exist")


def test_view(request):
    return HttpResponse("La aplicación está funcionando correctamente.")
