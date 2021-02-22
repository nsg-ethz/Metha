# Test 99

In Batfish, there is a OSPF inter-area route for 174.147.240.0/21 at Router2, which is not present in GNS3.

In GNS3, there are two routes missing in Batfish: One aggregate Null route for 128.0.0.0/1 and a

## Offending commands

__Router0__
```
router ospf 100
  ...
  area 0 range 128.0.0.0 128.0.0.0
  area 1 range 160.0.0.0 255.255.255.240 not-advertise cost 612
  redistribute connected
```

__Command description__

Used to consolidate and summarize routes at an Open Shortest Path First (OSPF) area boundary, use the area range command.

advertise/not-advertise/cost are the options

Routes from area X are summarized and only the summary is being redistributed into all the others. With `cost` one can define the cost of the aggregate address. When the option `not-advertise` is used, no route within the specified range is advertised to other areas.

[Cisco documentation](https://www.cisco.com/c/m/en_us/techdoc/dc/reference/cli/nxos/commands/ospf/area-range-ospf.html)

## Explanation

```
area 0 range 128.0.0.0 128.0.0.0
```

The aggregate route for 128.0.0.0/1 is missing in Batfish at the aggregating router (Router 0): GNS3 puts a null-route there. The real router prevents potential routing loops. Batfish would detect a routing loop, even though there isn't one.

The route 174.147.240.0/21 should not be present in Router2 in Batfish as it originally stems from area 0. All routes that are within the range 128.0.0.0/1 should be summarized in a route for 128.0.0.0/1 and the constituents should not be announced.

```
area 1 range 160.0.0.0 255.255.255.240 not-advertise cost 612
```

`cost 612` has no effect as the option `not-advertise` is being used. In addition, there are no networks in the specified range (160.0.0.0/28). The closest we get to that prefix is 160.64.0.0/11 at Router0 and Router2.

It is not clear why Batfish doesn't have the route for 134.31.0.0/17 at Router1. The network is originated in area 1 and router0 should redistribute it into area 0. The area range command doesn't cover the route.

```
redistribute connected subnets
```

The `subnets` keyword is important as otherwise only classful networks (/8, /16, /24) are redistributed. Apparently, this only matters for OSPF.

## Problematic scenario

## Check
