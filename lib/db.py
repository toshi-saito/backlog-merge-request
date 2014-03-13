# -*- coding: utf-8 -*-
import json
import os

class Db:
  def __init__(self, path, file):
    self.f = path+"/"+file
  def load(self, defval = "{}"):
    data = ""
    if os.path.exists(self.f):
      f = open(self.f, "r")
      for line in f:
        data += line
      f.close()
    else:
      data = defval
    return json.loads(data)
  def save(self, data):
    f = open(self.f, "w")
    f.write(json.dumps(data))
    f.close()

