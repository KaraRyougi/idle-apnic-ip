import csv
from telnetlib import Telnet

HE = "route-server.he.net"
RADb = "whois.radb.net"

csvfile = open('APNIC.csv')
no_route = open('no-route.csv', 'w')
no_route_object = open('no-route-object.csv', 'w')
not_announced = open('not-announced.csv', 'w')

reader = csv.DictReader(csvfile)

no_route_writer = csv.DictWriter(no_route, fieldnames=reader.fieldnames)
no_route_writer.writeheader()

no_route_object_writer = csv.DictWriter(no_route_object, fieldnames=reader.fieldnames)
no_route_object_writer.writeheader()

not_announced_writer = csv.DictWriter(not_announced, fieldnames=reader.fieldnames)
not_announced_writer.writeheader()

for row in reader:
    ip = row['allocation_address']
    he = Telnet(HE)
    he.read_until(b"route-server>")
    he.write(b"show ip bgp " + ip.encode('ascii') + b"\n")
    he_result = he.read_until(b"route-server>")
    he.close()
    if b"Network not in table" in he_result:
        no_route_writer.writerow(row)
        radb = Telnet(RADb, 43)
        radb.write(ip.encode('ascii') + b"\n")
        radb_result = radb.read_all()
        radb.close()
        if b"No entries found for the selected source(s)." in radb_result:
            no_route_object_writer.writerow(row)
        else:
            not_announced_writer.writerow(row)
            print(row['allocation_address'] + "/" + row['length'] + " from " + row['economy_name'])

no_route.close()
no_route_object.close()
not_announced.close()
csvfile.close()
