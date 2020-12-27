#!/data/data/com.termux/files/usr/bin/bash -e

# Use rclone --config /sdcard/.rclone/rclone.conf config to add new storage
# Place this file in ~/.termux/boot and chmod +x

# must be run with root privileges
[ $(id -u) -eq 0 ] || exec su --mount-master -c "LD_LIBRARY_PATH=$LD_LIBRARY_PATH HOME=$HOME PATH=$PATH:$HOME/bin $0"

# make sure to be in root mount namespace
[ $(readlink /proc/1/ns/mnt) = $(readlink /proc/self/ns/mnt) ] || nsenter -t 1 -m -- "$0"

Unmount() {
    fusermount -u /mnt/cloud/drive 2>/dev/null || :
}

# make sure it's not already mounted
Unmount

# make sure it's unmounted after rclone is killed
trap 'sleep 1; Unmount' EXIT

# mount remote in /sdcard/
mkdir /mnt/cloud
mkdir /mnt/cloud/drive
rclone --config /sdcard/.rclone/rclone.conf -v mount --daemon drive: /mnt/cloud/drive --gid 9997 --dir-perms 0771 --file-perms 0660 --umask=0 --allow-other
