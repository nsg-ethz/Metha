# Test 187

The route for 188.98.128.0/22 at Router0 has a metric of 65536 in Batfish and of 2 in GNS3.

## Offending commands

__Router0__
```
router ospf 100
 max-metric router-lsa
```

__Command description__

Used to configure the Open Shortest Path First (OSPF) protocol to advertise a maximum metric so that other routers do not prefer the router as an intermediate hop in their shortest path first (SPF) calculations, use the max-metric router-lsa command.

[Cisco documentation](https://www.cisco.com/c/m/en_us/techdoc/dc/reference/cli/nxos/commands/ospf/max-metric-router-lsa-ospf.html)

## Explanation

Here it seems, that `max-metric` is only applied to inter-area routes. In Test 47 however, `max-metric` is also applied to intra-area routes.

It seems that the max-metric is not applied in the backbone area.

## Problematic scenario

## Check