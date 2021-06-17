import sys
from esgcet.mapfile import ESGPubMapConv
import json
import os
import configparser as cfg
import argparse
from pathlib import Path


def get_args():
    parser = argparse.ArgumentParser(description="Publish data sets to ESGF databases.")

    home = str(Path.home())
    def_config = home + "/.esg/esg.ini"
    parser.add_argument("--project", dest="proj", default="", help="Set/overide the project for the given mapfile, for use with selecting the DRS or specific features, e.g. PrePARE, PID.")
    parser.add_argument("--map", dest="map", required=True, help="Mapfile ending in .map extension, contains metadata about the record.")
    parser.add_argument("--out-file", dest="out_file", help="Output file for map data in JSON format. Default is printed to standard out.")
    parser.add_argument("--ini", "-i", dest="cfg", default=def_config, help="Path to config file.")

    pub = parser.parse_args()

    return pub


def run():
    a = get_args()
    ini_file = a.cfg
    config = cfg.ConfigParser()
    if not os.path.exists(ini_file):
        print("Error: config file not found. " + ini_file + " does not exist.", file=sys.stderr)
        exit(1)
    if os.path.isdir(ini_file):
        print("Config file path is a directory. Please use a complete file path.", file=sys.stderr)
        exit(1)
    try:
        config.read(ini_file)
    except Exception as ex:
        print("Error reading config file: " + str(ex))
        exit(1)

    p = True
    if a.out_file is not None:
        p = False
        outfile = a.out_file



    proj = None
    if a.proj != "":
        proj = a.proj
    else:
        try:
            proj = config['user']['project']
        except:
            pass

    try:
        fullmap = a.map
    except:
        print("Error with argparse. Exiting.", file=sys.stderr)
        exit(1)

    mapconv = ESGPubMapConv(fullmap)
    map_json_data = None
    try:
        map_json_data = mapconv.mapfilerun()

    except Exception as ex:
        print("Error with converting mapfile: " + str(ex), file=sys.stderr)
        exit(1)

    if p:
        print(json.dumps(map_json_data))
    else:
        with open(outfile, 'w') as of:
            json.dump(map_json_data, of)


def main():
    run()


if __name__ == '__main__':
    sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.realpath(__file__))))
    main()
