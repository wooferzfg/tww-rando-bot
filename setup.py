from setuptools import find_packages, setup

setup(
    name='twwr-spoiler-log-bot',
    description='racetime.gg bot for generating TWWR spoiler log seeds.',
    license='MIT',
    classifiers=[
        'Development Status :: 5 - Production/Stable',
        'Environment :: Console',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9',
    ],
    url='https://racetime.gg/twwr',
    project_urls={
        'Source': 'https://github.com/wooferzfg/twwr-spoiler-log-bot',
    },
    version='1.0.0',
    install_requires=[
        'racetime_bot>=1.5.0,<2.0',
        'PyGithub>=1.53'
    ],
    packages=find_packages(),
    entry_points={
        'console_scripts': [
            'randobot=randobot:main',
        ],
    },
)
