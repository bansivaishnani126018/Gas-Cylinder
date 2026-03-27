import json
import datetime

# 👉 Load data
try:
    with open("gas_data.json", "r") as file:
        data = json.load(file)
        customers = data["customers"]
        bookings = data["bookings"]
        stock = data["stock"]
        booking_id_counter = data["booking_id"]
except:
    customers = {
        "7077": {"name": "Rahul Patel", "address": "Rajkot", "mobile": "9876543210"},
        "7078": {"name": "Amit Shah", "address": "Ahmedabad", "mobile": "9123456780"},
        "7114": {"name": "Priya Mehta", "address": "Surat", "mobile": "9988776655"},
        "7102": {"name": "Karan Joshi", "address": "Vadodara", "mobile": "9090909090"},
        "7103": {"name": "Neha Desai", "address": "Bhavnagar", "mobile": "8888888888"}
    }
    bookings = []
    stock = 50
    booking_id_counter = 1001

# 👉 Save function
def save_data():
    data = {
        "customers": customers,
        "bookings": bookings,
        "stock": stock,
        "booking_id": booking_id_counter
    }
    with open("gas_data.json", "w") as file:
        json.dump(data, file)

print("====================================")
print("     WELCOME TO GAS AGENCY SYSTEM")
print("====================================")

while True:
    print("\n----- MAIN MENU -----")
    print("1. Add Customer")
    print("2. View Customers")
    print("3. Book Gas")
    print("4. Check Stock")
    print("5. View Booked Gas")
    print("6. Search Booking by ID")
    print("7. Delete Customer")
    print("8. Update Customer")
    print("9. Exit")

    choice = input("Enter your choice: ")

    # 1️⃣ Add Customer
    if choice == "1":
        cust_id = input("Enter Customer ID: ")

        if cust_id in customers:
            print("❌ Customer ID already exists!")
            continue

        name = input("Enter Customer Name: ")
        address = input("Enter Address: ")
        mobile = input("Enter Mobile Number: ")

        if not mobile.isdigit() or len(mobile) != 10:
            print("❌ Invalid mobile number!")
            continue

        customers[cust_id] = {
            "name": name,
            "address": address,
            "mobile": mobile
        }

        save_data()
        print("✅ Customer added successfully!")

    # 2️⃣ View Customers
    elif choice == "2":
        print("\n===== CUSTOMER LIST =====")
        for cid, details in customers.items():
            print(f"ID      : {cid}")
            print(f"Name    : {details['name']}")
            print(f"Address : {details['address']}")
            print(f"Mobile  : {details['mobile']}")
            print("----------------------------")

    # 3️⃣ Book Gas
    elif choice == "3":
        cust_id = input("Enter Customer ID: ")

        if cust_id in customers:
            try:
                quantity = int(input("Enter Quantity: "))
            except:
                print("❌ Invalid input!")
                continue

            if quantity <= 0 or quantity > stock:
                print("❌ Invalid or insufficient stock!")
                continue

            price = 1000
            total = quantity * price
            gst = total * 0.05
            final = total + gst

            stock -= quantity

            now = datetime.datetime.now()
            date_time = now.strftime("%d-%m-%Y %H:%M:%S")

            booking = {
                "booking_id": booking_id_counter,
                "name": customers[cust_id]["name"],
                "mobile": customers[cust_id]["mobile"],
                "quantity": quantity,
                "total": total,
                "gst": gst,
                "final": final,
                "date_time": date_time
            }

            bookings.append(booking)

            print("\n====================================")
            print("        GAS BOOKING RECEIPT         ")
            print("====================================")
            print(f"Booking ID      : {booking_id_counter}")
            print(f"Date & Time     : {date_time}")
            print(f"Customer Name   : {booking['name']}")
            print(f"Mobile Number   : {booking['mobile']}")
            print("------------------------------------")
            print(f"Quantity        : {quantity}")
            print("------------------------------------")
            print(f"Total Amount    : ₹{total}")
            print(f"GST (5%)        : ₹{gst:.2f}")
            print("------------------------------------")
            print(f"Final Amount    : ₹{final:.2f}")
            print("====================================")

            booking_id_counter += 1
            save_data()

        else:
            print("❌ Customer not found!")

    # 4️⃣ Stock
    elif choice == "4":
        print(f"Available Cylinders in Stock: {stock}")

    # 5️⃣ Booking History
    elif choice == "5":
        if len(bookings) == 0:
            print("No bookings found.")
        else:
            for b in bookings:
                print("\n====================================")
                print("        GAS BOOKING RECEIPT         ")
                print("====================================")
                print(f"Booking ID      : {b['booking_id']}")
                print(f"Date & Time     : {b['date_time']}")
                print(f"Customer Name   : {b['name']}")
                print(f"Mobile Number   : {b['mobile']}")
                print("------------------------------------")
                print(f"Quantity        : {b['quantity']}")
                print("------------------------------------")
                print(f"Total Amount    : ₹{b['total']}")
                print(f"GST (5%)        : ₹{b['gst']:.2f}")
                print("------------------------------------")
                print(f"Final Amount    : ₹{b['final']:.2f}")
                print("====================================")

    # 6️⃣ Search Booking
    elif choice == "6":
        try:
            bid = int(input("Enter Booking ID: "))
        except:
            print("❌ Invalid input!")
            continue

        found = False

        for b in bookings:
            if b["booking_id"] == bid:
                print("\n====================================")
                print("        BOOKING RECEIPT             ")
                print("====================================")
                print(f"Booking ID      : {b['booking_id']}")
                print(f"Date & Time     : {b['date_time']}")
                print(f"Customer Name   : {b['name']}")
                print(f"Mobile Number   : {b['mobile']}")
                print("------------------------------------")
                print(f"Quantity        : {b['quantity']}")
                print("------------------------------------")
                print(f"Total Amount    : ₹{b['total']}")
                print(f"GST (5%)        : ₹{b['gst']:.2f}")
                print("------------------------------------")
                print(f"Final Amount    : ₹{b['final']:.2f}")
                print("====================================")
                print("   Booking Found Successfully ✅")
                print("====================================")

                found = True
                break

        if not found:
            print("❌ Booking not found!")

    # 7️⃣ Delete Customer
    elif choice == "7":
        cust_id = input("Enter Customer ID to delete: ")

        if cust_id in customers:
            confirm = input("Are you sure? (y/n): ")
            if confirm.lower() == 'y':
                del customers[cust_id]
                save_data()
                print("✅ Customer deleted successfully!")
        else:
            print("❌ Customer not found!")

    # 8️⃣ Update Customer
    elif choice == "8":
        cust_id = input("Enter Customer ID to update: ")

        if cust_id in customers:
            print("\n1. Name")
            print("2. Address")
            print("3. Mobile")

            opt = input("Enter choice: ")

            if opt == "1":
                customers[cust_id]["name"] = input("Enter new name: ")

            elif opt == "2":
                customers[cust_id]["address"] = input("Enter new address: ")

            elif opt == "3":
                mobile = input("Enter new mobile: ")
                if mobile.isdigit() and len(mobile) == 10:
                    customers[cust_id]["mobile"] = mobile
                else:
                    print("❌ Invalid mobile!")
                    continue
            else:
                print("❌ Invalid option!")
                continue

            save_data()
            print("✅ Customer updated successfully!")

        else:
            print("❌ Customer not found!")

    # 9️⃣ Exit
    elif choice == "9":
        save_data()
        print("🙏 Data saved successfully!")
        break

    else:
        print("❌ Invalid choice!")
