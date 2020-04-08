import setuptools

with open("README.md", "r") as rm:
    long_description = rm.read()

with open("requirements.txt") as r:
    requirements = r.readlines()

setuptools.setup(
    name="canano",
    version="0.0.2",
    author="Tj Bruno",
    author_email="Tbruno25@gmail.com",
    description="Python library for Canano Raspberry Pi add-on board",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/Tbruno25/canano",
    install_requires=requirements,
    packages=setuptools.find_packages(),
)
