# Student ID: 010873710
import copy
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
    _truck_time = datetime.datetime.strptime(truck.depart_time, "%H:%M:%S").time()
    _time_object = datetime.datetime.combine(datetime.date.today(), _truck_time)
    _delivery_time = (_time_object + datetime.timedelta(minutes=_time)).time()
    truck.depart_time = str(_delivery_time)

    # Update truck mileage
    truck.mileage += float(distance_between(truck.address, _next_delivery.address))

    # Update truck location
    truck.address = _next_delivery.address

    # Remove package from truck package list
    truck.packages.remove(_next_delivery)

    # Mark package as delivered and update delivery time
    ht.lookup(_next_delivery.id).status = "Delivered"
    ht.lookup(_next_delivery.id).delivery_time = str(_delivery_time)

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
            ht.lookup(i+1).departure_time = truck1.depart_time
            ht.lookup(i+1).delivery_truck = "truck1"

    # Load truck 1 with additional packages that have the same address
    for i in range(len(truck1.packages)):
        for j in range(len(ht.table)):
            if truck1.packages[i].address == ht.lookup(j+1).address and not ht.lookup(j+1).notes and ht.lookup(j+1).status == "At Hub":
                truck1.packages.append(ht.lookup(j+1))
                ht.lookup(j+1).status = "On Truck For Delivery"
                ht.lookup(j+1).departure_time = truck1.depart_time
                ht.lookup(i + 1).delivery_truck = "truck1"

    # Packages for truck 1 delivery 1 08:00 AM - 9:20 AM
    # truck1_delivery_1 = copy.deepcopy(truck1.packages)
    # print(f'truck1_delivery_1: {truck1_delivery_1}')

    # Deliver packages in truck 1
    while len(truck1.packages) > 0:
        deliver_packages(truck1, ht)

    # Load truck 2 with packages that have notes (e.g., delayed packages)
    truck2.depart_time = str(datetime.time(9, 5, 0))
    for i in range(len(ht.table)):
        if ht.lookup(i+1).notes and ht.lookup(i+1).status == "At Hub" and ht.lookup(i+1).id != 9:
            truck2.packages.append(ht.lookup(i+1))
            ht.lookup(i+1).status = "On Truck For Delivery"
            ht.lookup(i+1).departure_time = truck2.depart_time
            ht.lookup(i+1).delivery_truck = "truck2"

    # Packages for truck 2 delivery 1 09:05 AM - 10:57 AM
    # truck2_delivery_1 = truck2.packages
    # print(f'truck1_delivery_2: {truck2_delivery_1}')

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
            ht.lookup(i+1).departure_time = truck1.depart_time
            ht.lookup(i + 1).delivery_truck = "truck1_2"

    # Packages for truck 1 delivery 2 at 10:20 AM - 12:30 PM
    # truck1_delivery_2 = truck1.packages

    # Deliver packages
    while len(truck1.packages) > 0:
        deliver_packages(truck1, ht)

    # num = 0
    # for i in range(len(ht.table)):
    #     if 'EOD' not in ht.lookup(i+1).deadline:
    #         num += 1
    #         print(ht.lookup(i+1))
    # print(num)

    print("===========================================")
    print("Western Governors University Parcel Service")
    print("===========================================")

    # Display menu options
    print("\nPlease select a menu option to generate a report or retrieve package information\n")
    print("\t 1. Print All Package Status and Total Mileage")
    print("\t 2. Print a Single Package Status with a Time")
    print("\t 3. Print All Package Status Between Two Times")
    print("\t 4. Exit")

    valid_options = [1, 2, 3, 4]

    # Prompt the user for option selection
    option = None

    while option is None:
        user_input = input("\nEnter Menu Option: ")

        if user_input.isdigit() and int(user_input) in valid_options:
            option = int(user_input)
        else:
            print("Error: Invalid option provided.")

    if option == 1:
        for i in range(len(ht.table)):
            print(f'PackageID: {ht.lookup(i+1).id}, Address: {ht.lookup(i+1).address}, City: {ht.lookup(i+1).city},'
                  f'State: {ht.lookup(i+1).state}, Zip: {ht.lookup(i+1).zip}, Deadline: {ht.lookup(i+1).deadline},'
                  f'Status: {ht.lookup(i+1).status}, Delivery Time: {ht.lookup(i+1).delivery_time}')
        print(f'Total Mileage: {truck1.mileage + truck2.mileage}')

    if option == 2:
        pid = int(input("Enter Package ID: "))
        hr = int(input("Enter Hour (0 - 23): "))
        min = int(input("Enter Minute (0 - 59): "))
        package = ht.lookup(pid)
        lookup_time = str(datetime.time(hr, min, 0))

        if lookup_time >= package.delivery_time:
            print(f"Package ID: {package.id}, Package Status: Delivered at {package.delivery_time}")

        elif package.delivery_time > lookup_time >= package.departure_time:
            print(f"Package ID: {package.id}, Package Status: Out for delivery. Departed hub at {package.departure_time}")

        else:
            print(f"Package ID: {package.id}, Package Status: At Hub")

    if option == 3:
        start_hr = int(input("Enter Start Hour (0 - 23): "))
        start_min = int(input("Enter Start Minute (0 - 59): "))
        finish_hr = int(input("Enter Finish Hour (0 - 23): "))
        finish_min = int(input("Enter Finish Minute (0 - 59): "))
        start_time = str(datetime.time(start_hr, start_min, 0))
        finish_time = str(datetime.time(finish_hr, finish_min, 0))
        _truck1_ = []
        _truck2_ = []

# Truck 1_1 : 8:00 - 9:20
# Truck 1_2: 10:20 - 12:30
# Truck 2: 9:05 - 10:57
        for i in range(len(ht.table)):
            if ht.lookup(i+1).departure_time <= start_time and finish_time >= ht.lookup(i+1).delivery_time\
                    or finish_time >= ht.lookup(i+1).departure_time:
                if ht.lookup(i+1).delivery_truck == 'truck1' or ht.lookup(i+1).delivery_truck == 'truck1_2':
                    _truck1_.append(ht.lookup(i+1))
                if ht.lookup(i+1).delivery_truck == 'truck2':
                    _truck2_.append(ht.lookup(i+1))
        print('\nTruck 1:')
        for package in _truck1_:
            if package.delivery_time > finish_time:
                package.status = 'On Truck For Delivery'
            if package.status == 'On Truck For Delivery':
                print(f'PackageID: {package.id}, Package Status: {package.status}, Departed At: {package.departure_time}')
            if package.status == 'Delivered':
                print(f'PackageID: {package.id}, Package Status: {package.status}, Delivered At: {package.delivery_time}')

        print('\nTruck 2:')
        for package in _truck2_:
            if package.delivery_time > finish_time:
                package.status = 'On Truck For Delivery'
            if package.status == 'On Truck For Delivery':
                print(
                    f'PackageID: {package.id}, Package Status: {package.status}, Departed At: {package.departure_time}')
            if package.status == 'Delivered':
                print(
                    f'PackageID: {package.id}, Package Status: {package.status}, Delivered At: {package.delivery_time}')

    if option == 4:
        exit()

if __name__ == '__main__':
    main()