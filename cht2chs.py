# coding=utf-8
import os, sys, getopt
from pathlib import Path
import cht2chs_flutter as cc_flutter
import cht2chs_android as cc_android
import cht2chs_ios as cc_ios


# TBD
def print_help():
    print("")

if __name__ == '__main__':
    argv = sys.argv[1:]
    try:
        opts, args = getopt.getopt(argv,"hd:",["help", "dir="])
    except getopt.GetoptError:
        print_help()
        sys.exit(2)
    d = None
    for opt, arg in opts:
        if opt == '-d' or opt == "--dir":
            d = arg
    if not d:
        print("Please specify working directory")
        exit(1)
    if os.path.isfile(os.path.join(d, 'pubspec.yaml')):
        print("Flutter project: %s" % (d))
        cc_flutter.cht2chs(d)
    elif os.path.isfile(os.path.join(d, 'build.gradle')):
        print("Android project: %s" % (d))
        cc_android.cht2chs(d)
    elif os.path.isfile(os.path.join(d, 'Podfile')):
        print("iOS project: %s" % (d))
        cc_ios.cht2chs(d)