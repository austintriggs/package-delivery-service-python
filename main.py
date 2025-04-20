import csv
import datetime

from package import Package
from hashtable import HashTable
from truck import Truck

def load_package_data(hash_table):
    with open("csv_files/packages.csv") as package_info:
        packages = csv.reader(package_info)
        for package in packages:
            pId = int(package[0])
            pAddress = package[1]
            pCity = package[2]
            pState = package[3]
            pZip = package[4]
            pDeadline = package[5]
            pWeight = package[6]
            pNotes = package[7]
            pStatus = "At Hub"


            p = Package(pId, pAddress, pCity, pState, pZip, pDeadline, pWeight, pNotes, pStatus)

            hash_table.insert(pId, p)

def load_distance_data():
    distance_list = []
    with open("csv_files/distances.csv") as distance_info:
        distances = csv.reader(distance_info)
        for distance in distances:
            distance_list.append(distance)

        for i in range(len(distance_list)):
            for j in range(len(distance_list)):
                distance_list[i][j] = distance_list[j][i]
    return distance_list

def load_address_data():
    address_list = []
    with open("csv_files/addresses.csv") as address_info:
        addresses = csv.reader(address_info)
        for address in addresses:
            address_list.append(address[2])
    return address_list

def distance_between(address1, address2):
    distance_list = load_distance_data()
    address_list = load_address_data()
    return distance_list[address_list.index(address1)][address_list.index(address2)]

def deliver_packages(truck, ht):
    # Set next package to be delivered to first package on truck
    _next_delivery = truck.packages[0]

    # Find the closest distanced package on truck and set it to next delivery
    for package in truck.packages:
        if float(distance_between(truck.address, package.address)) <= float(distance_between(truck.address, _next_delivery.address)):
            _next_delivery = package

    # Calculate time to delivery
    _time = round(60*float(distance_between(truck.address, _next_delivery.address))/truck.speed)
    print(truck.depart_time)
    _truck_time = datetime.datetime.strptime(truck.depart_time, "%H:%M:%S").time()
    _time_object = datetime.datetime.combine(datetime.date.today(), _truck_time)
    _delivery_time = (_time_object + datetime.timedelta(minutes=_time)).time()
    truck.depart_time = str(_delivery_time)
    print(f'delivery time: {_delivery_time}')
    # truck.depart_time = truck.depart_time + _delivery_time
    print(f'_time: {_time}')
    # Update truck mileage
    truck.mileage += float(distance_between(truck.address, _next_delivery.address))
    # Update truck location
    truck.address = _next_delivery.address
    # Remove package from truck package list
    truck.packages.remove(_next_delivery)
    # Mark package as delivered and update delivery time
    ht.lookup(_next_delivery.id).status = "Delivered"
    ht.lookup(_next_delivery.id).delivery_time = str(_delivery_time)

    print(f'ht.lookup(package.id): {ht.lookup(_next_delivery.id)}')
    print(_next_delivery)

def main():
    truck1 = Truck()
    truck2 = Truck()

    ht = HashTable()
    load_package_data(ht)

    # Load truck 1 with packages that have a deadline and no notes
    for i in range(len(ht.table)):
        if 'EOD' not in ht.lookup(i+1).deadline and not ht.lookup(i+1).notes:
            truck1.packages.append(ht.lookup(i+1))
            ht.lookup(i+1).status = "On Truck For Delivery"
    print(len(truck1.packages))

    # Load truck 1 with additional packages that have the same address
    for i in range(len(truck1.packages)):
        for j in range(len(ht.table)):
            if truck1.packages[i].address == ht.lookup(j+1).address and not ht.lookup(j+1).notes and ht.lookup(j+1).status == "At Hub":
                truck1.packages.append(ht.lookup(j+1))
                ht.lookup(j+1).status = "On Truck For Delivery"

    # Deliver packages in truck 1
    while len(truck1.packages) > 0:
        deliver_packages(truck1, ht)

    # Load truck 2 with packages that have notes (e.g., delayed packages)
    truck2.depart_time = str(datetime.time(9, 5, 0))
    for i in range(len(ht.table)):
        if ht.lookup(i+1).notes and ht.lookup(i+1).status == "At Hub" and ht.lookup(i+1).id != 9:
            truck2.packages.append(ht.lookup(i+1))
            ht.lookup(i+1).status = "On Truck For Delivery"
    print(f'truck 2 packages len: {len(truck2.packages)}')

    # Deliver packages in truck 2
    while len(truck2.packages) > 0:
        deliver_packages(truck2, ht)

    # Truck 1 return to hub
    truck1.address = "4001 South 700 East"

    # Truck 1 wait until 10:20 am for package id 9 with wrong address
    truck1.depart_time = str(datetime.time(10, 20, 0))

    # Update package id 9 address
    ht.lookup(9).address = "410 S State St"
    ht.lookup(9).zip = '84111'

    # Load Truck 1 with remaining packages
    for i in range(len(ht.table)):
        if ht.lookup(i+1).status == "At Hub":
            truck1.packages.append(ht.lookup(i+1))

    while len(truck1.packages) > 0:
        deliver_packages(truck1, ht)

    # Return truck 1 to hub
    # truck1.mileage += float(distance_between(truck1.address, "4001 South 700 East"))
    # print(f'truck1 depart time: {truck1.depart_time}')

    # for i in range(len(ht.table)):
    #     if ht.lookup(i+1).notes:
    #         truck2.packages.append(ht.lookup(i+1))
    #         ht.lookup(i+1).status = "On Truck For Delivery"
    #     # print(ht.lookup(i+1))
    #     elif 'EOD' not in ht.lookup(i+1).deadline and not ht.lookup(i+1).notes:
    #     # elif not ht.lookup(i+1).notes and len(truck1.packages) < truck1.capacity:
    #         truck1.packages.append(ht.lookup(i+1))
    #         ht.lookup(i+1).status = "On Truck For Delivery"
    #     print(ht.lookup(i+1))


    # truck1_next_delivery = truck1.packages[0]
    # print(f'truck1_next_delivery: {truck1_next_delivery}')
    # for package in truck1.packages:
    #     # print(truck1_next_delivery)
    #     if float(distance_between(truck1.address, package.address)) < float(distance_between(truck1.address, truck1_next_delivery.address)):
    #         truck1_next_delivery = package
    #     print(distance_between(truck1.address, package.address))
    # print(f'truck1_next_delvivery: {truck1_next_delivery}')
    # print(distance_between(truck1.address, truck1_next_delivery.address))
    # print(len(truck1.packages))
    # print(truck1.mileage)
    # deliver_packages(truck1, ht)

    # while len(truck1.packages) > 0:
    #     deliver_packages(truck1, ht)
    print(len(truck1.packages))
    print(truck1.mileage)
    print(truck1.depart_time)

    # num = 0
    # for i in range(len(ht.table)):
    #     if 'Delivered' in ht.lookup(i+1).status and ht.lookup(i+1).notes:
    #         num += 1
    #         print(ht.lookup(i+1))
    # print(num)

    num = 0
    for i in range(len(ht.table)):
        if 'EOD' not in ht.lookup(i+1).deadline:
            num += 1
            print(ht.lookup(i+1))
    print(num)

if __name__ == '__main__':
    main()