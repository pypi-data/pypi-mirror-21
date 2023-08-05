from setuptools import setup

setup(name='asdb',
      version='0.3.1',
      description='Instant convenient debugger',
      url='https://github.com/alexmojaki/asdb',
      author='Alex Hall',
      author_email='alex.mojaki@gmail.com',
      license='MIT',
      packages=['asdb'],
      install_requires=['rpdb', 'littleutils'],
      scripts=['bin/asdb'],
      zip_safe=False)
