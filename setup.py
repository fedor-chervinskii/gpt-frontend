from setuptools import setup

setup(
    name='gpt-frontend',
    packages=['gpt_frontend'],
    include_package_data=True,
    install_requires=[
        'flask',
    ],
)
