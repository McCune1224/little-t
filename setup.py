import setuptools


setuptools.setup(
    name="little-t-ALEX-MCCUNE",
    version="0.0.1",
    author="Alex McCune",
    author_email="alexmccune1224@gmail.com",
    description="Little-t code",
    classifiers=[
        "Programming Language :: Python :: 3",
    ],
    package_dir={"": "src"},
    packages=setuptools.find_packages(where="src"),
    python_requires=">=3.9",
)
