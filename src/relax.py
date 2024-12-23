import os
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
	if not os.path.exists(project):
		mainfile_name = "main.tex"
		mainfile_path = os.path.join(project, mainfile_name)
		project_images_path = os.path.join(project, "img")

		os.mkdir(project)
		os.mkdir(project_images_path)

		os.makedirs(project, exist_ok=True)
		os.makedirs(project_images_path, exist_ok=True)

		try:
			project_template = get_template(template)

			with open(mainfile_path, "w") as mainfile:
				mainfile.write(project_template)
		except:
			shutil.rmtree(project)
			print("Error opening the template, try with another name")
	else:
		print(f"Error: The path '{project}' already exists.")


if __name__ == '__main__':
	relax()