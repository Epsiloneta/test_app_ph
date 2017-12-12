from setuptools import setup, Extension
from pybind_setup import get_pybind_include, BuildExt

ripser_module = Extension('easy_ph.ripser_wrapper_lib',
                    sources = ['ripser/ripser.cpp','easy_ph/ripser_wrapper.cpp'],
                    include_dirs=[
                          # Path to pybind11 headers
                          get_pybind_include(),
                          get_pybind_include(user=True)
                      ],
                    language='c++')

setup(name='easy_ph',
      version='0.1',
      description='Graphical GUI for Ripser and related persistent homology libraries',
      url='https://sites.google.com/site/estherib4n3z/',
      author='Esther Ibanez Marcelo',
      author_email='esther.epsilon@gmail.com',
      license='GPL 3',
      packages=['easy_ph'],
      install_requires=[
        'matplotlib',
        'networkx',
        'numpy',
        'pandas',
        'scipy',
        'seaborn',
        'pybind11>=2.2'
      ],
      entry_points = {
        'console_scripts': ['app_easy_ph=easy_ph.app_Easy_PH:run_app'],
      },
      ext_modules = [ripser_module],
      test_suite='nose.collector',
      tests_require=['nose'],
      cmdclass={'build_ext': BuildExt},
      zip_safe=False)