#!/usr/bin/env python3

import os
import subprocess
import shutil
import importlib.util
import sys
import click
from RelaxCore import *
from jinja2 import Environment, FileSystemLoader, Template


RELAX_ASCII = """
-----------------------
▗▄▄▖ ▗▞▀▚▖▗▖▗▞▀▜▌▄   ▄ 
▐▌ ▐▌▐▛▀▀▘▐▌▝▚▄▟▌ ▀▄▀  
▐▛▀▚▖▝▚▄▄▖▐▌     ▄▀ ▀▄ 
▐▌ ▐▌     ▐▙▄▄▖        
-----------------------"""

RELAX_VERSION="v0.0.2-Alpha"

def get_component_template(component, extension):
	component_py_code = f"""from RelaxCore import Component

@Component(template="{component}.tex")
def {component}(**kargs):
	return kargs
"""
	if extension == "tex":
		return f"{component} works!"
	elif extension == "py":
		return component_py_code

@click.group
def relaxCLI():
	pass

""" Shows the current version and prints hellow world """
@relaxCLI.command()
def version():
	print(RELAX_ASCII)
	print(RELAX_VERSION)


""" Generate components """
@relaxCLI.command()
@click.option('-c','--component', required=True, help='With a given name creates a new project to work in.', type=str)
@click.pass_context
def create(ctx, component):
	# Declarates the file paths for creation
	routes = [component, f"{component}/Img"]
	component_name = os.path.basename(component.strip())
	file_extensions = ["py", "tex"]

	# Create the file paths
	for route in routes:
		os.mkdir(route)
		os.makedirs(route, exist_ok=True)
		print(f"CREATED: {route}")

	for extension in file_extensions:
		file_path = os.path.join(component, f"{component_name}.{extension}")
		with open(file_path, 'w') as file:
			file.write(get_component_template(component, extension))


""" Creates New projects """
@relaxCLI.command()
@click.option('-p','--project', required=True, help='With a given name creates a new project to work in.', type=str)
@click.option('-t','--template', help='Define the type of the template', type=str)
@click.pass_context
def new(ctx, project, template):
	if os.path.exists(project):
		print(f"Error: The path '{project}' already exists.")
	else:
		extensions  = ["py", "tex"]
		mainfile_name = "main"
		
		os.mkdir(project)
		os.makedirs(project, exist_ok=True)
		print(f"CREATED: {project}")

		# Creates the main.tex and main.py file
		for extension in extensions:
			mainfile_path = os.path.join(project, f"{mainfile_name}.{extension}")
			
			with open(mainfile_path, 'w') as file:  
				file.write(get_component_template(mainfile_name, extension))






def compile_with_pdflatex(tex_file, output_dir, clean):
	"""
	Compiles the given .tex file into a PDF using pdflatex and places all output files in the specified directory.
	"""
	# Asegurarse de que el directorio de salida existe
	os.makedirs(output_dir, exist_ok=True)
	
	# Ejecutar pdflatex tres veces para asegurar la compilación completa (índices, referencias, etc.)
	for _ in range(3):
		subprocess.run(
			["pdflatex", "-output-directory", output_dir, tex_file],
			check=True
		)

	if clean == True:
		# Opcional: Limpiar archivos temporales
		for temp_file in ["aux", "log", "out", "toc"]:
			temp_file_path = os.path.join(output_dir, f"{os.path.splitext(os.path.basename(tex_file))[0]}.{temp_file}")
			if os.path.exists(temp_file_path):
				os.remove(temp_file_path)


""" Uses pdflatex to compile the project into a pdf file """
@relaxCLI.command()
@click.option('-p','--project', required=True, help='Must be the name of a project', type=str)
@click.option('-c', '--clean', help=r'Bool: Clean the "aux", "log", "out", "toc" files', type=bool)
@click.pass_context
def build(ctx, project, clean):
	if not os.path.exists(project):
		print(f"Error: The path '{project}' does not exist.")
	else:
		output_path = os.path.join(project, "output")

		mainfile_path = os.path.join(project, "main.py")
		if os.path.exists(mainfile_path):
			# Add the project directory to sys.path to make its modules discoverable
			sys.path.insert(0, project)

			# Import `main` dynamically from main.py
			spec = importlib.util.spec_from_file_location("main", mainfile_path)
			main_module = importlib.util.module_from_spec(spec)
			spec.loader.exec_module(main_module)

		
			if not os.path.exists(output_path):
				os.mkdir(output_path)
				print(f"CREATED: {output_path}")

			project_name = os.path.basename(os.path.normpath(project))
			output_file_path = os.path.join(output_path, f"{project_name}.tex")

			with open(output_file_path, 'w') as output_file:
				output_file.write(main_module.main()) # Writes the main() result into output file
			
			subprocess.run(["cat", output_file_path])

			tex_file = output_file_path
			compile_with_pdflatex(tex_file, output_path, clean)

		else:
			print(f"Error: main.py does not exist in {mainfile_path}")

def main():
    # Llama a la CLI de click
    relaxCLI()


if __name__ == '__main__':
	main()