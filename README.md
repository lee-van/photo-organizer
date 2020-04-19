# photo-organizer
Organizes a directory of photos by date. Adds an option '--user' flag to each folder
Uses exif if available, otherwise attempts to infer from filename

# Arguments and Usage
## Usage
```
usage: argdown [-h] --input INPUT [INPUT ...] --output OUTPUT [--user USER]
               [--noMerge]
```
## Arguments
### Quick reference table
|Short|Long       |Default|Description                                                        |
|-----|------------------|--------|-------------------------------------------------------------------|
|`-h` |`--help`          |        |show this help message and exit                                    |
|`-i` |`--input`         |`None`  |Input files                                                        |
|`-o` |`--output`        |`None`  |Output directory                                                   |
|`-u` |`--user`          |`None`  |Name of photographer                                               |
|`-n` |`--noMerge`       |`False` |Do not merge any files into existing folders even if no overwriting|
|`-f` |`--forceOverwrite`|`False` |Force overwrite existing files                                     |

### `-h`, `--help`
show this help message and exit

### `--input`, `-i` (Default: None)
Input files

### `--output`, `-o` (Default: None)
Output directory

### `--user`, `-u` (Default: None)
Name of photographer

### `--noMerge`, `-n`
Do not merge any files into existing folders even if no overwriting. I.e. do not modify any existing folders

### `--forceOverwrite`, `-f`
Force overwrite existing files

