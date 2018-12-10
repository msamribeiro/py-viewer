### Current Status

- Reads data from file, assuming it is separate by comma

- Toggles header based on first line of file

- Searches by single column, with syntax column:value

- Searches based on regex, with syntax column:regex

- Input parameters from command line and GUI.

- Alternates colors between rows, although not optionally.


### TODO

- Proper commenting and documentation
- Allow user-specified separator (typically tab, space, or comma).
- Restrict viewer to load top of file only rather than let user navigate through the file. Later, we may allow the tool to load the top N lines given a search query.
- Allow multiple data types. Currently everything is treated as a string, which leads to weird sorting.




### Wish List
- Show line counts for visible lines
- When searching from terminal, show top n based on search
- Regex search on multiple columns
- Regex search with numerical comparisons (=, >, <, ...)
- Editable cells and save to file
- Copy data to clipboard from viewer

