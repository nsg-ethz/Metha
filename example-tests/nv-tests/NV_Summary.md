## bgp-auto-summary
- Command:
  auto-summary

- Documentation:
  By default, BGP does not accept subnets redistributed from IGP. To advertise and carry subnet routes in BGP, use an explicit network command or the no auto-summary command. If you disable auto-summarization and have not entered a network command, you will not advertise network routes for networks with subnet routes unless they contain a summary route.

- Inaccuracy: 
  NV adds the summary route also to its own routing table, while the real Cisco devices only advertise it to their neighbors without storing it in its own routing table.

## bgp-bestpath-med-missing-as-worst
- Command:
  bgp bestpath med missing-as-worst

- Documentation:
  Multi-Exit-Discriminator (MED) is considered when selecting the best path among many paths. Paths with lower MED are preferred. By default, if a MED is missing, its value is set to 0, or most preferred. All routers in an AS should be configured the same way to ensure a consistent decision process throughout the AS.

  Use the bgp bestpath med missing-as-worst command to consider a missing MED value of a path as having the worst MED value, i.e. 4294967294.

- Inaccuracy: 
  NV does not set the MED to the worst value.

## bgp-set-community-local-AS
- Command:
  set community local-AS

- Documentation: 
  when setting a community, one can use names for well-known communities (e.g., local-AS). Local-AS is a special community that routes with this community cannot be advertised to eBGP peers.

- Inaccuracy:
  NV exports the route to eBGP peers even though the routes have the local-AS community set.

## bgp-set-community-no-advertise
- Command:
  set community no-advertise

- Documentation:
  When you add the "no-advertise" community to a prefix then the BGP router will use and store the route, but it will not advertise it to any other neighbors.

- Inaccuracy:
  NV exports the route to its neighbors.

## bgp-set-community-no-export
- Command:
  set community no-export

- Documentation:
  When you add the "no-export" community to a prefix then the BGP router will advertise the route only to iBGP neighbors, but it will not advertise it to any eBGP neighbors.

- Inaccuracy:
  NV exports the route to its eBGP neighbors.

## bgp-distance:
- Command:
  distance bgp 100 255 100

- Documentation:
  The distance bgp command allows you to change the administrative distance of a received BGP route. Default is 20 for external route, 200 for internal and 200 for local routes.

- Inaccuracy:
  NV does not apply the adminstrative distance change.

## bgp-no-announcement (Juniper):
- Inaccuracy:
  When a hybrid network is used (e.g., some Juniper and some Cisco routers), routes are somehow not exchanged via the Juniper router.

## bgp-administrative-distance (Juniper):
- Inaccuracy:
  BGP routes have a default administrative distance of 170 on some Juniper routers (vMX). NV takes the Cisco default for eBGP routes (20) instead.

## bgp-maxas-limit:
- Command:
  bgp maxas-limit 1

- Documentation:
  To configure the external Border Gateway Protocol (eBGP) to discard routes that have a high number of autonomous system (AS) numbers in the AS-path attribute, use the maxas-limit command.

- Inaccuracy:
  NV does not discard the routes based on this command.

## bgp-maximum-prefix:
- Command:
  neighbor 169.182.0.113 maximum-prefix 1

- Documentation:
  The BGP Maximum-Prefix feature allows you to control how many prefixes can be received from a neighbor. By default, this feature allows a router to bring down a peer when the number of received prefixes from that peer exceeds the configured Maximum-Prefix limit.

- Inaccuracy:
  NV does not model the maximum-prefix feature. The session between router0 and router1 is maintained despite router0 advertising two routes.

## bgp-metric-default-value:
- Documentation:
  The default MED value for BGP routes is 0.

- Inaccuracy:
  NV uses a default value of 80.

## bgp-no-auto-summary
- Command:
  no auto-summary

- Inaccuracy:
  NV redistributes a classful network (/24), even-though no-auto-summary is set and the actual prefix is more specific (/27).

## bgp-redistribute-match-as-path
- Command:
  redistribute connected route-map map_out_match_as_path
  !
  route-map map_out_match_as_path permit 1
   match as-path 2

- Documentation:
  Route-map match commands are only applied by the router software if they make sense in the context of the protocol specified in the redistribution command. However, the router lets you configure it.

- Inaccuracy:
  It seems like NV still applies the route-map.

## bgp-redistribute-match-community
- Command:
  redistribute connected route-map map_out_match_community
  route-map map_out_match_community permit 1
   match community 3 exact-match

- Documentation:
  Route-map match commands are only applied by the router software if they make sense in the context of the protocol specified in the redistribution command. However, the router still lets you configure it and it will be shown in the configuration, even though it is not actually applied.

- Inaccuracy:
  It seems like NV still applies the route-map.

## bgp-tie-break => False positive
- Can be timing dependent

## from-color-max
- Command:
  set policy-options policy-statement send-bgp term 1 from color 4294967295

- Inaccuracy:
  Parser error

## from-local-preference-max
- Command:
  set policy-options policy-statement send-bgp term 1 from local-preference 4294967295

- Inaccuracy:
  Parser error

## from-tag-max
- Command:
  set policy-options policy-statement send-bgp term 1 from tag 4294967295

- Inaccuracy:
  Parser error

## ospf-area-range-override-metric
- Command:
  set protocols ospf area 0.0.0.0 area-range 182.42.0.0/17 override-metric 200

- Documentation:
  Summarize the IP addresses specified in the range and override the metric to the specified value.

- Inaccuracy:
  NV does not override the metric. Probably this feature is not implemented.

## ospf-area-range
- Command:
  area 0 range 174.0.0.0 255.0.0.0

- Documentation:
  When an aggregate route is activated, the corresponding router installs a null route to prevent any routing loops.

- Inaccuracy:
  NV does not install the null route.

## ospf-default-originate-always
- Command:
  default-information originate always metric-type 1

- Documentation:
  This forces a router to advertise a default route in OSPF.

- Inaccuracy:
  NV does not advertise a default route. Probably this feature is not implemented.

## ospf-distance
- Command:
  distance 108

- Documentation:
  Allows to change the administrative distance of OSPF.

- Inaccuracy:
  NV does not apply the administrative distance change.

## ospf-max-metric-router-lsa
- Command:
  max-metric router-lsa

- Documentation:
  All point-to-point links should be set to the maximum metric to prevent transit traffic on that router.

- Inaccuracy:
  NV does not change the metric for the routes. Probably this feature is not implemented.

## ospf-max-metric-router-lsa-summary-lsa
- Command:
  max-metric router-lsa summary-lsa 8007324

- Documentation:
  Not only point-to-point links, but also stub links should be set to the maximum metric.

- Inaccuracy:
  NV does not change the metric for the routes. Probably this feature is not implemented.

## ospf-metric-default-value
- Inaccuracy:
  Somehow the OSPF routes have a metric of 1, when they should have a metric of 2. We only tested it on very small networks, so I cannot say if the metric is just always 1 or whether it is off by 1.

## ospf-priority
- Command:
  set protocols ospf area 0.0.0.1 interface ge-0/0/1.0 priority 0

- Documentation:
  When setting priority to 0, the interface is not involved in the designated router election (DR)

- Inaccuracy:
  NV probably does not implement that feature and does not consider DR election, which is also not very important.

## ospf-redistribute
- Command:
  redistribute static subnets

- Documentation:
  The router should redistribute all static routes into OSPF.

- Inaccuracy:
  NV does not redistribute the routes. The feature is probably not implemented.

## set-local-preference-max
- Command:
  set local-preference 4294967295

- Inaccuracy:
  Parse error

## set-metric
- Command:
  set metric 294967295

- Documentation:
  The metric/MED of every route matching the route-map should be set to the specified value.

- Inaccuracy:
  NV does not adapt the metric of the matching route. Probably not implemented.

## static-junos-default-preference
- Documentation:
  Juniper uses a administrative distance of 5 for static routes.

- Inaccuracy:
  NV uses an administrative distance of 1 for static routes.

## then-local-preference-max
- Command:
  set policy-options policy-statement send-bgp term 1 then local-preference 4294967295

- Inaccuracy:
  Parse error