from setuptools import setup, find_packages

setup(
    name="relax",
    version="0.0.2-alpha",
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
            "relax=relax:main"
        ]
    },
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: GNU General Public License v3 (GPLv3)",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.9",
)
