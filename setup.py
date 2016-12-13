from setuptools import setup

setup(
    name="mbtapy",
    version='0.1.0dev1',
    description='Python bindings for the MBTA-REALTIME API (v2)',
    author="Joseph Dougherty",
    author_email="mbtapy@jwdougherty.com",
    url='https://github.com/JDougherty/mbtapy',
    install_requires=['requests'],
    license='LICENSE', 
    packages=['mbtapy'],
)
