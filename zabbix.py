from pyzabbix import ZabbixAPI

# Create ZabbixAPI class instance
zapi = ZabbixAPI(url='https://172.28.1.29/zabbix/', user='Admin', password='zabbix')

# Get all monitored hosts
mon_hosts = zapi.host.get(monitored_hosts=1, output='extend')

# Get all disabled hosts
dis_hosts = zapi.do_request('host.get',
    {
    'filter': {'status': 1},
    'output': 'extend'
    })

# Filter results
hostnames1 = [host['host'] for host in mon_hosts]
hostnames2 = [host['host'] for host in dis_hosts['result']]


graphtest = zapi.do_request('graph.get',
    {
    "output": "extend",
    "hostids": 10144,
    "sortfield": "name"
    }
  )


print graphtest
