# Metha Topology Format

* ```name```: (Optional) name of the topology, defaults to the filename
* ```num_nodes```: Number of routers in this topology
* ```num_ases```: Number of BGP autonomous systems in this topology
* ```num_areas```: Number of OSPF areas in this topology
* ```links```: List of links in this topology, a link is given in the format ```[0, 1]``` which links the first and second router in the topology
* ```ospf_areas```: List of assignments of links to OSPF areas, the i-th entry corresponds to the i-th link defined above, assign ```null``` to disable OSPF on any given link
* ```ases```: List of assignments of routers to BGP autonomous systems, assign ```null``` to disable BGP
* ```router_types```: List router types as defined in ```router_types.py```
* ```protocols```(optional): Per router list of enabled protocols on this router

## Example

```
{
  "name": "test-topology"
  "num_nodes": 3,
  "num_ases": 0,
  "num_areas": 2,
  "links": [[0, 1], [0, 2]],
  "ospf_areas": [0, 1],
  "ases": [null, null, null],
  "router_types": ["JuniperVMX", "Cisco7200", "Cisco7200"],
  "protocols": [
    ["static", "ospf"], ["static", "ospf"], ["static", "ospf"]
  ]
}
```
