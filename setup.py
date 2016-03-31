#!/usr/bin/python


from setuptools import setup, find_packages
import txportal

version = txportal.__version__

install_requires = [
    'Twisted>=15.0.0',
    'txzmq',
    'msgpack-python'
]
install_requires_empty = []

package_data={}


setup(name='txportal',
      version=version,
      author='jamiesun',
      author_email='jamiesun.net@gmail.com',
      url='https://github.com/talkincode/txportal',
      license='MIT',
      description='Portal tools',
      long_description=open('README.md').read(),
      classifiers=[
       'Development Status :: 6 - Mature',
       'Intended Audience :: Developers',
       'Programming Language :: Python :: 2.6',
       'Programming Language :: Python :: 2.7',
       'Topic :: Software Development :: Libraries :: Python Modules',
       ],
      packages=find_packages(),
      package_data=package_data,
      keywords=['portal', 'cmcc','huawei','h3c','toughwlan'],
      zip_safe=True,
      scripts=["tpsim"],
      eager_resources=['txportal'],
      include_package_data=True,
      install_requires=install_requires,
)