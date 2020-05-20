import pathlib
from setuptools import setup

# The directory containing this file
HERE = pathlib.Path(__file__).parent


# text of the README file
README = (HERE/'README.md').read_text()

setup(
    name = 'Grid-World',
    version = '1.0.0',
    description = 'A simple API to variations of gridworld used for classic RL experiments',
    long_description = README,
    long_description_content_type = "text/markdown",
    url = 'https://github.com/AceEviliano/Grid-World',
    author = 'Rishi S Rao',
    author_email = 'harishi.ace@gmail.com',
    license = 'GPLv3.0',
    classifiers=[
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.7",
    ],
    packages=['gridworld'],
    include_package_data=True,
    install_requires=['numpy', 'matplotlib'],
    entry_points={
        'console_scripts': [
            'gridworld=gridworld.__main__:main',
        ]
    },
)
