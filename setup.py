import setuptools

with open('README.md', 'r') as f:
    long_description = f.read()

setuptools.setup(
    name='youtube-sdk-py',
    version='0.1.0',
    author='Ashwin Thanaraj',
    author_email='ashwinthanaraj@gmail.com',
    description='Python SDK for accessing Youtube APIs',
    license='MIT',
    long_description=long_description,
    long_description_content_type='text/markdown',
    keywords=['youtube', 'api', 'python', 'sdk', 'pip'],
    url='https://github.com/polydimensional/youtube-sdk-py',
    packages=setuptools.find_packages(),
    install_requires=['requests'],
    classifiers=[
        'Topic :: Internet :: WWW/HTTP',
        'Intended Audience :: Developers',
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ]
)
