import os


# IO
def check_dir(d):
    if not os.path.exists(d):
        print("Directory {} does not exist. Exit.".format(d))
        exit(1)


def check_file(file):
    if file is not None and not os.path.exists(file):
        print("File {} does not exist. Exit.".format(file))
        exit(1)


def ensure_dir(d, verbose=True):
    if not os.path.exists(d):
        if verbose:
            print("Directory {} do not exist; creating...".format(d))
        os.makedirs(d)

