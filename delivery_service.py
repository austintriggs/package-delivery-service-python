import csv
import datetime
from config import *
from package import Package
from hashtable import HashTable
from truck import Truck

class DeliveryService:
    def __init__(self):
        self.hash_table = HashTable()
        self.truck1 = Truck()
        self.truck2 = Truck()
        self.load_package_data()

    # Time Complexity: O(n) where n is number of packages in CSV
    # Space Complexity: O(n) for storing packages in hash table
    def load_package_data(self):
        """Load package data from CSV file into hash table."""
        with open(PACKAGE_FILE) as package_info:
            packages = csv.reader(package_info)
            for package in packages:
                p = Package(
                    int(package[0]),  # id
                    package[1],       # address
                    package[2],       # city
                    package[3],       # state
                    package[4],       # zip
                    package[5],       # deadline
                    package[6],       # weight
                    package[7],       # notes
                    "At Hub"          # status
                )
                self.hash_table.insert(p.id, p)

    # Time Complexity: O(n²) where n is number of addresses (due to nested loops for distance matrix)
    # Space Complexity: O(n²) for storing the distance matrix
    def load_distance_data(self):
        """Load and process distance data from CSV file."""
        distance_list = []
        with open(DISTANCE_FILE) as distance_info:
            distances = csv.reader(distance_info)
            for distance in distances:
                distance_list.append(distance)

            for i in range(len(distance_list)):
                for j in range(len(distance_list)):
                    distance_list[i][j] = distance_list[j][i]
        return distance_list

    # Time Complexity: O(n) where n is number of addresses in CSV
    # Space Complexity: O(n) for storing address list
    def load_address_data(self):
        """Load address data from CSV file."""
        address_list = []
        with open(ADDRESS_FILE) as address_info:
            addresses = csv.reader(address_info)
            for address in addresses:
                address_list.append(address[2])
        return address_list

    # Time Complexity: O(n) where n is number of addresses (due to index lookup)
    # Space Complexity: O(1) as it only returns a single value
    def distance_between(self, address1, address2):
        """Calculate distance between two addresses."""
        distance_list = self.load_distance_data()
        address_list = self.load_address_data()
        return distance_list[address_list.index(address1)][address_list.index(address2)]

    # Time Complexity: O(n) where n is number of packages on truck (due to min operation)
    # Space Complexity: O(1) as it only updates existing objects
    def deliver_packages(self, truck):
        """Deliver packages for a given truck."""
        if not truck.packages:
            return

        # Find closest package
        next_delivery = min(truck.packages, 
                          key=lambda p: float(self.distance_between(truck.address, p.address)))

        # Calculate delivery time
        distance = float(self.distance_between(truck.address, next_delivery.address))
        time_minutes = round(60 * distance / truck.speed)
        truck_time = datetime.datetime.strptime(truck.depart_time, "%H:%M:%S").time()
        time_object = datetime.datetime.combine(datetime.date.today(), truck_time)
        delivery_time = (time_object + datetime.timedelta(minutes=time_minutes)).time()
        
        # Update truck and package status
        truck.depart_time = str(delivery_time)
        truck.mileage += distance
        truck.address = next_delivery.address
        truck.packages.remove(next_delivery)

        package = self.hash_table.lookup(next_delivery.id)
        package.status = "Delivered"
        package.delivery_time = str(delivery_time)

    # Time Complexity: O(n²) where n is number of packages (due to nested loops for address matching)
    # Space Complexity: O(1) as it only updates existing objects
    def load_truck1_first_delivery(self):
        """Load truck 1 with packages that have deadlines and no special notes."""
        for i in range(len(self.hash_table.table)):
            package = self.hash_table.lookup(i+1)
            if 'EOD' not in package.deadline and not package.notes:
                self.truck1.packages.append(package)
                package.status = "On Truck For Delivery"
                package.departure_time = self.truck1.depart_time
                package.delivery_truck = "Truck #1, Delivery #1"

        # Load additional packages with same addresses
        for package in self.truck1.packages[:]:
            for i in range(len(self.hash_table.table)):
                other_package = self.hash_table.lookup(i+1)
                if (package.address == other_package.address and 
                    not other_package.notes and 
                    other_package.status == "At Hub"):
                    self.truck1.packages.append(other_package)
                    other_package.status = "On Truck For Delivery"
                    other_package.departure_time = self.truck1.depart_time
                    other_package.delivery_truck = "Truck #1, Delivery #1"

    # Time Complexity: O(n) where n is number of packages
    # Space Complexity: O(1) as it only updates existing objects
    def load_truck2(self):
        """Load truck 2 with packages that have special notes."""
        self.truck2.depart_time = TRUCK2_DEPARTURE_TIME
        for i in range(len(self.hash_table.table)):
            package = self.hash_table.lookup(i+1)
            if (package.notes and 
                package.status == "At Hub" and 
                package.id != 9):
                self.truck2.packages.append(package)
                package.status = "On Truck For Delivery"
                package.departure_time = self.truck2.depart_time
                package.delivery_truck = "Truck #2, Delivery #1"

    # Time Complexity: O(n) where n is number of packages
    # Space Complexity: O(1) as it only updates existing objects
    def load_truck1_second_delivery(self):
        """Load truck 1 with remaining packages after package 9 correction."""
        self.truck1.address = HUB_ADDRESS
        self.truck1.depart_time = PACKAGE_9_CORRECTION_TIME
        
        # Update package 9 address
        package_9 = self.hash_table.lookup(9)
        package_9.address = PACKAGE_9_CORRECTED['address']
        package_9.zip = PACKAGE_9_CORRECTED['zip']

        # Load remaining packages
        for i in range(len(self.hash_table.table)):
            package = self.hash_table.lookup(i+1)
            if package.status == "At Hub":
                self.truck1.packages.append(package)
                package.departure_time = self.truck1.depart_time
                package.delivery_truck = "Truck #1, Delivery #2"

    # Time Complexity: O(n²) where n is number of packages (due to deliver_packages being called multiple times)
    # Space Complexity: O(1) as it only updates existing objects
    def execute_delivery_plan(self):
        """Execute the complete delivery plan."""
        # First delivery run
        self.load_truck1_first_delivery()
        while self.truck1.packages:
            self.deliver_packages(self.truck1)

        # Second truck delivery
        self.load_truck2()
        while self.truck2.packages:
            self.deliver_packages(self.truck2)

        # Second delivery run
        self.load_truck1_second_delivery()
        while self.truck1.packages:
            self.deliver_packages(self.truck1)

    # Time Complexity: O(1) as it only performs simple addition
    # Space Complexity: O(1) as it only returns a single value
    def get_total_mileage(self):
        """Calculate total mileage for all trucks."""
        return self.truck1.mileage + self.truck2.mileage 