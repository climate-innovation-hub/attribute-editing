## Attribute editing

This repository contains the code used by the Climate Innovation Hub to standardise
the metadata in netCDF files it produces.

The `define_attributes.py` script determines the correct file attributes for a given data type/product. 
It outputs those attributes in the form of a shell script containing a series of `ncatted` commands
(for fixing file metadata after the fact) or a
YAML file containing each key/value attribute pair
(for reading into a Python script for editing attributes prior to writing an output file).

 
