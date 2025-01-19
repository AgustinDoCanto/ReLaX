import os
import subprocess
import shutil
import click
from jinja2 import Template


RELAX_ASCII = """
-----------------------
▗▄▄▖ ▗▞▀▚▖▗▖▗▞▀▜▌▄   ▄ 
▐▌ ▐▌▐▛▀▀▘▐▌▝▚▄▟▌ ▀▄▀  
▐▛▀▚▖▝▚▄▄▖▐▌     ▄▀ ▀▄ 
▐▌ ▐▌     ▐▙▄▄▖        
-----------------------"""

RELAX_VERSION="v1.0.0 (Alpha)"


### Auxiliar functions ###

def get_template(template_name):
	if os.path.exists(TEMPLATES_PATH):
		template_path = os.path.join(TEMPLATES_PATH, f"{template_name}.tex")
		if not os.path.exists(template_path):
			raise ValueError(f"The template '{template_name}.tex' does not exist in the given path.")
		else:
			with open(template_path, 'r') as template_file:
				template_content = template_file.read()
			return template_content
	else:
		raise ValueError(f"The templates path '{TEMPLATES_PATH}' does not exist.")

@click.group
def relax():
	pass

""" Shows the current version and prints hellow world """
@relax.command()
def hello():
	print(RELAX_ASCII)
	print(RELAX_VERSION)
	print("\n Hello world! \n")


def get_component_template(component, extension):
	if extension == "tex":
		template = r"""
\documentclass[a4paper,12pt]{article}

% Additional packages you may need
\usepackage[utf8]{inputenc}   % UTF-8 character encoding
\usepackage{amsmath}          % Package for advanced mathematics

% Document title
\title{My LaTeX Document}
\author{Document Author}
\date{\today}  % Current date

\begin{document}

% Print the title
\maketitle

\end{document}
"""
		return template

	

""" Generate components """
@relax.command()
@click.option('-c','--component', required=True, help='With a given name creates a new project to work in.', type=str)
@click.pass_context
def create(ctx, component):
	# Declarates the file paths for creation
	routes = [component, f"{component}/Img"]

	component_name = os.path.basename(component.strip())
	
	file_extensions = ["tex"]

	# Create the file paths
	for route in routes:
		os.mkdir(route)
		os.makedirs(route, exist_ok=True)
		print(f"CREATED: {route}")

	for extension in file_extensions:
		file_path = os.path.join(component, f"{component_name}.{extension}")
		with open(file_path, 'w') as file:
			file.write(get_component_template(component, extension))


""" Generate projects """
@relax.command()
@click.option('-p','--project', required=True, help='With a given name creates a new project to work in.', type=str)
@click.option('-t','--template', help='Define the type of the template', type=str)
@click.pass_context
def generate(ctx, project, template):
	if os.path.exists(project):
		print(f"Error: The path '{project}' already exists.")
	else:
		mainfile_name = "main.tex"
		mainfile_path = os.path.join(project, mainfile_name)
	
		os.mkdir(project)
		os.makedirs(project, exist_ok=True)

		create.callback(f"{project}/main")



""" Uses pdflatex to compile the project into a pdf file """
@relax.command()
@click.option('-p','--project', required=True, help='Must be the name of a project', type=str)
@click.pass_context
def build(ctx, project):
	build_file_path = os.path.join(project, BUILD_FILE_NAME)
	if not os.path.exists(project):
		print(f"Error: The path '{project}' does not exists.")
	elif not os.path.exists(build_file_path):
		print(f"Error: The path to '{BUILD_FILE_NAME}' build file does not exist")
	else:
		print(build_file_path)
		subprocess.run(["python", build_file_path])



if __name__ == '__main__':
	relax()