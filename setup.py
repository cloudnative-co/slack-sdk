from setuptools import setup, find_packages

setup(
    name="SlackSDK",
    version="0.0.1",
    description="Slack SDK for Python 3.6",
    author="sebastian",
    author_email="seba@cloudnative.co.jp",
    packages=find_packages(),
    install_requires=[
		"requests",
        "requests_toolbelt"
    ],
    entry_points={
        "console_scripts": [
        ]
    },
)
