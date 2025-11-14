#file: core/signals.py

# A modul gondoskodik arról, hogy létezzen egy admin:admin superuser
# (oktatási célú példa, nem éles használatra!)

from django.contrib.auth import get_user_model
from django.db.models.signals import post_migrate
from django.dispatch import receiver


@receiver(post_migrate)
def ensure_default_superuser(sender, **kwargs):
    """
    A függvény ellenőrzi, hogy van-e superuser.
    Ha nincs, automatikusan létrehoz egy admin:admin felhasználót.
    """

    User = get_user_model()

    # Ha már van superuser, nincs teendő
    if User.objects.filter(is_superuser=True).exists():
        return

    # Admin felhasználó létrehozása oktatási célokra
    User.objects.create_superuser(
        username='admin',
        password='admin',
        email='admin@example.com'
    )
