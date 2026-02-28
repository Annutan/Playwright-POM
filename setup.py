from setuptools import setup, find_packages

setup(
    name="test_frontend_settings",
    version="1.0.0",
    packages=find_packages(),
    install_requires=[
        "pytest>=7.0.0",
        "playwright>=1.30.0",
        "allure-pytest>=2.9.0",
        "python-dotenv>=0.20.0",
    ],
)