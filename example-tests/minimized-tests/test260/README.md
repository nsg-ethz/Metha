# Test 260

The administrative distance of OSPF routes differs between Batfish and GNS3.

## Offending commands

__Router0__
```
router ospf 100
  ...
  distance 82
```

__Router1__
```
router ospf 100
  ...
  distance 105
```

__Router2__
```
router ospf 100
  ...
  distance 108
```

__Command description__

The command allows to change the administrative distance of OSPF. The default administrative distance of OSPF is 110.

[Cisco documentation](https://www.cisco.com/c/m/en_us/techdoc/dc/reference/cli/nxos/commands/ospf/distance-ospf.html)

## Explanation

Batfish does not take the changed administrative distance into account and operates with the default value of 110.

## Problematic scenario