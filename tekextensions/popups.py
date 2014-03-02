__author__ = 'archen'

# Core Django imports
from django.conf.urls import url, patterns
from django.utils import six

# App-specific imports
from tekextensions import views


class Popup(object):
    """
    Generic Popup base class that should be inherited from for all
    ``Popup`` instances.

    Based on tastypie.resources.ResourceOptions

    """

    popup_name = 'default'
    template = None
    view = None
    form = None

    def __new__(cls, meta=None):
        overrides = {}

        # Handle overrides.
        if meta:
            for override_name in dir(meta):
                if not override_name.startswith('_'):
                    overrides[override_name] = getattr(meta, override_name)

        if six.PY3:
            return object.__new__(type('Popup', (cls,), overrides))
        else:
            return object.__new__(type(b'Popup', (cls,), overrides))


class AddRelatedObjectPopup(Popup):
    def urls(self):
        """
        Constructs the url patterns for inclusion in a URLConf.

        """

        pattern_list = [
            url(r'^add/(?P<model_name>\w+)/?$', views.add_new_model,
                kwargs={'template': getattr(self, 'template', None),
                        'form': getattr(self, 'form', None)},
                name=getattr(self, 'popup_name', None)),
        ]

        url_patterns = patterns('',
                                *pattern_list
                                )
        return url_patterns