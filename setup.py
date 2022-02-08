from setuptools import find_packages, setup

long_description = ""
with open("README.md") as ifp:
    long_description = ifp.read()

setup(
    name="bureaucrat",
    version="0.0.1",
    packages=find_packages(),
    install_requires=["eth-brownie"],
    extras_require={
        "dev": [
            "black",
            "moonworm >= 0.1.9",
        ],
        "distribute": ["setuptools", "twine", "wheel"],
    },
    description="Signature verification on Solidity smart contracts",
    long_description=long_description,
    long_description_content_type="text/markdown",
    author="zomglings",
    author_email="nkashy1@gmail.com",
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Programming Language :: Python",
        "License :: OSI Approved :: Apache Software License",
        "Topic :: Software Development :: Libraries",
    ],
    python_requires=">=3.6",
    url="https://github.com/zomglings/bureaucrat",
    entry_points={
        "console_scripts": [
            "bureaucrat=bureaucrat.cli:main",
        ]
    },
    include_package_data=True,
)
