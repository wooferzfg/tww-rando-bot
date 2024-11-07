from setuptools import find_packages, setup

setup(
    name='tww-rando-bot',
    description='racetime.gg bot for generating TWW Randomizer seeds.',
    license='GNU General Public License v3.0',
    classifiers=[
        'Development Status :: 5 - Production/Stable',
        'Environment :: Console',
        'License :: OSI Approved :: GNU General Public License v3 (GPLv3)',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9',
    ],
    url='https://racetime.gg/twwr',
    project_urls={
        'Source': 'https://github.com/wooferzfg/tww-rando-bot',
    },
    version='1.0.0',
    install_requires=[
        'racetime_bot@git+https://github.com/wooferzfg/racetime-bot@tww-rando-bot',
        'PyGithub==2.5.0',
        'shortuuid==1.0.13',
        'isodate>=0.6.1,<0.7',
    ],
    packages=find_packages(),
    entry_points={
        'console_scripts': [
            'randobot=randobot:main',
        ],
    },
)
