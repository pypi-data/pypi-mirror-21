import os
import sys
import time
import opie
import click
import tarfile
import usb.core
import usb.util
from helpers import u, mount

VENDOR_TE = 0x2367
PRODUCT_OP1 = 0x0002
OP1_BASE_DIRS = set(['tape', 'album', 'synth', 'drum'])

def ensure_connection():
    if not is_connected():
        print("Please connect your OP-1 and put it in DISK mode (Shift+COM -> 3)...")
        wait_for_connection()

def is_connected():
    return usb.core.find(idVendor=VENDOR_TE, idProduct=PRODUCT_OP1) is not None

def wait_for_connection():
    try:
        while True:
            time.sleep(1)
            if is_connected():
                break
    except KeyboardInterrupt:
        sys.exit(0)

def get_mount_or_die_trying():
    ensure_connection()
    mount = find_op1_mount()
    if mount is None:
        print("Waiting for OP-1 disk to mount...")
        mount = wait_for_op1_mount()
        if mount is None:
            exit("Failed to find mount point of OP-1. Feel free to file an issue.")
    return mount

def find_op1_mount():
    dirs = []
    mounts = mount.get_potential_mounts()
    if mounts is None:
        dirs = [os.path.join("/Volumes", x) for x in u.get_visible_folders("/Volumes")]
    else:
        dirs = [x[1] for x in mounts]

    for dir in dirs:
        subdirs = u.get_visible_folders(dir)
        if set(subdirs) & OP1_BASE_DIRS == OP1_BASE_DIRS:
            return dir

    return None

def wait_for_op1_mount(timeout=5):
    i=0
    try:
        while i < timeout:
            time.sleep(1)
            mount = find_op1_mount()
            if mount is not None:
                return mount
            i += 1
        print("timed out waiting for mount.")
        return None
    except KeyboardInterrupt:
        sys.exit(0)

