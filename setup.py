from setuptools import setup

long_description = """# win-raw-in
Enumerate raw input devices and receive input events with device ID on Windows.
"""

setup(
    name='win-raw-in',
    version='0.1.0',
    author='Philipp Holl',
    author_email='philipp@mholl.de',
    packages=['winrawin'],
    url='https://github.com/holl-/win-raw-in',
    license='MIT',
    description='Enumerate raw input devices and receive input events with device ID on Windows',
    keywords='keyboard mouse hook raw input',
    long_description=long_description,
    install_requires=['dataclasses'],
    classifiers=[
        'Development Status :: 4 - Beta',
        'License :: OSI Approved :: MIT License',
        'Operating System :: Microsoft :: Windows',
        'Programming Language :: Python :: 3',
        'Topic :: Software Development :: Libraries :: Python Modules',
        'Topic :: Utilities',
    ],
)
