"""
Main module for the Huawei modem E3372 wrapper
"""
from datetime import datetime
from dataclasses import dataclass
import requests
from xmltodict3 import XmlTextToDict
import xml.etree.cElementTree as ET

SESSION_PATH = 'api/webserver/SesTokInfo'
SMS_LIST_PATH = 'api/sms/sms-list'
SMS_DELETE_PATH = 'api/sms/delete-sms'
SMS_COUNT_PATH = 'api/sms/sms-count'
SMS_READ_PATH = 'api/sms/set-read'


@dataclass()
class SMSMessage:
    index: int
    phone_number: str
    content: str
    sms_date: datetime


def parse_to_xml(content):
    return ET.fromstring(content.decode('utf-8'))


def parse_sms_list(content):
    sms_list = []
    root = parse_to_xml(content)
    message_list = root.findall('*/Message')
    for message in message_list:
        sms = SMSMessage(index=message.find('Index').text,
                         content=message.find('Content').text,
                         phone_number=message.find('Phone').text,
                         sms_date=datetime.strptime(message.find('Date').text,
                                                    '%Y-%m-%d %H:%M:%S'))
        sms_list.append(sms)

    return sms_list


def parse_result_from_response(response):
    xml_as_dict = XmlTextToDict(response, ignore_namespace=True).get_dict()
    if 'response' in xml_as_dict:
        if xml_as_dict['response'] == "OK":
            return True
    return False;


class ModemConnector(object):
    """
    Connector for modem, serving all methods
    """

    def set_session_vars(self) -> None:
        """
        Set session and token obtained from a server
        """
        xml = requests.get(self.modem_url + SESSION_PATH).text
        xml_as_dict = XmlTextToDict(xml, ignore_namespace=True).get_dict()
        self._session = xml_as_dict['response']['SesInfo']
        self._token = xml_as_dict['response']['TokInfo']

    def __init__(self, modem_url="http://192.168.8.1/"):
        self.modem_url = modem_url
        self._session = ''
        self._token = ''
        self.sms_list = []

    def _headers(self):
        self.set_session_vars()
        return {'Cookie': self._session,
                "__RequestVerificationToken": self._token,
                "X-Requested-With": "XMLHttpRequest",
                "Content-Type": "application/x-www-form-urlencoded; charset=UTF-8"}

    def get_sms_list(self, read_count=20):
        xml = """
            <?xml version="1.0" encoding="UTF-8"?>
            <request><PageIndex>1</PageIndex>
            <ReadCount>{}</ReadCount>
            <BoxType>1</BoxType>
            <SortType>0</SortType>
            <Ascending>0</Ascending>
            <UnreadPreferred>0</UnreadPreferred>
            </request>""".format(
            read_count
        )
        response = requests.post(self.modem_url + SMS_LIST_PATH, data=xml, headers=self._headers())
        return parse_sms_list(response.content)

    def sms_count_unread(self, inbox_type="local"):
        xml = requests.get(self.modem_url + SMS_COUNT_PATH, headers=self._headers()).text
        dictResponse = XmlTextToDict(xml, ignore_namespace=True).get_dict()
        if inbox_type == "sim":
            return dictResponse["response"]["SimUnread"]
        if inbox_type == "local":
            return dictResponse["response"]["LocalUnread"]
        return None

    def sms_delete(self, index):
        xml = """
            <?xml version="1.0" encoding="UTF-8"?>
            <request>
            <Index>{}</Index>
            </request>""".format(
            index
        )

        response = requests.post(self.modem_url + SMS_DELETE_PATH, data=xml, headers=self._headers())
        return parse_result_from_response(response.text)

    def sms_set_read(self, index):
        xml = """
               <?xml version="1.0" encoding="UTF-8"?>
               <request>
               <Index>{}</Index>
               </request>""".format(
            index
        )
        response = requests.post(self.modem_url + SMS_READ_PATH, data=xml, headers=self._headers())
        return parse_result_from_response(response.text)
