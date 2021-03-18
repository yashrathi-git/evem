from setuptools import setup

setup(
    name="event_manager",
    version="1.0",
    packages=["event_manager"],
    include_package_data=True,
    install_requires=[
        "Pygments",
        "colorama",
        "SQLAlchemy",
        "premailer",
        "mistune",
        "humanize",
        "Jinja2",
        "Click",
        "beautifulsoup4",
        "python_dateutil",
    ],
    entry_points="""
        [console_scripts]
        evem=event_manager.__main__:cli
    """,
)
