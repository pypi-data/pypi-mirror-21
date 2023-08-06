"""
Flask-Pika
-------------
This extension provides a simple way to expose a Pika blocking channel inside of Flask.

Once a channel is obtained, use it as you would any normal Pika blocking channel.
"""
from setuptools import setup


setup(
    name='Flask-Pika-NG',
    version='0.3.3',
    url='https://github.com/experimentaltelephony/flask-pika',
    license='BSD',
    author='Charlie Wolf',
    author_email='charlie@flow180.com',
    description='Pika amqp flask extension',
    long_description=__doc__,
    zip_safe=False,
    include_package_data=True,
    py_modules=['flask_pika'],
    platforms='any',
    install_requires=[
        'Flask',
        'pika>=0.10'
    ],
    classifiers=[
        'Environment :: Web Environment',
        'Intended Audience :: Developers',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Topic :: Internet :: WWW/HTTP :: Dynamic Content',
        'Topic :: Software Development :: Libraries :: Python Modules'
    ]
)
