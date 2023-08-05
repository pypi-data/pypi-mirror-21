from setuptools import setup
 
setup(
	name='FlightReportManager',
	packages = ['FlightReportManager'],
	scripts=['FlightReportManager/RunFlightReportManager'],
	version='0.3',
	description = 'Store and manage your Parrot Bebop flights. Visualise your flight and export it to many different formats.',
	author = 'Johannes Kinzig',
	author_email = 'johannes_kinzig@icloud.com',
	url = 'https://johanneskinzig.de/software-development/flightreportmanager.html',
	include_package_data=True,
	license='Apache License, Version 2.0',
	install_requires=[
        "DroneDataConversion",
        "matplotlib",
        "appdirs",
        "pyglet",
        "geoplotlib",
    ]
	)