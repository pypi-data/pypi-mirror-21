from distutils.core import setup, Extension
import numpy

setup(
    name='nuclitrack',
    version='1.1.1',
    description='Nuclei tracking program',
    author='Sam Cooper',
    author_email='sam@socooper.com',
    license='MIT',
    packages=['nuclitrack'],
    install_requires=['Cython','numpy','matplotlib','scipy','scikit-image','scikit-learn','kivy','h5py'],
    ext_modules=[
        Extension("tracking_c_tools", ["nuclitrack/tracking_c_tools.c"], include_dirs=[numpy.get_include()]),
        Extension("segmentation_c_tools", ["nuclitrack/segmentation_c_tools.c"], include_dirs=[numpy.get_include()]),
        Extension("numpy_to_image", ["nuclitrack/numpy_to_image.c"], include_dirs=[numpy.get_include()])]
)
