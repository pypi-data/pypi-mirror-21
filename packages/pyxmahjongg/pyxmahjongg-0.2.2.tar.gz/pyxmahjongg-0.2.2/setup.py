from setuptools import setup, find_packages


def readme():
    with open('README.rst', 'r') as f:
        content = f.read()
    return content


setup(name='pyxmahjongg',
      version='0.2.2',
      description='The classic UNIX xmahjongg for Python 3',
      long_description=readme(),
      entry_points={'console_scripts': [
          'pyxmahjongg = pyxmahjongg.pyxmahjongg:main',
      ]},
      classifiers=[
        'Development Status :: 4 - Beta',
        'Environment :: Console',
        'Intended Audience :: Other Audience',
        'License :: Free for non-commercial use',
        'Natural Language :: English',
        'Programming Language :: Python',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.6',
      ],
      keywords='mahjongg game',
      url='https://github.com/kbr/pyxmahjongg',
      author='Klaus Bremer',
      author_email='bremer@bremer-media.de',
      license='Free for non-commercial use',
      install_requires=['pillow>=4.0.0'],
      packages=find_packages(),
      include_package_data=True,
      zip_safe=False
)
