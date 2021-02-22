# Test 47


In Batfish, Router0 receives a default route from both Router1 and Router2. In GNS3, Router0 doesn't receive these default routes.

## Offending commands

__Router0__
```
router ospf 100
  ...
  max-metric router-lsa include-stub summary-lsa 8007324
```

__Router1__
```
router ospf 100
  ...
  max-metric router-lsa summary-lsa 3466083
```

__Command description__
`max-metric router-lsa` and `summary-lsa XXXXXXX` are almost like two different commands: max-metric is applied to router-lsas and the second part is applied to summary-lsa. The high value is only set as cost to summary-lsa.

Router1,default,134.31.0.0/17,Router0,174.147.240.1,dynamic,ospfIA,8072859 = 8007324 + 65535,110,

The summary-lsa value will only be applied to routes announced from one area to another. All other (intra-area) routes (router-lsa) will be assigned a max-metric of 65535. This is visible in the following route:

Router0,default,131.157.254.248/29,Router2,134.31.0.2,dynamic,ospf,65536,110,

[Cisco documentation](https://www.cisco.com/c/m/en_us/techdoc/dc/reference/cli/nxos/commands/ospf/max-metric-router-lsa-ospf.html)

## Explanation

Router2 is missing a route to 174.146.240.0/21 with metric 8007325. This network is originated at Router1 in area 0. Therefore, only the `summary-lsa 8007324` is applied and not the max-metric router-lsa. But why? it's the same for the route for 134.31.0.0/17 and there both values are added. Does it make a difference if it is announced from backbone (area 0) to a stub area (area 1) and vice-versa?

## Problematic scenario

This command is often used during planned maintenance. It is used if one needs to do some work on a router (e.g., to upgrade the router OS) and wants to shift traffic away from that router.

One could imagine that an operator wants to use Batfish to first check if it is safe to apply the `max-metric` command. If Batfish falsely says that it is safe, it could have a terrible outcome.

## Check

Router0 and Router2 are both in area 1. The network 131.157.254.248/29 is as well in area 1 (even though there is not `ip ospf 100 area 1`, why?). Hence, Router1 will `apply max-metric router-lsa` and set the cost to max 65535. Why is there the cost 1 higher?

The route 134.31.0.0/17 at Router1 is an intra-area route as it part of area 1. Hence, Router1 first applies `max-metric router-lsa` and then also `summary-lsa 8007324`.