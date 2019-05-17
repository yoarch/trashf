import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="trashf",
    version="1.0.1",
    python_requires='>=3',
    author="yoarch",
    author_email="yo.managements@gmail.com",
    description="CLI tool to safely remove any file and directory by putting them in the trash",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/yoarch/trashf",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    entry_points={
	"console_scripts": [
	"trashf = trashf.trashf:main",
	"rt = trashf.trashf:main"
        ]
    })
