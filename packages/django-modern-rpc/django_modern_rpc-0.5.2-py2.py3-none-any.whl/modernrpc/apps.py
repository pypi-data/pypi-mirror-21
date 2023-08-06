# coding: utf-8
import inspect
import warnings
from importlib import import_module

from django.apps import AppConfig

from modernrpc.conf import settings
from modernrpc.core import register_rpc_method, get_all_method_names, unregister_rpc_method


class ModernRpcConfig(AppConfig):

    name = 'modernrpc'
    verbose_name = 'Django Modern RPC'

    def ready(self):

        if settings.MODERNRPC_METHODS_MODULES:

            # When project use a persistant cache (Redis, memcached, etc.) the cache is not always flushed
            # when django project is restarted. As a result, we may have a registry with a list of methods
            # from the last run.
            methods_before_lookup = get_all_method_names()

            modules_to_scan = settings.MODERNRPC_METHODS_MODULES
            # Add internal system methods to the registry
            modules_to_scan.append('modernrpc.system_methods')

            for module_name in modules_to_scan:

                try:
                    module = import_module(module_name)

                except ImportError:
                    msg = 'Unable to load module "{}" declared in settings.MODERNRPC_METHODS_MODULES. Please ensure ' \
                          'it is available and doesn\'t contains any error'.format(module_name)
                    warnings.warn(msg, category=Warning)
                    continue

                for _, func in inspect.getmembers(module, inspect.isfunction):
                    if getattr(func, 'modernrpc_enabled', False):
                        registered_name = register_rpc_method(func)
                        try:
                            # Ensure method is not listed in methods_before_lookup after registration
                            methods_before_lookup.remove(registered_name)
                        except ValueError:
                            pass

            # Some rpc methods stored in the registry from the last run were not registered this session.
            # That means a RPC method has been deleted from the code (or the decorator has been removed)
            # In such case, we must remove the function from the registry
            for useless_method in methods_before_lookup:
                unregister_rpc_method(useless_method)

        else:
            txt = "settings.MODERNRPC_METHODS_MODULES is not set. Django-modern-rpc cannot determine which python " \
                  "modules define your RPC methods. Please define settings.MODERNRPC_METHODS_MODULES to indicate the " \
                  "modules that contains your methods."
            warnings.warn(txt, category=Warning)
