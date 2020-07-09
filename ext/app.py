from config_file import config, mapping_config
from log_config import LogConfig
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


def can_send_data_out(message):
    msg_dict = eval(message)
    imei = msg_dict['imei_no']
    return imei in mapping_config.values()


def send_data_to_ws(message):
    log.info('Sending data to API.')
    resp = requests.post(WS_URL, data=message)
    log.info('response from API: {}'.format(resp.text))


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
            send_data_to_ws(message)

    def on_disconnected(self):
        log.warning('MQ disconnected')
        conn.connect(MQ_USER, MQ_PASS, wait=True)
        conn.subscribe(destination=MQ_DEST, id=1, ack='auto')


conn = stomp.Connection(host_and_ports=HOST_AND_PORTS,
                        heartbeats=(4000, 4000))
conn.set_listener('SampleListener', SampleListener(conn))
conn.connect(MQ_USER, MQ_PASS, wait=True)
conn.subscribe(destination=MQ_DEST, id=1, ack='auto')
time.sleep(60)
conn.disconnect()
