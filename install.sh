#!/bin/bash

main(){
	python -m venv venv
	source venv/bin/activate
	pip install -r requeriments.txt
	# make_alias # UNCOMMENT this if you wanna create the relax alias in your system
}

make_alias(){
	CONFIG_FILE="$HOME/.bashrc"

	ALIAS_COMMAND="alias relax='python relax.py'"

	if ! grep -Fxq "$ALIAS_COMMAND" "$CONFIG_FILE"; then
	    echo "$ALIAS_COMMAND" >> "$CONFIG_FILE"
	    source ~/.bashrc
	    echo "Alias added to $CONFIG_FILE"
	else
	    echo "Error: the alias already exists $CONFIG_FILE"
	fi
}

main