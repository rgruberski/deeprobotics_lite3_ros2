import os
from glob import glob
from setuptools import find_packages, setup

package_name = 'deeprobotics_lite3_description'

setup(
    name=package_name,
    version='0.0.1',
    packages=find_packages(exclude=['test']),
    data_files=[
        ('share/ament_index/resource_index/packages', ['resource/' + package_name]),
        ('share/' + package_name, ['package.xml']),
        (os.path.join('share', package_name, 'launch'), glob('launch/*.launch.py')),
        (os.path.join('share', package_name, 'urdf'), glob('urdf/*')),
        (os.path.join('share', package_name, 'meshes'), [file for file in glob('meshes/**/*', recursive=True) if os.path.isfile(file)]),
        (os.path.join('share', package_name, 'rviz'), glob('rviz/*'))
    ],
    install_requires=['setuptools'],
    zip_safe=True,
    maintainer='Robert Gruberski',
    maintainer_email='rgruberski@gmail.com',
    description='The DeepRobotics Lite 3 quadruped robot description package, tailored for ROS2 usage',
    license='TODO: License declaration',
    tests_require=['pytest'],
    entry_points={
        'console_scripts': [
        ],
    },
)
