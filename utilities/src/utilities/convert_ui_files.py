"""
Automates converting *.ui files from the GUI to *.py files.
Must be run inside the docker container

"""
from os.path import splitext
from glob import glob
import ntpath
import subprocess


PROGRAM = 'pyuic5'
UI_DIR = '/workspaces/gust/src/main/python/gust/gui/ui'


def path_leaf(path):
    """Properly get the file from an arbitrary path independent of the OS.

    Parameters
    ----------
    path : string
        Full path of a file.

    Returns
    -------
    string
        Name of the file with the file extension.

    """
    head, tail = ntpath.split(path)
    return tail or ntpath.basename(head)


if __name__ == "__main__":
    for file in glob('{:s}/*.ui'.format(UI_DIR)):
        f_name = splitext(path_leaf(file))[0]
        args = [PROGRAM, '-x', '{:s}/{:s}.ui'.format(UI_DIR, f_name),
                '-o', '{:s}/{:s}.py'.format(UI_DIR, f_name)]
        print(' '.join(args))
        subprocess.run(args)
