from distutils.core import setup
from distutils.extension import Extension
from Cython.Distutils import build_ext

ext_modules = [Extension("moving_average", ["moving_average.pyx"])]



setup(
	name ='Moving average',
	cmdclass = {'build_ext':build_ext},
	ext_modules = ext_modules
)

