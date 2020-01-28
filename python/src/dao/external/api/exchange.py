import json
from common.base_dao.base import DAO
from requests import Session
from requests.packages.urllib3.util.retry import Retry
from requests.adapters import HTTPAdapter
from requests.models import Response

class ExchangeDAO(object):
    def __init__(self, version="v4", currency="BRL", result='rates', **kwargs):
        self.response_data = result
        self.sleep = kwargs.get('sleep')
        self.retries = kwargs.get('retries')
        self.timeout = kwargs.get('timeout')
        self.backoff_factor = kwargs.get('backoff_factor')
        
        self.endpoint = 'https://api.exchangerate-api.com/%s/latest/%s' % (version, currency)
        self.session = ExchangeDAO.__requestSetup(self.retries, self.sleep)
    
    def __transform(self, data):
        data = {key: 1/value for key, value in json.loads(data.text)[self.response_data].items()}
        data.update({'USD': 3.81})
        return data
    
    @staticmethod
    def __requestSetup(retries, sleep):
        session = Session()
        retry = Retry(total=retries, read=retries, backoff_factor=sleep)
        adapter = HTTPAdapter(max_retries=retry)
        session.headers = {'Content-type': 'application/json'}
        session.mount('http://', adapter)
        return session

    def collect(self):
        """Carrega os valores atuais de cada moeda, aplicando as 
        transformacoes necessarias para disponibilizacao dos dados"""
        try:
            request = ExchangeDAO.__requestSetup(retries=self.retries, sleep=self.sleep)
            data = request.get(self.endpoint, timeout=self.timeout)
            return self.__transform(data)
        except Exception as err:
            """TODO"""
            raise Exception