from distutils.core import setup
from distutils.extension import Extension
from Cython.Distutils import build_ext

ext_modules = [Extension("extract_stat", ["extract_stat.pyx"])]



setup(
	name ='Extract stat',
	cmdclass = {'build_ext':build_ext},
	ext_modules = ext_modules
)
