from setuptools import find_packages,setup
from typing import List

hyphen = '-e .'
def get_requirements(file_path:str)->List[str]:
    #this gonna return list of requirements
    requirements = []
    with open(file_path) as file:
        requirements = file.readlines()
        requirements = [req.replace("/n","") for req in requirements]

        if hyphen in requirements:
            requirements.remove(hyphen)

    return requirements



setup(
    name = 'mlproject', 
    version = '0.0.1',
    author = 'shivam',
    author_email = "shivam4806@gmail.com",
    packages = find_packages(),
    install_requires= get_requirements('requirements.txt')
)