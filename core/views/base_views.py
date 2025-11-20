#file: core/views/base_views.py
# Alap nézetek: kezdőoldal, statikus oldalak.

from django.shortcuts import render


def index_view(request):
    """A projekt főoldala."""
    return render(request, "index.html")
