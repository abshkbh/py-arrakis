from setuptools import setup, find_packages

setup(
    name="py-arrakis",
    version="0.1.1",
    author="Abhishek Bhardwaj",
    author_email="abshkbh@gmail.com",
    description="Python SDK for the Arrakis sandboxes - https://github.com/abshkbh/arrakis",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    url="https://github.com/abshkbh/py-arrakis",
    packages=find_packages(),
    install_requires=[
        "requests>=2.25.0",
    ],
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Programming Language :: Python :: 3.12",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Intended Audience :: Developers",
        "Topic :: Software Development :: Libraries :: Python Modules",
    ],
    python_requires=">=3.9",
    keywords="virtualization, sandbox, vm, testing",
)
