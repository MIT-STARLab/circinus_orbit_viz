#  uniform tools for doing I/O operations on parameter and data files in CIRCINUS pipeline
# 
# @author Kit Kennedy

# TODO: need to cast integer IDs to string in this code

import copy

sat_ids_spec_opts = ['duplicate','synthesize']

def parse_sat_ids(sat_ids_spec,force_duplicate = False):
    if type (sat_ids_spec)==str:
        tokens = sat_ids_spec.split (',')
        if (tokens[0] in sat_ids_spec_opts) or force_duplicate:
            if  tokens[1] == 'range_inclusive':
                sat_ids = [str(ID) for ID in range ( int(tokens[2]), int (tokens[3])+1)]
                return sat_ids
            else:
                raise NotImplementedError
        else:
            raise  Exception ("Expected 'duplicate' as first token for sat_ids (%s)"%(sat_ids_spec))
    raise NotImplementedError

def duplicate_entry_for_sat_ids(params_entry,force_duplicate = False):
    new_entries = []

    sat_ids = parse_sat_ids(params_entry['sat_ids'],force_duplicate)

    for sat_id in sat_ids:
        new_entry =  copy.copy (params_entry)
        del new_entry["sat_ids"]
        new_entry["sat_id"] = sat_id
        new_entries.append (new_entry)

    return new_entries

def unpack_sat_entry_list(entry_list,force_duplicate = False):
    """unpacks a list of parameter entries for a set of satellites
    
    a list of parameter entries can contain collapsed entries that specify the properties for more than one satellite ID. in this case we need to convert those collapsed entries into unique entries for each satellite ID. So this:

    "sat_orbit_params": [
        {
            "sat_id": 0,
            "blah1": {
                ...
            },
            "blah2": ...
        },
        {
            "sat_ids": "synthesize,range_inclusive,1,29",
            "blah1": {
                ...
            },
            "blah2": ...
        }
    ]

    turns into:
    "sat_orbit_params": [
        {
            "sat_id": 0,
            "blah1": {
                ...
            },
            "blah2": ...
        },
        {
            "sat_id": 1,
            "blah1": {
                ...
            },
            "blah2": ...
        },
        {
            "sat_id": 2,
            "blah1": {
                ...
            },
            "blah2": ...
        },
        ...
        {
            "sat_id": 29,
            "blah1": {
                ...
            },
            "blah2": ...
        }
    ]

    :param entry_list: a list of  dictionaries containing satellite parameters,  with each dictionary having a "sat_id" or "sat_ids" field
    :type entry_list: list
    :returns:  a list of dictionaries, where each dictionary is unique for each "sat_id" (each has that field; "sat_ids" field is no longer present). also returns a list of sat IDs found
    :rtype: {list, list}
    """

    new_entries = []

    for entry in entry_list:
        #  if this field is present, that means the parameter entry applies for more than one satellite ID.  need to unpack for all the relevant satellite ID
        if entry.get('sat_ids', None):
            new_entries += duplicate_entry_for_sat_ids ( entry,force_duplicate)
        else:
            new_entries.append(entry)

    sat_ids = [str (entry['sat_id']) for entry in new_entries]

    return new_entries, sat_ids

def sort_input_params_by_sat_IDs(params_list,sat_id_order):

    sorted_params = []
    def sort_func(params_entry):
        return sat_id_order.index (params_entry['sat_id'])

    sorted_params_list = sorted(params_list, key= lambda x: sort_func(x))

    return sorted_params_list


def make_and_validate_sat_id_order(sat_id_order_pre,num_satellites,all_sat_ids=None):
    """ makes (if necessary) and validates the sat ID order specification list
    
    converts the sat ID order list found in the orbit prop inputs file into a list that is usable for ordering satellites In internal CIRCINUS components. It is often specified as "default" in the input file. A valid output looks like this, for example:

    "sat_id_order": [
        0,
        1,
        "2",
        "my_favorite_satellite",
        99,
        "5"
    ],

    In this case, the user has chosen to replace the normal satellite IDs 3 and 4  with custom IDs.  this is perfectly fine. Note that satellite IDs can be integers, strings, floats, whatever...

    If the "sat_id_order" field in sat_params from the input file is "defaut", then the output sat_id_order will either be a list of ordinals for every satellite if all_sat_ids is  not provided, or will be equal to all_sat_ids if it is provided.

    :param sat_id_order_pre:  the "sat_id_order" from the input file
    :type sat_id_order_pre: list
    :param num_satellites:  the number of satellites
    :type num_satellites: int
    :param all_sat_ids:  list of set IDs to use as default if provided, defaults to None
    :type all_sat_ids:  list, optional
    :returns:  the canonical sat_id_order to use in internal processing
    :rtype: {list}
    :raises: Exception, Exception
    """

    # if the default is specified, then we'll make a default list based on the order in which we find IDs
    if sat_id_order_pre == 'default':
        #  if are provided a list of all the IDs, use that as the default
        if all_sat_ids:
            sat_id_order = [str(sat_id) for sat_id in all_sat_ids]
        #  if we are not provided a list of the all the IDs,  we assume that every ID is just an ordinal
        else:            
            sat_id_order = [str(sat_indx) for sat_indx in range (num_satellites)]

    if len(sat_id_order) != num_satellites:
        raise Exception ("Number of satellite IDs is not equal to number of satellites specified in input file")
    if len(set(sat_id_order)) != len(sat_id_order):
        raise Exception ("Every satellite ID should be unique") 

    return sat_id_order

def make_and_validate_gs_id_order(gs_params):
    """ makes and validates the gs ID order specification list
    
    """

    # if the default is specified, then we'll make a default list based on the order in which we find IDs
    gs_id_order = [str(station['id']) for  station in gs_params['stations']]

    if len(gs_id_order) != gs_params['num_stations']:
        raise Exception ("Number of gs IDs is not equal to number of ground stations specified in input file")
    if len(set(gs_id_order)) != len(gs_id_order):
        raise Exception ("Every gs ID should be unique") 

    return gs_id_order