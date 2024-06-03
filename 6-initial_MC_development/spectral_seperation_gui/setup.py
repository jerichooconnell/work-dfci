from setuptools import setup, find_packages

setup(
    name='mli_gui',
    version='0.1',
    packages=find_packages(),
    install_requires=[
        # List your package dependencies here
        'matplotlib',
        'numpy',
        'spekpy',
    ],
    entry_points={
        'console_scripts': [
            # List any console scripts here
            'mli_gui=mli_gui.__main__:main',
        ]
    },
    author='Your Name',
    author_email='your.email@example.com',
    description='A short description of your package',
    url='https://github.com/your-username/your-package-name',
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9',
    ],
)
