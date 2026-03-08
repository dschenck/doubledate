import setuptools
import re
import ast
import os

# https://stackoverflow.com/questions/6786555/automatic-version-number-both-in-setup-py-setuptools-and-source-code
with open(os.path.join(os.path.dirname(__file__), "doubledate/__init__.py"), "rb") as f:
    version = str(
        ast.literal_eval(
            re.compile(r"__version__\s+=\s+(.*)")
            .search(f.read().decode("utf-8"))
            .group(1)
        )
    )

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="doubledate",
    version=version,
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
    install_requires=["python-dateutil", "sortedcontainers"],
)
