import setuptools

with open("README.md", "r") as readme:
    long_description = readme.read()

setuptools.setup(
    name="WizardVsWorld",
    version= "1.0.0",
    author="Logan D.G. Smith",
    author_email="loganda.smith@ufl.edu",
    description="2D tactical game involving magic and malice.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/lukeherczeg/WizardvsWorld",
    packages=setuptools.find_namespace_packages(include=['WizardVsWorld', 'WizardVsWorld.*', 'WizardVsWorld.assets/*', 'WizardVsWorld.classes/*']),
    package_data={
        '':['*.png', '*.ogg', '*.PNG', '*.txt']
    },
    install_requires=[
        "pygame==1.9.6"
    ],
    entry_points={
        'console_scripts':['WizardVsWorld=classes.game:main']
    },
    classifiers = [
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent"
    ],
    python_requires=">=3.7, <3.8",
)