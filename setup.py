from setuptools import setup

setup(
    name='fc00.org',
    version='0.1.0',
    packages=['fc00'],
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
