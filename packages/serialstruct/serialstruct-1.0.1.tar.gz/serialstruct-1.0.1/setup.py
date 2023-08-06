from setuptools import setup, find_packages


setup(
        name='serialstruct',
        version='1.0.1',
        description=('Implements a StructuredPacket for pySerial\'s '
            'serial.threaded module'),
        author='Eric Oswald',
        author_email='eoswald39@gmail.com',
        license='MIT',
        packages=find_packages(exclude=['test']),
        install_requires=['pyserial']
)
