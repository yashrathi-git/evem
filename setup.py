from setuptools import setup

setup(
    name="mylifelogger",
    version="1.0",
    packages=["mylifelogger"],
    include_package_data=True,
    install_requires=["Pygments==2.3.1",
                      "colorama==0.4.3",
                      "SQLAlchemy==1.3.23",
                      "premailer==3.7.0",
                      "mistune==2.0.0rc1",
                      "humanize==3.2.0",
                      "Jinja2==2.11.2",
                      "Click==7.0",
                      "beautifulsoup4==4.9.3",
                      "python_dateutil==2.8.1"
                      ],
    entry_points="""
        [console_scripts]
        mll=mylifelogger.__main__:cli
    """,
)
