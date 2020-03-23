import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="doubledate",
    version="0.0.6",
    author="david.schenck@outlook.com",
    author_email="david.schenck@outlook.com",
    description="A calendar wrapper",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/dschenck/doubledate",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    install_requires=['python-dateutil', 'sortedcontainers']
)
