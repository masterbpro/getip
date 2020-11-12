from setuptools import setup, find_packages

from get_ip import __version__

setup(
    name='getip',
    version=__version__,
    url='https:github.com/masterbpro/getip',
    packages=find_packages(),
    python_requires='>3.5',
    install_requires=open('requirements.txt').read().split(),
    entry_points={
        'console_scripts': [
            'getip = get_ip.core:main',
        ],
    },
)
