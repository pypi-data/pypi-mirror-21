from setuptools import setup, find_packages

setup(name='npr',
      version='0.1.3',
      description='NPR cloud framework',
      long_description='Self-authenticating module for accessing NPR APIs in Python.',
      classifiers=[
        'Development Status :: 3 - Alpha',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
        'Topic :: Internet :: WWW/HTTP',
      ],
      keywords='public radio stream metadata api service',
      url='http://github.com/perrydc/npr',
      author='Demian Perry',
      author_email='dperry@npr.org',
      license='MIT',
      py_modules=['npr'],
      install_requires=[
          'requests','requests[security];python_version<"2.9"','future',
      ],
)
