import os

import requests

from bitfusion import api
from bitfusion.lib.session import ApiSession

class BFApi():
  def __init__(self, host='http://localhost:5000', api_base_url='/api',
               auth=None, timeout=5, cookies=None, username=None, password=None):

    self._session = ApiSession(host, auth, timeout)

    # Set the API data controllers
    self.Gpu = api.GpuFactory(self._session)
    self.Node = api.NodeFactory(self._session, self.Gpu)
    self.Volume = api.VolumeFactory(self._session)
    self.Workspace = api.WorkspaceFactory(self._session, self.Gpu)

    if api_base_url:
      self.set_api_base_url(api_base_url)

    if cookies:
      self.set_cookies(cookies)
    elif username and password:
      self.login(username, password)


  def login(self, username, password):
    payload = {
      'email': username,
      'password': password
    }

    self._session.post('/auth/login', payload)
    return self._session.cookies.get_dict()


  def set_api_base_url(self, base_path):
    self.Node.base_url = os.path.join(base_path, 'node')
    self.Volume.base_url = os.path.join(base_path, 'volume')
    self.Workspace.base_url = os.path.join(base_path, 'workspace')

  def set_auth(self, auth):
    self._session.auth = auth


  def set_cookies(self, cookies):
    self._session.cookies = requests.cookies.cookiejar_from_dict(cookies)
