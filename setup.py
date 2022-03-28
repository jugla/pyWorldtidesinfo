"""Setup of the package."""
import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="pyWorldtidesinfo",
    version="2.0.1",
    license="MIT",
    author="jugla",
    author_email="jugla@users.github.com",
    description="Get tides info from World Tides Info Server",
    long_description=long_description,
    url="http://github.com/jugla/pyWorldtidesinfo/",
    packages=setuptools.find_packages(include=["pyworldtidesinfo"]),
    setup_requires=["requests", "setuptools"],
    install_requires=["requests"],
    entry_points={
        "console_scripts": ["pyworldtidesinfo = pyworldtidesinfo.__main__:main"]
    },
)
