import xmlrpclib

class Backlog:
  def __init__(self, space, user_id, password):
    url = "https://%s:%s@%s.backlog.jp/XML-RPC" % (user_id, password, space)
    self.proxy = xmlrpclib.ServerProxy(url)

  def get_projects(self):
    projects = self.proxy.backlog.getProjects()
    ps = {}
    for p in projects:
      ps[p["key"]] = p["id"]
    return ps

  def create_issue(self, project_id, title, comment):
    res = self.proxy.backlog.createIssue({"projectId":project_id, "summary":title, "description": comment})
    return res["key"]

  def add_comment(self, key, comment):
    self.proxy.backlog.addComment({"key":key, "content": comment})

  def is_closed(self, key):
    res = self.proxy.backlog.getIssue(key)
    return res["status"]["id"] == 4
