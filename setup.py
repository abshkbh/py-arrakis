from setuptools import setup, find_packages

setup(
    name="py-arrakis",
    version="0.0.1",
    author="Abhishek Bhardwaj",
    author_email="abshkbh@gmail.com",
    description="SDK (wip) for https://github.com/abshkbh/arrakis",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    url="https://github.com/abshkbh/py-arrakis",
    packages=find_packages(),
    classifiers=[
        "Development Status :: 1 - Planning",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.9",
)
