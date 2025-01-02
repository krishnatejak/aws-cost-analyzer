from setuptools import setup, find_packages

setup(
    name='aws-cost-analyzer',
    version='0.1.0',
    packages=find_packages(),
    install_requires=[
        'flask',
        'flask-cors',
        'boto3',
        'gunicorn',
        'gevent'
    ],
)