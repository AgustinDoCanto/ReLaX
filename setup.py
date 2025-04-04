from setuptools import setup, find_packages

setup(
    name="relax",
    version="0.0.2-alpha",
    author="Agustin Do Canto",
    author_email="docantocontacto@email.com",
    description="A project for managing TeX components with RelaxCore",
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
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.6",
)
