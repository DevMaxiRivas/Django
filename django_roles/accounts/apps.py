from django.apps import AppConfig


class AccountsConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "accounts"
    verbose_name = "perfiles"

    # La funcion se llama cuando se carga la aplicacion y se utiliza
    # para realizar cualquier inicializacion o configuracion que deba
    # realizarse antes de que se pueda usar la aplicacion
    def ready(self):
        import accounts.signals
