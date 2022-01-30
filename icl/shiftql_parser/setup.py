import setuptools

long_description = ()

setuptools.setup(
    name="shiftql_parser",
    version="0.0.1",
    author="Xiaozhe Yao",
    author_email="askxzyao@gmail.com",
    description="ShiftQL Parser",
    long_description=long_description,
    long_description_content_type="text/markdown",
    packages=["libparser"],
    license="MIT",
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Intended Audience :: Developers",
        "Intended Audience :: Education",
        "Intended Audience :: Information Technology",
        "Intended Audience :: Science/Research",
        "Topic :: Scientific/Engineering",
        "Topic :: Scientific/Engineering :: Image Recognition",
        "Topic :: Software Development",
    ],
    install_requires=[
        "ply"
    ],
)
