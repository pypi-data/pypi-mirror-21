SmartTAP: Smart card Transport Analysis Package

Version: 1.0
Author: John Tasker
Contact: john_tasker@outlook.com
License: GNU GPL V3.0

This is the initial release of the SmartTAP package which is capable of
conducting data cleaning and preparation activities on public transport smart
card data. This package was developed using GoCard data provided by Translink
for the South-East Queensland, Australia public transport network.

RUN PACKAGE
To run the software, open GUIModule.py using Python 3. A Tkinter GUI will
appear. A directory must be specified containing the smart card data in .csv
format (e.g. Aug15Pr.csv), a Routes.txt file (GTFS Routes.txt standard), a
Stops.txt file (GTFS Stops.txt standard). The directory can also contain a list 
of commuters who will be used to filter all trip records. This file must be in 
.csv format.

	SETTINGS
	To specify the database name, input this into the provided box and click 
	'Set Database Name'. The provided name must end in .db. By default the
	database will be named 'GoCard.db'.
	
	Operation/processing timings are set on by default. If you do not wish to
	see timings click the 'Time - ON' button and it will change to 'Time - OFF'.
	The button will also change colour from green to red. To turn timing on
	click the button again.
	
	The output window (lower section of GUI) will display the outputs of
	operations/processing and will automatically scroll to the most recent
	output. If you wish to clear the output window click the 'Clear Output'
	button. This will remove all text from the window.
