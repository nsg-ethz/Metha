# Test 192

In Batfish, Router0 receives a default route from both Router1 and Router2. In GNS3, Router0 doesn't receive these default routes.

## Offending commands

__Router0__
```
router ospf 100
  ...
  default-information originate always metric-type 1
```

__Router1 and Router2__
```
router ospf 100
  ...
  default-information originate
```

__Command description__
If it is a normal area (not a stub/totally stub/NSSA), then one can make a router advertise a default route into OSPF. With the keyword `always`, one can force the router to advertise the default route even if the router doesn't have default route.

The metric-type tells the router with which external metric it should announce it. There are two external metrics and they just differ in how the cost of the route is caluclated. Type E1 means that the cost is equal to the link-state metric (sum of the internal and external costs). Type E2 only consider the external costs and ignore the cost to reach the AS boundary router (the one injecting the route). The default is metric-type=E2.

[Cisco documentation](https://www.cisco.com/c/m/en_us/techdoc/dc/reference/cli/nxos/commands/ospf/default-information-originate-ospf.html)
[More information](https://www.cisco.com/c/en/us/support/docs/ip/open-shortest-path-first-ospf/13692-21.html)

## Explanation

The metric-type is crucial for this bug to happen. If we just use `default-information originate always`, Batfish will not announce the other default routes at Router1 and Router2 anymore.

Probably, Batfish only advertises a default-route if there is one present in the routing table that is not of the same type as they would advertise. Since we change the type to E1, Batfish sees this route and starts to advertise a type E2 route.

## Problematic scenario