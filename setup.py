from setuptools import setup, find_packages
import os
import re

def read_version():
    version_file = os.path.join(os.path.dirname(__file__), "src/relax/", "__version__.py")
    with open(version_file, encoding="utf-8") as f:
        match = re.search(r'^__version__\s*=\s*["\'](.+?)["\']', f.read())
        if match:
            return match.group(1)
        raise RuntimeError("No se pudo encontrar la versión.")

setup(
    name="doc-relax",
    version=read_version(),
    author="Agustin Do Canto",
    author_email="docantocontacto@gmail.com",
    description="ReLaX (Rendering Environment for LaTeX) is a rendering framework designed to automate the creation of documents using LaTeX-based templates.",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    packages=find_packages(where="src"),
    package_dir={"": "src"},
    include_package_data=True,
    install_requires=[
        "click",
        "jinja2"
    ],
    entry_points={
        "console_scripts": [
            "relax=relax.relax:main"
        ]
    },
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: GNU General Public License v3 (GPLv3)",
        "Operating System :: OS Independent",
    ],
    url="https://github.com/AgustinDoCanto/ReLaX",
    project_urls={
        "Bug Tracker": "https://github.com/AgustinDoCanto/ReLaX/issues",
        "Documentation": "https://github.com/AgustinDoCanto/ReLaX#readme",
        "Source Code": "https://github.com/AgustinDoCanto/ReLaX",
    },
    python_requires=">=3.9",
)
