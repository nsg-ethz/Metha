# Test 251

In Batfish all three routers have get advertised a default-route from their neighbors.

## Offending commands

__Router0__

```
router bgp 1
  neighbor 222.28.200.2 default-originate
```

__Router2__

```
router bgp 2
  neighbor 132.254.178.2 default-originate
  neighbor 222.28.200.1 default-originate route-map map5
  ...
!
ip prefix-list list2 seq 73 deny 213.168.89.0/24
ip prefix-list list2 seq 100 permit 147.104.0.0/14
no cdp log mismatch duplex
!
route-map map5 deny 19
 match ip address prefix-list list2
 match as-path 87
 set metric -750
 set weight 20
 set origin incomplete
 set as-path prepend 846
 set comm-list 244 delete
!
route-map map5 permit 38
 match community 113
!
```

__Router2__

```
router bgp 3
  neighbor 132.254.178.1 default-originate
```

__Command description__

Used to inject routes from one routing domain into the Border Gateway Protocol (BGP), use the redistribute command. 

[More information](https://www.cisco.com/c/en/us/support/docs/ip/border-gateway-protocol-bgp/213952-configure-bgp-to-advertise-a-default-rou.html#anc9)

## Explanation

The router starts advertising a default route to the specific BGP peer no matter if it has a default route or not in its BGP RIB.

It would be interesting to get more information for those BGP routes: What is their AS path? Then, we could see where the routes actually originate. Router2, for example, should not originate a default route to Router0. Still, Router0 gets a route from Router2. The question is whether this is a route that Router2 originated, or Router1 originated and Router2 advertised to Router0.

In GNS3, we don't see any default routes. That's also a bit weird as one Cisco documentation says that a router should originate it no matter if it has a default-route or not.

## Problematic scenario

## Check
