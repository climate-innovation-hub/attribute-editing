"""Command line program for defining file attributes for a given data type/product."""
import pdb
import argparse

import yaml
import xarray as xr


def main(args):
    """Run the program."""
    
    with open('global_attributes.yml', "r") as reader:
        global_attrs_template = yaml.load(reader, Loader=yaml.BaseLoader)
    assert args.product in global_attrs_template
    attr_dict = global_attrs_template['universal'] | global_attrs_template[args.product]

    #ds = xr.open_dataset(args.infile)
        
    attr_edits = ' '
    for key, value in attr_dict.items():
        new_attr = f"""-a {key},global,o,c,"{value}" """
        attr_edits = attr_edits + new_attr
    
    clear_global_attrs = f"ncatted -h -a ,global,d,, {args.infile}"
    add_global_attrs = f"ncatted -h {attr_edits} {args.infile}"
    if args.outfile:
        with open(args.outfile, "w") as f:
	        f.write(clear_global_attrs + "\n")
	        f.write(add_global_attrs)
    else:
	    print(clear_global_attrs)
	    print(add_global_attrs) 


if __name__ == '__main__':
    parser = argparse.ArgumentParser(
        description=__doc__,
        argument_default=argparse.SUPPRESS,
        formatter_class=argparse.RawDescriptionHelpFormatter
    )     
    parser.add_argument("infile", type=str, help="data file for metadata editing")
    parser.add_argument("product", type=str, choices=('qqscale',), help="product type")
    
    parser.add_argument("--outfile", type=str, default=None, help="output file name")

    args = parser.parse_args()
    main(args)
