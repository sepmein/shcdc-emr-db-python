from setuptools import setup, find_packages

setup(
    name="shcdc-emr-db",
    version="0.1.0",
    packages=find_packages(),
    install_requires=[
        "sqlalchemy>=2.0.0",
        "psycopg2-binary>=2.9.9",
        "langchain-community>=0.0.10",
        "configparser>=6.0.0",
    ],
    author="SHCDC",
    author_email="",
    description="A Python package for managing EMR database operations",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    url="",
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.8",
) 