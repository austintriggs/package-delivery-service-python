# Configuration constants for the package delivery service

# File paths
PACKAGE_FILE = "csv_files/packages.csv"
DISTANCE_FILE = "csv_files/distances.csv"
ADDRESS_FILE = "csv_files/addresses.csv"

# Hub address
HUB_ADDRESS = "4001 South 700 East"

# Time constants
PACKAGE_9_CORRECTION_TIME = "10:20:00"
TRUCK2_DEPARTURE_TIME = "09:05:00"

# Package 9 original and corrected addresses
PACKAGE_9_ORIGINAL = {
    'address': '300 State St',
    'zip': '84103'
}

PACKAGE_9_CORRECTED = {
    'address': '410 S State St',
    'zip': '84111'
}

# Menu options
MENU_OPTIONS = {
    1: "Print All Package Status and Total Mileage",
    2: "Print a Single Package Status with a Time",
    3: "Print All Package Status with a Time",
    4: "Exit"
} 