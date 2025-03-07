from setuptools import setup, find_packages

setup(
    name="py-arrakis",
    version="0.0.1",
    author="Abhishek Bhardwaj",
    author_email="abshkbh@gmail.com",
    description="A placeholder package to reserve the py-arrakis name",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    url="https://github.com/abshkbh/py-arrakis",
    packages=find_packages(),
    classifiers=[
        "Development Status :: 1 - Planning",
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.6",
)
