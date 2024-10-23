from setuptools import setup, find_packages

setup(
    name="static-site-generator",
    version="0.0.1",  # Early version
    description="A simple static site generator in Python",
    packages=find_packages(),
    python_requires=">=3.7",
    install_requires=[],  # Add regular dependencies if any
    extras_require={
        "dev": [
            "pre-commit",
            "coverage",
            "flake8",
            "black",
            "isort",
            "mypy",  # Optional
        ],
    },
)
