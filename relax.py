import os
import click

RELAX_ASCII = """
-----------------------
▗▄▄▖ ▗▞▀▚▖▗▖▗▞▀▜▌▄   ▄ 
▐▌ ▐▌▐▛▀▀▘▐▌▝▚▄▟▌ ▀▄▀  
▐▛▀▚▖▝▚▄▄▖▐▌     ▄▀ ▀▄ 
▐▌ ▐▌     ▐▙▄▄▖        
-----------------------"""

RELAX_VERSION="v1.0.0 (Alpha)"

@click.group
def relax():
	pass


""" Shows the current version and prints hellow world """
@relax.command()
def hello():
	print(RELAX_ASCII)
	print(RELAX_VERSION)
	print("\n Hello world! \n")


if __name__ == '__main__':
	relax()