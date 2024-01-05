import cv2
import sqlite3
import csv
import qrcode
def create_connection():
    try:
        connection=sqlite3.connect('qr_codes.sql')
        cursor=connection.cursor()
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS qr_codes (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                filename TEXT,
                qr_value TEXT
            )
        ''')
        connection.commit()
        return connection
    except sqlite3.Error as e:
        print(f"Error: {e}")
        return None
def insert_qr_code(filename, qr_value):
    try:
        connection = create_connection()
        cursor = connection.cursor()
        cursor.execute("INSERT INTO qr_codes (filename, qr_value) VALUES (?, ?)", (filename, qr_value))
        connection.commit()
        connection.close()
    except sqlite3.Error as e:
        print(f"Error: {e}")
def read_qr_code(filename):
    try:
        img=cv2.imread(filename)
        detect=cv2.QRCodeDetector()
        value, points, straight_qrcode=detect.detectAndDecode(img)
        if value:
            insert_qr_code(filename, value)
            export_to_csv()
        return value
    except Exception as e:
        print(f"Error: {e}")
        return None
def export_to_csv():
    try:
        connection=create_connection()
        cursor=connection.cursor()
        cursor.execute('SELECT * FROM qr_codes')
        rows=cursor.fetchall()
        with open('qr_codes.csv', 'w', newline='') as csvfile:
            csv_writer=csv.writer(csvfile)
            csv_writer.writerow(['ID', 'Filename', 'QR Value'])
            for row in rows:
                csv_writer.writerow(row)
    except sqlite3.Error as e:
        print(f"Error: {e}")
def encode_link_to_qr(link, filename):
    qr=qrcode.QRCode(version=1, error_correction=qrcode.constants.ERROR_CORRECT_L, box_size=10, border=4)
    qr.add_data(link)
    qr.make(fit=True)
    img=qr.make_image(fill_color="black", back_color="white")
    img.save(filename)
def switch_case(choice):
    if choice == 1:
        filename=input("Enter the filename: ")
        value=read_qr_code(filename)
        print(f"QR Code Value: {value}")
    elif choice == 2:
        link=input("Enter the link to encode: ")
        filename=input("Enter the filename to save the QR code: ")
        encode_link_to_qr(link, filename)
        print(f"QR Code for {link} saved to {filename}")
if __name__ == "__main__":
    while True:
        print("1.Read QR Code from Image")
        print("2.Encode Link to QR Code and Save")
        print("3.Exit")
        choice=int(input("Enter your choice: "))
        if choice == 3 or choice > 3:
            print("Thank you for using TejasQR.Have a Nice Day!")
            break
        switch_case(choice)
