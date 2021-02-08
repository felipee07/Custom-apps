import asyncio
import requests
import base64

from walkoff_app_sdk.app_base import AppBase


class Alienvault(AppBase):
    __version__ = "1.0.0"
    app_name = "alienvault"

    def __init__(self, redis, logger, console_logger=None):
        print("INIT")
        """
        Each app should have this __init__ to set up Redis and logging.
        :param redis:
        :param logger:
        :param console_logger:
        """
        super().__init__(redis, logger, console_logger)

    def get_token(self, url, apiuser, apikey) -> dict:
        # HTTPS only.
        if "http://" in url:
            url = url.replace("http://", "")
        else:
            url = url.replace("https://", "")
        bear = base64.b64encode(f"{apiuser}:{apikey}".encode()).decode()
        headers = {'Authorization': f'Basic {bear}'}
        r = requests.post(f'https://{url}/api/2.0/oauth/token?grant_type=client_credentials', headers=headers)
        if r.status_code != 200:
            raise RuntimeError('Authentication failed. Check username/Password')
        else:
            return {f"Authorization": f"Bearer {r.json()['access_token']}"}

    async def get_alarms(self, url, apiuser, apikey, params=None) -> str:
        """Pull alarms from the AlienVault API."""
        headers = self.get_token(url, apiuser, apikey)
        r = requests.get(f"https://{url}/api/2.0/alarms/?{params}", headers=headers)
        if r.status_code != 200:
            raise RuntimeError('Alienvault API return an error')
        else:
            return r.text

    async def get_alarmid(self, url, apiuser, apikey, alarm_id) -> str:
        """Pull a specific alarm from the AlienVault API."""
        headers = self.get_token(url, apiuser, apikey)
        r = requests.get(f"https://{url}/api/2.0/alarms/{alarm_id}", headers=headers)
        if r.status_code != 200:
            raise RuntimeError('Alienvault API return an error')
        else:
            return r.text

    async def get_label(self, url, apiuser, apikey, alarm_id) -> str:
        """Get labels from an alarm."""
        headers = self.get_token(url, apiuser, apikey)
        r = requests.get(f"https://{url}/api/2.0/alarms/{alarm_id}/labels", headers=headers)
        if r.status_code != 200:
            return "{'alarm_labels': []}"
        else:
            return r.text

    async def put_label(self, url, apiuser, apikey, alarm_id, label_id) -> int:
        """Put labels on an alarm using the AlienVault API."""
        headers = self.get_token(url, apiuser, apikey)
        r = requests.put(f"https://{url}/api/2.0/alarms/{alarm_id}/labels/{label_id}", headers=headers)
        if r.status_code != 200:
            raise RuntimeError('Alienvault API return an error')
        else:
            return r.status_code

    async def delete_label(self, url, apiuser, apikey, alarm_id, label_id) -> int:
        """Delete labels from an alarm using the AlienVault API."""
        headers = self.get_token(url, apiuser, apikey)
        r = requests.delete(f"https://{url}/api/2.0/alarms/{alarm_id}/labels/{label_id}", headers=headers)
        if r.status_code != 204:
            raise RuntimeError('Alienvault API return an error')
        else:
            return r.status_code

    async def get_events(self, url, apiuser, apikey, params=None) -> str:
        """Pull events from the AlienVault API."""
        headers = self.get_token(url, apiuser, apikey)
        r = requests.get(f"https://{url}/api/2.0/events/?{params}", headers=headers)
        if r.status_code != 200:
            raise RuntimeError('Alienvault API return an error')
        else:
            return r.text

    async def get_eventid(self, url, apiuser, apikey, eventid) -> str:
        """Pull a specific event from the AlienVault API."""
        headers = self.get_token(url, apiuser, apikey)
        r = requests.get(f"https://{url}/api/2.0/events/{eventid}", headers=headers)
        if r.status_code != 200:
            raise RuntimeError('Alienvault API return an error')
        else:
            return r.text


if __name__ == "__main__":
    asyncio.run(Alienvault.run(), debug=True)

