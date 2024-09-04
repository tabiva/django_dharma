import importlib
import pkgutil
from typing import List, Protocol, Type

from django.conf import settings


def collect_protocol_implementations(protocol: Type[Protocol]) -> List[Type[Protocol]]:
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
                        attr = getattr(module, attr_name)
                        if (
                            isinstance(attr, type)
                            and issubclass(attr, protocol)
                            and attr is not protocol
                        ):
                            implementations.append(attr)
                except Exception as e:
                    print(f"Error processing module {module_name}: {e}")
        except ModuleNotFoundError:
            print(f"Module {app} not found")

    return implementations
