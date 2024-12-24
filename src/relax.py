import os
import subprocess
import shutil
import click

RELAX_ASCII = """
-----------------------
▗▄▄▖ ▗▞▀▚▖▗▖▗▞▀▜▌▄   ▄ 
▐▌ ▐▌▐▛▀▀▘▐▌▝▚▄▟▌ ▀▄▀  
▐▛▀▚▖▝▚▄▄▖▐▌     ▄▀ ▀▄ 
▐▌ ▐▌     ▐▙▄▄▖        
-----------------------"""

RELAX_VERSION="v1.0.0 (Alpha)"
TEMPLATES_PATH = "./templates"
BUILD_FILE_NAME = "build.py"

MINIMAL_TEMPLATE = r"""
\documentclass[a4paper,12pt]{article}

% Additional packages you may need
\usepackage[utf8]{inputenc}   % UTF-8 character encoding
\usepackage{amsmath}          % Package for advanced mathematics
\usepackage{graphicx}         % Package to insert images
\usepackage{hyperref}         % For links in the document
\usepackage{geometry}         % For adjusting margins

% Adjusting margins
\geometry{top=2cm, bottom=2cm, left=2cm, right=2cm}

% Document title
\title{My LaTeX Document}
\author{Document Author}
\date{\today}  % Current date

\begin{document}

% Print the title
\maketitle

\section{Introduction}

\end{document}
"""

BUILD_FILE_CONTENT = r"""
import os
import subprocess

MAIN_FILE_NAME = "main.tex"
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
MAIN_FILE_PATH = os.path.join(SCRIPT_DIR, MAIN_FILE_NAME)

def compile(main_file_path):
	if os.path.exists(main_file_path):
		subprocess.run([
			"pdflatex",
			"-output-directory", SCRIPT_DIR,
			main_file_path
		])
	else:
		print(f"Error: '{main_file_path}' does not exist.")

if __name__ == '__main__':
	compile(MAIN_FILE_PATH)
"""

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


""" Generte projects """
@relax.command()
@click.option('--project', required=True, help='With a given name creates a new project to work in.', type=str)
@click.option('--template', help='Define the type of the template', type=str)
@click.pass_context
def generate(ctx, project, template):
	if os.path.exists(project):
		print(f"Error: The path '{project}' already exists.")
	else:
		mainfile_name = "main.tex"
		mainfile_path = os.path.join(project, mainfile_name)
	
		buildfile_path = os.path.join(project, BUILD_FILE_NAME) 

		project_images_path = os.path.join(project, "img")

		os.mkdir(project)
		os.mkdir(project_images_path)

		os.makedirs(project, exist_ok=True)
		os.makedirs(project_images_path, exist_ok=True)

		try:
			if not template:
				project_template = MINIMAL_TEMPLATE
			else:
				project_template = get_template(template)

			with open(mainfile_path, "w") as mainfile:
				mainfile.write(project_template)

			with open(buildfile_path, "w") as buildfile:
				buildfile.write(BUILD_FILE_CONTENT)

		except:
			shutil.rmtree(project)
			print("Error opening the template, try with another name")


""" Uses pdflatex to compile the project into a pdf file """
@relax.command()
@click.option('--project', required=True, help='Must be the name of a project', type=str)
@click.pass_context
def compile(ctx, project):
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