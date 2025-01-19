#!/bin/bash

main(){
    # Navigate to the src directory
    cd src
    # Create a virtual environment
    python -m venv venv
    # Activate the virtual environment
    source venv/bin/activate
    # Install the required dependencies
    pip install -r requeriments.txt
    # Create the symlink for the relax command
    make_symlink
}

make_symlink(){
    # Define the project directory, script path, and symlink path
    PROJECT_DIR="$HOME/Escritorio/Proyectos/Relax-Project/Relax/src"
    SCRIPT_PATH="$PROJECT_DIR/relax.py"
    BIN_PATH="$HOME/.local/bin/relax"

    # Remove the previous symlink if it exists
    if [ -f "$BIN_PATH" ]; then
        echo "Removing the previous symlink..."
        rm "$BIN_PATH"
    fi

    # Create a new symlink pointing to the latest version of relax.py
    ln -s "$SCRIPT_PATH" "$BIN_PATH"
    echo "Symlink created at $BIN_PATH pointing to $SCRIPT_PATH"
}

# Run the main function
main
