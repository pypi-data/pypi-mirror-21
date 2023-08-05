#!/usr/bin/python3
# -*- coding: UTF-8 -*-
from setuptools import setup
import platform


setup(
	name='Jalapeno-Lite',
	version='0.1.3',
	author='Chenghao Qian',
	author_email='qch.jacob.jm@gmail.com',
	include_package_data=True,
	packages=['Jalapeno',
				'Jalapeno.lib',
				'Jalapeno.utils',
				'Jalapeno.views',
				'Jalapeno.GUI'
				],
	scripts=['Jaloc','JaloLite'],
	url='https://github.com/ChenghaoQ/Jalapeno',
	license='LGPL',
	description='Lite version of Jalapeno, Browser driven GUI',
	keywords= ['Flask','Blog','site Generator','static site'],
	install_requires=['Markdown >= 2.6.6',
						'Flask >= 0.10.1',
						'Pygments >= 2.1.3 ',
						'MarkupSafe >= 0.23',
						'Flask-FlatPages >= 0.6',
						'Frozen-Flask >= 0.12']
)