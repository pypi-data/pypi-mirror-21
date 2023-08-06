try:
    from setuptools import setup
except ImportError:
    import ez_setup
    ez_setup.use_setuptools()
    from setuptools import setup

import sys
import platform

with open('README.rst') as f:
    readme = f.read()


def mcl_data_files():
    """
    Automatically detects the platform and sets the appropriate mcl binary
    """

    data_file = None

    if sys.platform in ["linux2"]:
        data_file = ["trifusion/data/resources/mcl/linux/mcl"]

    elif sys.platform in ["win32", "cygwin"]:
        if platform.architecture()[0] == "64bit":
            data_file = ["trifusion/data/resources/mcl/windows/64bit/"
                         "mcl64.exe",
                         "trifusion/data/resources/mcl/windows/64bit/"
                         "cygwin1.dll",
                         "trifusion/data/resources/usearch/64bit/vcomp100.dll"]
        else:
            data_file = ["trifusion/data/resources/mcl/windows/32bit/"
                         "mcl32.exe",
                         "trifusion/data/resources/mcl/windows/32bit/"
                         "cygwin1.dll",
                         "trifusion/data/resources/usearch/32bit/vcomp100.dll"]

    return data_file


mcl_file = mcl_data_files()

setup(
    name="trifusion",
    version="0.5.0-2",
    packages=["trifusion",
              "trifusion.base",
              "trifusion.data",
              "trifusion.data.backgrounds",
              "trifusion.data.resources",
              "trifusion.data.screens",
              "trifusion.ortho",
              "trifusion.process"],
    package_data={"trifusion": ["*.kv"],
                  "trifusion.data.screens": ["*.kv"],
                  "trifusion.data.backgrounds": ["*.png", "*.ico"],
                  "trifusion.data.resources": [".desktop"]},
    install_requires=[
        "seaborn",
        "configparser",
        "matplotlib",
        "numpy",
        "psutil",
        "scipy",
        "progressbar2"
    ],
    description=("Streamlining phylogenomic data gathering, processing and "
                 "visualization"),
    long_description=readme,
    url="https://github.com/ODiogoSilva/TriFusion",
    author="Diogo N Silva",
    author_email="odiogosilva@gmail.com",
    license="GPL3",
    classifiers=["Development Status :: 3 - Alpha",
                 "Intended Audience :: Science/Research",
                 "License :: OSI Approved :: GNU General Public License v3 ("
                 "GPLv3)",
                 "Natural Language :: English",
                 "Operating System :: POSIX :: Linux",
                 "Operating System :: MacOS :: MacOS X",
                 "Operating System :: Microsoft :: Windows",
                 "Programming Language :: Python :: 2 :: Only",
                 "Topic :: Scientific/Engineering :: Bio-Informatics"],
    scripts=mcl_file,
    entry_points={
        "gui_scripts": [
            "TriFusion = trifusion.TriFusion:gui_exec"
        ],
        "console_scripts": [
            "orthomcl_pipeline = trifusion.orthomcl_pipeline:main",
            "TriSeq = trifusion.TriSeq:main",
            "TriStats = trifusion.TriStats:main"
        ]
    },
)