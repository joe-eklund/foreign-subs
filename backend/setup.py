"""Define user package requirements and various project metadata."""

from setuptools import setup, find_packages

VERSION = __import__('fsubs').__VERSION__

setup(name='fsubs',
      version=VERSION,
      author='Joe Eklund, Sam Eklund, Nick Wong, Sam Maphey',
      packages=find_packages(),
      entry_points={
          'console_scripts': [
              'fsubs = fsubs.__main__:cli',
          ]
      },
      install_requires=[
        'addict',
        'fastapi',
        'pyjwt',
        'pymongo',
        'python-multipart',
        'typer',
        'uvicorn',
      ],
      )
