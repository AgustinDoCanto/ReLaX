# Created By: Agustin Do Canto 2025

import os
from jinja2 import Environment, FileSystemLoader

components_paths = []

def create_environment():
	"""
	Configura el entorno Jinja2 dinámicamente basado en los componentes registrados.
	"""
	return Environment(
		loader=FileSystemLoader(components_paths),
		block_start_string='<$',
		block_end_string='$>',
		variable_start_string='<<',
		variable_end_string='>>',
		comment_start_string='<#',
		comment_end_string='#>'
	)

# Inicializamos el entorno Jinja2
env = create_environment()

"""
Renderiza un componente Jinja2 utilizando el contexto recibido.
"""
def render_component(template_name, **context):
	template = env.get_template(template_name)
	return template.render(**context)

# Decorador genérico
def Component(template):
	"""
	Decorador que envuelve la función para renderizar un componente con contexto combinado.
	"""
	def decorator(func):
		def wrapper(**given_context):
			# Agregar el directorio actual del componente si no está en components_paths
			component_dir = os.path.dirname(os.path.abspath(func.__code__.co_filename))
			if component_dir not in components_paths:
				components_paths.append(component_dir)
				global env  # Actualizar el entorno dinámicamente
				env = create_environment()
				
			# Obtener el contexto predeterminado desde la función decorada
			default_context = func()
			# Combinar contextos: el contexto dado tiene prioridad sobre el predeterminado
			combined_context = {**default_context, **given_context}
			# Renderizar la plantilla con el contexto combinado
			return render_component(template_name=template, **combined_context)
		return wrapper
	return decorator
