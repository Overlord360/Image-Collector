import os, sys
import argparse

from concurrent.futures import ProcessPoolExecutor
from shutil import copyfile, copystat

from tqdm import tqdm

IMAGE_EXTENSIONS = [".jpg", ".jpeg", ".png", ".gif", ".bmp", ".tiff", ".svg", ".webp"]
MAX_WORKERS = 1

def main(args):
    print(f"Collecting images from {args.directory}")

    src_list = find_images(args.directory)
    size = len(src_list)
    print(f"Found {size} images.")
    
    dst_list = make_dst_list(src_list, args.output)
    print("*************")
    src_list, dst_list = remove_duplicates(src_list, dst_list)
    print(f"Removed {size - len(src_list)} files with the same name.")
    size = len(src_list)
    print("*************")
    src_list, dst_list = check_if_file_exists(src_list, dst_list)
    print(f"Removed {size - len(src_list)} files that already exist.")
    print("*************")
    if args.workers > 0:
        MAX_WORKERS = args.workers
    else:
        MAX_WORKERS = os.cpu_count()
    print(f"Using {MAX_WORKERS} workers.")
    _ = copy_images(src_list, dst_list)
    
    if args.metadata:
        _ = copy_image_metadata(src_list, dst_list)

    sys.exit(0)

def copy_images(src_list, dst_list):
    print(f"Copying {len(src_list)} images to {args.output}")
    with ProcessPoolExecutor(max_workers=MAX_WORKERS) as executor:
        results = list(tqdm(executor.map(copyfile, src_list, dst_list), total=len(src_list)))
    return results
def copy_image_metadata(src_list, dst_list):
    print(f"Copying metadata for images:")
    with ProcessPoolExecutor(max_workers=MAX_WORKERS) as executor:
        results = list(tqdm(executor.map(copystat, src_list, dst_list), total=len(src_list)))
    return results

# recursively find all images in the directory and subdirectories
def find_images(directory):
    images = []
    for root, dirs, files in tqdm(os.walk(os.path.abspath(directory))):
        for file in files:
            extension = os.path.splitext(file)[1].lower()
            if extension in IMAGE_EXTENSIONS:
                images.append(os.path.join(root, file))
    return images

def make_dst_list(src_list, dst_dir):
    dst_list = []
    print("Making destination list")
    for src in tqdm(src_list, total=len(src_list)):
        dst = os.path.join(dst_dir, os.path.basename(src))
        dst_list.append(dst)
    return dst_list

def check_if_file_exists(src_list, dst_list):
    new_src_list = []
    new_dst_list = []
    print("Checking if files already exist")
    for src, dst in tqdm(zip(src_list, dst_list), total=len(src_list)):
        if not os.path.exists(dst):
            new_src_list.append(src)
            new_dst_list.append(dst)
    return new_src_list, new_dst_list

def remove_duplicates(src_list, dst_list):
    seen = set()
    new_src_list = []
    new_dst_list = []
    print("Removing duplicate files from dst_list")
    for src, dst in tqdm(zip(src_list, dst_list), total=len(src_list)):
        if dst not in seen:
            seen.add(dst)
            new_src_list.append(src)
            new_dst_list.append(dst)
    return new_src_list, new_dst_list




def argparse_builder():
    parser = argparse.ArgumentParser(description="Collect images from a directory and its subdirectories. and copy to a new directory.")
    parser.add_argument("directory", type=str, help="The directory to search for images.")
    parser.add_argument("output", type=str, help="The directory to copy the images to.")
    parser.add_argument("--workers", type=int, default=0, help="The number of workers to use for copying images.")
    parser.add_arguement("-m", "--metadata", action="store_true", help="Copy metadata for images.")
    return parser

if __name__ == "__main__":
    parser = argparse_builder()
    args = parser.parse_args()
    main(args)