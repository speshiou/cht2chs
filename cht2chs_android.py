# -*- coding: utf-8 -*-
import os
from pathlib import Path
import zh_converter as zc

CHS_COUNTRY_CODES = [ "CN", "SG" ]
CHT_COUNTRY_CODES = [ "TW", "HK", "MO" ]

def cht2chs(root):
    for code in CHS_COUNTRY_CODES:
        filename = os.path.join(root, "app/src/main/res/values-zh-r%s/strings.xml" % (code))
        Path(os.path.dirname(filename)).mkdir(parents=True, exist_ok=True)
        with open(filename, "w") as dest:
            with open(os.path.join(root, "app/src/main/res/values/strings.xml"), "r") as f:
                for line in f:
                    chs_line = zc.cht_to_chs(line)
                    dest.write(chs_line)
                
    for code in CHT_COUNTRY_CODES:
        filename = os.path.join(root, "app/src/main/res/values-zh-r%s/strings.xml" % (code))
        Path(os.path.dirname(filename)).mkdir(parents=True, exist_ok=True)
        with open(filename, "w") as dest:
            with open(os.path.join(root, "app/src/main/res/values/strings.xml"), "r") as f:
                for line in f:
                    dest.write(line)
    print("Finish!")
        
        