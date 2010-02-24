import sys
import nationalrail
from setuptools import setup, find_packages

setup(
    name="pynationalrail",
    version=nationalrail.__VERSION__,
    packages=find_packages(exclude=['tests', 'myrail', 'myrail.*',]),
    install_requires = ['BeautifulSoup>=3.1.0.1'],
    
    description="Python implementation of National rail api (UK)",
    author="Prabhu Subramanian",
    author_email="prabhu.subramanian@gmail.com",
    maintainer="Prabhu Subramanian",
    maintainer_email="prabhu.subramanian@gmail.com",
    
    url="http://github.com/prabhu/pynationalrail",
)
