from setuptools import setup

setup(name='bpc8583',
      version='1.2',
      
      description='BPC\'s flavour of ISO8583 banking protocol library and toolkit',
      long_description=open('README.md').read(),
      
      classifiers=[
        'License :: OSI Approved :: GNU Lesser General Public License v2 (LGPLv2)',
        'Operating System :: OS Independent',
        
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
        
        'Topic :: Communications',
        'Intended Audience :: Developers',
      ],
      
      keywords='ISO8583 POS financial banking payment',
      
      url='https://github.com/timgabets/bpc8583',
      author='Tim Gabets',
      author_email='tim@gabets.ru',
      
      license='LGPLv2',
      packages=['bpc8583'],
      install_requires=['enum34', 'pycrypto', 'pytlv'],
      zip_safe=True)