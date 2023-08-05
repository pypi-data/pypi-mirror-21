from importlib import import_module


class require_modules(object):
    """Context manager to check the availability of required modules"""

    def __init__(self, modules):
        self._missing_modules = []
        for module in modules:
            try:
                import_module(module)
            except ImportError:
                self._missing_modules.append(module)

    def __enter__(self):
        return self._missing_modules

    def __exit__(self, exc_type, exc_value, traceback):
        return False
