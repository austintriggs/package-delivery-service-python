# WGUPS Package Delivery Service

A Python-based package delivery service simulation for WGU C950 - Data Structures and Algorithms II. This project implements an efficient route planning and delivery distribution system for the Western Governors University Parcel Service (WGUPS).

## Project Overview

The WGUPS needs to optimize their daily local deliveries (DLD) to ensure packages are delivered on time while maintaining efficiency. This project provides a solution for managing deliveries in Salt Lake City with the following constraints:
- Three trucks and two drivers
- Average of 40 packages per day
- Combined total distance must be under 140 miles
- All packages must be delivered by their deadlines

## Features

- Efficient route planning algorithm
- Real-time package tracking
- Interactive command-line interface
- Package status monitoring by various criteria
- Support for special delivery requirements
- Distance optimization
- Time-based delivery scheduling

## Project Structure

```
package-delivery-service-python/
├── main.py              # Application entry point
├── delivery_service.py  # Core delivery logic and algorithms
├── ui.py               # User interface implementation
├── config.py           # Configuration settings
├── hashtable.py        # Custom hash table implementation
├── package.py          # Package class definition
├── truck.py            # Truck class definition
└── csv_files/          # Data files for locations and packages
```

## Requirements

- Python 3

## Setup and Installation

1. Clone the repository:
   ```bash
   git clone https://github.com/austintriggs/package-delivery-service-python.git
   cd package-delivery-service-python
   ```

2. Run the application:
   ```bash
   python main.py
   ```

## Usage

The application provides an interactive command-line interface where you can:
- View package status at any time
- Track delivery progress
- Monitor truck locations
- Check delivery times
- View total distance traveled

## Key Assumptions

- Each truck can carry a maximum of 16 packages
- Trucks travel at an average speed of 18 mph
- No fuel constraints or collisions
- Two drivers for three trucks
- Hub departure time: 8:00 AM
- Instantaneous loading and delivery times
- Package #9 address correction at 10:20 AM
- Bidirectional equal distances between locations

## Implementation Details

The project uses several key data structures and algorithms:
- Custom hash table for efficient package lookup
- Graph-based route optimization
- Time-based scheduling system
- Priority-based package assignment