from setuptools import setup, find_packages

with open('requirements.txt') as f:
    required = f.read().splitlines()

setup(
        name='ssbio',
        version='0.9.0',
        author='Nathan Mih',
        author_email='nmih@ucsd.edu',
        license='MIT',
        url='http://github.com/nmih/ssbio',
        description='Tools to enable structural systems biology',
        packages=find_packages(),
        package_dir={'ssbio': 'ssbio'},
        package_data={'ssbio': ['ssbio/etc/*']},
        scripts=['ssbio/structure/utils/cleanpdb.py',
                 'ssbio/sequence/properties/aggregation_propensity.py',
                 'ssbio/sequence/properties/thermostability.py',
                 'ssbio/structure/utils/mutatepdb.py',
                 'ssbio/structure/utils/tleap.py',
                 'ssbio/databases/drugbank.py',
                 'ssbio/structure/properties/msms.py'],
        long_description=open('README.md').read(),
        install_requires=required
)
