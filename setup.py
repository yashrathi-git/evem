from setuptools import setup

setup(
    name="mylifelogger",
    version="1.0",
    packages=["mylifelogger"],
    include_package_data=True,
    install_requires=["click==7.1.2",
                      "SQLAlchemy==1.3.23"],
    entry_points="""
        [console_scripts]
        mll=mylifelogger.__main__:cli
    """,
)
