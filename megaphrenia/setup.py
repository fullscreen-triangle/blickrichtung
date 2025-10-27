"""
Setup script for Megaphrenia package.

Modern installation uses pyproject.toml, but this file is kept
for backwards compatibility and editable installs.
"""

from setuptools import setup, find_packages
import os

# Read the README for long description
here = os.path.abspath(os.path.dirname(__file__))
with open(os.path.join(here, 'README.md'), 'r', encoding='utf-8') as f:
    long_description = f.read()

setup(
    name="megaphrenia",
    version="1.0.0",
    author="Kundai Farai Sachikonye",
    author_email="sachikonye@wzw.tum.de",
    description="Biological Integrated Circuits with Shooting + Harmonic Balance Validation",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/kundai/megaphrenia",
    project_urls={
        "Bug Tracker": "https://github.com/kundai/megaphrenia/issues",
        "Documentation": "https://github.com/kundai/megaphrenia/blob/main/README.md",
        "Source Code": "https://github.com/kundai/megaphrenia",
    },
    packages=find_packages(where="src"),
    package_dir={"": "src"},
    classifiers=[
        "Development Status :: 4 - Beta",
        "Intended Audience :: Science/Research",
        "Topic :: Scientific/Engineering :: Bio-Informatics",
        "Topic :: Scientific/Engineering :: Physics",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Programming Language :: Python :: 3.12",
    ],
    python_requires=">=3.8",
    install_requires=[
        "numpy>=1.21.0",
        "scipy>=1.7.0",
        "pyyaml>=5.4.0",
    ],
    extras_require={
        "dev": [
            "pytest>=7.0.0",
            "pytest-cov>=3.0.0",
            "black>=22.0.0",
            "flake8>=4.0.0",
            "mypy>=0.950",
        ],
        "viz": [
            "matplotlib>=3.5.0",
            "seaborn>=0.11.0",
        ],
    },
    entry_points={
        "console_scripts": [
            # Add command-line scripts here if needed
            # "megaphrenia=megaphrenia.cli:main",
        ],
    },
    include_package_data=True,
    zip_safe=False,
)

