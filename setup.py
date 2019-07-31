from setuptools import setup, find_packages
import webget

setup(
    name=webget.__title__,
    author=webget.__author__,
    version=webget.__version__,
    python_requires="~=3.7",
    packages=find_packages(),
    install_requires=["scrapy", "selenium"],
    include_package_data=True,
)
