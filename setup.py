from setuptools import find_packages, setup
setup(
    name='VisualSecretSharing',
    packages=find_packages(include=['VisualSecretSharing']),
    version='1.0.0',
    description='Basic function to create encrypted images.',
    author='David Šenica',
    license='MIT',
    python_requires='>=3.8',
    install_requires=['numpy>=1.20.1', 'Pillow>=8.1.0'],
    setup_requires=['pytest-runner'],
    tests_require=['pytest>=6.2.2'],
    test_suite='tests',
)