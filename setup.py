import os
import re
from setuptools import setup


setup(name='dbm-center',
      version='0.2.0',
      description='dbm-center 数据库管理中心服务端程序',
      author="Neeky",
      author_email="neeky@live.com",
      maintainer='Neeky',
      maintainer_email='neeky@live.com',
      scripts=['bin/dbm-center'],
      packages=['dbmcenter'],
      package_data={'dbmcenter': ['dbm-center/*', 'dbm-center/css/*', 'dbm-center/js/*']},
      url='https://github.com/Neeky/dbm-center',
      python_requires='>=3.6.*',
      classifiers=[
          'Development Status :: 4 - Beta',
          'Intended Audience :: Developers',
          'Operating System :: POSIX',
          'Operating System :: MacOS :: MacOS X',
          'Programming Language :: Python :: 3.6',
          'Programming Language :: Python :: 3.7',
          'Programming Language :: Python :: 3.8']
      )