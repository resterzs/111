from setuptools import setup

APP = ['html_generator.py']
OPTIONS = {
    'argv_emulation': True,
    'iconfile': None,
    'packages': [],
}

setup(
    app=APP,
    options={'py2app': OPTIONS},
    setup_requires=['py2app'],
)
