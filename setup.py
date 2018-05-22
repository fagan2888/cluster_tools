from setuptools import setup, find_packages

setup(
    name='cluster_tools',
    version='0.1',
    description='handy script to the inconvenient slurm',
    url='http://github.com/mavenlin/cluster_tools',
    author='Min Lin',
    author_email='mavenlin@gmail.com',
    license='MIT',
    packages=find_packages(),
    zip_safe=False,
    install_requires=[
        'uuid',
        'click',
        'invoke',
        'gitpython',
        'fabric',
        'colorama',
    ],
    scripts=[
        'cluster_tools/submit',
    ],
)
