"""
Blickrichtung Computational Validation Suite
Setup configuration for package installation
"""

from setuptools import setup, find_packages
from pathlib import Path

# Read the contents of README file
this_directory = Path(__file__).parent
long_description = (this_directory / "src" / "computing" / "README.md").read_text(encoding='utf-8')

setup(
    name="blickrichtung-computing",
    version="2.0.0",
    author="Kundai Sachikonye",
    author_email="your.email@example.com",  # Update this
    description="Computational validation suite for consciousness programming framework",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/yourusername/blickrichtung",  # Update this
    project_urls={
        "Bug Tracker": "https://github.com/yourusername/blickrichtung/issues",
        "Documentation": "https://github.com/yourusername/blickrichtung/tree/main/docs",
        "Source Code": "https://github.com/yourusername/blickrichtung",
    },
    packages=find_packages(where="src"),
    package_dir={"": "src"},
    classifiers=[
        "Development Status :: 4 - Beta",
        "Intended Audience :: Science/Research",
        "Topic :: Scientific/Engineering :: Bio-Informatics",
        "Topic :: Scientific/Engineering :: Medical Science Apps.",
        "Topic :: Scientific/Engineering :: Physics",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Programming Language :: Python :: 3.12",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.8",
    install_requires=[
        "numpy>=1.20.0",
        "scipy>=1.7.0",
        "matplotlib>=3.3.0",
        "networkx>=2.5",
    ],
    extras_require={
        "dev": [
            "pytest>=6.0",
            "pytest-cov>=2.0",
            "black>=21.0",
            "flake8>=3.9",
            "mypy>=0.900",
            "sphinx>=4.0",
            "sphinx-rtd-theme>=0.5",
        ],
        "notebooks": [
            "jupyter>=1.0",
            "ipython>=7.0",
            "pandas>=1.2.0",
            "seaborn>=0.11.0",
        ],
    },
    entry_points={
        "console_scripts": [
            "blickrichtung-validate=computing.run_extended_validations:main",
            "blickrichtung-flux=computing.metabolic_flux_hierarchy:main",
            "blickrichtung-mapper=computing.metabolic_hierarchy_mapper:main",
        ],
    },
    include_package_data=True,
    package_data={
        "computing": ["*.json", "*.yaml"],
    },
    keywords=[
        "consciousness programming",
        "biological computing",
        "metabolic hierarchies",
        "pharmacodynamics",
        "oscillatory networks",
        "Kuramoto oscillators",
        "thermodynamic computation",
    ],
    zip_safe=False,
)
