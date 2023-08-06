from setuptools import setup, find_packages

setup(name='python-genomespaceclient',
      version="0.2",
      description='Python bindings and commandline client to the GenomeSpace'
      ' API',
      author='GVL Project',
      author_email='help@genome.edu.au',
      url='http://python-genomespaceclient.readthedocs.org/',
      install_requires=['cloudbridge>=0.3,<0.4', 'requests'],
      extras_require={
          'dev': ['tox', 'sphinx']
      },
      packages=find_packages(),
      license='MIT',
      classifiers=[
          'Development Status :: 4 - Beta',
          'Environment :: Console',
          'Intended Audience :: Developers',
          'Intended Audience :: Science/Research',
          'License :: OSI Approved :: MIT License',
          'Operating System :: OS Independent',
          'Programming Language :: Python',
          'Topic :: Software Development :: Libraries :: Python Modules',
          'Programming Language :: Python :: 2.7',
          'Programming Language :: Python :: 3',
          'Programming Language :: Python :: 3.4',
          'Programming Language :: Python :: 3.5',
          'Programming Language :: Python :: Implementation :: CPython',
          'Programming Language :: Python :: Implementation :: PyPy'],
      entry_points={
          'console_scripts': [
              'genomespace = genomespaceclient:main'
          ]
      },
      test_suite="test"
      )
