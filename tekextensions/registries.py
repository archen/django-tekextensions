# Core Python imports
from __future__ import unicode_literals, print_function

# Core Django imports
from django.core.exceptions import ImproperlyConfigured
from django.conf.urls import url, patterns, include
from django.core.urlresolvers import reverse

# Third-party imports

# App specific imports


class PopupRegistry(object):
    """
    Registry implementation for tying models together with their respective
    views, forms, and/or templates.

    """

    def __init__(self):
        self._registry = {}

    def register(self, popup):
        """
        Register a popup instance.

        """
        popup_name = getattr(popup, 'popup_name', None)

        if popup_name is None:
            raise ImproperlyConfigured("Popup %r must define a 'popup_name'." % popup)

        self._registry[popup_name] = popup

    def unregister(self, popup_name):
        """
        If present, unregisters a ``Popup``.

        """

        if popup_name in self._registry:
            del(self._registry[popup_name])

    @property
    def urls(self):
        """
        Provides URLconf details for all registered ``Popups``.

        """

        pattern_list = []

        for name in sorted(self._registry.keys()):
            pattern_list.append(url(r'^popup/(?P<model_name>\w+)/?$', include(self._registry[name].urls)))

        url_patterns = []

        url_patterns += patterns('',
                                 *pattern_list
                                 )
        return url_patterns

    def _build_reverse_url(self, name, args=None, kwargs=None):
        """
        A convenience hook for overriding how URLs are built.

        See ``NamespacedPopupRegistry._build_reverse_url`` for an example.
        """
        return reverse(name, args=args, kwargs=kwargs)


class NamespacedPopupRegistry(PopupRegistry):
    """
    An API subclass that respects Django namespaces.
    """
    def __init__(self, urlconf_namespace=None):
        super(NamespacedPopupRegistry, self).__init__()
        self.urlconf_namespace = urlconf_namespace

    def register(self, popup):
        super(NamespacedPopupRegistry, self).register(popup)

    def _build_reverse_url(self, name, args=None, kwargs=None):
        namespaced = "%s:%s" % (self.urlconf_namespace, name)
        return reverse(namespaced, args=args, kwargs=kwargs)