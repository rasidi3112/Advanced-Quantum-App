from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

with open("requirements.txt", "r", encoding="utf-8") as fh:
    requirements = [
        line.strip()
        for line in fh
        if line.strip() and not line.startswith("#")
    ]

setup(
    name="advanced-quantum-app",
    version="2.0.0",
    author="rasidi3112",
    author_email="",
    description="Advanced Quantum Computing Application with 11 quantum algorithms",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/rasidi3112/Advanced-Quantum-App",
    project_urls={
        "Bug Tracker": "https://github.com/rasidi3112/Advanced-Quantum-App/issues",
        "Source Code": "https://github.com/rasidi3112/Advanced-Quantum-App",
    },
    packages=find_packages(exclude=["tests*"]),
    classifiers=[
        "Development Status :: 4 - Beta",
        "Intended Audience :: Education",
        "Intended Audience :: Science/Research",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Programming Language :: Python :: 3.12",
        "Topic :: Scientific/Engineering :: Physics",
        "Topic :: Education",
    ],
    python_requires=">=3.9",
    install_requires=requirements,
    entry_points={
        "console_scripts": [
            "quantum-app=main:main",
        ],
    },
    keywords="quantum computing, qiskit, quantum algorithms, quantum simulation",
    license="MIT",
)
