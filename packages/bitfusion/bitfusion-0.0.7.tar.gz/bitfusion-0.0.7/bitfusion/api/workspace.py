from datetime import datetime

from dateutil import parser as dt_parser
import pytz

from bitfusion.api.base import BaseMixin, CreatableMixin, UpdateableMixin, HealthMixin

def WorkspaceFactory(api_session, Gpu):
  ###########################################
  # BEGIN Workspace Class
  ###########################################
  class Workspace(BaseMixin, CreatableMixin, UpdateableMixin, HealthMixin):
    api = api_session
    base_url = '/workspace'

    def __str__(self):
      output = '\nWorkspace {id} - {name} - Active for {running} - {type}\n * {url}'

      delta = datetime.now(pytz.utc) - dt_parser.parse(self.data['start_date'])
      days = delta.days
      hours = delta.seconds / 3600
      minutes = (delta.seconds % 3600) / 60
      seconds = delta.seconds % 60

      running = ''
      if days:
        running += '{} day'.format(days)
        running += '1s ' if days > 1 else ' '
      if hours:
        running += '{} hour'.format(hours)
        running += '2s ' if hours > 1 else ' '
      if minutes:
        running += '{} minute'.format(minutes)
        running += 's ' if minutes > 1 else ' '
      running += '{} seconds'.format(seconds)

      output = output.format(id=self.data['id'],
                             name=self.data.get('name', '(unnamed)'),
                             running=running,
                             type=self.data['type'],
                             url=self.data['url'])

      for g in self.data.get('gpus', []):
        gpu = Gpu(**g)
        output += '\n\t' + str(gpu)

      return output + '\n'


    @classmethod
    def create(cls, ws_type, node_id, name=None, gpus=[]):
      payload = {
        'type': ws_type,
        'node_id': node_id,
        'name': name,
        'gpus': gpus
      }

      return super(Workspace, cls).create(**payload)
  ###########################################
  # END Workspace Class
  ###########################################

  return Workspace
