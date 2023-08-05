from setuptools import setup

setup(
    name='playlistfromsong',
    packages=['playlistfromsong'],
    version='0.22',
    description='An offline music station generator',
    author='schollz',
    url='https://github.com/schollz/playlistfromsong',
    author_email='hypercube.platforms@gmail.com',
    download_url='https://github.com/schollz/playlistfromsong/archive/v0.22.tar.gz',
    keywords=['music', 'youtube', 'playlist'],
    classifiers=[],
    install_requires=[
        "requests",
        "youtube_dl",
        'appdirs',
        'pyyaml',
        'beautifulsoup4',
    ],
    setup_requires=['pytest-runner'],
    tests_require=[
        'pytest-flake8',
        'pytest',
        'pytest-cov'

    ],
    entry_points={'console_scripts': [
        'playlistfromsong = playlistfromsong.__main__:main',
    ], },
)
