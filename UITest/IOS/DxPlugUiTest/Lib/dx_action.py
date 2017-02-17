# -*- coding: utf-8 -*-

from appium.webdriver.connectiontype import ConnectionType

__author__ = 'liaoben'

def change_network(driver,state):
    state_dict = {
        'wifi':ConnectionType.WIFI_ONLY,
        'data':ConnectionType.DATA_ONLY,
        'airplane':ConnectionType.AIRPLANE_MODE,
        'none':ConnectionType.NO_CONNECTION,
        'all':ConnectionType.ALL_NETWORK_ON
    }
    if not state_dict.has_key(state):
        print 'Wrong state'
        return False
    try:
        driver.set_network_connection(state_dict[state])
        return True
    except Exception,e:
        print 'Exception',e
        return False

if __name__ == '__main__':
    pass