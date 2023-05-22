from setuptools import setup
from glob import glob
import os

package_name = 'rgb_navigate'

setup(
    name=package_name,
    version='0.0.0',
    packages=[package_name],
    data_files=[
        ('share/ament_index/resource_index/packages',
            ['resource/' + package_name]),
        ('share/' + package_name, ['package.xml']),
        (os.path.join('share', package_name), glob('launch/*launch.[pxy][yma]*')),
    ],
    install_requires=['setuptools'],
    zip_safe=True,
    maintainer='arya',
    maintainer_email='aryaebrahimi3000@mail.um.ac.ir',
    description='TODO: Package description',
    license='TODO: License declaration',
    tests_require=['pytest'],
    entry_points={
        'console_scripts': [
            'rgb_navigate = rgb_navigate.rgb_navigate:main'
        ],
    },
)
