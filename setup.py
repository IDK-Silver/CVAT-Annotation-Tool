from setuptools import setup, find_packages


with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name="cvat",
    version="0.1.0",
    author="黃毓峰",
    author_email="a288235403@gmail.com",
    description="",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/yourusername/cvat",
    package_dir={"": "src"},
    packages=find_packages(where="src"),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.6",
    install_requires=[  
        "certifi",
        "charset-normalizer",
        "idna",
        "numpy<=1.26.4",
        "opencv-python",
        "pandas",
        "pillow",
        "python-dateutil",
        "pytz",
        "requests", 
        "simplejson",
        "six",
        "urllib3>=2.2.2",
    ],
    extras_require={
        "dev": [
            "pytest>=6.0",
            "pytest-cov>=2.0",
        ],
    },
)