from random import randrange

# on memory tables
ROUTE_TABLE = []
# {
#   "DESTINATION_IP": "10.10.10.1",
#   "DESTINATION_MASK": "255.255.255.0"
# }

ARP_TABLE = []
# {
#   "GATEWAY": "10.10.10.0",
#   "MAC_ADDRESS": "08:00:27:e7:97:00"
# }


def generate_random_mac():
  rand = "%012x" % randrange(12 ** 12)

  return " ".join([
    str(rand[i]) + str(rand[i + 1]) if i % 2 == 0 else ""
    for i in range(len(rand))
  ]).replace("  ", ":").strip()


def bitwise_and(bits_a, bits_b):
  bits_compared = []

  for i in range(len(bits_a)):
    bit_a = bits_a[i]
    bit_b = bits_b[i]

    bits_compared.append("1" if bit_a == "1" and bit_b == "1" else "0")

  return "".join(bits_compared)


def address_dec_to_bin(address_dec):
  address_parts = address_dec.split(".")
  address_bin = ""

  for part in address_parts:
    part = bin(int(part, 10))[2:]

    if len(part) < 8:
      missing_zeroes = 8 - len(part)
      part = ("0" * missing_zeroes) + str(part)

    address_bin = str(address_bin) + str(part)

  return address_bin


def address_bin_to_dec(address_bin):
  address_dec = ""

  while len(address_bin) > 0:
    if len(address_dec) > 0:
      address_dec = str(address_dec) + "." + str(int(address_bin[:8], 2))
    else:
      address_dec = str(int(address_bin[:8], 2))

    address_bin = address_bin[8:]

  return address_dec


def add_gateway_to_arp_table(gateway):
  ARP_TABLE.append({
    "GATEWAY": gateway,
    "MAC_ADDRESS": generate_random_mac()
  })


def check_arp_table(gateway):
  results = [
    True
      if arp_entry["GATEWAY"] == gateway
      else False
    for arp_entry in ARP_TABLE
  ]

  return any(results)


def get_gateway_from_route(route):
  address_dec = route["DESTINATION_IP"]
  print('[INFO] address_dec', address_dec)

  dest_mask = route["DESTINATION_MASK"]
  print('[INFO] dest_mask', dest_mask)

  address_bin = address_dec_to_bin(address_dec)
  print('[INFO] address_bin', address_bin)

  mask_bin = address_dec_to_bin(dest_mask)
  print('[INFO] mask_bin', mask_bin)

  gateway_bin = bitwise_and(address_bin, mask_bin)
  print('[INFO] gateway_bin', gateway_bin)

  gateway_dec = address_bin_to_dec(gateway_bin)
  print('[INFO] gateway_dec', gateway_dec)

  return gateway_dec


def route():
  for route in ROUTE_TABLE:
    gateway = get_gateway_from_route(route)

    gateway_known = check_arp_table(gateway)

    if gateway_known == False:
      add_gateway_to_arp_table(gateway)

    print(ARP_TABLE)
    print("---------------------------------------------------")


def main():
  routes = [{
    "DESTINATION_IP": "10.10.10.1",
    "DESTINATION_MASK": "255.255.255.0"
  }, {
    "DESTINATION_IP": "10.10.10.254",
    "DESTINATION_MASK": "255.255.255.0"
  }, {
    "DESTINATION_IP": "10.10.100.50",
    "DESTINATION_MASK": "255.255.255.0"
  }, {
    "DESTINATION_IP": "192.168.0.100",
    "DESTINATION_MASK": "255.255.255.0"
  }]
  ROUTE_TABLE.extend(routes)

  route()


if __name__ in "__main__":
  main()
