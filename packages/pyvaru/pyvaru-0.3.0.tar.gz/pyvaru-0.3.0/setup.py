from distutils.core import setup

with open('README.rst', 'r') as readme:
    long_description = readme.read()

setup(
    name='pyvaru',
    version='0.3.0',
    description='Rule based data validation library for python.',
    long_description=long_description,
    author='Davide Zanotti',
    author_email='davidezanotti@gmail.com',
    license='MIT',
    url='https://github.com/daveoncode/pyvaru',
    classifiers=[
        # How mature is this project? Common values are
        #   3 - Alpha
        #   4 - Beta
        #   5 - Production/Stable
        'Development Status :: 5 - Production/Stable',

        # Indicate who your project is intended for
        'Intended Audience :: Developers',
        'Topic :: Software Development :: Libraries',

        # Pick your license as you wish (should match "license" above)
        'License :: OSI Approved :: MIT License',

        # Specify the Python versions you support here. In particular, ensure
        # that you indicate whether you support Python 2, Python 3 or both.
        'Programming Language :: Python :: 3.2',
        'Programming Language :: Python :: 3.3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
    ],
    keywords='validation rule model data',
    packages=['pyvaru'],
    data_files=[('README.rst', ['README.rst'])],
)
