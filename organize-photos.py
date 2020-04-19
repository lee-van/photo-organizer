import os, sys, re, exifread, argparse
from glob import glob

from typing import List

################################################################################################################################################################

def parse_exif(image_files:List[str]):
    """
    Parses list of images, returns dict of dicts (key=filename, value=exif dict)
    """
    handles = {file:open(file, 'rb') for file in image_files}
    exif_dict = {file:exifread.process_file(handle) for file,handle in handles.items()}
    return exif_dict

def parse_exifdict(exif_dict, key):
    """
    Parses dict of exif metadata for key
    """  
    values = {file:str(exif[key]) for file,exif in exif_dict.items()}
    return values

def parse_datetime(datetime_str):
    m = re.match(r'(\d+):(\d+):(\d+) (\d+):(\d+):(\d+)', datetime_str)
    (year, month, day, hour, minute, second) = m.groups()
    return (year, month, day, hour, minute, second)

def parse_args():
    parser = argparse.ArgumentParser(description='Basic photo organizer based on exif metadata')
    parser.add_argument('--input', '-i', nargs='+', required=True, help='Input files')
    parser.add_argument('--output', '-o', required=True, help='Output directory')
    parser.add_argument('--user', '-u', required=False, help='Name of photographer')
    parser.add_argument('--forceOverwrite', '-f', action='store_true', help='Force overwrite existing files')
    args = parser.parse_args()
    return args

def move_files(datetimes_tuple, args):
    skipped = 0
    for file, datetime in datetimes_tuple.items():
        (year, month, day, hour, minute, second) = datetime
        user = ''
        if args.user:
            user = f"_{args.user}"
        output_dir = os.path.join(args.output, f"{year}-{month}-{day}{user}")
        if not os.path.exists(output_dir):
           os.makedirs(output_dir)
        destination = os.path.join(output_dir, os.path.basename(file))
        if os.path.exists(destination):
            if args.forceOverwrite:
                print(f'WARNING: overwriting file {destination}', file=sys.stderr)
                os.rename(file, destination)
            else:
                print(f'WARNING: skipping file {destination}', file=sys.stderr)
                skipped += 1
        else: 
            os.rename(file, destination)
    return skipped  

################################################################################################################################################################

if __name__ == "__main__":

    args = parse_args()

    #file: exif dict
    exif_dict = parse_exif(args.input)

    #file: datetime (and datetime tuples) dict
    datetimes = parse_exifdict(exif_dict, 'Image DateTime')
    datetimes_tuple = {file:parse_datetime(datetime_str) for file, datetime_str in datetimes.items()}

    #move files to new folder
    move_files(datetimes_tuple, args)
