#!/usr/bin/env python
from setuptools.command.build_ext import build_ext
import codecs
import glob
import os
import setuptools
import sys


__version__ = "0.1.0"


here = os.path.abspath(os.path.dirname(__file__))


# Get the long description from the README file
with codecs.open(os.path.join(here, "README.rst"), encoding="utf-8") as file:
    long_description = file.read()


def find_files(
        pattern):
    result = []
    for root, directories, _ in os.walk("."):
        for directory in directories:
            result += glob.glob(os.path.join(root, directory, pattern))
    return result


# As of Python 3.6, CCompiler has a `has_flag` method.
# cf http://bugs.python.org/issue26689
def has_flag(compiler, flagname):
    """
    Return a boolean indicating whether a flag name is supported on
    the specified compiler
    """
    import tempfile
    with tempfile.NamedTemporaryFile("w", suffix=".cpp") as f:
        f.write("int main (int argc, char **argv) { return 0; }")
        try:
            compiler.compile([f.name], extra_postargs=[flagname])
        except setuptools.distutils.errors.CompileError:
            return False
    return True


def cpp_flag(compiler):
    """
    Return the -std=c++[14/17] compiler flag. The c++17 is prefered over
    c++14 (when it is available).
    """
    # if has_flag(compiler, "-std=c++17"):
    #     return "-std=c++17"
    if has_flag(compiler, "-std=c++14"):
        return "-std=c++14"
    else:
        raise RuntimeError("Unsupported compiler -- at least C++14 support "
           "is needed!")


class BuildExt(setuptools.command.build_ext.build_ext):
    """
    A custom build extension for adding compiler-specific options
    """
    c_opts = {
        "msvc": ["/EHsc"],
        "unix": [],
    }

    if sys.platform == "darwin":
        c_opts["unix"] += ["-stdlib=libc++", "-mmacosx-version-min=10.7"]

    def build_extensions(self):
        compiler_type = self.compiler.compiler_type
        opts = self.c_opts.get(compiler_type, [])
        if compiler_type == "unix":
            opts.append('-DVERSION_INFO="{}"'.format(
                self.distribution.get_version()))
            opts.append(cpp_flag(self.compiler))
            if has_flag(self.compiler, "-fvisibility=hidden"):
                opts.append("-fvisibility=hidden")
        elif compiler_type == "msvc":
            opts.append('/DVERSION_INFO=\\"{}\\"'.format(
                self.distribution.get_version()))
        for ext in self.extensions:
            ext.extra_compile_args = opts
        build_ext.build_extensions(self)


setuptools.setup(
    name="lue",
    version=__version__,
    description="The LUE Python package allows you to perform I/O to the LUE "
        "Scientific Database, which is an HDF5 binary data format",
    long_description=long_description,
    author="PCRaster R&D Team",
    author_email="info@pcraster.eu",
    url="https://github.com/pcraster/lue",
    packages=setuptools.find_packages(),
    ext_modules=[
        setuptools.Extension("lue",
            sources=find_files("*.c*"),
            include_dirs=[
                ".",
            ],
            libraries = ["boost_filesystem", "boost_system", "hdf5"],
            language="c++"
        )
    ],
    install_requires=[
        # "docopt>=xxx",
        # "numpy>=xxx"
    ],
    cmdclass={"build_ext": BuildExt},
    license="GPLV3",
    classifiers=[
        "Development Status :: 1 - Planning",
        "Intended Audience :: Science/Research",
        "License :: OSI Approved :: GNU General Public License v3 or later (GPLv3+)",
        "Operating System :: POSIX :: Linux",
        "Operating System :: MacOS :: MacOS X",
        "Operating System :: Unix",
        "Operating System :: Microsoft :: Windows",
        "Programming Language :: C++",
        "Programming Language :: Python :: 2",
        "Programming Language :: Python :: 2.7",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.5",
        "Topic :: Database",
        "Topic :: Scientific/Engineering :: GIS",
    ],
    keywords="LUE, PCRaster, HDF5, scientific database, "
        "field-based modeling, agent-based modeling",
)
