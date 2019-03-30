import setuptools


def long_description():
    with open('README.md', 'r') as file:
        return file.read()


setuptools.setup(
    name='aiothrottler',
    version='0.0.15',
    author='Michal Charemza',
    author_email='michal@charemza.name',
    description='Throttler for asyncio Python',
    long_description=long_description(),
    long_description_content_type='text/markdown',
    url='https://github.com/michalc/aiothrottler',
    py_modules=[
        'aiothrottler',
    ],
    python_requires='~=3.5',
    tests_require=[
        'aiofastforward==0.0.24',
    ],
    test_suite='test',
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
        'Framework :: AsyncIO',
    ],
)
