"""
# Setup tool
# Module Version: 1.0
# Developed by Anodev. (https://github.com/OPHoperHPO)
"""


import os
import wget
import tarfile


class Config:
    """Config object"""
    # general
    arc_name = "model.tar.gz"
    # xception_model
    xc_url = "http://download.tensorflow.org/models/deeplabv3_pascal_train_aug_2018_01_04.tar.gz"
    xc_dir = os.path.join("..", "models", "xception_model")


def prepare():
    """Creates folders"""
    print("Create folders")
    try:
        if not os.path.exists(Config.xc_dir):
            os.makedirs(Config.xc_dir)
    except BaseException as e:
        print("Error creating model folders! Error:", e)
        exit(1)
    return True


def download():
    """Loads model archives"""
    path_xc = os.path.join(Config.xc_dir, Config.arc_name)
    try:
        if os.path.exists(path_xc):
            os.remove(path_xc)
        print("Start download model archives!")
        wget.download(Config.xc_url, out=path_xc)
        print("Download finished!")
    except BaseException as e:
        print("Error download model archives! Error:", e)
        exit(1)
    return True


def untar():
    """Untar archives"""
    path_xc = os.path.join(Config.xc_dir, Config.arc_name)
    try:
        print("Start unpacking")
        if path_xc.endswith("tar.gz"):
            tar = tarfile.open(path_xc, "r:gz")
            tar.extractall(path=Config.xc_dir)
            tar.close()
            os.rename(os.path.join(Config.xc_dir, "deeplabv3_pascal_train_aug"),
                      os.path.join(Config.xc_dir, "model"))
            print("Unpacking 2 archive finished!")
    except BaseException as e:
        print("Unpacking error! Error:", e)
        exit(1)
    return True


def clean():
    """Cleans temp files"""
    path_xc = os.path.join(Config.xc_dir, Config.arc_name)
    try:
        if os.path.exists(path_xc):
            os.remove(path_xc)
    except BaseException as e:
        print("Cleaning error! Error:", e)
    return True


def setup():
    """Performs program setup before use"""
    if prepare():
        if download():
            if untar():
                if clean():
                    print("Setup finished! :)")
                    exit(0)


if __name__ == "__main__":
    setup()
