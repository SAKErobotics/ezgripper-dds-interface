from setuptools import setup, find_packages

package_name = 'ezgripper_dds_interface'

setup(
    name=package_name,
    version='1.0.0',
    packages=find_packages(exclude=['tests']),
    install_requires=[
        'dynamixel-sdk>=4.0.0',
        'pyserial>=3.5',
    ],
    zip_safe=True,
    maintainer='SAKE Robotics',
    maintainer_email='support@sakerobotics.com',
    description='Generic DDS interface for SAKE Robotics EZGripper',
    license='BSD',
    python_requires='>=3.8',
    entry_points={
        'console_scripts': [
            'ezgripper-dds-test = ezgripper_dds_interface.interface:main',
        ],
    },
)
