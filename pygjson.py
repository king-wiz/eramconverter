import xml.etree.ElementTree as ET

"""

Information:

Provide structure to compiling GEOJSON files

"""

def parseFilters(inp: str): 

    r = inp.split(',')
    out = [0]

    for i in r:

        out.append(int(i))

    return out

def convertDefault(key, val):

    if key == 'Lines': return {'text': val}
    elif key == 'Underline': return {'underline': bool(val)}
    elif key == 'Opaque': return {'opaque': bool(val)}
    elif key == 'XOffset': return {'xOffset': int(val)}
    elif key == 'YOffset': return {'yOffset': int(val)}
    elif key == 'Size': return {'size': int(val)}
    elif key == 'Style': return {'style': val}
    elif key == 'Size': return {'size': int(val)}
    elif key == 'Bcg': return {'bcg': int(val)}
    elif key == 'Color': return {'color': val}
    elif key == 'Filters': return {'filters': parseFilters(val)}
    elif key == 'Thickness': return {'thickness': int(val)}

def mergeNonDefaults(normal:list, override:list):

    output = []
    over = []

    for i in override:
        over.append(list(i.keys())[0])
        output.append(i)

    for z in normal:

        k = list(z.keys())[0]
        if k not in over:
            output.append(z)

    return output

def generate(object):

    #Object is an XML GeoMapObject

    NAME:str = object.attrib["Description"]
    OUTPUT:dict = {

        'type': 'FeatureCollection',
        'features': []

    }

    t_def:list = []
    s_def:list = []
    l_def:list = []

    for defaults in object:

        o_type:str = str(defaults).split("'")[1]

        for default in dict(defaults.attrib):

            if o_type == 'TextDefaults':

                t_def.append(convertDefault(default, defaults.attrib[default]))

            elif o_type == 'SymbolDefaults':

                s_def.append(convertDefault(default, defaults.attrib[default]))

            elif o_type == 'LineDefaults':

                l_def.append(convertDefault(default, defaults.attrib[default]))

        for data in defaults:

            p_data = data.attrib
            d_type = p_data['{http://www.w3.org/2001/XMLSchema-instance}type']

            t_nondef = []
            s_nondef = []
            l_nondef = []

            #Get non standard defaults

            for nonstandard in p_data:

                if nonstandard not in ['Lat', 'Lon', 'StartLat', 'StartLon', 'EndLat', 'EndLon', '{http://www.w3.org/2001/XMLSchema-instance}type']:

                    if len(p_data[nonstandard]) > 0:

                        if d_type == 'Text':

                            t_nondef.append(convertDefault(nonstandard, p_data[nonstandard]))

                        elif d_type == 'Symbol':

                            s_nondef.append(convertDefault(nonstandard, p_data[nonstandard]))

                        elif d_type == 'Line':

                            l_nondef.append(convertDefault(nonstandard, p_data[nonstandard]))

            if d_type == 'Text':

                rValues = {}
                merge = mergeNonDefaults(t_def, t_nondef)

                for n in merge:

                    d0 = list(n.keys())[0]
                    rValues[d0] = n[d0]

                OUTPUT['features'].append({

                    'type': 'Feature',
                    'geometry': {

                        'type': 'Point',
                        'coordinates': [float(p_data['Lon']), float(p_data['Lat'])]

                    },

                    'properties': rValues

                })

            elif d_type == 'Symbol':

                rValues = {}
                merge = mergeNonDefaults(s_def, s_nondef)

                for n in merge:

                    d0 = list(n.keys())[0]
                    rValues[d0] = n[d0]

                OUTPUT['features'].append({

                    'type': 'Feature',
                    'geometry': {

                        'type': 'Point',
                        'coordinates': [float(p_data['Lon']), float(p_data['Lat'])]

                    },

                    'properties': rValues

                })

            if d_type == 'Line':

                rValues = {}
                merge = mergeNonDefaults(l_def, l_nondef)

                for n in merge:

                    d0 = list(n.keys())[0]
                    rValues[d0] = n[d0]

                OUTPUT['features'].append({

                    'type': 'Feature',
                    'geometry': {

                        'type': 'LineString',
                        'coordinates': [[float(p_data['StartLon']), float(p_data['StartLat'])], [float(p_data['EndLon']), float(p_data['EndLat'])]]

                    },

                    'properties': rValues

                })

    return OUTPUT, NAME




                    

                


                        








