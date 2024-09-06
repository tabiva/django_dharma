from setuptools import find_packages, setup

setup(
    name="django-dharma",
    version="0.1",
    packages=find_packages(),
    include_package_data=True,
    description="A Django app to run checks on models",
    author="Ivan Tabarelli",
    author_email="itabarelli@gmail.com",
    url="https://github.com/tabiva/django-dharma",
    classifiers=[
        "Programming Language :: Python :: 3",
        "Framework :: Django",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    install_requires=[
        "Django>=3.2",
    ],
)
