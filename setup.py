from setuptools import setup, find_packages

setup(
    name="mind_bender_machine_learning",
    version="0.1.0",
    description="Clinical Data Warehouse EDW & 3x3 Transition Matrix ML Pipeline",
    author="Mind Bender AI Team",
    packages=find_packages(where="src"),
    package_dir={"": "src"},
    python_requires=">=3.10",
    install_requires=[
        "sqlmodel>=0.0.14",
        "pydantic>=2.0.0",
        "sqlalchemy>=2.0.0",
        "pandas>=2.0.0",
        "numpy>=1.24.0",
        "scikit-learn>=1.2.0",
    ],
    entry_points={
        "console_scripts": [
            "mind-bender-pipeline=pipeline:main",
        ],
    },
)
