## Attribute editing

This repository contains the code used by the Climate Innovation Hub to standardise
the metadata in netCDF files it produces.

(Default/standard metadata keys and values are defined in the YAML files in this repository.)

The `define_attributes.py` script determines the correct file attributes for a given data type/product. 
It outputs a series of `ncatted` commands that can be run to correct the metadata.

### Usage
 
If you're a member of the `wp00` project on NCI
(i.e. if you're part of the CSIRO Climate Innovation Hub),
the easiest way to use the scripts in this directory is to use the cloned copy at `/g/data/wp00/shared_code/attribute-editing/`.
They can be run using the Python environment at `/g/data/wp00/users/dbi599/miniconda3/envs/cih/bin/python`.

If you'd like to run the scripts in your own Python environment,
you'll need to make sure the `xarray` and `pyyaml` libraries are installed.

Running the `define_attributes.py` script at the command line with the `-h` option explains the user options:

```bash
$ /g/data/wp00/users/dbi599/miniconda3/envs/cih/bin/python /g/data/wp00/shared_code/frequency-analysis/define_attributes.py -h
```

```
usage: define_attributes.py [-h] [--outfile OUTFILE] [--custom_global_attrs [CUSTOM_GLOBAL_ATTRS ...]]
                            [--del_var_attrs [DEL_VAR_ATTRS ...]]
                            infile {qqscale}

Command line program for defining file attributes for a given data type/product.

positional arguments:
  infile                data file for metadata editing
  {qqscale}             product type

optional arguments:
  -h, --help            show this help message and exit
  --outfile OUTFILE     new data file (if none infile is just modified in place)
  --custom_global_attrs [CUSTOM_GLOBAL_ATTRS ...]
                        Custom global attributes (e.g. title="QQ Scaled Climate Variables, daily tmin")
  --del_var_attrs [DEL_VAR_ATTRS ...]
                        variable attributes to delete
```

It's important to note that the script prints a series of `ncatted` commands to the screen.
It doesn't run those commands.
To run them you can cut and paste them into your command line or redirect the output of the script
to a file (i.e. a shell script) and then run that script.


### Example 1

The metadata in a QQ-scaled daily minimum temperature data file can be corrected
by running the following command.
It applies the default global attributes, plus
the `--del_var_attrs` option has been used to delete the `coordinates` attribute from any variables that have it
and `--custom_global_attrs` has been used to define a custom "title" global attribute.
The output has been redirected to a script called `fix.sh` which can be run to execute the commands.

```
/g/data/wp00/users/dbi599/miniconda3/envs/cih/bin/python /g/data/wp00/shared_code/frequency-analysis/define_attributes.py /g/data/dk7/kcn599/for_Leanne/QQ-Scaled_daily/tasmin_AUS_GFDL-ESM2M_rcp45_r1i1p1_CSIRO-QQS-AGCD-1981-2010_day_wrt_1986-2005_2036-2065.nc qqscale --del_var_attrs coordinates --custom_global_attrs title="QQ Scaled Climate Variables, daily tmin" > fix.sh
```

IMPORTANT: This command will edit the existing data file.
If you'd rather create a new data file, use the `--outfile` option and give the name of the new file.

