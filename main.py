# Student ID: 010873710
from delivery_service import DeliveryService
from ui import PackageDeliveryUI

def main():
    # Initialize the delivery service
    delivery_service = DeliveryService()
    
    # Execute the delivery plan
    delivery_service.execute_delivery_plan()
    
    # Initialize and run the UI
    ui = PackageDeliveryUI(delivery_service)
    ui.run()

if __name__ == '__main__':
    main()