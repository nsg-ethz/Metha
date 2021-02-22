# Test 223

Router0 gets two equivalent routes from both Router1 and Router2. It picks a different route/next hop in Batfish and GNS3.

## Offending commands

__Router1__

```
router bgp 2
 redistribute connected
```

__Command description__

Used to inject routes from one routing domain into the Border Gateway Protocol (BGP), use the redistribute command. 

[Cisco documentation](https://www.cisco.com/c/m/en_us/techdoc/dc/reference/cli/n5k/commands/redistribute-bgp.html)

## Explanation

Both Router1 and Router2 advertise a route for 132.254.178.0/23 to Router0. The routes are equivalent: Hence, the best path selection comes down to the tie break. This depends on the implementation: It could be the route that was received first, the route with lower egress IP, the route with the lowest router id, or the route with the lowest router address (from the neighbor command).

[BGP decision process](https://www.cisco.com/c/en/us/support/docs/ip/border-gateway-protocol-bgp/13753-25.html)

The route from Router2 has the lower egress IP, the lower router id and the lower router address.

## Problematic scenario

A network has a policy that traffic should always leave via egress A if it is available. Wwhen Batfish checks it assures the operator that everything is working fine. However, the actually leaves through egress B.

## Check

