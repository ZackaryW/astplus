from setuptools import setup, find_packages

setup(
    name='ast-plus',
    version='0.0.2',
    packages=find_packages(),
    # pre-alpha
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Programming Language :: Python :: 3.10',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
    python_requires='>=3.6',
    install_requires=[
        'ast',
    ],
    author='Zackary W',
    description='ast-plus is an extension to ast that allows easier modification of ast nodes',
    url='https://github.com/ZackaryW/astplus',
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
)
