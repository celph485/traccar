from datetime import datetime
from datetime import timedelta
from config_file import config, mapping_config
from log_config import LogConfig
import json
import stomp
import time
import requests


log = LogConfig(__name__).get_logger()


log.info('Starting application {}'.format(config['APP_NAME']))
log.debug('Listing all the config variables.')
for key in config:
    log.debug('{} = {}'.format(key, config[key]))


HOST_AND_PORTS = [(config['MQ_HOST'], config['MQ_PORT'])]
MQ_USER = config['MQ_USER']
MQ_PASS = config['MQ_PASS']
MQ_DEST = config['MQ_DESTINATION']
WS_URL = config['TARGET_WS_URL']
GMT_IMEI_LIST = config['GMT_IMEI'].split(',')
DATE_TIME_FORMATE = '%Y-%m-%d %H:%M:%S'


def can_send_data_out(message):
    msg_dict = eval(message)
    imei = msg_dict['imei_no']
    return imei in mapping_config.values()


def send_data_to_ws(message):
    log.info('Sending data to API.')
    resp = requests.post(WS_URL, data=message)
    log.info('response from API: {}'.format(resp.text))


def update_datetime_str(str_dt):
    dt_obj = datetime.strptime(str_dt, '%Y-%m-%d %H:%M:%S')
    updated_dt_obj = dt_obj + timedelta(minutes=330)
    return updated_dt_obj.strftime('%Y-%m-%d %H:%M:%S')


def update_message_for_tz(message):
    log.info('Updating timezone for the message, adding +0530 Hrs')
    msg_dict = eval(message)
    datetime_str = msg_dict['time']
    updated_datetime_str = update_datetime_str(datetime_str)
    msg_dict['time'] = updated_datetime_str
    updated_message = json.dumps(msg_dict)
    log.info('Updated message: %s'% updated_message)
    return updated_message


def get_updated_message(message):
    msg_dict = eval(message)
    imei = msg_dict['imei_no']
    if imei in GMT_IMEI_LIST:
        return update_message_for_tz(message)
    return message


class SampleListener(stomp.ConnectionListener):
    def __init__(self, conn):
        self.conn = conn

    def on_error(self, header, body):
        log.error('received an error body: %s' % body)

    def on_message(self, header, message):
        log.info('received a data message: \n %s' % message)
        can_send = can_send_data_out(message)
        log.info('can send: %r' % can_send)
        if can_send:
            formatted_msg = get_updated_message(message)
            send_data_to_ws(formatted_msg)

    def on_disconnected(self):
        log.warning('MQ disconnected')

    def on_heartbeat_timeout(self):
        log.warning('Heartbeat time out')

    def on_receiver_loop_completed(self, headers, body):
        log.warning('receiver loop completed')


conn = stomp.Connection(host_and_ports=HOST_AND_PORTS,
                        heartbeats=(4000, 4000))
conn.set_listener('SampleListener', SampleListener(conn))
conn.connect(MQ_USER, MQ_PASS, wait=True)
conn.subscribe(destination=MQ_DEST, id=1, ack='auto')