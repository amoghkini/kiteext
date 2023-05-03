"""
    kite_alerts.py

    API wrapper for Kite alerts REST APIs.
    :license: MIT.
    :author: algo.trade.n.alerts
    :webpage: https://gitlab.com/algo.trade.n.alerts  
    
"""

import urllib.parse
import json
import kiteconnect.exceptions as ex
import logging
from six.moves.urllib.parse import urljoin
import requests
from os import path
from enum import Enum
from typing import Literal

from kiteconnect import KiteConnect, KiteTicker

log = logging.getLogger(__name__)

class AlertAttributes(Enum):
    """
        Enum of rules allowed in Kite(Zerodha) alert creation
    """

    LAST_TRADED_PRICE           = 'LastTradedPrice'
    HIGH_PRICE                  = 'HighPrice'
    LOW_PRICE                   = 'LowPrice'
    OPEN_PRICE                  = 'OpenPrice'
    CLOSE_PRICE                 = 'ClosePrice'
    DAY_CHANGE                  = 'DayChange'
    DAY_CHANGE_PERCENT          = 'DayChangePercent'
    INTRA_DAY_CHNAGE            = 'IntraDayChange'
    INTRA_DAY_CHNAGE_PERCENT    = 'IntraDayChangePercent'
    LAST_TRADED_QUANTITY        = 'LastTradedQuantity'
    AVERAGE_TRADE_PRICE         = 'AverageTradePrice'
    VOLUME_TRADED               = 'VolumeTraded'
    TOTAL_BUY_QUANTITY          = 'TotalBuyQuantity'
    TOTAL_SELL_QUANTITY         = 'TotalSellQuantity'
    OPEN_INTEREST               = 'OpenInterest'
    OPEN_INTEREST_DAY_HIGH      = 'OpenInterestDayHigh'
    OPEN_INTEREST_DAY_LOW       = 'OpenInterestDayLow'

class Operations(Enum):

    """
        Enum of operators allowed in alert creation
    """
    GREATHER_THAN               = '>'
    GREATHER_THAN_OR_EQUAL_TO   = '>='
    LESS_THAN                   = '<'
    LESS_THAN_OR_EQUAL_TO       = '<='
    EQUAL_TO                    = '=='


class AlertManagement:

    """
    Wrapper for Kite Alerts API

    For Eaxmple:
        z = KiteExt()

        z.login_using_enctoken(userid= '', public_token='', enctoken='' )

        # z.login_with_credentials(userid='',password='',pin=))
        am = AlertManagement(kwc=z)
    """

    def __init__(self, kwc: KiteConnect) -> None:
        '''
         - `kwc` intialized KiteConnect object reference
        '''
        self. url = "https://kite.zerodha.com/oms/alerts"
        self.headers = {
            'Authorization': f'enctoken {kwc.enctoken}',
            'Content-Type': 'application/x-www-form-urlencoded'
        }
        self.reqsession = requests.session()
    

    def _create_alert(self, payload: any = None) -> json:
        response = self.reqsession.post(
            self.url, headers=self.headers, data=payload)
        return response.json()

    def create_alert_on_value(
        self,
        name: str, 
        lhs_exchange: Literal['NSE','BSE','MCX','NFO','BFO','BCD','CDS'],
        lhs_tradingsymbol: str,
        lhs_attribute: AlertAttributes,
        operator: Operations,
        rhs_constant: float) -> json:
        """
            For Example:

                response = am.create_alert_on_value(
                                name=  'API-Price-Below',
                                lhs_exchange='NSE',
                                lhs_tradingsymbol='MCX',
                                lhs_attribute=AlertAttributes.LAST_TRADED_PRICE,
                                operator=Operations.LESS_THAN,
                                rhs_constant=1440.85
                            )
        """
        payload = {
            'name': name, 
            'lhs_exchange': lhs_exchange, 
            'lhs_tradingsymbol': lhs_tradingsymbol,
            'lhs_attribute': lhs_attribute.value, 
            'operator': operator.value, 
            'rhs_type': 'constant', 
            'rhs_constant': rhs_constant
            }

        print(payload)

        return self._create_alert(payload=payload)

    
    def create_alert_on_instrument(
        self,
        name: str, 
        lhs_exchange: Literal['NSE','BSE','MCX','NFO','BFO','BCD','CDS'],
        lhs_tradingsymbol: str,
        lhs_attribute: AlertAttributes,
        operator: Operations,
        rhs_exchange: Literal['NSE','BSE','MCX','NFO','BFO','BCD','CDS'],
        rhs_tradingsymbol: str,
        rhs_attribute: AlertAttributes) -> json:
        """
            For Example:

                response = am.create_alert_on_instrument(
                                name=  'API-Price-Below',
                                lhs_exchange='BSE',
                                lhs_tradingsymbol='NIFTYBEES',
                                lhs_attribute=AlertAttributes.LAST_TRADED_PRICE,
                                operator=Operations.LESS_THAN,
                                rhs_exchange: 'NSE',
                                rhs_tradingsymbol: 'NIFTYQLITY',
                                rhs_attribute: AlertAttributes.LAST_TRADED_PRICE
                            )
        """
        payload = {
            'name': name, 
            'lhs_exchange': lhs_exchange, 
            'lhs_tradingsymbol': lhs_tradingsymbol,
            'lhs_attribute': lhs_attribute.value, 
            'operator': operator.value, 
            'rhs_type': 'instrument', 
            'rhs_exchange': rhs_exchange,
            'rhs_tradingsymbol': rhs_tradingsymbol.value,
            'rhs_attribute': rhs_attribute.value
            }

        return self._create_alert(payload=payload)

    def get_alerts(self) -> json:
        response = self.reqsession.get(self.url, headers=self.headers)
        return response.json()


    def enable_alert(self, uuid: str) -> json:
        """
            Example:
                print(am.enable_alert(response['data']['uuid']))
        """

        payload = {'status': 'enabled'}
        response = self.reqsession.get(
            self.url+f'/{uuid}', data=payload, headers=self.headers)
        return response.json()


    def disable_alert(self, uuid: str) -> json:
        """
            Example:
                print(am.disable_alert(response['data']['uuid']))
        """
        payload = {'status': 'disabled'}
        response = self.reqsession.get(
            self.url+f'/{uuid}', data=payload, headers=self.headers)

        return response.json()

    
    def modify_alerts(self,uuid:str, payload: json) -> json:
        """
            Get Hold of alert you want to modify along with UUID. UUID is present in response of alert creation.
        """
        
        response = self.reqsession.get(
            self.url+f'/{uuid}', data=payload, headers=self.headers)

        return response.json()
    

    def delete_alerts(self, uuids: list) -> json:
        '''
    
            Example:
            uuids = [alert['uuid'] for alert in am.get_alerts()['data']]
            print(am.delete_alerts(uuids=uuids))
        '''
        uuids_str = '&'.join(f'uuid={uuid}' for uuid in uuids)
        print(uuids_str)
        response = self.reqsession.delete(
            self.url, headers=self.headers, params=uuids_str)

        return response.json()
