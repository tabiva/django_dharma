import importlib
import inspect
import os
import pkgutil

from django.conf import settings

from django_dharma.core import CheckCollector


def _inherits_from_check_collector(module, attr_name, base_class):
    attr = getattr(module, attr_name)
    if isinstance(attr, list) or not attr:
        return False

    attr_file = inspect.getfile(attr)
    base_class_file = inspect.getfile(base_class)

    return (
        isinstance(attr, type)
        and issubclass(attr, base_class)
        and id(attr) != id(base_class)
        and os.path.abspath(attr_file) != os.path.abspath(base_class_file)
    )


def collect_protocol_implementations(
    base_class: CheckCollector = CheckCollector,
) -> list[CheckCollector]:
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
                        if _inherits_from_check_collector(
                            module, attr_name, base_class
                        ):

                            implementations.append(getattr(module, attr_name))

                except TypeError:
                    continue
                except Exception as e:
                    print(f"Error processing module {module_name}: {e}")
        except (ModuleNotFoundError, ImportError):
            print(f"Module {app} not found")

    return implementations
