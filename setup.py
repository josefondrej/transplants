import setuptools

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setuptools.setup(
    name="transplants",  # Replace with your own username
    version="0.0.1",
    author="Josef Ondrej",
    author_email="josef.ondrej@outlook.com",
    description="Solver for the paired kidney exchange programmes",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/josefondrej/transplants",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.8',
)
