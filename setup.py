from setuptools import setup, find_packages

setup(
    name="parallel-dl",
    version="0.1.0",
    packages=find_packages(),
    install_requires=[
        "requests>=2.28.0",
        "tqdm>=4.65.0",
    ],
)
