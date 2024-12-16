import socket
import pickle
import getpass
import random
import time
import datetime
import csv
import logging

# Set up logging
logging.basicConfig(level=logging.ERROR, format='%(message)s')  # Adjust to only show errors

# CSV file for performance metrics
performance_data = []

# Function to log performance metrics
def log_performance(operation, start_time, end_time, latency, rtt):
    data = {
        'latency': latency*(1000),
        'rtt': rtt*(1000)
    }
    performance_data.append(data)

def send_request(request, server_ip='127.0.0.1', port=12345):
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client_socket.connect((server_ip, port))
    
    # Measure RTT
    start_time = time.time()
    client_socket.sendall(pickle.dumps(request))
    
    # Measure latency
    latency_start_time = time.time()
    response_data = receive_all(client_socket)  # Ensure full response is received
    latency = time.time() - latency_start_time
    end_time = time.time()
    
    rtt = end_time - start_time  # Total RTT includes the time to send and receive

    log_performance(request['action'], start_time, end_time, latency, rtt)
    
    client_socket.close()
    
    return pickle.loads(response_data)

# Function to ensure full data is received before unpickling
def receive_all(sock, buffer_size=4096):
    data = b''
    while True:
        part = sock.recv(buffer_size)
        data += part
        if len(part) < buffer_size:
            break
    return data

def fetch_available_cities():
    request = {'action': 'fetch_cities'}
    cities = send_request(request)

    if not cities:
        print("No available cities.")
        return []

    print("\nAvailable Cities:")
    for index, city in enumerate(cities):
        print(f"{index + 1}. {city}")

    return cities

def fetch_destination_cities(source):
    request = {'action': 'fetch_cities'}
    cities = send_request(request)

    if not cities:
        print("No available cities.")
        return []

    destination_cities = [city for city in cities if city != source]

    print("\nAvailable Cities for Destination:")
    if not destination_cities:
        print("No cities available for destination.")
        return []

    for index, city in enumerate(destination_cities):
        print(f"{index + 1}. {city}")

    return destination_cities

def search_transport(origin, destination):
    request = {
        'action': 'fetch_transports',
        'origin': origin,
        'destination': destination
    }
    transport_options = send_request(request)

    if not transport_options:
        print("No available transport options.")
        return None

    print("\nAvailable Transport Options:")
    for index, option in enumerate(transport_options):
        print(f"{index + 1}. Type: {option[1]}, Cost: ${option[2]}")

    while True:
        try:
            choice = int(input("\nSelect a transport option (1, 2, etc.): ")) - 1
            if 0 <= choice < len(transport_options):
                return transport_options[choice]
            else:
                print("Invalid choice. Please select a valid option.")
        except ValueError:
            print("Invalid input. Please enter a number.")

def select_hotel(destination):
    request = {
        'action': 'fetch_hotels',
        'destination': destination
    }
    hotel_options = send_request(request)

    if not hotel_options:
        print("No available hotels.")
        return None, None

    print("\nAvailable Hotel Options:")
    for index, option in enumerate(hotel_options):
        print(f"{index + 1}. {option[1]}")  # Show hotel name

    hotel_choice = int(input("\nSelect a hotel option (1, 2, etc.): ")) - 1

    if 0 <= hotel_choice < len(hotel_options):
        selected_hotel = hotel_options[hotel_choice]
        room_types = select_room_type(selected_hotel[0])  # Fetch room types based on selected hotel ID
        return selected_hotel, room_types
    else:
        print("Invalid choice. Please select a valid option.")
    return None, None

def select_room_type(hotel_id):
    request = {
        'action': 'fetch_room_types',
        'hotel_id': hotel_id
    }
    room_types = send_request(request)

    if not room_types:
        print("No available room types.")
        return None

    print("\nAvailable Room Types:")
    for index, room in enumerate(room_types):
        print(f"{index + 1}. {room[2]}, Cost: ${room[3]}")  # room[2] for room type, room[3] for cost

    while True:
        try:
            choice = int(input("\nSelect a room type (1, 2, etc.): ")) - 1
            if 0 <= choice < len(room_types):
                return room_types[choice]  # Return selected room type
            else:
                print("Invalid choice. Please select a valid option.")
        except ValueError:
            print("Invalid input. Please enter a number.")

def process_payment(total_amount):
    account_number = input("\nEnter your bank account number: ")
    password = getpass.getpass("Enter your bank password: ")

    payment_request = {
        'action': 'process_payment',
        'total_amount': total_amount,
        'account_number': account_number,
        'password': password
    }

    result = send_request(payment_request)

    return result

import os

def save_performance_data():
    try:
        file_exists = os.path.isfile('performance_metrics.csv')  # Check if file exists

        # Open the CSV file in append mode
        with open('performance_metrics.csv', 'a', newline='') as csvfile:
            fieldnames = ['latency', 'rtt']
            writer = csv.DictWriter(csvfile, fieldnames=fieldnames)

            # Write the header only if the file is new or empty
            if not file_exists:  # Write header only if file does not already exist
                writer.writeheader()

            # Write the performance data to the file
            for data in performance_data:
                writer.writerow(data)

    except Exception as e:
        logging.error(f"Error saving performance data: {e}")


if __name__ == "__main__":
    print("Welcome to the Hotel Booking Application!")

    available_cities = fetch_available_cities()
    if not available_cities:
        print("No cities available. Exiting...")
        exit(1)

    origin = input("\nEnter the origin city: ").strip()
    
    if origin not in available_cities:
        print("Invalid origin city. Please restart the application and select a valid city.")
        exit(1)

    same_city_hotel = input("\nDo you want to book a hotel in the same city? (yes/no): ").strip().lower()
    destination = origin 
    if same_city_hotel in ['yes', 'y']:
        destination = origin
    else:
        destination_cities = fetch_destination_cities(origin)
        if not destination_cities:
            print("No valid destination cities available.")
            exit(1)
        destination = input("\nEnter the destination city: ").strip()
        if destination not in destination_cities:
            print("Invalid destination. Please restart the application and select a valid city.")
            exit(1)

    hotel, room_type = select_hotel(destination)

    transport = None
    if destination != origin:
        transport_booking = input("\nWould you like to book transport as well? (yes/no): ").strip().lower()
        if transport_booking in ['yes', 'y']:
            transport = search_transport(origin, destination)
    
    # Calculate total amount
    transport_cost = transport[2] if transport else 0
    hotel_cost = room_type[3]  # Only room type cost
    total_amount = transport_cost + hotel_cost

    # Process payment
    payment_result = process_payment(total_amount)

    if payment_result and payment_result['status'] == 'success':
        print("\nPayment Successful!")

        # Prepare booking details
        booking_id = f"BOOK-{random.randint(1000, 9999)}"
        booking_details = {
            'booking_id': booking_id,
            'transport_type': transport[1] if transport else None,
            'origin': origin,
            'destination': destination,
            'transport_cost': transport_cost,
            'hotel_name': hotel[1] if hotel else None,
            'room_type': room_type[2],
            'hotel_cost': hotel_cost,
            'total_amount': total_amount
        }
        
        # Save booking
        save_request = {
            'action': 'save_booking',
            'booking': booking_details
        }
        save_result = send_request(save_request)

        # Print booking details
        if save_result['status'] == 'success':
            print("\nBooking Details:")
            print(f"  Booking ID: {booking_id}")
            print(f"  Total Amount: ${total_amount}")
        else:
            print("\nFailed to save booking.")
    else:
        print(f"Payment Failed: {payment_result.get('message', 'Unknown error')}")

    print("\nThank you for using the Hotel Booking Application!")

    # Save performance data at the end
    save_performance_data()
