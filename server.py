#! /usr/bin/env python
# -*- coding: utf-8 -*-

import sys
sys.path.append('lib')

from bottle import route, run, template, request, redirect
from backlog import Backlog
import os
from db import Db
base_path = os.path.abspath(os.path.dirname(__file__))
db_path =  base_path + "/db";
print base_path

def createBacklog():
  d = Db(base_path + "/config", "config.json");
  data = d.load()
  bl = data["backlog"]
  return Backlog(bl["space"], bl["user_id"], bl["password"])

@route("/")
def index():
  redirect("/new")

@route('/new')
def new():
  b = createBacklog()
  projects = b.get_projects()
  return template('view/new.html', projects=projects)

@route('/create', method='POST')
def create():
  p = request.params
  b = createBacklog()
  issue = b.create_issue(p.project, "Merge Request into " + p.target_branch + " from " + p.branch, p.comment)
  db = Db(db_path, "requests.db")
  data = db.load("[]")
  data.append({"pid": p.project, "repo": p.repo, "branch": p.branch, "target_branch": p.target_branch, "issue": issue})
  db.save(data)
  redirect("/new")

# initialize
if not os.path.exists(db_path):
  os.mkdir(db_path)

run(host='0.0.0.0', port=8080)
