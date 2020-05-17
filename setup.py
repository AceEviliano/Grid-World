
# text of the README file
README = (HERE/'RAEDME.md').read_text()

setup(
	name = 'GridWorld'
	version = '1.0.0'
	description = 'A simple API to variations of gridworld used for classic RL experiments'

	long_description = README

	

)

setup(
    name = 'GridWorld',
    version = '1.0.0',
    description = 'A simple API to variations of gridworld used for classic RL experiments',
    long_description = README,
    long_description_content_type = "text/markdown",
    url = 'https://github.com/AceEviliano/Grid-World',
    author = 'Rishi S Rao',
    author_email = 'harishi.ace@gmail.com',
    license = 'MIT',
    classifiers=[
        "License :: OSI Approved :: MIT License",
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
