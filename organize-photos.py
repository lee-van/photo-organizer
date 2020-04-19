import os, sys, re, argparse
from glob import glob
from typing import List

import exifread, progressbar

################################################################################################################################################################

def parse_exif(image_files:List[str], key:str):
    """
    Parses list of images, returns dict of dicts (key=filename, value=exif dict)
    """
    exif_values = {}
    for file in progressbar.progressbar(image_files):
        with open(file, 'rb') as handle:
            exif_dict = exifread.process_file(handle)
            exif_values[file] = str(exif_dict[key]) if (key in exif_dict) else None
    return exif_values


def infer_datetime_from_filename(filename:str):
    m = re.match(r'(20\d{2})[:\-_\.](\d{2})[:\-_\.](\d{2})', filename)
    if m:
        (year, month, day) = m.groups()
        return (year, month, day, None, None, None)
    else:
        return None

def parse_datetime(datetime_str:str):
    m = re.match(r'(\d+):(\d+):(\d+) (\d+):(\d+):(\d+)', datetime_str)
    (year, month, day, hour, minute, second) = m.groups()
    return (year, month, day, hour, minute, second)


def parse_args():
    parser = argparse.ArgumentParser(description='Basic photo organizer based on exif metadata')
    parser.add_argument('--input', '-i', nargs='+', required=True, help='Input files')
    parser.add_argument('--output', '-o', required=True, help='Output directory')
    parser.add_argument('--user', '-u', required=False, help='Name of photographer')
    parser.add_argument('--noMerge', '-n', action='store_true', help='Do not merge any files into existing folders even if no overwriting')
    parser.add_argument('--forceOverwrite', '-f', action='store_true', help='Force overwrite existing files')
    args = parser.parse_args()
    return args


def set_destinations(datetimes:dict, args):
    """
    Defines mv destination for files based on datetime and user
    """  
    output_dirs = set()
    destinations = {}
    for file, datetime in datetimes.items():
        if datetime:
            (year, month, day, hour, minute, second) = parse_datetime(datetime)
        else:
            try:
                (year, month, day, hour, minute, second) = infer_datetime_from_filename(file)
                print(f'WARNING: \'Image DateTime\' inferred from filename not exif {file}', file=sys.stderr)
            except:
                destinations[file] = None
                continue
        
        user = ''
        if args.user:
            user = f"_{args.user}"
        output_dir = os.path.join(args.output, f"{year}-{month}-{day}{user}")
        output_dirs.add(output_dir)
        destination = os.path.join(output_dir, os.path.basename(file))
        destinations[file] = destination

    return (output_dirs, destinations)


def check_if_outputdirs_exist(output_dirs:set):
    existing_output_dirs = set()
    for output_dir in output_dirs:
        if os.path.exists(output_dir):
            existing_output_dirs.add(output_dir)
    return existing_output_dirs


def move_files(destinations:dict, args, dirsToSkip = set()):
    """
    Moves files, skipping if 1) no metadata parsed, 2) avoid merge, or 3) avoid overwrite
    """      
    skipped = 0   
    for file, destination in progressbar.progressbar(destinations.items()):
        if not destination:
            print(f'WARNING: \'Image DateTime\' could not be parsed, skipping file {file}', file=sys.stderr)
            skipped += 1
            continue

        output_dir = os.path.dirname(destination)
        if output_dir in dirsToSkip:
            print(f'WARNING: to avoid merging into existing directory, skipping file {file} -> {destination}', file=sys.stderr)
            skipped += 1
            continue

        if not os.path.exists(output_dir):
           os.makedirs(output_dir)

        if os.path.exists(destination):
            if args.forceOverwrite:
                print(f'WARNING: overwriting file {destination}', file=sys.stderr)
                os.rename(file, destination)
            else:
                print(f'WARNING: to avoid overwriting, skipping file {file} -> {destination}', file=sys.stderr)
                skipped += 1
        else: 
            os.rename(file, destination)

    return skipped  

################################################################################################################################################################

if __name__ == "__main__":

    args = parse_args()

    #file: exif dict
    print("LOG: parsing exif data")
    datetimes = parse_exif(args.input, 'Image DateTime')

    #move files to new folder
    print("LOG: moving files")
    (output_dirs, destinations) = set_destinations(datetimes, args)
    if args.noMerge:
        existing_output_dirs = check_if_outputdirs_exist(output_dirs)
        move_files(destinations, args, existing_output_dirs)
    else:
        move_files(destinations, args)

