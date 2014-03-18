#! /usr/bin/env python
# -*- coding: utf-8 -*-

# cronで定期的に実行する。
# db/requests.dbを参照し、
# git cloneしdiffをBacklogにコメント。
# clone 済みのものについては、git pullを行い、
# 追加されたコミットすべてについて
# diffをbacklogにコメントする。

import sys
sys.path.append('lib')
import os
import re
import commands
from db import Db
from backlog import Backlog

base_path = os.path.abspath(os.path.dirname(__file__))
db_path =  base_path + "/db";

d = Db(base_path + "/config", "config.json");
data = d.load()
bl = data["backlog"]
backlog = Backlog(bl["space"], bl["user_id"], bl["password"])

db = Db(db_path, "requests.db")

def overwrite_row(row):
  data = db.load()
  nd = [];
  for r in data:
    if r["issue"] == row["issue"]:
      nd.append(row)
    else:
      nd.append(r)
  db.save(nd)

def remove_row(row):
  data = db.load()
  nd = [];
  for r in data:
    if r["issue"] != row["issue"]:
      nd.append(r)
  db.save(nd)

def head(path):
  head = commands.getoutput("cd %s && git log --oneline -1" % (path))
  return re.sub(r' .*$', "", head)

def kval(h, key):
  return key in h and h[key]

def writeDiffComments(path, row):
  log = commands.getoutput("cd %s && git log --oneline" % (path))
  logs = log.split("\n")
  wl = []
  for v in logs:
    v = v.decode("utf8")
    if v.startswith(row["head"]):
      break;
    wl.append(v)
  wl.reverse()
  lhash = row["head"]
  for v in wl:
    print "add comment: " + v
    h = re.sub(r' .*$', "", v)
    diff = commands.getoutput("cd %s && git diff %s %s" % (path, lhash, h))
    comment = v+"\n\n{code}\n"+diff+"\n{/code}"
    backlog.add_comment(row["issue"], comment)
    lhash = h

data = db.load()
for row in data:
  rpath = "%s/repos/%s" % (base_path, row["issue"])

  # 課題がclosedになっていたら監視をやめる
  if (backlog.is_closed(row["issue"])):
    commands.getoutput("rm -rf %s" % (rpath))
    remove_row(row)
    continue

  # cloneされていなければcloneする。
  if not kval(row, "cloned") and not kval(row, "cloning"):
    print "cloning " + row["issue"] + " ..."
    row["cloning"] = True
    overwrite_row(row)
    repo = re.sub(r'^https:\/\/', "https://%s:%s@" % (bl["user_id"], bl["password"]), row["repo"])
    commands.getoutput("git clone %s %s" % (repo, rpath))
    commands.getoutput("cd %s && git fetch" % (rpath))
    commands.getoutput("cd %s && git checkout -b %s origin/%s" % (rpath, row["branch"], row["branch"]))
    diff = commands.getoutput("cd %s && git diff %s..origin/%s" % (rpath, row["branch"], row["target_branch"]))
    comment = "{code}\n"+diff+"\n{/code}"
    backlog.add_comment(row["issue"], comment)
    row["cloning"] = False
    row["cloned"] = True
    overwrite_row(row)
    continue

  # clone済みならgit pullして差分をコメント
  if kval(row, "cloned") and not kval(row, "fetching"):
    print "fetching " + row["issue"] + " ..."
    row["fetching"] = True
    overwrite_row(row)
    row["head"] = head(rpath)
    print "current head: " + row["head"]
    overwrite_row(row)
    commands.getoutput("cd %s && git pull origin %s" % (rpath, row["branch"]))
    head = head(rpath)
    print "fetched.\ncurrent head: " + head
    if head != row["head"]:
      writeDiffComments(rpath, row)
    row["fetching"] = False
    overwrite_row(row)

