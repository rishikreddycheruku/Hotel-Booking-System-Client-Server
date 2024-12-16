import sqlite3

def view_bookings():
    # Connect to the SQLite database
    conn = sqlite3.connect('hotel_booking.db')
    cursor = conn.cursor()
    
    # Query to fetch all bookings
    cursor.execute('''
    SELECT booking_id, transport_type, origin AS source, destination, transport_cost, hotel_name, room_type, hotel_cost, total_amount
    FROM Bookings
    ''')
    
    bookings = cursor.fetchall()
    
    # Check if there are bookings
    if not bookings:
        print("No bookings found.")
    else:
        print("Bookings:")
        print(f"{'Booking ID':<15} {'Transport':<15} {'Source':<15} {'Destination':<15} {'Transport Cost':<15} {'Hotel Name':<20} {'Room Type':<20} {'Hotel Cost':<10} {'Total Amount':<10}")
        for booking in bookings:
            booking_id, transport_type, source, destination, transport_cost, hotel_name, room_type, hotel_cost, total_amount = booking

            # Handle None values by providing default values
            transport_type = transport_type or 'N/A'
            transport_cost = transport_cost if transport_cost is not None else 0
            hotel_name = hotel_name or 'N/A'
            room_type = room_type or 'N/A'
            hotel_cost = hotel_cost if hotel_cost is not None else 0
            total_amount = total_amount if total_amount is not None else 0

            # Print the booking details with proper formatting
            print(f"{booking_id:<15} {transport_type:<15} {source:<15} {destination:<15} ${transport_cost:<14} {hotel_name:<20} {room_type :<20} ${hotel_cost:<10} ${total_amount:<10}")
    
    # Close the database connection
    conn.close()

# Call the view_bookings function to display bookings
if __name__ == "__main__":
    view_bookings()
