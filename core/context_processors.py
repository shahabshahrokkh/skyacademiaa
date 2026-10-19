"""Context processor to inject site settings into all templates."""

from .models import SiteSettings


def site_settings(request):
    """Add global site settings to template context."""
    try:
        settings = SiteSettings.load()
    except Exception:
        settings = None
    return {'site_settings': settings}
