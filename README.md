# Image-Compiler

## Description
Gets all images from a directory and all it's subdirectories and their subdirectories...
Then copies them into one folder.

Note: any images with duplicate names will be skipped (only the first instance is copied)

## Run

`pip install -r requirements.txt`

`python ImageCollector.py <src_dir_root> <dst_dir>`

You can use `python ImageCollector.py -h` for help

### Optional flags:

`--workers` - manually specify how many workers to use. By default it uses the number of threads your CPU has

`-m, --metadata` - additionally copies the image metadata (e.g. date modified, permissions, etc)

