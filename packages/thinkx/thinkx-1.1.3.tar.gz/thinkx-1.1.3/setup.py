# To install locally: python setup.py develop
# To register: python setup.py register
# To make distribution and upload it: python setup.py sdist upload

from setuptools import setup


def readme():
    try:
        with open('README.md') as f:
            return f.read()
    except IOError:
        return ''

setup(name='thinkx',
      version='1.1.3',
      description='Modules supporting books by Allen Downey',
      long_description=readme(),
      url='http://github.com/AllenDowney/ThinkX',
      author='Allen Downey',
      author_email='downey@allendowney.com',
      license='MIT',
      py_modules=['thinkbayes', 'thinkbayes2', 'thinkstats2', 'thinkplot', 'thinkdsp'],
      install_requires=[
          'matplotlib',
          'numpy',
          'pandas',
          'scipy',
          'markdown',
      ],
      test_suite='nose.collector',
      tests_require=['nose', 'nose-cover3'],
      include_package_data=True,
      zip_safe=False)
