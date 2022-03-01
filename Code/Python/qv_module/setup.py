import setuptools

with open("README.md", "r") as f:
    long_description = f.read()

setuptools.setup(
    name='qv_module',
    version='0.0.1',
    author='XX',
    author_email='xx@xx.xx',
    description='an example of a python module.',
    long_description=long_description,
    long_description_content_type='ext/markdown',
    packages=setuptools.find_packages(),
    classifiers=(
        "Programming Language :: Python :: 3",
        "Operating System :: OS Independent",
    ),
)