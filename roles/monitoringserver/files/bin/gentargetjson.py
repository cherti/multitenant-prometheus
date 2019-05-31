#!/usr/bin/env python3

import sys, subprocess, yaml, os, shutil, getpass, json
os.chdir(os.path.expanduser("~/scrapetargets"))

fname = input("file-basename: ") + '.json'
if os.path.exists(fname):
    print("file exists, will not do anything", file=sys.stderr)
    exit(1)

all_targets = []

def read_label():
    lname = input("if an additional label shall be added to metrics of the provided host(s), provide its name: ")
    lname.replace(" ", "_")
    if lname != "":
        lvalue = input("Provide label value for {}".format(lname))
        return lname, lvalue
    else:
        return None, None

def new_targetset():
    targetset = {'targets': [], 'labels': {}}

    targetset['labels']['__scheme__'] = input("http or https? [https]") or "https"

    commaseptargets = input("targets (comma-separated list of URL:port)")
    targetset['targets'] = [t.strip() for t in commaseptargets.split(",")]


    lname, lvalue = read_label()
    while lname:
        targetset['labels'][lname] = lvalue
        lname, lvalue = read_label()

    return targetset

choice = "y"
while choice in ["y", "Y"]:
    all_targets.append(new_targetset())
    choice = input("add another target in this file? [y/N]")

json.dump(all_targets, open(fname, "w"), indent="  ")
