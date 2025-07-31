from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name="project-structure-creator",
    version="0.1.0",
    author="Wiradjuri",
    author_email="bmuzza1992@hotmail.com",
    description="A tool to create project structures from text descriptions",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/Wiradjuri/project-structure-creator",
    packages=find_packages(),
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
    ],
    python_requires=">=3.8",
    install_requires=[
        # Add your dependencies here
        
    ],
    entry_points={
        "console_scripts": [
            "project-structure-creator=project_structure_creator.main:main",
            "project-structure-creator-gui=project_structure_creator.gui:run_gui",
        ],
    },
)
