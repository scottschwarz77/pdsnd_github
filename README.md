# Bikeshare Statistics

## Date created

June 9, 2024

## Description

This program computes bikeshare statistics, such as the most common travel times and the average trip duration. Data from three cities (Chicago, New York, and Washington) can be used. In addition to viewing bikeshare statistics, the user can view data from individual bike trips.

## Components of the installation

This program uses one Python file (`bikeshare.py`) and three data files: `chicago.csv`, `new_york_city.csv`, and `washington.csv`. The Python file is run using the Python interpreter. While the program runs, one or more of the data files will be accessed, depending on which city is selected.

## Installation

1. The Bikeshare Statistics program requires Python to be installed. Python can be downloaded [here](https://www.python.org/downloads/).

2. From the command line, clone the [bikeshare repo](https://github.com/scottschwarz77/pdsnd_github) from Github.

3. Change to the directory where the repo was cloned. To run the program, see the next section.

## Usage

To run the program, run the following command:

```
python3 bikeshare.py
```

You will be asked a few questions as to what filters to apply to the data:

- Which city would you like see data for?
- Would you like to filter the data for the month, day, both, or none at all? (If applicable, you will be asked for the specific month/day).

After answering the two questions above, statistics about the data will be displayed. Following that, you will be prompted if you want to see individual rows of data.
