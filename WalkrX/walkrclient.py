import requests

BASE_URL = 'https://universe.walkrgame.com/api/v1'


class APIError(Exception):
   def __init__(self, status_code):
      super().__init__(self)
      self.status_code = status_code
      self.message = 'Request failed with status code {}'.format(status_code)


class WalkrClient:
   def __init__(self, auth_token, client_version, platform, timezone=8, locale='en'):
      """
      Model of Walkr client
      :param auth_token: authorization token
      :param client_version: client version
      :param platform: client platform, can be 'android' or 'ios'
      :param timezone: timezone
      :param locale: locale
      """
      self.headers = {
         'content-type': 'application/json',
         'accept-encoding': 'gzip',
         'user-agent': 'UnityWeb/1.0 (Unity 5.5.1p4; Android OS 7.1.1 / API-25 (N6F26R/3582520))',
         'connection': 'close',
         'host': 'universe.walkrgame.com'
      }
      self.auth_token = auth_token
      self.version = client_version
      self.platform = platform
      self.tz = timezone
      self.locale = locale
      self.session = requests.Session()

   def fetch(self, url, payload, method='GET'):
      """
      base method to talk to server
      :param url: api url
      :param payload: data
      :return: server json response in a dict
      :raise APIError:
      """
      payload['auth_token'] = self.auth_token
      payload['client_version'] = self.version
      payload['platform'] = self.platform
      payload['timezone'] = self.tz
      payload['locale'] = self.locale
      result = self.session.request(method=method, url=url, data=payload, headers=self.headers)

      if result.status_code == 200:
         return result.json()
      else:
         raise APIError(result.status_code)

   def fetch_now(self, system_time):
      """
      get server time and time range
      :param system_time: current system timestamp
      :return: dict containing server time
      """
      url = BASE_URL + '/now'
      payload = {'system_time': system_time}
      return self.fetch(url, payload)

   def fetch_shops(self):
      """
      get items in shop
      :return: dict containing list of items in shop
      """
      url = BASE_URL + '/shops'
      payload = {}
      return self.fetch(url, payload)

   def fetch_epics(self):
      """
      get list of epics
      :return: dict containing list of epics
      """
      url = BASE_URL + '/epics'
      payload = {}
      return self.fetch(url, payload)

   def update_games(self, data):
      """
      upload game status to server
      :param data: 
      :returns: dict indicating success or not
      """
      url = BASE_URL + '\games'
      payload = {'data': data}
      return self.fetch(url, payload, 'POST')

   def fetch_friends_count(self):
      """
      get count of friends
      :return: dict with friends count
      """
      url = BASE_URL + '/users/friends_count'
      payload = {}
      return self.fetch(url, payload)

   def fetch_current_fleet(self):
      """
      get information about current fleet
      :return: dict containing information about current fleet
      """
      url = BASE_URL + '/fleets/current'
      payload = {}
      return self.fetch(url, payload)

   def fetch_fleet_comments(self, fleet_id, offset=0, limit=30):
      """
      get comments of current fleet
      :param fleet_id: id of current fleet, available in current fleet info
      :param offset: offset, default is 0
      :param limit: limit, default is 30
      :return: dict containing list of comments
      """
      url = BASE_URL + '/fleets/{}/comments'.format(fleet_id)
      payload = {
         'offset': offset,
         'limit': limit
      }
      return self.fetch(url, payload)

   def fetch_bridge(self):
      """
      get bridge information
      :return: pilots information in your bridge
      """
      url = BASE_URL + '/pilots'
      payload = {}
      return self.fetch(url, payload)

   def check_energy(self, pilot_id):
      """
      harvest converted energy by friends on bridge
      :param pilot_id: 
      :return: amount of energy checked 
      """
      url = BASE_URL + '/pilots/{}/check'.format(pilot_id)
      payload = {}
      return self.fetch(url, payload, 'POST')

   def fetch_friends(self, order_by='population', offset=0, limit=100):
      """
      get list of friends
      :param order_by: 
      :param offset: 
      :param limit: 
      :return: 
      """
      url = BASE_URL + '/users/friends'
      payload = {
         'order_by': order_by,
         'offset': offset,
         'limit': limit
      }
      return self.fetch(url, payload)

   def fetch_friend_invitations(self):
      """
      get friend invitations
      :return: dict containing list of friend invites
      """
      url = BASE_URL + '/users/friend_invitations'
      payload = {}
      return self.fetch(url, payload)

   def fetch_new_friends_count(self):
      """
      get count of new friends
      :return: dict containing new friends count 
      """
      url = BASE_URL + '/users/new_friends_count'
      payload = {}
      return self.fetch(url, payload)

   def fetch_booster(self):
      """
      get booster status
      :return: booster status 
      """
      url = BASE_URL + '/boosts'
      payload = {}
      return self.fetch(url, payload)

   def start_booster(self):
      """
      start booster
      :return: booster status
      """
      url = BASE_URL + '/boosts'
      payload = {}
      return self.fetch(url, payload, 'POST')

   def update_booster_information(self, booster_id, data):
      """
      upload motion data to server during booster on
      :param booster_id: 
      :param data: 
      :return: success or not
      """
      url = BASE_URL + '/boosts/{}'.format(booster_id)
      payload = {'data': data}
      return self.fetch(url, payload, 'PUT')

   def convert_energy(self, converted_energy):
      """
      convert energy for co-pilots
      :param converted_energy: amount of energy converted
      :return: 
      """
      url = BASE_URL + '/pilots/convert'
      payload = {'converted_energy': converted_energy}
      return self.fetch(url, payload, 'POST')

   def fetch_pedometer_settings(self, brand, device_model, os_version):
      """
      get pedometer settings
      :param brand: 
      :param device_model: 
      :param os_version: API level for android, iOS version for iOS
      :return: pedometer settings
      """
      url = BASE_URL + '/pedometer_settings'
      payload = {
         'brand': brand,
         'device_model': device_model,
         'os_version': os_version
      }
      return self.fetch(url, payload)

   def check_reward(self, fleet_id):
      """
      claim epic rewards
      :param fleet_id: 
      :return: epic rewards
      """
      url = BASE_URL + '/fleets/{}/check_reward'.format(fleet_id)
      payload = {}
      return self.fetch(url, payload, 'POST')

   def donate_energy(self, fleet_id, hitpoints, event_id, energy):
      """
      donate energy for fleet
      :param fleet_id: fleet id
      :param hitpoints: stamina points consumed
      :param event_id: event id
      :param energy: amount of energy to donate
      :return: donate amount and hitpoint information
      """
      url = BASE_URL + '/fleets/{}/donate'.format(fleet_id)
      payload = {
         'event_status': 'path',
         'event_type': 'traveling',
         'event_id': event_id,
         'hitpoints': hitpoints,
         'energy': energy
      }
      return self.fetch(url, payload, 'POST')

   def donate_resources(self, fleet_id, hitpoints, event_id, value_a=0, value_b=0, value_c=0):
      """
      donate resources for fleet
      :param fleet_id: fleet id
      :param hitpoints: stamina points consumed
      :param event_id: event id
      :param value_a: value of resource a or coins
      :param value_b: value of resource b or food
      :param value_c: value of resource c
      :return: donate amount and hitpoint information
      """
      url = BASE_URL + '/fleets/{}/donate'.format(fleet_id)
      payload = {
         'event_status': 'event',
         'event_type': 'currency',
         'event_id': event_id,
         'hitpoints': hitpoints,
         'value_a': value_a,
         'value_b': value_b,
         'value_c': value_c
      }
      return self.fetch(url, payload, 'POST')

   def fetch_invite_list(self, epic_id, offset=0, limit=100):
      """
      fetch list of friends to invite to an epic
      :param epic_id: 
      :param offset: 
      :param limit: 
      :return: dict containing list of friends and invite status
      """
      url = BASE_URL + '/fleets/invite_list'
      payload = {
         'epic_id': epic_id,
         'offset': offset,
         'limit': limit
      }
      return self.fetch(url, payload)

   def check_friend(self, user_id):
      """
      check if the user is friend
      :param user_id: 
      :return: is friend or not
      """
      url = BASE_URL + '/users/check_friend'
      payload = {'user_id': user_id}
      return self.fetch(url, payload)

   def fetch_fleet_badges(self):
      """
      get list of fleet avatars
      :return: dict containing list of fleet avatars
      """
      url = BASE_URL + '/fleets/badges'
      payload = {}
      return self.fetch(url, payload)

   def fetch_fleet_list(self, epic_id, country_code='US', offset=0, limit=30):
      """
      get list of fleets under an epic
      :param epic_id: 
      :param country_code: 
      :param offset: 
      :param limit: 
      :return: dict containing list of fleets
      """
      url = BASE_URL + '/fleets'
      payload = {
         'epic_id': epic_id,
         'country_code': country_code,
         'offset': offset,
         'limit': limit
      }
      return self.fetch(url, payload)

   def create_fleet(self, members, badge_front, badge_back, name, epic_id, privacy='public', is_invitable=False):
      """
      create a fleet
      :param members: array of user_id of users to be invited
      :param badge_front: number of front badge
      :param badge_back: number of back badge
      :param name: fleet name
      :param epic_id: 
      :param privacy: 'public' or 'private'
      :param is_invitable: boolean, if allow invitation of members 
      :return: success or not
      """
      url = BASE_URL + '/fleets'
      members_string = '0, ' + ', '.join(members)
      payload = {
         'epic_id': epic_id,
         'members': members_string,
         'badge_front': badge_front,
         'badge_back': badge_back,
         'privacy': privacy,
         'is_invitable': is_invitable
      }
      return self.fetch(url, payload, 'POST')