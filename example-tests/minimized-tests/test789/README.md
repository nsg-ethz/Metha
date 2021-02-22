# Test 789

Router2 redistributes two static routes into OSPF (143.128.0.0/10 and 128.0.0.0/10). These routes are only present in GNS3. The same happens for the static route at Router0 for 128.0.0.0/2.

## Offending commands

__Router0__
```
router ospf 100
  ...
  redistribute static
...
ip route 128.0.0.0 192.0.0.0 FastEthernet0/1
```

__Router2__
```
router ospf 100
  ...
 redistribute static
...
ip route 128.0.0.0 255.192.0.0 FastEthernet0/1
ip route 143.128.0.0 255.192.0.0 FastEthernet0/0
```

__Command description__
```
ip route 128.0.0.0 255.192.0.0 FastEthernet0/1
```

The above command creates a static route. It directs all traffic for the prefix 128.0.0.0/10 (network address 128.0.0.0, netmask 255.192.0.0) to the interface `FastEthernet0/1`.

```
 redistribute static
```
This tells the OSPF routing process to advertise static routes in its area.

[More information](https://www.cisco.com/c/en/us/td/docs/switches/datacenter/sw/5_x/nx-os/unicast/configuration/guide/l3_cli_nxos/l3_route.html)
[More information](https://www.cisco.com/c/en/us/support/docs/ip/enhanced-interior-gateway-routing-protocol-eigrp/8606-redist.html#ospf)

## Explanation

The problem has to be with the `redistribute static` command. All the routers have the static routes in their routing tables, but no router received an advertisement for such a route through OSPF.

## Problematic scenario