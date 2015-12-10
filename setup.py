# coding=utf-8

from setuptools import setup, find_packages

setup(
    name='ultros-tools',
    version='0.0.1',
    packages=find_packages(),
    package_dir={},
    scripts=[],
    url='https://ultros.io',
    license='Attribution License 2.0',
    author='Gareth Coles',
    author_email='gdude2002@gmail.com',
    description='Provides various tools for developers looking to extend '
                'Ultros',

    entry_points={
        "console_scripts": [
            "ultros-packager = ultros_packager.__main__:main"
        ]
    }
)
