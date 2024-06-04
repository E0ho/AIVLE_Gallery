from django.apps import AppConfig


class GalleryuserConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'GalleryUser'

    def ready(self):
        import GalleryUser.signals