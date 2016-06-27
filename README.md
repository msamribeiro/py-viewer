# csv-viewer
A basic CSV/TSV viewer for large files

# Usage

viewer.py \[-hd|--header\] \[-re|--regex\] \[-s|--search column:row\] filename

* *header* treats first line of file as a header
* *regex* treats the row argument of *search* as a regular expression
* *search* displays only items matching 'row' from column 'column'

* sample usages: 
    * python viewer.py sample-data/FL\_insurance\_small.csv
    * python viewer.py --header sample-data/FL\_insurance\_small.csv
    * python viewer.py --header -re -s county:CLAY*


# Planned Additions

* Migration to python3
* Proper logging information
* Proper testing of buffering and chunking
* Show line numbers
* Correct usage with large files


# Disclaimer

This project is ongoing and currently in its early stages.
This tool currently has serious known issues and should be used at your own risk.
