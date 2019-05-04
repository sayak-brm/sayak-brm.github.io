#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# Writer: MaxdSre
# Blog: https://axdlog.com
# Date: Wed 2018-07-11 12:10:23 -0400 EDT
# Usage: Installing Or Upgrading Hugo On GNU/Linux

# Project: https://github.com/gohugoio/hugo
# Description: Hugo is a static HTML and CSS website generator written in Go.


# import requests
from urllib.request import Request,urlopen
import json
import re
import os
import tarfile
# remove unempty dirs
from shutil import rmtree
import subprocess

utility_name = 'Hugo'
hugo_release_api='https://api.github.com/repos/gohugoio/hugo/releases/latest'
symlink_path = '/usr/local/bin/hugo'
pack_save_dir = '/tmp'
target_dir = "/opt/" + utility_name
hugo_binary_path = target_dir + "/hugo"
is_latest_version = True

# - extract release info from api
raw_data = urlopen(Request(hugo_release_api, headers={'User-Agent': 'Mozilla/5.0'})).read().decode()
# raw_data = requests.get(hugo_release_api, timeout=0.5).text

json_data = json.loads(raw_data)

release_version = json_data['tag_name'].lstrip('v')
release_date = json_data['published_at']
release_pack_link=''
release_pack_size=''

for item in json_data['assets']:
    if re.search(r"Linux-64bit.*tar.gz$",item['name']):
        release_pack_link=item['browser_download_url']
        release_pack_size=item['size']
        break
    else:
        continue

# - if existed latest version
if os.path.exists(hugo_binary_path):
    version_info = subprocess.getoutput(hugo_binary_path + " version")
    version_num = re.search(r".*?v([\d.]+).*", version_info).group(1)

    if version_num == release_version:
        print("Latest version {} existed.".format(release_version))
    else:
        is_latest_version = False
        # remove target dir
        if os.path.exists(target_dir) and os.path.isdir(target_dir):
            rmtree(target_dir)
        print("Local version {} < latest version {}.".format(version_num, release_version))
else:
    is_latest_version = False

if is_latest_version == False:
    # remove target dir
    if os.path.exists(target_dir) and os.path.isdir(target_dir):
        rmtree(target_dir)

if not os.path.exists(target_dir):
    # - download
    pack_save_path = pack_save_dir.rstrip("/") + "/" + release_pack_link.split("/")[-1]

    if os.path.exists(pack_save_path) and os.path.getsize(pack_save_path) == release_pack_size:
        print("Find existed pack {}.".format(pack_save_path))
    else:
        if os.path.exists(pack_save_path):
            os.remove(pack_save_path)
        # https://stackoverflow.com/questions/7243750/download-file-from-web-in-python-3
        with open(pack_save_path, "wb") as file:
            # response = requests.get(release_pack_link)
            # file.write(response.content)

            response = urlopen(release_pack_link)
            file.write(response.read())

            if os.path.exists(pack_save_path) and os.path.getsize(pack_save_path) == release_pack_size:
                print("Successfully download pack {}!".format(pack_save_path))

    # - decompress
    tar = tarfile.open(pack_save_path, 'r:gz')
    # 1. extract all file
    tar.extractall(path=target_dir)

    # 2. extract needed file
    # for item in tar:
    #     if not item.name.endswith(".md"):
    #         tar.extract(item, path=target_dir)

    # - create symlink
    if os.path.exists(hugo_binary_path):
        print("Successfully install {} v{}!".format(utility_name, release_version))

        if os.path.islink(symlink_path):
            os.unlink(symlink_path)
            # os.remove(symlink_path)
        os.symlink(hugo_binary_path, symlink_path)
        print("\nSymlink info: \n{}".format(subprocess.getoutput("ls -lh " + symlink_path)))

    # - remove package
    if os.path.exists(pack_save_path):
        os.remove(pack_save_path)


if os.path.exists(hugo_binary_path):
    print("\nHugo info: \n{}".format(subprocess.getoutput(hugo_binary_path + " version")))

# Script End