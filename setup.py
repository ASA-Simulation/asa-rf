from setuptools import find_packages, setup

setup(
    name="asa-rf",
    packages=find_packages(include=["rf"]),
    version="0.0.1",
    description="ASA rf modeling scripts",
    author="Diego Geraldo, Adrisson Samersla",
    author_email="diegodg@fab.mil.br, samerslaars@fab.mil.br",
    license="MIT",
    install_requires=[
        "matplotlib==3.8.3",
        "numpy==1.26.4",
    ],
    setup_requires=["pytest-runner"],
    test_suite="tests",
)
