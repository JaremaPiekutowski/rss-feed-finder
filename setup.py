from setuptools import setup, find_packages

setup(
    name='rssfeedfinder',
    version='0.1',
    packages=find_packages(),
    install_requires=[
        'requests',
        'beautifulsoup4'
    ],
    author='Jarema Piekutowski',
    author_email='jarema.piekutowski@gmail.com',
    description='A package to find RSS feeds in websites',
    keywords='rss feed finder'
)
