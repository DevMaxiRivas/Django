# # import os
# from typing import Any
# from django.shortcuts import render, redirect

# # Autenticacion
# from django.contrib.auth import authenticate, login

# # Vistas
# from django.views.generic import (
#     ListView,
#     TemplateView,
# )

# # Grupos
# from django.contrib.auth.models import Group

# # Formularios
# from .forms import RegisterForm

# from django.views import View

# # PAGINA DE INICIO
# @add_group_name_to_context


from typing import Any
from django.shortcuts import render, redirect, get_object_or_404

from django.contrib.auth import authenticate, login
from django.views.generic import (
    ListView,
    TemplateView,
    CreateView,
    UpdateView,
    DeleteView,
    DetailView,
)

from django.contrib.auth.models import Group

# from .forms import RegisterForm, UserForm, ProfileForm, CourseForm, UserCreationForm
from .forms import RegisterForm, UserCreationForm
from django.views import View

class HomeView(TemplateView):
    template_name = "home.html"

    # Funcion que determina el Grupo al que pertenece el usuario
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        user = self.request.user
        group_name = None
        if user.is_authenticated:
            group = Group.objects.filter(user=user).first()
            if group:
                group_name = group.name

        context["group_name"] = group_name
        return context

# # REGISTRO DE USUARIOS
class RegisterView(View):
    # Cargamos la pagina con el fprmulario
    def get(self, request):
        data = {"form": RegisterForm()}
        return render(request, "registration/register.html", data)

    # Manejamos el formulario que se envia al servidor
    def post(self, request):
        user_creation_form = RegisterForm(data=request.POST)
        if user_creation_form.is_valid():
            user_creation_form.save()
            user = authenticate(
                username=user_creation_form.cleaned_data["username"],
                password=user_creation_form.cleaned_data["password1"],
            )
            login(request, user)

            # Actualizar el campo created_by_admin del modelo Profile
            user.profile.created_by_admin = False
            user.profile.save()

            return redirect("home")
        data = {"form": user_creation_form}
        return render(request, "registration/register.html", data)
