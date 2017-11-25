from setuptools import setup, Extension

ripser_module = Extension('ripser_lib',
                    sources = ['ripser/ripser.cpp'],
                    extra_compile_args=['-std=c++11'])

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
 	  ext_modules = [ripser_module],
      zip_safe=False)