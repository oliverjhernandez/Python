#!/usr/local/bin/python2

from elasticsearch import Elasticsearch
import json

ip = "172.28.8.211"

def allocation_explain(index,shard,primary):
  req_body = {
            "index": index,
            "shard": shard,
            "primary": primary
          }
  es = Elasticsearch([ip], maxsize=1)
  return es.cluster.allocation_explain(body=req_body)

def cat_shards():
  es = Elasticsearch([ip], maxsize=1)
  shards = es.cat.shards()
  unassigned_shards = []
  for line in shards.splitlines():
    if 'UNASSIGNED' in line and line.strip().split()[2] == 'p':
        unassigned_shards.append((line.strip().split()[0:2]))
  return unassigned_shards

def allocate_shard(index,shard,node_name):
  reroute_body = {
    "commands": [{
        "allocate_stale_primary": {
            "index": index,
            "shard": shard,
            "node": node_name,
            "accept_data_loss": True
        }
    }]
  }
  es = Elasticsearch([ip], maxsize=1)
  return es.cluster.reroute(reroute_body)

def run():
  for index,shard in cat_shards():
    explanation = allocation_explain(index, shard, True)
    for key in explanation['nodes']:
      if explanation['nodes'][key]['store']['shard_copy'] == "STALE":
        node_name = explanation['nodes'][key]['node_name']
    try:
      allocate_shard(index,shard,node_name)
      print "Index: " + index + " with shard " + shard + " has been rerouted."
    except Exception as error:
       print(error)



if __name__ == '__main__':
  run()
