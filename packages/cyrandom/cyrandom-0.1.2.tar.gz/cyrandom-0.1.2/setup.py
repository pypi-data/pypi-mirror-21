from setuptools import setup, Extension
from Cython.Build import cythonize

ext = Extension("cyrandom",
                sources=["cyrandom.pyx",
                         "_mersenne.c",
                         "_seed.c"])

setup(
    name="cyrandom",
    version='0.1.2',
    description='Fast random number generation.',
    long_description="A fast cython replacement for the standard library's random module.",
    url='https://github.com/Noctem/cyrandom',
    author='David Christenson',
    author_email='mail@noctem.xyz',
    license='MIT',
    classifiers=[
        'Development Status :: 4 - Beta',
        'Intended Audience :: Developers',
        'Programming Language :: Cython',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3 :: Only',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
        'License :: OSI Approved :: MIT License'
    ],
    keywords='cyrandom random rng cython',
    ext_modules = cythonize([ext],
                            compiler_directives={'language_level': 3})
)
