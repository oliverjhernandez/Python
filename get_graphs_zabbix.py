#!/usr/bin/env python
# coding: utf-8


from os import listdir
from ConfigParser import ConfigParser
from os.path import expanduser
from socket import getfqdn
from cookielib import CookieJar
from datetime import datetime, timedelta
from email import Encoders
from email.MIMEBase import MIMEBase
from email.MIMEMultipart import MIMEMultipart
from email.MIMEText import MIMEText
from email.Utils import formatdate
from urllib import urlencode
from urllib2 import build_opener, HTTPCookieProcessor
# from zabbix_common import Configuration
import pycurl
import StringIO
import smtplib

# either edit these values or provide a config file which will overwrite the values below
ZABBIX_FRONTEND_URL = u'https://172.28.1.29/zabbix'
ZABBIX_USERNAME = 'Admin'
ZABBIX_PASSWORD = 'zabbix'

GRAPH_WIDTH = 600
GRAPH_HEIGHT = 200
GRAPH_PERIOD = 60 * 60 * 24 * 7 # 7 days
# you can get the graph ids from the URL when watching a graph in the frontend
GRAPH_IDS = [632]

SMTP_FROM = u'zabbix@%s' % getfqdn()
SMTP_TO = [u'recipient@example.com']
SMTP_SUBJECT = u'Zabbix Report'
SMTP_SERVER = u'localhost'

SMSTRADE_API_URL = 'https://gateway.smstrade.de'
SMSTRADE_KEY = 'abcd1234'
SMSTRADE_ROUTE = 'basic'
# if from is set to something non-empty, the route is changed to 'gold'
SMSTRADE_FROM = ''
# a simple custom reference to help identifying e.g. SMS delivery reports (maybe empty, max. 30 chars)
SMSTRADE_REF = 'zabbix'
# this enables the debug mode on the smstrade API, i.e. SMS are not delivered and not accounted
SMSTRADE_DEBUG = True

########################################################################
class Configuration(object):

    #----------------------------------------------------------------------
    def __init__(self, additional_config_filepath=None):
        self.graph_height = GRAPH_HEIGHT
        self.graph_ids = GRAPH_IDS
        self.graph_period = GRAPH_PERIOD
        self.graph_width = GRAPH_WIDTH
        self.smstrade_api_url = SMSTRADE_API_URL
        self.smstrade_debug = SMSTRADE_DEBUG
        self.smstrade_from = SMSTRADE_FROM
        self.smstrade_key = SMSTRADE_KEY
        self.smstrade_ref = SMSTRADE_REF
        self.smstrade_route = SMSTRADE_ROUTE
        self.smtp_from = SMTP_FROM
        self.smtp_server = SMTP_SERVER
        self.smtp_subject = SMTP_SUBJECT
        self.smtp_to = SMTP_TO
        self.zabbix_frontend_url = ZABBIX_FRONTEND_URL
        self.zabbix_password = ZABBIX_PASSWORD
        self.zabbix_username = ZABBIX_USERNAME

        self._parser = None
        self._vars = dict(fqdn=getfqdn())
        self._additional_config_filepath = additional_config_filepath

    #----------------------------------------------------------------------
    def read(self):
        config_file_paths = self._get_config_file_paths()
        self._parser = ConfigParser()
        self._parser.read(config_file_paths)

        self._get_string('zabbix', 'zabbix_frontend_url')
        self._get_string('zabbix', 'zabbix_password')
        self._get_string('zabbix', 'zabbix_username')
        self._get_bool('zabbix_smstrade', 'smstrade_debug')
        self._get_int('zabbix_graph', 'graph_height')
        self._get_int('zabbix_graph', 'graph_period')
        self._get_int('zabbix_graph', 'graph_width')
        self._get_list('zabbix_graph', 'graph_ids')
        self._get_list('zabbix_graph', 'smtp_to')
        self._get_string('zabbix_graph', 'smtp_from')
        self._get_string('zabbix_graph', 'smtp_server')
        self._get_string('zabbix_graph', 'smtp_subject')
        self._get_string('zabbix_smstrade', 'smstrade_api_url')
        self._get_string('zabbix_smstrade', 'smstrade_from')
        self._get_string('zabbix_smstrade', 'smstrade_key')
        self._get_string('zabbix_smstrade', 'smstrade_ref')
        self._get_string('zabbix_smstrade', 'smstrade_route')

    #----------------------------------------------------------------------
    def _get_config_file_paths(self):
        config_file_paths = list()
        # various config file paths
        config_file_paths.append(u'/etc/zabbix-scripts.conf')
        config_file_paths.append(u'/etc/zabbix/zabbix-scripts.conf')
        config_file_paths.append(expanduser(u'~/.zabbix-scripts.conf'))

        if self._additional_config_filepath:
            config_file_paths.append(self._additional_config_filepath)

        return config_file_paths

    #----------------------------------------------------------------------
    def _get_string(self, section, key):
        if self._parser.has_option(section, key):
            value = self._parser.get(section, key, vars=self._vars)
            setattr(self, key, value)

    #----------------------------------------------------------------------
    def _get_int(self, section, key):
        if self._parser.has_option(section, key):
            value = self._parser.getint(section, key)
            setattr(self, key, value)

    #----------------------------------------------------------------------
    def _get_list(self, section, key):
        if self._parser.has_option(section, key):
            value = self._parser.get(section, key)
            value = eval(value)
            setattr(self, key, value)

    #----------------------------------------------------------------------
    def _get_bool(self, section, key):
        if self._parser.has_option(section, key):
            value = self._parser.getboolean(section, key)
            setattr(self, key, value)






## CONFIGURATION
server = 'https://172.28.1.29/zabbix/'
user = 'Admin'
password = 'zabbix'
img_path    = "/root/tmp_images/"
tmp_cookies = ""
url_index   = server + "index.php"
url_graph   = server + "chart2.php"
url_api     = server + "api_jsonrpc.php"

login_data  = {'name' : user, 'password' : password, 'enter' : "Sign in"}

def GraphImageById(width, height, graphid, period = 3600):
    global server, user, password, tmp_cookies, url_index, url_graph, url_api, img_path, login_data
    ## file names
    filename_cookie = tmp_cookies + "zabbix_cookie_" + graphid + ".txt"
    image_name = img_path + "zabbix_graph_" + graphid + ".png"
    ## setup curl
    b = StringIO.StringIO()
    conn = pycurl.Curl()
    conn.setopt(pycurl.URL, url_index)
    conn.setopt(pycurl.HEADER, false)
    conn.setopt(pycurl.HTTPPOST, login_data)
    conn.setopt(pycurl.SSL_VERIFYPEER, false)
    conn.setopt(pycurl.COOKIEJAR, filename_cookie)
    conn.setopt(pycurl.COOKIEFILE, filename_cookie)
    ## Start connection
    conn.perform()
    ## Get graphs
    conn.setopt(pycurl.URL, url_graph + "?graphid=" + graphid + "&width=" + width + "&height=" + height + "&period=" + period)
    output = conn.perform()
    conn.close()
    ## Delete cookie
    print "Content-type: image/png\n"
    os.unlink(filename_cookie)
    fp = open(image_name, 'w')
    fwrite = (fp, output)
    fp.close()
    print "Content-type: text/html\n"


    # $ch = curl_init();
    # curl_setopt($ch, CURLOPT_URL, $z_url_index);
    # curl_setopt($ch, CURLOPT_HEADER, false);
    # curl_setopt($ch, CURLOPT_RETURNTRANSFER, true);
    # curl_setopt($ch, CURLOPT_BINARYTRANSFER, true);
    # curl_setopt($ch, CURLOPT_SSL_VERIFYPEER, false);
    # curl_setopt($ch, CURLOPT_POST, true);
    # curl_setopt($ch, CURLOPT_POSTFIELDS, $z_login_data);
    # curl_setopt($ch, CURLOPT_COOKIEJAR, $filename_cookie);
    # curl_setopt($ch, CURLOPT_COOKIEFILE, $filename_cookie);
    # // login
    # curl_exec($ch);
    # // get graph
    # curl_setopt($ch, CURLOPT_URL, $z_url_graph ."?graphid=" .$graphid ."&width=" .$width ."&height=" .$height ."&period=" .$period);
    # $output = curl_exec($ch);
    # curl_close($ch);
    # // delete cookie
    # header("Content-type: image/png");
    # unlink($filename_cookie);
    # $fp = fopen($image_name, 'w');
    # fwrite($fp, $output);
    # fclose($fp);
    # header("Content-type: text/html");


#----------------------------------------------------------------------
# def get_graph(config, cookie_jar, graph_id, start_time):
#     url = u'%s/chart2.php' % config.zabbix_frontend_url
#     data = urlencode(dict(
#             stime=start_time,
#             graphid=graph_id,
#             width=config.graph_width,
#             height=config.graph_height,
#             period=config.graph_period))

#     cookie_processor = HTTPCookieProcessor(cookie_jar)
#     opener = build_opener(cookie_processor)

#     request = opener.open(url, data)
#     graph_image = request.read()
#     return graph_image


#----------------------------------------------------------------------
# def send_mail(config, images):
#     msg = MIMEMultipart()
#     msg['From'] = config.smtp_from
#     msg['To'] = u', '.join(config.smtp_to)
#     msg['Date'] = formatdate(localtime=True)
#     msg['Subject'] = config.smtp_subject

#     msg.attach(MIMEText(u'Zabbix Report'))

#     i = 0
#     for image in images:
#         part = MIMEBase('image', 'png')
#         part.set_payload(image)
#         Encoders.encode_base64(part)
#         part.add_header('Content-Disposition', 'attachment; filename="%s.png"' % i)
#         msg.attach(part)
#         i += 1

#     smtp = smtplib.SMTP(config.smtp_server)
#     smtp.sendmail(config.smtp_from, config.smtp_to, msg.as_string())
#     smtp.close()


#----------------------------------------------------------------------
def main():
    config = Configuration()
    config.read()

    # start_time = datetime.now() - timedelta(seconds=config.graph_period)
    # start_time = start_time.strftime(u'%Y%m%d%H%M%S')

    # cookie_jar = login(config)

    # images = list()
    # for graph_id in config.graph_ids:
    #     image = get_graph(config, cookie_jar, graph_id, start_time)
    #     images.append(image)

    # logout(config, cookie_jar)

    # send_mail(config, images)


if __name__ == '__main__':
    main()
