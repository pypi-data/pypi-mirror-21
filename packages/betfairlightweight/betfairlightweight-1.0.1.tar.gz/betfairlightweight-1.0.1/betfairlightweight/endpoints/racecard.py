import re
import datetime
from requests import ConnectionError

from ..exceptions import APIError, RaceCardError
from ..utils import check_status_code
from .baseendpoint import BaseEndpoint
from .. import resources


class RaceCard(BaseEndpoint):
    """
    RaceCard operations.
    """

    app_key = None

    def login(self, session=None):
        """
        Parses app key from betfair exchange site.

        :param requests.session session: Requests session object
        """
        session = session or self.client.session
        response = session.get(self.login_url)
        app_key = re.findall(r'''"appKey":\s"(.*?)"''', response.text)
        if app_key:
            self.app_key = app_key[0]
        else:
            raise RaceCardError("Unable to find appKey")

    def get_race_card(self, market_ids, data_entries=None, session=None):
        """
        Returns a list of race cards based on market ids provided.

        :param list market_ids: The filter to select desired markets
        :param str data_entries: Data to be returned
        :param requests.session session: Requests session object

        :rtype: list[resources.RaceCard]
        """
        if not self.app_key:
            raise RaceCardError("You need to login before requesting a race_card\n"
                                "APIClient.race_card.login()")
        params = self.create_race_card_req(market_ids, data_entries)
        date_time_sent = datetime.datetime.utcnow()
        response = self.request(params=params, session=session)
        return self.process_response(response.json(), resources.RaceCard, date_time_sent)

    def request(self, method=None, params=None, session=None):
        session = session or self.client.session
        try:
            response = session.get(self.url, params=params, headers=self.headers)
        except ConnectionError:
            raise APIError(None, method, params, 'ConnectionError')
        except Exception as e:
            raise APIError(None, method, params, e)

        check_status_code(response)
        return response

    @staticmethod
    def create_race_card_req(market_ids, data_entries):
        if not data_entries:
            data_entries = 'RACE, TIMEFORM_DATA, RUNNERS, RUNNER_DETAILS'
        return {
            'dataEntries': data_entries,
            'marketId': ','.join(market_ids)
        }

    @property
    def headers(self):
        return {
            'Connection': 'keep-alive',
            'Content-Type': 'application/json',
            'X-Application': self.app_key
        }

    @property
    def login_url(self):
        return 'https://www.betfair.com/exchange/plus/'

    @property
    def url(self):
        return 'https://www.betfair.com/rest/v2/raceCard'
