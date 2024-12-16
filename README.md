Here’s the updated `README.md`:

---

# Hotel-Booking-System-Client-Server

A multi-functional Hotel Booking System that combines transport and accommodation bookings with payment processing and database management. This project is designed as a networked client-server application using Python and SQLite.

---

## Features

- **Server-Side Functionalities:**
  - Dynamic database setup for hotels, rooms, and transport options.
  - Fetch available cities, transport, and hotel options.
  - Process payments and validate bank account credentials.
  - Save booking details and retrieve them when needed.

- **Client-Side Functionalities:**
  - Intuitive interface for selecting transport and hotel options.
  - Process payments securely.
  - Save booking details on the server.

- **View Bookings:**
  - View all bookings stored in the database in a tabular format.

---

## File Descriptions

### 1. `server.py`
Handles all server-side operations:
- Sets up the SQLite database with predefined hotels, transport, and room types.
- Processes client requests for:
  - Fetching available cities.
  - Retrieving transport and hotel options.
  - Processing payments through a mock banking system.
  - Storing booking details in the database.
- Multi-threaded to handle multiple client connections simultaneously.

### 2. `client.py`
Provides a client-side interface for:
- Selecting cities, transport options, and hotel rooms.
- Processing payments using mock bank credentials.
- Saving booking details on the server.

### 3. `view_bookings.py`
Displays all booking information stored in the database in a user-friendly tabular format.

---

## Requirements

- Python 3.7+
- SQLite (comes pre-installed with Python)
- Modules:
  - `socket`
  - `pickle`
  - `sqlite3`
  - `getpass`
  - `random`
  - `time`
  - `datetime`
  - `csv`
  - `threading`
  - `logging`

---

## Installation

1. Clone the repository:
   ```bash
   git clone https://github.com/rishikreddycheruku/Hotel-Booking-System-Client-Server.git
   cd Hotel-Booking-System-Client-Server
   ```

2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```
   (If using any additional libraries, create a `requirements.txt` file).

3. Ensure `server.py` is running:
   ```bash
   python server.py
   ```

4. Run the client to start booking:
   ```bash
   python client.py
   ```

5. To view saved bookings:
   ```bash
   python view_bookings.py
   ```

---

## Usage

### Start the Server
Run `server.py` to initialize the server and set up the database:
```bash
python server.py
```

### Use the Client
Run `client.py` to interact with the application:
1. Select origin and destination cities.
2. Choose transport and hotel options.
3. Process payment and complete booking.
4. Booking details will be saved automatically.

### View Bookings
Run `view_bookings.py` to display all saved bookings in the database:
```bash
python view_bookings.py
```

### Network Configuration
- By default, the server runs on `127.0.0.1` (localhost). 
- To enable the system to work over a network:
  - Modify the IP address in `server.py` (line with `server_socket.bind`) to the server’s local IP address (e.g., `192.168.x.x`) or `0.0.0.0` for all interfaces.
  - Update the `server_ip` variable in `client.py` to point to the same server IP.

---

## Database Schema

1. **Transport Table**: Stores details about available transport options.
2. **Hotel Table**: Stores hotel information by destination.
3. **RoomType Table**: Stores room types and costs for each hotel.
4. **Bookings Table**: Saves details of completed bookings.

---

## Example Booking Workflow

1. **Start Client**: Run `client.py` and choose an origin city.
2. **Select Destination**: Pick a destination from the available options.
3. **Choose Transport and Hotel**: Select transport and room types.
4. **Process Payment**: Enter mock bank credentials to confirm payment.
5. **Save Booking**: Booking is saved, and the client displays details.

---

## Future Improvements

- **Enhanced Authentication**: Replace mock banking with secure APIs.
- **Web-Based UI**: Build a web interface for broader accessibility.
- **Advanced Analytics**: Include detailed usage analysis and visualization.

---

## License

This project is licensed under the MIT License. See `LICENSE` for details.

---

## Acknowledgements

- SQLite for lightweight database management.
- Python for enabling fast prototyping and networking capabilities.
