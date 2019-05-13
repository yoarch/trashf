import sys
import os
import subprocess
import ntpath
import shutil
from os import stat
from pwd import getpwuid
from datetime import datetime

CBRED = '\033[38;5;196;1m'
CBORANGE = '\033[38;5;202;1m'
CBGREEN = '\033[38;5;40;1m'

CBWHITE = '\033[1;37m'
# CBPURPLE = '\033[1;35m'
CBBLUE = '\033[1;34m'

CBASE = '\033[0m'

TRASH_PATH = os.environ['HOME'] + "/.local/share/Trash/files/"


def check_help_request(args):
    if len(args) == 1 and (args[0] == "-h" or args[0] == "--help"):
        README_path = "/usr/lib/trashf/README.md"

        f = open(README_path, 'r')
        print(CBBLUE + "\n\t#######      trashf documentation      #######\n" + CBWHITE)

        for line in f:
            if line == "```sh\n" or line == "```\n" or line == "<pre>\n" or line == "</pre>\n":
                continue
            line = line.replace('```sh', '').replace('```', '').replace('<pre>', '').replace('</b>', '').\
                replace('<b>', '').replace('<!-- -->', '').replace('<br/>', '').replace('```sh', '').\
                replace('***', '').replace('***', '').replace('**', '').replace('*', '')

            print(" " + line, end='')
        print(CBASE)
        exit()


# def run(command):
#     return subprocess.Popen(command, shell=True, stdout=subprocess.PIPE).stdout.readlines()

def OK(msg=""):
    print(CBGREEN + "\n\t[OK] " + CBASE + msg)


def INFO(msg=""):
    # print(CBWHITE + "\n\t[INFO] " + CBASE, end='')
    print(CBWHITE + "\n\t[INFO] " + CBASE + msg)


def WARNING(msg=""):
    print(CBORANGE + "\n\t[WARNING] " + CBASE + msg)


def ERROR(msg=""):
    print(CBRED + "\n\t[ERROR] " + CBASE + msg)


def skipped():
    print(CBBLUE + "\n\t\t\tskipped\n\n" + CBASE)


def path_exists(path):
    if not os.path.exists(path):
        return False
    return True


def get_abs_path(fs):
    abs_fpaths = list()
    for f in fs:
        abs_fpaths.append(os.path.normpath((os.path.join(os.getcwd(), os.path.expanduser(f)))))
    return abs_fpaths


def get_fname(fpath):
    head, tail = ntpath.split(fpath)
    return tail or ntpath.basename(head)


def error_man(init_msg, err_msg, fpath, fpath_in_trash):
    ERROR(init_msg + " error:\n\t\t" + str(err_msg))

    sudo_conf = input(CBWHITE + "\n\t\tuse sudo?\n\t\t\t[Enter] to proceed\t\t\t[any case] to skip\n")
    if sudo_conf == "":
        subprocess.check_call(['sudo', "mv", fpath, fpath_in_trash])
    else:
        skipped()
        return False
    return True


def trashf(fpath):
    fname = get_fname(fpath)
    fpath_in_trash = TRASH_PATH + fname

    if path_exists(fpath_in_trash):
        WARNING(CBBLUE + "%s " % fname + CBASE + "already exists in trash")

        cdatetime = datetime.now()
        ctime = cdatetime.strftime("_%Y_%m_%d-%H_%M_%S")
        fpath_in_trash = fpath_in_trash + ctime
        print("\t\trenaming " + CBBLUE + " %s " % fname + CBASE + "to " + CBBLUE + "%s " % (fname + ctime) + CBASE + "before moving to trash")

    # shutil.move(fpath, fpath_in_trash)
    moved = True

    try:
        shutil.move(fpath, fpath_in_trash)

    except PermissionError as err_msg:
        moved = error_man("permission", err_msg, fpath, fpath_in_trash)

    except OSError as err_msg:
        moved = error_man("os", err_msg, fpath, fpath_in_trash)

    except Exception as err_msg:
        moved = error_man("", err_msg, fpath, fpath_in_trash)

    if moved:
        if check_f_moved_to_trash(fpath, fpath_in_trash):
            OK(CBBLUE + "%s" % fpath + CBASE + " moved to trash" + CBASE)
        else:
            print("an issue occurred when moving file " + CBBLUE + "%s" % fpath + CBASE + " to trash\n\tplease check the integrity of this file")


def check_f_moved_to_trash(fpath, fpath_in_trash):
    if os.path.exists(fpath) or not os.path.exists(fpath_in_trash):
        if os.path.exists(fpath):
            WARNING(CBBLUE + "%s" % fpath + CBASE + " still exists")
        if not os.path.exists(fpath_in_trash):
            WARNING(CBBLUE + "%s" % fpath_in_trash + CBASE + " not in trash")
        return False
    return True


def get_fowner(fpath):
    return getpwuid(stat(fpath).st_uid).pw_name


def main():
    input_fpaths = sys.argv[1:]
    check_help_request(input_fpaths)
    fpaths = get_abs_path(input_fpaths)

    for fpath in fpaths:

        if not path_exists(fpath):
            WARNING(CBBLUE + " %s " % fpath + CBASE + "doesn't exists")
            skipped()
            continue

        trashf(fpath)


if __name__ == "__main__":
    main()
