from setuptools import setup

setup(
    name='TreetaggerWidget',
    version='0.0.1',
    packages=['TreetaggerWidget'],
    entry_points={'orange.widgets': 'MyWidgets = TreetaggerWidget'},
    install_requires=[
        'Orange>=2.1,<3',
        'Orange-Textable>=1.5.2',
    ],
    author='University of Lausanne',
    license='GNU General Public License v3 (GPLv3)',
    keywords=[
        'tree-tagger',
        'POS tagging',
    ],
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Intended Audience :: Science/Research',
        'License :: OSI Approved :: GNU General Public License v3 (GPLv3)',
        'Programming Language :: Python :: 2 :: only',
        'Programming Language :: Python :: 2.6',
        'Programming Language :: Python :: 2.7',
    ],    
)
