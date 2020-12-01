# coding=utf-8
import os, re, fnmatch
from pathlib import Path
import zh_converter as zc

CHS_COUNTRY_CODES = [ "zh-Hans" ]
CHT_COUNTRY_CODES = [ "zh-Hant" ]

def _get_string_map(filepath):
    p = re.compile(r"\"(.*)\".*=.*\"(.*)\";")
    strings = {}
    if os.path.isfile(filepath):
        with open(filepath, "r") as f:
            for line in f:
                if not line.startswith("\""):
                    continue
                matches = p.match(line)
                if matches:
                    key = matches.group(1)
                    value = matches.group(2)
                    strings[key] = value
                    print(key)
    return strings

def _localize_res(root_path):
    localizable_cht = _get_string_map(os.path.join(root_path, "zh-Hant.lproj/Localizable.strings"))

    with open("%s/L.swift" % (root_path), "w") as dest:
            dest.write("// Generated code, do not modify manually\n\n")
            dest.write("import Foundation\n\n")
            dest.write("class L {\n\n")
            for key, value in sorted(localizable_cht.items()):
                dest.write("\tclass var %s: String {\n" % (key))
                dest.write("\t\tget {\n")
                dest.write("\t\t\treturn NSLocalizedString(\"%s\", comment: \"\")\n" % (key))
                dest.write("\t\t}\n")        
                dest.write("\t}\n\n")
            dest.write("}")
                
    for code in CHS_COUNTRY_CODES:
        locale_dir = os.path.join(root_path, "%s.lproj" % (code))
        filename = os.path.join(locale_dir, "Localizable.strings")
        Path(locale_dir).mkdir(parents=True, exist_ok=True)
        strings_chs = _get_string_map(filename)
        with open(filename, "w") as dest:
            for key, value in sorted(localizable_cht.items()):
                if key in strings_chs:
                    value = strings_chs[key]
                else:
                    value = zc.cht_to_chs(value)
                dest.write("\"%s\" = \"%s\";\n" % (key, value))
                    
    for code in CHT_COUNTRY_CODES:
        locale_dir = os.path.join(root_path, "%s.lproj" % (code))
        filename = os.path.join(locale_dir, "Localizable.strings")
        Path(locale_dir).mkdir(parents=True, exist_ok=True)
        with open(filename, "w") as dest:
            for key, value in sorted(localizable_cht.items()):
                dest.write("\"%s\" = \"%s\";\n" % (key, value))

def _localize_view(root, f):
    dirname = os.path.dirname(os.path.join(root, f))
    if os.path.basename(dirname) == "Base.lproj":
        fname = os.path.splitext(os.path.basename(os.path.join(root, f)))[0]
        cht = os.path.join(os.path.dirname(dirname), "zh-Hant.lproj", fname + ".strings")

        localizable_cht = _get_string_map(cht)        
        for code in CHS_COUNTRY_CODES:
            locale_dir = Path(dirname).parent
            filename = os.path.join(locale_dir, code + ".lproj", fname + ".strings")
            Path(locale_dir).mkdir(parents=True, exist_ok=True)
            strings_chs = _get_string_map(filename)
            with open(filename, "w") as dest:
                for key, value in sorted(localizable_cht.items()):
                    if key in strings_chs:
                        value = strings_chs[key]
                    else:
                        value = zc.cht_to_chs(value)
                    dest.write("\"%s\" = \"%s\";\n" % (key, value))

def cht2chs(root_path):
    for root, dirs, files in os.walk(root_path):
        for f in files:
            if fnmatch.fnmatch(f, "*.storyboard") or fnmatch.fnmatch(f, "*.xib"):
                _localize_view(root, f)
                pass
            elif root.endswith("zh-Hant.lproj") and fnmatch.fnmatch(f, "Localizable.strings"):
                _localize_res(Path(root).parent)