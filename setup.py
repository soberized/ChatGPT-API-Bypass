from setuptools import setup, find_packages

setup(
    name='chatgpt-api-bypass',
    version='0.1.0',
    packages=find_packages(),
    install_requires=[
        'selenium>=4.0.0',
        'undetected-chromedriver>=3.5.0', 
    ],
    author='rep', 
    description='A Python package to use chatgpt like an API without an API key.',
    long_description=open('README.md').read() if 'README.md' else '',
    long_description_content_type='text/markdown' if 'README.md' else 'text/plain',
    url='https://github.com/soberized/ChatGPT-API-Bypass',
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License', 
        'Operating System :: OS Independent',
        'Intended Audience :: Developers',
        'Topic :: Software Development :: Libraries :: Python Modules',
        'Topic :: Internet :: WWW/HTTP :: Browsers',
    ],
    python_requires='>=3.8', 
    keywords='chatgpt automation selenium api bypass ai free workaround',
)
