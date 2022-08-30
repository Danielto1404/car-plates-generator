from setuptools import setup, find_packages

setup(
    name='car-plates-generator',
    packages=find_packages(exclude=[]),
    version='0.0.1',
    license='MIT',
    description='PyTorch implementation of car licence plates GAN',
    author='Daniil Korolev',
    url='https://github.com/Danielto1404/car-plates-generataor',
    keywords=[
        'Artificial Intelligence',
        'Generative Adversarial Networks',
        'Deep Learning',
        'Object Detection',
        'Car Licence Plates'
    ],
    install_requires=[
        'numpy',
        'bs4',
        'tqdm',
        'requests',
        'cfscrape'
    ],
    classifiers=[
        'Development Status :: 4 - Beta',
        'Intended Audience :: Developers',
        'Topic :: Scientific/Engineering :: Artificial Intelligence',
        'Programming Language :: Python :: 3.9',
    ]
)
