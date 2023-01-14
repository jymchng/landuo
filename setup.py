from setuptools import find_packages, setup

with open("README.md") as f:
    long_description = f.read()

__version__ = "1.5.2"

_extras_require = { }

extras_require = { }

setup(
    name="landuo",
    version=__version__,
    author="Jim Chng",
    author_email="jimchng@outlook.com",
    description="landuo's lazyproperty = cached_property + property",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/jymchng/landuo",
    project_urls={
        "Documentation": "https://landuo.readthedocs.io/",
        "Issue Tracker": "https://github.com/landuo-developers/landuo/issues",
    },
    keywords=["lazy-property", "lazy", "property", "cached", "cached-property", "cached_property", "lazy_property"],
    license="MIT",
    data_files=[("", ["LICENSE"])],
    packages=[],
    package_data={},
    install_requires=[],
    extras_require=extras_require,
    python_requires=">=3.7",
    platforms="any",
    classifiers=[
        "Development Status :: 5 - Production/Stable",
        "Operating System :: OS Independent",
        "License :: OSI Approved :: MIT License",
        "Intended Audience :: Science/Research",
        "Programming Language :: Python",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Topic :: Scientific/Engineering",
    ],
)
