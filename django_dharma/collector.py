import importlib
import pkgutil
import traceback

from django.conf import settings

from django_dharma.protocols import CheckProtocol
import inspect

from typing import List, Type
from importlib import import_module
from django.apps import apps


def _implements_protocol(module, attr_name, protocol):
    attr = getattr(module, attr_name)
    return (
        isinstance(getattr(module, attr_name), type)
        and issubclass(attr, protocol)
        and attr is not protocol
    )


def collect_protocol_implementations(protocol: CheckProtocol) -> list[CheckProtocol]:
    """
    Collects all classes that implement a specific protocol across the entire project.

    :param protocol: The protocol class to search for implementations.
    :return: A list of classes implementing the specified protocol.
    """
    implementations = []

    for app in settings.INSTALLED_APPS:
        try:
            app_module = importlib.import_module(app)

            for _, module_name, _ in pkgutil.iter_modules(
                app_module.__path__, app + "."
            ):
                try:
                    module = importlib.import_module(module_name)

                    for attr_name in dir(module):
                        if _implements_protocol(module, attr_name, protocol):
                            implementations.append(getattr(module, attr_name))

                except TypeError:
                    traceback.print_exc()
                    continue
                except Exception as e:
                    print(f"Error processing module {module_name}: {e}")
        except (ModuleNotFoundError, ImportError):
            print(f"Module {app} not found")

    return implementations
