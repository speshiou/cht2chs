# coding=utf-8
import os, json
from pathlib import Path
import zh_converter as zc

CHS_COUNTRY_CODES = [ "CN", "SG", "base" ]
CHT_COUNTRY_CODES = [ "TW", "HK", "MO", "base" ]

def cht2chs(root):
    if not os.path.isfile(os.path.join(root, 'pubspec.yaml')):
        print(root, "is not a flutter project")
        exit(1)
    l10n_config_filename = os.path.join(root, 'l10n.yaml')
    if not os.path.isfile(l10n_config_filename):
        print(l10n_config_filename, "not found")
        exit(1)    
    base_arb = {}
    with open(os.path.join(root, "lib/l10n/base.arb"), "r") as f:
        base_arb = json.load(f)

    for code in CHS_COUNTRY_CODES:
        suffix = "" if code == "base" else "_" + code
        filename = os.path.join(root, "lib/l10n/intl_zh_Hans%s.arb" % (suffix))
        Path(os.path.dirname(filename)).mkdir(parents=True, exist_ok=True)
        output = {
            "@@locale": "zh_Hans%s" % (suffix),
        }
        with open(filename, "w") as dest:
            for key, value in base_arb.items():
                if key.startswith("@"):
                    continue
                chs_value = zc.cht_to_chs(value)
                output[key] = chs_value
            dest.write(json.dumps(output, indent=2, sort_keys=True, ensure_ascii=False))
                    
    for code in CHT_COUNTRY_CODES:
        suffix = "" if code == "base" else "_" + code
        filename = os.path.join(root, "lib/l10n/intl_zh_Hant%s.arb" % (suffix))
        Path(os.path.dirname(filename)).mkdir(parents=True, exist_ok=True)
        output = {
            "@@locale": "zh_Hant%s" % (suffix),
        }
        with open(filename, "w") as dest:
            for key, value in base_arb.items():
                if key.startswith("@"):
                    continue
                output[key] = value
            dest.write(json.dumps(output, indent=2, sort_keys=True, ensure_ascii=False))
        
        