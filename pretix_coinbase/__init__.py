from django.utils.translation import gettext_lazy

try:
    from pretix.base.plugins import PluginConfig
except ImportError:
    raise RuntimeError("Please use pretix 2.7 or above to run this plugin!")

__version__ = "1.0.0"


class PluginApp(PluginConfig):
    name = "pretix_coinbase"
    verbose_name = "Coinbase"

    class PretixPluginMeta:
        name = gettext_lazy("Coinbase")
        author = "Marvin Schopf"
        description = gettext_lazy("Accept payments via Coinbase")
        visible = True
        version = __version__
        category = "PAYMENT"
        compatibility = "pretix>=2.7.0"

    def ready(self):
        from . import signals  # NOQA


default_app_config = "pretix_coinbase.PluginApp"
