from setuptools import setup

with open('requirements.txt') as f:
    install_requires = f.read().splitlines()

setup(
    name='tbot',
    version='0.79',
    author='Thomas Erlang',
    author_email='thomas@erlang.dk',
    url='',
    description='',
    long_description=__doc__,
    packages=['tbot'],
    package_dir={'': '.'},
    zip_safe=False,
    install_requires=install_requires,
    license=None,
    include_package_data=True,
    entry_points={
        'console_scripts': [
            'tbot = tbot.runner:main',
        ],
    },
    classifiers=[],
)