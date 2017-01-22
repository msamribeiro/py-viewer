# csv-viewer
A basic CSV viewer for large files

## Usage

```sh
viewer.py [-hd|--header] [-re|--regex] [-s|--search column:row] filename
```

 * header treats first line of file as a header
 * regex treats the row argument of *search* as a regular expression
 * search displays only items matching the string/regex 'row' from column 'column'

* sample usages

```sh
$ python viewer.py sample-data/FL_insurance_small.csv
$ python viewer.py --header sample-data/FL_insurance_small.csv
$ python viewer.py --header -re -s county:CLAY*
```

## Disclaimer

This is an ongoing project and currently still in development.
This tool has known issues and should be used at your own risk.
