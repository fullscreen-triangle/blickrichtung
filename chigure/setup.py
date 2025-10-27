"""
Setup script for Chigure - Consciousness Validation Engine

This file exists for backwards compatibility with older pip versions.
Modern installations should use pyproject.toml.
"""

from setuptools import setup, find_packages
from pathlib import Path

# Read the long description from README
this_directory = Path(__file__).parent
long_description = ""
readme_path = this_directory / "README.md"
if readme_path.exists():
    long_description = readme_path.read_text(encoding='utf-8')

setup(
    name="chigure",
    version="1.0.0",
    description="Consciousness Validation Engine: Physical implementation of consciousness detection",
    long_description=long_description,
    long_description_content_type="text/markdown",
    author="Kundai",
    author_email="your.email@example.com",
    url="https://github.com/yourusername/blickrichtung",
    license="MIT",
    
    # Package discovery
    package_dir={"": "src"},
    packages=find_packages(where="src"),
    
    # Python version requirement
    python_requires=">=3.8",
    
    # Core dependencies
    install_requires=[
        "numpy>=1.21.0",
        "scipy>=1.7.0",
        "matplotlib>=3.4.0",
        "pandas>=1.3.0",
        "scikit-learn>=1.0.0",
        "tqdm>=4.62.0",
    ],
    
    # Optional dependencies
    extras_require={
        "dev": [
            "pytest>=7.0.0",
            "pytest-cov>=3.0.0",
            "black>=22.0.0",
            "flake8>=4.0.0",
            "mypy>=0.950",
            "ipython>=8.0.0",
            "jupyter>=1.0.0",
        ],
        "hardware": [
            "pyserial>=3.5",
            "pyvisa>=1.12.0",
            "pyvisa-py>=0.5.3",
        ],
        "visualization": [
            "plotly>=5.0.0",
            "seaborn>=0.11.0",
            "networkx>=2.6.0",
        ],
    },
    
    # Entry points for command-line scripts
    entry_points={
        "console_scripts": [
            "chigure-validate=scripts.run_validation:main",
            "chigure-experiment=experimental.complete_system:run_complete_experiment",
        ],
    },
    
    # Package metadata
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
    ],
    
    keywords=[
        "consciousness",
        "oscillatory-holes",
        "categorical-completion",
        "oxygen-clock",
        "BMD",
        "thought-geometry",
        "neuroscience",
        "pharmacology",
    ],
    
    # Include package data
    include_package_data=True,
    zip_safe=False,
)

