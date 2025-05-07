import datetime
from config import *

class PackageDeliveryUI:
    def __init__(self, delivery_service):
        self.delivery_service = delivery_service

    def display_header(self):
        """Display the application header."""
        print("===========================================")
        print("Western Governors University Parcel Service")
        print("===========================================")

    def display_menu(self):
        """Display the menu options."""
        print("\nPlease select a menu option to generate a report or retrieve package information\n")
        for option_num, option_text in MENU_OPTIONS.items():
            print(f"\t {option_num}. {option_text}")

    def get_menu_option(self):
        """Get and validate user's menu selection."""
        while True:
            user_input = input("\nEnter Menu Option: ")
            if user_input.isdigit() and int(user_input) in MENU_OPTIONS:
                return int(user_input)
            print("Error: Invalid option provided.")

    def print_all_packages(self):
        """Print status of all packages and total mileage."""
        for i in range(len(self.delivery_service.hash_table.table)):
            package = self.delivery_service.hash_table.lookup(i+1)
            print(f'PackageID: {package.id}, Address: {package.address}, City: {package.city}, '
                  f'State: {package.state}, Zip: {package.zip}, Deadline: {package.deadline}, '
                  f'Truck: {package.delivery_truck}, Status: {package.status}, '
                  f'Delivery Time: {package.delivery_time}')
        print(f'Total Mileage: {self.delivery_service.get_total_mileage()}')

    def print_single_package(self):
        """Print status of a single package at a specific time."""
        pid = int(input("Enter Package ID: "))
        hr = int(input("Enter Hour (0 - 23): "))
        min = int(input("Enter Minute (0 - 59): "))
        package = self.delivery_service.hash_table.lookup(pid)
        lookup_time = str(datetime.time(hr, min, 0))

        # Handle package 9 address correction
        if lookup_time < PACKAGE_9_CORRECTION_TIME:
            package_9 = self.delivery_service.hash_table.lookup(9)
            package_9.address = PACKAGE_9_ORIGINAL['address']
            package_9.zip = PACKAGE_9_ORIGINAL['zip']

        if lookup_time >= package.delivery_time:
            print(f"Package ID: {package.id}, Address: {package.address}, Deadline: {package.deadline}, "
                  f"Truck: {package.delivery_truck}, Status: Delivered at {package.delivery_time}")
        elif package.delivery_time > lookup_time >= package.departure_time:
            print(f"Package ID: {package.id}, Address: {package.address}, Deadline: {package.deadline}, "
                  f"Truck: {package.delivery_truck}, Status: Out for delivery. Departed hub at {package.departure_time}")
        else:
            print(f"Package ID: {package.id}, Address: {package.address}, Deadline: {package.deadline}, "
                  f"Truck: None, Status: At Hub")

    def print_all_packages_at_time(self):
        """Print status of all packages at a specific time."""
        start_hr = int(input("Enter Start Hour (0 - 23): "))
        start_min = int(input("Enter Start Minute (0 - 59): "))
        start_time = str(datetime.time(start_hr, start_min, 0))

        # Handle package 9 address correction
        if start_time < PACKAGE_9_CORRECTION_TIME:
            package_9 = self.delivery_service.hash_table.lookup(9)
            package_9.address = PACKAGE_9_ORIGINAL['address']
            package_9.zip = PACKAGE_9_ORIGINAL['zip']

        for i in range(len(self.delivery_service.hash_table.table)):
            package = self.delivery_service.hash_table.lookup(i+1)
            
            # Update package status based on time
            if package.delivery_time > start_time:
                package.status = "On Truck for Delivery"
                package.delivery_time = "TBD"
            if package.departure_time > start_time:
                package.delivery_truck = "None"
                package.status = "At Hub"
                package.delivery_time = "TBD"

            print(f'PackageID: {package.id}, Address: {package.address}, City: {package.city}, '
                  f'State: {package.state}, Zip: {package.zip}, Deadline: {package.deadline}, '
                  f'Truck: {package.delivery_truck}, Status: {package.status}, '
                  f'Delivery Time: {package.delivery_time}')

    def run(self):
        """Run the main UI loop."""
        self.display_header()
        self.display_menu()

        while True:
            option = self.get_menu_option()

            if option == 1:
                self.print_all_packages()
            elif option == 2:
                self.print_single_package()
            elif option == 3:
                self.print_all_packages_at_time()
            elif option == 4:
                break 