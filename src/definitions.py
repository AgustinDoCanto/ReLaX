from jinja2 import Environment, FileSystemLoader

# Configuración de Jinja2
env = Environment(loader=FileSystemLoader('templates'))

# Registro global de componentes
components_registry = {}

# Decorador para definir componentes
def Component(template_name):
    def decorator(cls):
        cls.template = env.get_template(template_name)
        components_registry[cls.__name__] = cls
        return cls
    return decorator
