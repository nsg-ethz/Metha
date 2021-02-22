# Test 326

In Batfish a null route is installed in the routing table of router0 which is not present in the GNS3 routing table.

## Offending commands

__Router0__
```
router bgp 1
  address-family ipv4
    aggregate-address 128.0.0.0 128.0.0.0
```

__Command description__
Border Gateway Protocol (BGP) allows the aggregation of specific routes into one route with the use of the `aggregate-address address mask [as-set] [summary-only] [suppress-map map-name] [advertise-map map-name] [attribute-map map-name]` command. When you issue the `aggregate-address` command without any arguments, there is no inheritance of the individual route attributes (such as AS_PATH or community), which causes a loss of granularity.

Configure an aggregation network range. _When_ viable routes that match the network range enter the BGP table, an aggregate route is created. On the originating router, the aggregated prefix sets the next-hop to Null0. The route to Null0 is automatically created by BGP as a loop-prevention mechanism.

Two rules from the book "Troubleshooting IP Routing Protocols":
Rule 1: Aggregation or summarization of subnets can happen only if those subnet exist in BGP table.
Rule 2: For the aggregated (summarized) route, Cisco IOS installs an IP route with the next hop to Null0 in the IP routing table. This is done to insure that a valid route exists in the routing table to announce it to other BGP peers.

[Cisco documentation](https://www.cisco.com/c/m/en_us/techdoc/dc/reference/cli/nxos/commands/bgp/aggregate-address-bgp.html)
[More information](https://www.ciscopress.com/articles/article.asp?p=2756480&seqNum=13)

## Explanation

Batfish creates the Null0 route to prevent loops even though no aggregation takes place (no matching routes are advertised through BGP).

## Problematic scenario

There are different pods that are all connected through a backbone. Each pod has a default route to the backbone. One pod should be isolated for security reasons from the rest, hence traffic to 10.0.0.0/16 should be blocked. All pod border routers have ACLs for that purpose. In one of the pod border routers this line got forgotten, but there is some left-over `aggregate-address` command for 10.0.0.0/16. 

If one checks that 10.0.0.0/16 is indeed isolated from all pods, Batfish will falsely assure it, because of the Null0 route.

## Check

All routers are in the same AS. When looking at the routing tables, it looks like no BGP routes are exchanged. What is going on? At least the connected routes should be advertised, as redistribute connected is used.