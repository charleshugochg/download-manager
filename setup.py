from setuptools import setup


def readfile(filename):
    with open(filename, 'r+') as f:
        return f.read()


setup(
    name="download_manager",
    version="0.1",
    description="",
    long_description=readfile('README.md'),
    author="Charles Hugo",
    author_email="minheinkhant@hotmail.com",
    url="",
    py_modules=['main'],
    entry_points={
        'console_scripts': [
            'download = downloader_manager:main'
        ]
    }, install_requires=['click', 'requests']
)
