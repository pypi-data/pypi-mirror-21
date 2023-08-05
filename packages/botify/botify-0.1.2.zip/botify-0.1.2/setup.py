from setuptools import setup

version = '0.1.2'
name = 'botify'
install_requires = []

setup(name=name,
      version=version,
      description='Natural Language based Commands Processing Framework',
      install_requires=install_requires,
      long_description=open('README.rst', 'rt').read(),
      author='Priyam Singh',
      author_email='priyamsingh.22296@gmail.com',
      packages=['botify'],
      url='https://github.com/pri22296/{0}'.format(name),
      download_url='https://github.com/pri22296/{0}/tarball/{1}'.format(name, version),
      license='MIT',
      classifiers=[
          'Development Status :: 3 - Alpha',
          'Intended Audience :: Developers',
          'License :: OSI Approved :: MIT License',
          'Programming Language :: Python',
          'Programming Language :: Python :: 3.5',
      ],
)
