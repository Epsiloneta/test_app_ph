from setuptools import setup

setup(name='easy_ph',
      version='0.1',
      description='Graphical GUI for Ripser and related persistent homology libraries',
      url='http://....',
      author='Esther Ibanez',
      author_email='todo@gmail.com',
      license='MIT',
      packages=['easy_ph'],
      install_requires=[
		'matplotlib',
		'networkx',
		'numpy',
		'pandas',
		'scipy',
		'seaborn'
      ],
      entry_points = {
        'console_scripts': ['app_easy_ph=easy_ph.app_Easy_PH:run_app'],
 	  },
      zip_safe=False)