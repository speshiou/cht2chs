# coding=utf-8
import os, sys

ROOT_DIR = os.path.dirname(os.path.abspath(__file__))
sys.path.append(os.path.join(ROOT_DIR, "pylib"))

import opencc # pylint: disable=import-error
converter = opencc.OpenCC('tw2sp.json')

def cht_to_chs(src):
    return converter.convert(src)