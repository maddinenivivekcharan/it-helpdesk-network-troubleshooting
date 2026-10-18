# Networking fundamentals

An IP address identifies an interface at the network layer; the prefix/subnet
mask determines which destinations are local. A default gateway forwards traffic
toward other networks. DNS maps names to records such as IPv4 A and IPv6 AAAA.
DHCP commonly supplies an IPv4 lease, prefix, gateway and resolver settings.
IPv6 can use router advertisements and DHCPv6; IPv4 problems alone do not prove
that every protocol is down.

IPv4 loopback 127.0.0.1 and IPv6 ::1 test the local host, not a router or internet.
A 169.254.x.x address is IPv4 link-local and often follows failure to obtain a
DHCP lease. Confirm whether DHCP and IPv4 routing were expected before concluding
there is a fault. Private lab addresses differ from publicly routed addresses;
never infer authorization to test a target from the type of address.

Work through the layers: physical link -> interface/address -> local route ->
resolver -> transport/application. Check one hypothesis at a time and record
what each result supports. A ping sends ICMP; DNS uses resolver protocols;
a website also needs routing, transport, TLS and application health. Therefore
neither DNS success nor a ping reply proves that an application works. A timeout
may reflect filtering rather than a failed host.

A gateway failure can affect many services; a DNS failure may affect only names;
Wi-Fi association can succeed before captive portal authentication; a VPN can
supply routes and split DNS for internal services. Inspect the required approved
VPN state rather than changing resolvers or bypassing controls.

The tool sends two ping requests to one supplied destination. It has no discovery
or scanning feature. Prefer loopback for demonstrations and mocked tests for
failure scenarios. Use documentation-only names such as example.test in fixtures;
these examples are not real corporate systems.
