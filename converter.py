import os
import re
import sys
import xml.etree.ElementTree as ET
from datetime import datetime
import json
import pygjson

VERBOSE = True
PATH = os.getcwd()

def fixFileName(i):

    i = i.replace('#', '')
    i = i.replace('%', '')
    i = i.replace('{', '')
    i = i.replace('}', '')
    i = i.replace('\\', '')
    i = i.replace('$', '')
    i = i.replace('!', '')
    i = i.replace('!', '')
    i = i.replace('\'', '')
    i = i.replace('"', '')
    i = i.replace(':', '')
    i = i.replace('@', '')
    i = i.replace('<', '')
    i = i.replace('>', '')
    i = i.replace('*', '')
    i = i.replace('?', '')
    i = i.replace('/', '')
    i = i.replace(' ', '')
    i = i.replace('+', '')
    i = i.replace('`', '')
    i = i.replace('|', '')
    i = i.replace('=', '')

    return i

def log(text: str, override=False):

    if VERBOSE and not override:
        print(f"log | {text} [{datetime.now()}]")
    elif override:
        print(f"log | {text} [{datetime.now()}]")

def request_input(text: str):

    z:str = input(f"input | {text} $ ")
    return z

def excepted(exception: str):

    log(f"Exception encountered! {str(exception)}", override=True)
    log(f"Stopping! Code: 1", override=True)
    sys.exit(0)

log("Starting vERAM Conversion Program", override=True)

user_selected_file = request_input("Enter vERAM facility file")

log("Loading XML GeoMap Files", override=True)

tree = ET.ElementTree()

try:

    tree = ET.parse(user_selected_file)

except (ET.ParseError, FileNotFoundError) as e:

    excepted(e)

ROOT = tree.getroot()
OUTDIR = request_input("Enter output directory")

PATH += f"\\{OUTDIR}"

GMO = []
GM = []
GM_LEN = 1-len(GMO)
GMO_LEN = 0

def recurse(i, c:int):

    global GMO_LEN, GM_LEN

    for x in i:

        attr = x.attrib

        z:str = str(x).split("'")[1]


        if z == "GeoMap": 
            GM_LEN+=1
            log("New GeoMap found!", override=True)
            c+=1
            GMO.append({attr["Name"]: []})
            GM.append(attr["Name"])

        if z == "GeoMapObject" and "Description" in attr: 

            log(f'Loaded map: {attr["Description"]}, {GM[c-1]}')
            GMO[c-1][GM[c-1]].append(x)
            GMO_LEN+=1

        recurse(x, c)
    
recurse(ROOT, 0)

log(f"GeoMap Files loaded successfully! ({1+GM_LEN})", override=True)

log(f"Beginning conversion process. GeoMaps to convert: {GM_LEN-1}, GeoMapObjects to convert: {GMO_LEN}")

it = 0

def filterc(f: list):

    o = [0]

    for x in f.split(','):

        o.append(int(x))

    return o

for mapn in range(GM_LEN-1):

    map = GMO[mapn][GM[mapn]]

    n1 = 0

    for a in map:

        m, n = pygjson.generate(a)
        log(f"Conversion complete for {n}!")

        f1 = f'\\{n}_{GM[mapn]}'
        f1 = fixFileName(f1)
        f1 = PATH + '\\' + f1 + '.geojson'

        with open(f1, 'w+') as f:

            json.dump(m, f)

log("Conversion complete!")             