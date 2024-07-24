import mysql.connector as pymysql
from datetime import datetime

passwrd = None
db = None  
C = None

def base_check():
    check = 0
    db = pymysql.connect(host="localhost", user="root", password=passwrd)
    cursor = db.cursor()
    cursor.execute('SHOW DATABASES')
    result = cursor.fetchall()
    for r in result:
        for i in r:
            if i == 'hotel_management':
                cursor.execute('USE hotel_management')
                check = 1
    if check != 1:
        create_database()

def table_check():
    db = pymysql.connect(host="localhost", user="root", password=passwrd)
    cursor = db.cursor()
    cursor.execute('SHOW DATABASES')
    result = cursor.fetchall()
    for r in result:
        for i in r:
            if i == 'hotel_management':
                cursor.execute('USE hotel_management')
                cursor.execute('SHOW TABLES')
                result = cursor.fetchall()
                if len(result) <= 2:
                    create_tables()
                else:
                    print('      Booting systems...')

def create_database():
    try:
        db = pymysql.connect(host="localhost", user="root", password=passwrd)
        cursor = db.cursor()
        cursor.execute("CREATE DATABASE IF NOT EXISTS hotel_management")
        db.commit()
        db.close()
        print("Database 'hotel_management' created successfully.")
    except pymysql.Error as e:
        print(f"Error creating database: {str(e)}")

def create_tables():
    try:
        db = pymysql.connect(host="localhost", user="root", password=passwrd, database="hotel_management")
        cursor = db.cursor()
        
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS rooms (
                ROOM_ID INT PRIMARY KEY,
                ROOM_TYPE VARCHAR(255),
                PRICE DECIMAL(10, 2),
                AVAILABLE INT
            )
        """)
        
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS customers (
                CUSTOMER_ID INT PRIMARY KEY,
                NAME VARCHAR(255),
                PHONE_NO VARCHAR(15)
            )
        """)
        
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS bookings (
                BOOKING_ID INT AUTO_INCREMENT PRIMARY KEY,
                CUSTOMER_ID INT,
                ROOM_ID INT,
                CHECK_IN_DATE DATE,
                CHECK_OUT_DATE DATE,
                TOTAL_AMOUNT DECIMAL(10, 2),
                FOREIGN KEY (CUSTOMER_ID) REFERENCES customers(CUSTOMER_ID),
                FOREIGN KEY (ROOM_ID) REFERENCES rooms(ROOM_ID)
            )
        """)
        
        db.commit()
        db.close()
        print("Tables 'rooms', 'customers', and 'bookings' created successfully.")
    except pymysql.Error as e:
        print(f"Error creating tables: {str(e)}")

def add_room():
    room_id = int(input("Enter Room ID: "))
    room_type = input("Enter Room Type: ")
    price = float(input("Enter Room Price: "))
    available = int(input("Enter Number of Available Rooms: "))
    data = (room_id, room_type, price, available)
    sql = "INSERT INTO rooms (ROOM_ID, ROOM_TYPE, PRICE, AVAILABLE) VALUES (%s, %s, %s, %s)"
    try:
        C.execute(sql, data)
        db.commit()
        print('Room added successfully...')
    except pymysql.Error as e:
        print(f"Error adding room: {str(e)}")

def view_rooms():
    C.execute("SELECT * FROM rooms")
    result = C.fetchall()
    for r in result:
        print(r)

def update_room():
    room_id = int(input("Enter Room ID to update: "))
    field = input("Enter field to update [ROOM_TYPE, PRICE, AVAILABLE]: ")
    new_value = input(f"Enter new value for {field}: ")
    if field == 'PRICE':
        new_value = float(new_value)
    elif field == 'AVAILABLE':
        new_value = int(new_value)
    sql = f"UPDATE rooms SET {field} = %s WHERE ROOM_ID = %s"
    try:
        C.execute(sql, (new_value, room_id))
        db.commit()
        print('Room updated successfully...')
    except pymysql.Error as e:
        print(f"Error updating room: {str(e)}")

def delete_room():
    room_id = int(input("Enter Room ID to delete: "))
    sql = "DELETE FROM rooms WHERE ROOM_ID = %s"
    try:
        C.execute(sql, (room_id,))
        db.commit()
        print('Room deleted successfully...')
    except pymysql.Error as e:
        print(f"Error deleting room: {str(e)}")

def register_customer():
    customer_id = int(input("Enter Customer ID: "))
    name = input("Enter Customer Name: ")
    phone_no = input("Enter Customer Phone Number: ")
    data = (customer_id, name, phone_no)
    sql = "INSERT INTO customers (CUSTOMER_ID, NAME, PHONE_NO) VALUES (%s, %s, %s)"
    try:
        C.execute(sql, data)
        db.commit()
        print('Customer registered successfully...')
    except pymysql.Error as e:
        print(f"Error registering customer: {str(e)}")

def view_customers():
    C.execute("SELECT * FROM customers")
    result = C.fetchall()
    for r in result:
        print(r)

def book_room():
    customer_id = int(input("Enter Customer ID: "))
    room_id = int(input("Enter Room ID: "))
    check_in_date = input("Enter Check-In Date (YYYY-MM-DD): ")
    check_out_date = input("Enter Check-Out Date (YYYY-MM-DD): ")
    total_amount = float(input("Enter Total Amount: "))
    data = (customer_id, room_id, check_in_date, check_out_date, total_amount)
    sql = "INSERT INTO bookings (CUSTOMER_ID, ROOM_ID, CHECK_IN_DATE, CHECK_OUT_DATE, TOTAL_AMOUNT) VALUES (%s, %s, %s, %s, %s)"
    try:
        C.execute(sql, data)
        db.commit()
        print('Room booked successfully...')
    except pymysql.Error as e:
        print(f"Error booking room: {str(e)}")

def view_bookings():
    C.execute("SELECT * FROM bookings")
    result = C.fetchall()
    for r in result:
        print(r)

def main():
    global passwrd
    passwrd = input("Enter password for MySQL: ")

    base_check()
    table_check()
    
    global db, C
    db = pymysql.connect(host="localhost", user="root", password=passwrd, database="hotel_management")
    C = db.cursor()
    
    while True:
        log = input("For Admin: A, For Customer: C, Exit: X ::: ")
        if log.upper() == "A":
            while True:
                menu = input('''Add Room: AR, View Rooms: VR, Update Room: UR, Delete Room: DR, Register Customer: RC, View Customers: VC, Book Room: BR, View Bookings: VB, Exit: X :::''')
                if menu.upper() == 'AR':
                    add_room()
                elif menu.upper() == 'VR':
                    view_rooms()
                elif menu.upper() == 'UR':
                    update_room()
                elif menu.upper() == 'DR':
                    delete_room()
                elif menu.upper() == 'RC':
                    register_customer()
                elif menu.upper() == 'VC':
                    view_customers()
                elif menu.upper() == 'BR':
                    book_room()
                elif menu.upper() == 'VB':
                    view_bookings()
                elif menu.upper() == 'X':
                    break
                else:
                    print("Wrong Input")
                    
        elif log.upper() == "C":
            print("Customer Interface")
            # Customer-specific functionalities can be added here.
            
        elif log.upper() == "X":
            break
        else:
            print("Wrong Input")

if __name__ == "__main__":
    main()
