from setuptools import setup


_locals = {}
with open('invocare/ssh/_version.py') as fh:
    exec(fh.read(), None, _locals)
version = _locals['__version__']


setup(name='invocare-ssh',
      version=version,
      author='Justin Bronn',
      author_email='jbronn@gmail.com',
      description='SSH Invocations',
      long_description='Implementions of SSH-related invoke tasks.',
      license='Apache License 2.0',
      url='https://github.com/jbronn/invocare-ssh',
      download_url='https://pypi.python.org/pypi/invocare-ssh/',
      install_requires=[
        'invocare>=0.2.1,<1.0.0',
      ],
      packages=['invocare.ssh'],
      zip_safe=False,
      classifiers=[
          'Development Status :: 4 - Beta',
          'Intended Audience :: Developers',
          'Intended Audience :: System Administrators',
          'License :: OSI Approved :: Apache Software License',
          'Programming Language :: Python',
          'Programming Language :: Python :: 2',
          'Programming Language :: Python :: 3',
      ],
)
