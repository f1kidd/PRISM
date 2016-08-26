## Synopsis

This set of codes downloads PRISM weather data from Oregon State's PRISM database, and accumulates data into growing degree days, accumulated precipitation, or extreme weather counts based on user input date ranges.

## Code Example

To call functions, use execute.py, which is a wrap up script for all functions needed.

For example, to generate cumulative precipitation maps between April and October, from 2000 to 2010, call:

prec_exec(path,2000,2010,4,10)

## Motivation

PRISM weather data is a series of dataset retrieved from satellite remote sensing. It provides a bunch of daily weather variables, e.g., tmin, tmax, precipitation, for the continental US. It has a spatial resolution of 13KMs.

Using PRISM data, we can easily generate more sophisticated accumulation maps. For example, to calculate annual growing degree days (GDD), which is a measure of how much heat crops receive in a given growing season. Or, weekly, monthly, or yearly precipitation maps. 

## Notes

The user need to create a new folder storing daily and accumulated rasters, say, "C:/PRISM". Then, use this folder as the path when executing. The program will automatically generates required sub-folders under this folder. 

## Author

Xinde "James" Ji, Virginia Tech, xji@vt.edu
