from setuptools import setup, find_packages

setup(
    name='scraping-library',
    version='0.1',
    packages=find_packages(),
    install_requires=[
        'beautifulsoup4',
        'requests',
    ],
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.10',
    ],
)
