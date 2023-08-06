try:
    from setuptools import setup
except ImportError:
    from distutils.core import setup
from collections import defaultdict
import os

# Build a list of all project modules, as well as supplementary files
main_package = "spinn_utilities"
data_extensions = {".aplx", ".xml"}
main_package_dir = os.path.join(os.path.dirname(__file__), main_package)
start = len(main_package_dir)
packages = []
package_data = defaultdict(list)
for dirname, dirnames, filenames in os.walk(main_package_dir):
    if '__init__.py' in filenames:
        package = "{}{}".format(
            main_package, dirname[start:].replace(os.sep, '.'))
        packages.append(package)
    for filename in filenames:
        _, ext = os.path.splitext(filename)
        if ext in data_extensions:
            package = "{}{}".format(
                main_package, dirname[start:].replace(os.sep, '.'))
            package_data[package].append("*{}".format(ext))
            break

setup(
    name="SpiNNUtilities",
    version="4.0.0a1",
    description="Utility classes and functions for SpiNNaker projects",
    url="https://github.com/SpiNNakerManchester/SpiNNUtilities",
    license="GNU GPLv3.0",
    packages=packages,
    package_data=package_data,
    install_requires=['six']
)
