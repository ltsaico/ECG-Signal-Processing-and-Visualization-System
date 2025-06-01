from setuptools import setup, find_packages

setup(
    name="ecg_signal_package",
    version="0.1.0",
    packages=find_packages(),
    install_requires=[
        "numpy",  # Example dependency
    ],
    author="Louis Tsai",
    description="ECG-signal-processing-and-visualization-system",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    classifiers=[
        "Programming Language :: Python :: 3",
    ],
)
