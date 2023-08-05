
import os
import re
try:
    from setuptools import setup, find_packages
except ImportError:
    from distutils.core import setup, find_packages

base_dir = os.path.dirname(os.path.abspath(__file__))


def get_version(filename="minchin/pelican/plugins/cname.py"):
    with open(os.path.join(base_dir, filename), encoding="utf-8") as initfile:
        for line in initfile.readlines():
            m = re.match("__version__ *= *['\"](.*)['\"]", line)
            if m:
                return m.group(1)

setup(
    name="minchin.pelican.plugins.cname",
    version=get_version(),
    description="Pelican plugin that adds a `CNAME` file to the output root. Useful for publishing to Github Pages. Written in Python.",
    long_description="\n\n".join([open(os.path.join(base_dir, "README.rst")).read()]),
    author="W. Minchin",
    author_email="w_minchin@hotmail.com",
    url="https://github.com/MinchinWeb/minchin.pelican.plugins.cname",
    packages=find_packages(),
    namespace_packages=['minchin',
                        'minchin.pelican',
                        'minchin.pelican.plugins'],
    include_package_data=True,
    install_requires=[
        'pelican',
        ],
    classifiers=[
        'Development Status :: 5 - Production/Stable',
        'Environment :: Console',
        'License :: OSI Approved :: GNU Affero General Public License v3',
        'Programming Language :: Python',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.2',
        'Programming Language :: Python :: 3.3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
        'Framework :: Pelican :: Plugins',
        ],
)
