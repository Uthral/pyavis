from abc import ABC, abstractmethod

class Backend(ABC):
    _widget_registry_name = "widget"
    _gfx_registry_name = "gfx"

    @classmethod
    def register_gfx(backend, entity):
        def decorator(gfx_class):
            backend.get_gfx_registry()[entity] = gfx_class
        return decorator
    
    @classmethod
    def register_widget(backend, entity):
        def decorator(widget_class):
            backend.get_widget_registry()[entity] = widget_class
        return decorator
    
    @classmethod
    def get_gfx_registry(backend):
        return backend._get_registry(backend._gfx_registry_name)
    
    @classmethod
    def get_widget_registry(backend):
        return backend._get_registry(backend._widget_registry_name)
    
    @classmethod
    @abstractmethod
    def _get_registry(backend, registry_name) -> dict:
        pass



    
