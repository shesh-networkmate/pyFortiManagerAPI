from setuptools import setup

with open("README.md", "r") as fh:
    long_description = fh.read()

setup(
    name='pyFortiManagerAPI',
    description='A Python wrapper for the FortiManager REST API',
    version='0.0.44',
    py_modules=["pyFortiManagerAPI"],
    package_dir={'': 'src'},
    keywords=['Fortimanager', 'RestAPI', 'API', 'Fortigate', 'Fortinet', "python", "Fortimanager Rest API",
              "Fortimanager Rest API Python", "Python examples"],
    classifiers=[
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
        'Operating System :: OS Independent',
    ],
    long_description=long_description,
    long_description_content_type="text/markdown",
    install_requires=['requests', 'urllib3'],
    extra_require={"dev": ["pytest>=3.7"]},
    url="https://github.com/akshaymane920/pyFortiManagerAPI",
    author="Akshay Mane",
    author_email="akshaymane920@gmail.com",
)
