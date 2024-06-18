from setuptools import setup, find_packages

setup(
    name='AnaHiePro',
    version='0.1.0',
    author='Oleh Danylevych',
    author_email='danylevych123@gmail.com',
    description='"AnaHiePro" is a module that allows solving various tasks of systems analysis using the Analytic Hierarchy Process (AHP).',
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    url='https://github.com/danylevych/AnaHiePro',
    packages=find_packages(),
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
    python_requires='>=3.6',
)
