from setuptools import setup

setup(
    name='web',
    version='0.1.0',
    packages=['web'],
    include_package_data=True,
    install_requires=[
        'flask',
        'flask-sqlalchemy',
        'networkx',
        'pygraphviz',
    ],
    extras_require={
        'testing': [
        ],
        'staging': [
            'gunicorn'
        ],
        'prod': [
            'gunicorn'
        ]
    }
)
