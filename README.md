# PyViewer
A basic CSV viewer for large files.

PyViewer loads the top N MB from a CSV-like file and displays it as a table for the user. It allows quick searching over the columns with regular expressions. 

## Usage

```sh
viewer.py [-hd|--header] [-re|--regex] [-s|--search column:row] filename
```

- **header** treats first line of file as a header
- **regex** treats the row argument of *search* as a regular expression
- **search** displays only items matching the string/regex 'row' from column 'column'
- sample usages

```sh
$ cd src
$ python viewer.py ../sample-data/csv_100x10.csv
$ python viewer.py --header ../sample-data/csv_100x10.csv
$ python viewer.py --header -re -s strb_0:.*?land$ ../sample-data/csv_100x10.csv
```



## Documentation

See this [page](docs/index.md) for further details.

