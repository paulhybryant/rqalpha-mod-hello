# pip >= 10
from pip._internal.req import parse_requirements
from setuptools import (
    find_packages,
    setup,
)
import pathlib

with open(
        pathlib.Path(__file__).parent.joinpath('rqalpha_mod_local_source',
                                               'VERSION.txt'), 'rb') as f:
    version = f.read().decode('ascii').strip()
    """
        作为一个合格的mod，应该要有版本号哦。
    """

setup(
    name='rqalpha-mod-local-source',  #mod名
    version=version,
    description='RQAlpha Mod to load bar data from local file',
    packages=find_packages(exclude=[]),
    author='paulhybryant',
    author_email='paulhybryant@gmail.com',
    license='Apache License v2',
    package_data={'': ['*.*']},
    url='https://github.com/paulhybryant/rqalpha-mod-local-source',
    install_requires=[
        str(ir.requirement)
        for ir in parse_requirements("requirements.txt", session=False)
    ],
    zip_safe=False,
    classifiers=[
        'Programming Language :: Python',
        'Operating System :: Microsoft :: Windows',
        'Operating System :: Unix',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
    ],
)
