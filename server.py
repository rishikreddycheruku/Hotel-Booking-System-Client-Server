import socket
import pickle
import sqlite3
import threading

# Sample in-memory database of bank accounts
bank_accounts = [
    {'account_number': '12345', 'password': 'pass', 'balance': 100000.00},
    {'account_number': '54321', 'password': 'pass', 'balance': 50000.00},
]

# Database setup and functions
def setup_database():
    conn = sqlite3.connect('hotel_booking.db')
    cursor = conn.cursor()
    
    cursor.execute("DROP TABLE IF EXISTS Hotel")
    cursor.execute("DROP TABLE IF EXISTS RoomType")
    cursor.execute("DROP TABLE IF EXISTS Transport")
    
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS Transport (
        id INTEGER PRIMARY KEY,
        type TEXT,
        cost REAL,
        origin TEXT,
        destination TEXT
    )
    ''')

    cursor.execute('''
    CREATE TABLE IF NOT EXISTS Hotel (
        id INTEGER PRIMARY KEY,
        name TEXT,
        destination TEXT
    )
    ''')

    cursor.execute('''
    CREATE TABLE IF NOT EXISTS RoomType (
        id INTEGER PRIMARY KEY,
        hotel_id INTEGER,
        type TEXT,
        cost REAL,
        FOREIGN KEY(hotel_id) REFERENCES Hotel(id)
    )
    ''')

    cursor.execute('''
    CREATE TABLE IF NOT EXISTS Bookings (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        booking_id TEXT,
        transport_type TEXT,
        origin TEXT,
        destination TEXT,
        transport_cost REAL,
        hotel_name TEXT,
        room_type TEXT,
        hotel_cost REAL,
        total_amount REAL
    )
    ''')

    # Insert transport data
    transports = [
        ('Bus', 30, 'San Francisco', 'Los Angeles'),
        ('Train', 110, 'San Francisco', 'Chicago'),
        ('Flight', 290, 'San Francisco', 'New York'),
        ('Bus', 60, 'Los Angeles', 'Chicago'),
        ('Train', 210, 'Los Angeles', 'New York'),
        ('Flight', 160, 'Los Angeles', 'San Francisco'),
        ('Flight', 240, 'Chicago', 'New York'),
        ('Bus', 80, 'Chicago', 'Los Angeles'),
        ('Bus', 80, 'Chicago', 'San Francisco'),
        ('Train', 170, 'New York', 'San Francisco'),
        ('Flight', 210, 'New York', 'Chicago'),
        ('Flight', 210, 'New York', 'Los Angeles'),
    ]
    cursor.executemany("INSERT OR IGNORE INTO Transport (type, cost, origin, destination) VALUES (?, ?, ?, ?)", transports)

    # Insert hotel data
    hotels = [
        ('Luxury Inn', 'San Francisco'),
        ('Cityscape Hotel', 'San Francisco'),
        ('Downtown Suites', 'San Francisco'),
        ('Sunset Suites', 'Los Angeles'),
        ('Beachside Hotel', 'Los Angeles'),
        ('Hollywood Heights', 'Los Angeles'),
        ('Skyline Plaza', 'Chicago'),
        ('Riverfront Suites', 'Chicago'),
        ('City Central', 'Chicago'),
        ('Bay Area Resort', 'New York'),
        ('Empire State Hotel', 'New York'),
        ('Urban Retreat', 'New York'),
    ]
    cursor.executemany("INSERT OR IGNORE INTO Hotel (name, destination) VALUES (?, ?)", hotels)

    # Insert room types data
    room_types = [
        (1, 'Single Room', 150), (1, 'Double Room', 200), (1, 'Suite', 250), (1, 'Delux Suite', 350),
        (2, 'Single Room', 80), (2, 'Double Room', 130), (2, 'Suite', 230),
        (3, 'Single Room', 80), (3, 'Double Room', 130), (3, 'Suite', 230),
        (4, 'Single Room', 110), (4, 'Double Room', 160), (4, 'Suite', 260), (4, 'Delux Suite', 360),
        (5, 'Single Room', 95), (5, 'Double Room', 145), (5, 'Suite', 245),
        (6, 'Single Room', 85), (6, 'Double Room', 135), (6, 'Suite', 235),
        (7, 'Single Room', 105), (7, 'Double Room', 155), (7, 'Suite', 255), (7, 'Delux Suite', 370),
        (8, 'Single Room', 75), (8, 'Double Room', 125), (8, 'Suite', 225),
        (9, 'Single Room', 110), (9, 'Double Room', 160), (9, 'Suite', 260),
        (10, 'Single Room', 120), (10, 'Double Room', 170), (10, 'Suite', 270), (10, 'Delux Suite', 400),
        (11, 'Single Room', 130), (11, 'Double Room', 180), (11, 'Suite', 290),
        (12, 'Single Room', 140), (12, 'Double Room', 190), (12, 'Suite', 300),
    ]

    cursor.executemany("INSERT INTO RoomType (hotel_id, type, cost) VALUES (?, ?, ?)", room_types)

    conn.commit()
    conn.close()

def validate_bank_credentials(account_number, password):
    for account in bank_accounts:
        if account['account_number'] == account_number and account['password'] == password:
            return account
    return None

def has_sufficient_balance(account, total_amount):
    return account['balance'] >= total_amount

def process_payment(request):
    account_number = request.get('account_number')
    password = request.get('password')
    total_amount = request.get('total_amount')

    account = validate_bank_credentials(account_number, password)
    if account and has_sufficient_balance(account, total_amount):
        account['balance'] -= total_amount
        return {'status': 'success'}
    else:
        return {'status': 'failure', 'message': 'Invalid account credentials or insufficient balance'}

def get_available_cities():
    conn = sqlite3.connect('hotel_booking.db')
    cursor = conn.cursor()

    cursor.execute("SELECT DISTINCT origin FROM Transport")
    origin_cities = [row[0] for row in cursor.fetchall()]
    cursor.execute("SELECT DISTINCT destination FROM Transport")
    destination_cities = [row[0] for row in cursor.fetchall()]
    cursor.execute("SELECT DISTINCT destination FROM Hotel")
    hotel_cities = [row[0] for row in cursor.fetchall()]

    all_cities = set(origin_cities + destination_cities + hotel_cities)
    conn.close()
    
    return list(all_cities)

def get_transport_options(origin, destination):
    conn = sqlite3.connect('hotel_booking.db')
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM Transport WHERE origin=? AND destination=?", (origin, destination))
    transport_options = cursor.fetchall()
    conn.close()
    return transport_options

def get_hotel_options(destination):
    conn = sqlite3.connect('hotel_booking.db')
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM Hotel WHERE destination=?", (destination,))
    hotel_options = cursor.fetchall()
    conn.close()
    return hotel_options

def get_room_types(hotel_id):
    conn = sqlite3.connect('hotel_booking.db')
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM RoomType WHERE hotel_id=?", (hotel_id,))
    room_types = cursor.fetchall()
    conn.close()
    return room_types

def save_booking(booking_details):
    try:
        conn = sqlite3.connect('hotel_booking.db')
        cursor = conn.cursor()
        cursor.execute(''' 
        INSERT INTO Bookings (booking_id, transport_type, origin, destination, transport_cost, hotel_name, room_type, hotel_cost, total_amount)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
        ''', (booking_details['booking_id'], booking_details['transport_type'], booking_details['origin'], booking_details['destination'],
              booking_details['transport_cost'], booking_details['hotel_name'], booking_details['room_type'], booking_details['hotel_cost'], booking_details['total_amount']))
        conn.commit()
    except Exception as e:
        print(f"Database error: {e}")
    finally:
        conn.close()

def handle_client(conn):
    with conn:
        try:
            request = pickle.loads(receive_all(conn))
            print(f"Received request: {request}")

            if request['action'] == 'fetch_cities':
                cities = get_available_cities()
                conn.sendall(pickle.dumps(cities))
                print(f"Sent response: {cities}")

            elif request['action'] == 'fetch_transports':
                transport_options = get_transport_options(request['origin'], request['destination'])
                conn.sendall(pickle.dumps(transport_options))
                print(f"Sent response: {transport_options}")

            elif request['action'] == 'fetch_hotels':
                hotel_options = get_hotel_options(request['destination'])
                conn.sendall(pickle.dumps(hotel_options))
                print(f"Sent response: {hotel_options}")

            elif request['action'] == 'fetch_room_types':
                room_types = get_room_types(request['hotel_id'])
                conn.sendall(pickle.dumps(room_types))
                print(f"Sent response: {room_types}")

            elif request['action'] == 'process_payment':
                result = process_payment(request)
                conn.sendall(pickle.dumps(result))
                print(f"Sent response: {result}")

            elif request['action'] == 'save_booking':
                booking_details = request['booking']
                save_booking(booking_details)
                response = {'status': 'success'}
                conn.sendall(pickle.dumps(response))
                print(f"Sent response: {response}")

        except Exception as e:
            print(f"Error handling client: {e}")
            conn.sendall(pickle.dumps({'status': 'failure', 'message': str(e)}))

def receive_all(sock, buffer_size=4096):
    data = b''
    while True:
        part = sock.recv(buffer_size)
        data += part
        if len(part) < buffer_size:
            break
    return data

def start_server():
    setup_database()
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.bind(('127.0.0.1', 12345))
    server_socket.listen(5)
    print("Server started and listening for connections.")

    while True:
        conn, addr = server_socket.accept()
        print(f"Connected by {addr}")
        threading.Thread(target=handle_client, args=(conn,)).start()

if __name__ == "__main__":
    start_server()
