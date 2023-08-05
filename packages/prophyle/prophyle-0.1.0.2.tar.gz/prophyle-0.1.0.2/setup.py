from setuptools import setup
from setuptools import Extension
from setuptools import find_packages

import os
import subprocess
import glob

from distutils.command.build_ext import build_ext as _build_ext

fake_ext = Extension(
	"prophyle.fake_extension",
	["prophyle/fake_extension.c"],
)

class build_ext(_build_ext):
	def run(self):
		subprocess.call('make -C prophyle', shell=True)
		_build_ext.run(self)

setup(
	name='prophyle',

	version='0.1.0.2',


	description='ProPhyle metagenomic classifier',
	#long_description=long_description,

	url='https://github.com/karel-brinda/prophyle',

	author='Karel Brinda, Kamil Salikhov, Simone Pignotti, Gregory Kucherov',
	author_email='kbrinda@hsph.harvard.edu, salikhov.kamil@gmail.com, pignottisimone@gmail.com, gregory.kucherov@univ-mlv.fr',

	license='MIT',

	classifiers=[
		'Development Status :: 4 - Beta',
		'Topic :: Scientific/Engineering :: Bio-Informatics',
		'Programming Language :: Python :: 3 :: Only',
		'License :: OSI Approved :: MIT License',
	],

	keywords='metagenomics classification NGS',

	packages = find_packages(),

	install_requires=['ete3', 'numpy', 'wheel'],

	package_data={
		'prophyle': [
			'*',
			'prophyle-assembler/*.cpp',
			'prophyle-assembler/*.h',
			'prophyle-assembler/Makefile',
			'prophyle-assembler/prophyle-assembler',
			'prophyle-index/*.c',
			'prophyle-index/*.h',
			'prophyle-index/Makefile',
			'prophyle-index/prophyle-index',
			'prophyle-index/bwa/*.c',
			'prophyle-index/bwa/*.h',
			'prophyle-index/bwa/Makefile',
			'prophyle-index/bwa/bwa',
		]
	},

	ext_modules=[fake_ext],

	entry_points={
          'console_scripts': [
              'prophyle = prophyle.prophyle:main'
          ]
      },

	cmdclass={'build_ext': build_ext},
)
