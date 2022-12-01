"""Command line program for defining file attributes for a given data type/product."""

import argparse
import itertools

import yaml
import xarray as xr


class store_dict(argparse.Action):
    """An argparse action for parsing a command line argument as a dictionary.

    Examples
    --------
    title="hello world" becomes {'title': 'hello world'}

    """

    def __call__(self, parser, namespace, values, option_string=None):
        setattr(namespace, self.dest, dict())
        for value in values:
            key, val = value.split("=")
            getattr(namespace, self.dest)[key] = val


def get_template_attrs(template_file, product):
    """Get global attributes from template"""
    
    with open(template_file, "r") as reader:
        attr_template = yaml.load(reader, Loader=yaml.BaseLoader)
    assert product in attr_template
    attr_dict = attr_template['universal'] | attr_template[product]

    return attr_dict


def get_file_attrs(infile, keep_list=[]):
    """Get attribute information from data file."""
    
    attrs_from_data = {}
    ds = xr.open_dataset(args.infile)
    try:
        attrs_from_data['time_coverage_start'] = ds['time'].values[0].isoformat()
        attrs_from_data['time_coverage_end'] = ds['time'].values[-1].isoformat()
    except:
        pass

    spatial_attrs = [
        'geospatial_lat_min',
        'geospatial_lat_max',
        'geospatial_lon_min',
        'geospatial_lon_max'
    ]
    for spatial_attr in spatial_attrs:
        if spatial_attr in ds.attrs:
            attrs_from_data[spatial_attr] = ds.attrs[spatial_attr]
        else:
            _temp, dim, mode = spatial_attr.split('_')
            idx = 0 if mode == 'min' else -1
            attrs_from_data[spatial_attr] = str(ds[dim].values[idx])

    for keep_attr in keep_list:
        attrs_from_data[keep_attr] = ds.attrs[keep_attr]
        
    ds.close()
    
    return attrs_from_data


def main(args):
    """Run the program."""

    template_attr_dict = get_template_attrs(args.template_file, args.product)     
    file_attr_dict = get_file_attrs(args.infile, keep_list=args.keep_attrs)
    new_attr_dict = template_attr_dict | file_attr_dict
    new_attr_dict = new_attr_dict | args.custom_global_attrs
        
    attr_edits = ' '
    for key, value in new_attr_dict.items():
        new_attr = f"""-a {key},global,o,c,"{value}" """
        attr_edits = attr_edits + new_attr

    clear_global_attrs = f"ncatted -h -a ,global,d,, {args.infile}"
    if args.outfile:
        clear_global_attrs = f"{clear_global_attrs} {args.outfile}"
        outfile = args.outfile
    else:
        outfile = args.infile
    add_global_attrs = f"ncatted -h {attr_edits} {outfile}"

    print(clear_global_attrs)
    print(add_global_attrs)

    if args.del_var_attrs:
        attr_removals = ' '
        ds = xr.open_dataset(args.infile)
        var_list = list(ds.keys())
        for var_name, var_attr in itertools.product(var_list, args.del_var_attrs):
            del_attr = f"-a {var_attr},{var_name},d,, "
            attr_removals = attr_removals + del_attr
        remove_var_attrs = f"ncatted -h {attr_removals} {outfile}"
        print(remove_var_attrs)


if __name__ == '__main__':
    parser = argparse.ArgumentParser(
        description=__doc__,
        argument_default=argparse.SUPPRESS,
        formatter_class=argparse.RawDescriptionHelpFormatter
    )     
    parser.add_argument("infile", type=str, help="data file for metadata editing")
    parser.add_argument("product", type=str, choices=('qqscale', 'agcd'), help="product type")
    parser.add_argument("template_file", type=str, help="YAML file with metadata defaults")
    
    parser.add_argument(
        "--outfile",
        type=str,
        default=None,
        help="new data file (if none infile is just modified in place)"
    )
    parser.add_argument(
        "--keep_attrs",
        type=str,
        nargs="*",
        default=[],
        help="Global attributes to keep from infile",
    )
    parser.add_argument(
        "--custom_global_attrs",
        type=str,
        nargs="*",
        action=store_dict,
        default={},
        help="""Custom global attributes (e.g. title="QQ Scaled Climate Variables, daily tmin")""",
    )
    parser.add_argument("--del_var_attrs", type=str, nargs='*', default=[], help="variable attributes to delete")

    args = parser.parse_args()
    main(args)
