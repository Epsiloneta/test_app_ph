from setuptools import setup, Extension
import platform

compile_options = []
osfamily = platform.uname()[0]
if osfamily == 'Windows':
    compile_options.append('/EHsc')

if osfamily == 'Linux':
    compile_options.append('-std=c++11')


class get_pybind_include(object):
    """Helper class to determine the pybind11 include path

    The purpose of this class is to postpone importing pybind11
    until it is actually installed, so that the ``get_include()``
    method can be invoked. """

    def __init__(self, user=False):
        self.user = user

    def __str__(self):
        import pybind11
        return pybind11.get_include(self.user)


ripser_module = Extension('easy_ph.ripser_wrapper_lib',
                    sources = ['ripser/ripser.cpp','easy_ph/ripser_wrapper.cpp'],
                    extra_compile_args=compile_options,
                    include_dirs=[
                          # Path to pybind11 headers
                          get_pybind_include(),
                          get_pybind_include(user=True)
                      ],
                    runtime_library_dirs=['.'])

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
      zip_safe=False)