import setuptools

with open('README.md', 'r') as fh:
    long_description = fh.read()

setuptools.setup(
    name = 'wizards-vs-world-logandgsmith',
    version = '0.0.1',
    author = 'Logan D.G. Smith',
    author_email = 'loganda.smith@ufl.edu',
    description = '2D tactical game involving magic and malice.',
    long_description = long_description,
    long_description_content = 'text/markdown',
    url = 'https://github.com/lukeherczeg/WizardvsWorld',
    packages = setuptools.find_packages(),
    classifiers = [
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent'
    ],
    python_requires='=3.7'
)