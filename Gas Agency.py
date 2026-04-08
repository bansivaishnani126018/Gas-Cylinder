import json
import datetime
import tkinter as tk
from tkinter import messagebox
import matplotlib.pyplot as plt

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

# ================= GRAPH =================
def show_bar_graph():
    if not bookings:
        messagebox.showerror("Error", "No data available")
        return

    customer_count = {}
    for b in bookings:
        name = b["name"]
        customer_count[name] = customer_count.get(name, 0) + 1

    names = list(customer_count.keys())
    counts = list(customer_count.values())

    plt.figure()
    plt.bar(names, counts)
    plt.yticks(range(0, max(counts) + 1))

    plt.title("Total Bookings per Customer")
    plt.xlabel("Customer")
    plt.ylabel("Bookings")
    plt.show()

def show_pie_chart():
    if not bookings:
        messagebox.showerror("Error", "No data available")
        return

    payment_data = {"Cash": 0, "UPI": 0, "Card": 0}

    for b in bookings:
        method = b.get("payment_method", "Cash")
        if method in payment_data:
            payment_data[method] += 1

    labels = []
    sizes = []

    for k, v in payment_data.items():
        if v > 0:
            labels.append(k)
            sizes.append(v)

    plt.figure()
    plt.pie(sizes, labels=labels, autopct='%1.0f%%')
    plt.title("Payment Method Distribution")
    plt.show()

# ================= GUI =================
root = tk.Tk()
root.title("Gas Cylinder Agency Control Panel")
root.geometry("1100x650")
root.configure(bg="#2b2b2b")

header = tk.Frame(root, bg="#ff6a00", height=70)
header.pack(fill="x")

tk.Label(header, text="🔥 GAS CYLINDER AGENCY CONTROL PANEL",
         font=("Arial", 20, "bold"),
         bg="#ff6a00", fg="black").pack(pady=10)

menu = tk.Frame(root, bg="#1c1c1c", width=260)
menu.pack(side="left", fill="y")

content = tk.Frame(root, bg="#2b2b2b")
content.pack(side="right", expand=True, fill="both")

def clear():
    for w in content.winfo_children():
        w.destroy()

def btn(text, cmd):
    tk.Button(menu, text=text,
              width=25, height=2,
              bg="#444444", fg="white",
              activebackground="#ff6a00",
              font=("Arial", 10, "bold"),
              bd=0,
              command=cmd).pack(pady=6)

# ================= FUNCTIONS =================

def add_customer():
    clear()
    entries = {}

    for f in ["Customer ID","Name","Address","Mobile"]:
        tk.Label(content, text=f, fg="white", bg="#2b2b2b").pack()
        e = tk.Entry(content)
        e.pack()
        entries[f] = e

    def submit():
        cust_id = entries["Customer ID"].get()

        if cust_id in customers:
            messagebox.showerror("Error","Customer ID already exists!")
            return

        name = entries["Name"].get()
        address = entries["Address"].get()
        mobile = entries["Mobile"].get()

        if not mobile.isdigit() or len(mobile) != 10:
            messagebox.showerror("Error","Invalid mobile number!")
            return

        customers[cust_id] = {
            "name": name,
            "address": address,
            "mobile": mobile
        }

        save_data()
        messagebox.showinfo("Success","Customer added successfully!")

    tk.Button(content,text="ADD CUSTOMER",
              bg="#ff6a00", fg="black",
              font=("Arial",10,"bold"),
              command=submit).pack(pady=10)

def view_customers():
    clear()
    for cid, details in customers.items():
        tk.Label(content,
                 text=f"{cid} | {details['name']} | {details['address']} | {details['mobile']}",
                 fg="white", bg="#2b2b2b", anchor="w").pack(fill="x")

def book_gas():
    clear()

    tk.Label(content,text="Customer ID",fg="white",bg="#2b2b2b").pack()
    cust_entry = tk.Entry(content); cust_entry.pack()

    tk.Label(content,text="Quantity",fg="white",bg="#2b2b2b").pack()
    qty_entry = tk.Entry(content); qty_entry.pack()

    def submit():
        global stock, booking_id_counter

        cust_id = cust_entry.get()

        if cust_id not in customers:
            messagebox.showerror("Error","Customer not found!")
            return

        try:
            quantity = int(qty_entry.get())
        except:
            messagebox.showerror("Error","Invalid input!")
            return

        if quantity <= 0 or quantity > stock:
            messagebox.showerror("Error","Invalid or insufficient stock!")
            return

        price = 1000
        total = quantity * price
        gst = total * 0.18
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

        # 👉 Payment Method Window
        payment_window = tk.Toplevel(root)
        payment_window.title("Select Payment Method")
        payment_window.geometry("300x200")

        def confirm_payment(method):
            booking["payment_method"] = method

            receipt = f"""
====================================
        GAS BOOKING RECEIPT
====================================
Booking ID      : {booking_id_counter}
Date & Time     : {date_time}
Customer Name   : {booking['name']}
Mobile Number   : {booking['mobile']}
------------------------------------
Quantity        : {quantity}
------------------------------------
Total Amount    : ₹{total}
GST (18%)       : ₹{gst:.2f}
------------------------------------
Final Amount    : ₹{final:.2f}
Payment Method  : {method}
====================================
"""
            messagebox.showinfo("Receipt", receipt)
            payment_window.destroy()

        tk.Label(payment_window, text="Select Payment Method",
                 font=("Arial", 12, "bold")).pack(pady=10)

        tk.Button(payment_window, text="Cash", width=15,
                  command=lambda: confirm_payment("Cash")).pack(pady=5)

        tk.Button(payment_window, text="UPI", width=15,
                  command=lambda: confirm_payment("UPI")).pack(pady=5)

        tk.Button(payment_window, text="Card", width=15,
                  command=lambda: confirm_payment("Card")).pack(pady=5)

        booking_id_counter += 1
        save_data()

    tk.Button(content,text="BOOK GAS",
              bg="#ff6a00", fg="black",
              font=("Arial",10,"bold"),
              command=submit).pack(pady=10)

def check_stock():
    clear()
    tk.Label(content,text=f"Available Cylinders: {stock}",
             fg="white", bg="#2b2b2b",
             font=("Arial",14,"bold")).pack(pady=20)

def view_bookings():
    clear()
    if not bookings:
        tk.Label(content,text="No bookings found.",fg="white",bg="#2b2b2b").pack()
        return

    for b in bookings:
        method = b.get("payment_method", "Cash")
        tk.Label(content,
                 text=f"{b['booking_id']} | {b['name']} | Qty: {b['quantity']} | ₹{b['final']} | {method}",
                 fg="white", bg="#2b2b2b", anchor="w").pack(fill="x")

def search_booking():
    clear()
    tk.Label(content,text="Enter Booking ID",fg="white",bg="#2b2b2b").pack()
    e = tk.Entry(content); e.pack()

    def search():
        try:
            bid = int(e.get())
        except:
            messagebox.showerror("Error","Invalid input!")
            return

        for b in bookings:
            if b["booking_id"] == bid:
                messagebox.showinfo("Found", f"{b}")
                return

        messagebox.showerror("Error","Booking not found!")

    tk.Button(content,text="SEARCH",
              bg="#ff6a00", fg="black",
              command=search).pack(pady=10)

def delete_customer():
    clear()
    tk.Label(content,text="Enter Customer ID",fg="white",bg="#2b2b2b").pack()
    e = tk.Entry(content); e.pack()

    def delete():
        if e.get() in customers:
            if messagebox.askyesno("Confirm","Are you sure?"):
                del customers[e.get()]
                save_data()
                messagebox.showinfo("Done","Deleted")
        else:
            messagebox.showerror("Error","Customer not found")

    tk.Button(content,text="DELETE",
              bg="#ff6a00", fg="black",
              command=delete).pack(pady=10)

def update_customer():
    clear()

    tk.Label(content,text="Customer ID",fg="white",bg="#2b2b2b").pack()
    cid = tk.Entry(content); cid.pack()

    tk.Label(content,text="New Name").pack()
    name_entry = tk.Entry(content); name_entry.pack()

    tk.Label(content,text="New Address").pack()
    addr_entry = tk.Entry(content); addr_entry.pack()

    tk.Label(content,text="New Mobile").pack()
    mob_entry = tk.Entry(content); mob_entry.pack()

    def update_name():
        if cid.get() in customers:
            customers[cid.get()]["name"] = name_entry.get()
            save_data()
            messagebox.showinfo("Done","Name updated")

    def update_address():
        if cid.get() in customers:
            customers[cid.get()]["address"] = addr_entry.get()
            save_data()
            messagebox.showinfo("Done","Address updated")

    def update_mobile():
        if cid.get() in customers:
            mob = mob_entry.get()
            if mob.isdigit() and len(mob)==10:
                customers[cid.get()]["mobile"] = mob
                save_data()
                messagebox.showinfo("Done","Mobile updated")
            else:
                messagebox.showerror("Error","Invalid mobile")

    tk.Button(content,text="Update Name",command=update_name).pack(pady=5)
    tk.Button(content,text="Update Address",command=update_address).pack(pady=5)
    tk.Button(content,text="Update Mobile",command=update_mobile).pack(pady=5)

# ================= MENU =================
btn("Add Customer", add_customer)
btn("View Customers", view_customers)
btn("Book Gas", book_gas)
btn("Check Stock", check_stock)
btn("View Bookings", view_bookings)
btn("Search Booking", search_booking)
btn("Delete Customer", delete_customer)
btn("Update Customer", update_customer)

btn("📊 Booking Graph", show_bar_graph)
btn("🥧 Sales Pie Chart", show_pie_chart)

btn("Exit", root.destroy)

root.mainloop()
