from pydoc import text
import tkinter as tk
from tkinter import ttk
from tkinter import messagebox
import n8n

current_cart = {}
current_total = 0

root = tk.Tk()
root.title("AI Customer Order Management")
root.geometry("750x700")


# -------------------------
# Functions
# -------------------------

def analyze_order():
    global current_cart, current_total

    message = message_entry.get().strip()

    if message == "":
        messagebox.showerror("Error", "Please enter a customer message.")
        return
    

    cleaned = n8n.clean_message(message)
    cart = n8n.build_cart(cleaned, n8n.products, n8n.number_words)
 
    if  not cart:
        messagebox.showerror(
            "Invalid Order",
            "No valid products found.\n\nAvailable Products:\n• Shirt\n• T-shirt\n• Hoodie\n• Pants"
        )
        return

    total = n8n.calculate_total(cart, n8n.prices)

    current_cart = cart
    current_total = total

    reply = n8n.generate_reply(cart, total)

    reply_box.config(state="normal")
    reply_box.delete("1.0", tk.END)
    reply_box.insert(tk.END, reply)
    reply_box.config(state="disabled")

    confirm_button.config(state="normal")


def confirm_order_gui():
    global current_cart, current_total

    customer_name = customer_entry.get().strip()

    if customer_name == "":
        messagebox.showerror("Error", "Please enter customer name.")
        return

    if not current_cart:
        messagebox.showerror("Error", "Please analyze an order first.")
        return

    orders = n8n.load_orders()

    order_id = n8n.generate_order_id(orders)

    n8n.save_order(
        order_id,
        customer_name,
        current_cart,
        current_total
    )

    messagebox.showinfo(
        "Success",
        "Order Saved Successfully!"
    )

    # Clear everything
    message_entry.delete(0, tk.END)
    customer_entry.delete(0, tk.END)

    reply_box.config(state="normal")
    reply_box.delete("1.0", tk.END)
    reply_box.config(state="disabled")

    current_cart = {}
    current_total = {}

    confirm_button.config(state="disabled")


def cancel_order():
    global current_cart, current_total

    message_entry.delete(0, tk.END)
    customer_entry.delete(0, tk.END)

    reply_box.config(state="normal")
    reply_box.delete("1.0", tk.END)
    reply_box.config(state="disabled")

    current_cart = {}
    current_total = 0

    confirm_button.config(state="disabled")


def view_orders():
    window = tk.Toplevel(root)
    window.title("Order History")
    window.geometry("700x500")

    orders = n8n.load_orders()

    tree = ttk.Treeview(
        window,
        columns=("ID", "Customer", "Product", "Qty", "Total"),
        show="headings"
    )

    tree.heading("ID", text="Order ID")
    tree.heading("Customer", text="Customer")
    tree.heading("Product", text="Product")
    tree.heading("Qty", text="Quantity")
    tree.heading("Total", text="Total")

    tree.column("ID", width=100, anchor="center")
    tree.column("Customer", width=150, anchor="center")
    tree.column("Product", width=120, anchor="center")
    tree.column("Qty", width=80, anchor="center")
    tree.column("Total", width=120, anchor="center")

    if not orders:
        tk.Label(
            window,
            text="No orders found.",
            font=("Arial", 14)
        ).pack(pady=20)
        return

    for order in orders:
        tree.insert(
            "",
            tk.END,
            values=(
                order[0],
                order[1],
                order[2],
                order[3],
                order[4]
            )
        )

    scrollbar = ttk.Scrollbar(
        window,
        orient="vertical",
        command=tree.yview
    )

    tree.configure(yscrollcommand=scrollbar.set)

    scrollbar.pack(side="right", fill="y")

    tree.pack(fill="both", expand=True)


def open_search_customer():
    window = tk.Toplevel(root)
    window.title("Search Customer")
    window.geometry("750x550")

    customer_label = tk.Label(
        window,
        text="Customer Name:",
        font=("Arial", 14)
    )
    customer_label.pack(anchor="w", padx=20)

    customer_entry = tk.Entry(
        window,
        width=20,
        font=("Arial", 12)
    )
    customer_entry.pack(padx=20, pady=10)

    tree = ttk.Treeview(
        window,
        columns=("ID", "Product", "Qty", "Total"),
        show="headings"
    )

    tree.heading("ID", text="Order ID")
    tree.heading("Product", text="Product")
    tree.heading("Qty", text="Quantity")
    tree.heading("Total", text="Total")

    tree.column("ID", width=120)
    tree.column("Product", width=150)
    tree.column("Qty", width=80, anchor="center")
    tree.column("Total", width=120, anchor="center")

    def perform_search():

        name = customer_entry.get().strip()

        if name == "":
            messagebox.showerror(
                "Error",
                "Please enter customer name.",
                parent=window
            )
            return

        orders = n8n.load_orders()

        for item in tree.get_children():
            tree.delete(item)

        found = False

        for order in orders:
            if order[1].strip().lower() == name.lower():

                found = True

                tree.insert(
                    "",
                    tk.END,
                    values=(
                        order[0],
                        order[2],
                        order[3],
                        order[4]
                    )
                )

        if not found:
            messagebox.showinfo(
                "Search",
                "No orders found for this customer.",
                parent=window
            )

    search_button = tk.Button(
        window,
        text="Search",
        font=("Arial", 12, "bold"),
        width=20,
        command=perform_search
    )
    search_button.pack(pady=10)

    tree.pack(fill="both", expand=True)


def open_search_product():
    window = tk.Toplevel(root)
    window.title("Search Product")
    window.geometry("750x550")

    product_label = tk.Label(
        window,
        text="Product Name:",
        font=("Arial", 14)
    )
    product_label.pack(anchor="w", padx=20)

    product_entry = tk.Entry(
        window,
        width=20,
        font=("Arial", 12)
    )
    product_entry.pack(padx=20, pady=10)

    tree = ttk.Treeview(
        window,
        columns=("ID", "Customer", "Qty", "Total"),
        show="headings"
    )

    tree.heading("ID", text="Order ID")
    tree.heading("Customer", text="Customer")
    tree.heading("Qty", text="Quantity")
    tree.heading("Total", text="Total")

    tree.column("ID", width=120)
    tree.column("Customer", width=150)
    tree.column("Qty", width=80, anchor="center")
    tree.column("Total", width=120, anchor="center")

    def perform_search():

        name = product_entry.get().strip()

        if name == "":
            messagebox.showerror(
                "Error",
                "Please enter product name.",
                parent=window
            )
            return

        orders = n8n.load_orders()

        for item in tree.get_children():
            tree.delete(item)

        found = False

        for order in orders:
            if order[2].strip().lower() == name.lower():

                found = True

                tree.insert(
                    "",
                    tk.END,
                    values=(
                        order[0],
                        order[1],
                        order[3],
                        order[4]
                    )
                )

        if not found:
            messagebox.showinfo(
                "Search",
                "No orders found for this product.",
                parent=window
            )

    search_button = tk.Button(
        window,
        text="Search",
        font=("Arial", 12, "bold"),
        width=20,
        command=perform_search
    )
    search_button.pack(pady=10)

    tree.pack(fill="both", expand=True)

def delete_button_order():
    window=tk.Toplevel(root)
    window.title("Delete Order")
    window.geometry("750x550")

    delete_label=tk.Label(
        window,
        text="Delete Order",
        font=("Arial",12,"bold")

        


)
    delete_label.pack(anchor="w",padx=10)


    delete_entry=tk.Entry(

        window,
        width=20,
        font=("Arial",12)





    )
    delete_entry.pack(padx=20,pady=10)

    def perform_delete():

        order_id=delete_entry.get().strip()
        if order_id=="":
            
            messagebox.showerror("Error","Please Enter a Valid Order ID",parent=window)
            return

        
        orders=n8n.load_orders()
        new_orders=[]
    
        found=False

        for order in orders:
            
            if order_id.strip().upper() == order[0].strip().upper():
                

                found=True
            else:
                new_orders.append(order)
        if found:
            response=messagebox.askokcancel("Confirm Delete",  
                f'Delete{order_id}?',parent=window
                )
            if not response:
               return
            

            n8n.save_all_orders(new_orders)
            delete_entry.delete(0,tk.END)

            messagebox.showinfo(

                "Success",'Order deleted Successfully.',
                parent=window

            )

        else:
            messagebox.showerror(
    "Error",
    "Order ID not found.",parent=window
)
        

    

    delete = tk.Button(
        window,
        text="Delete",
        font=("Arial", 12, "bold"),
        width=20,
        command=perform_delete
        )
    delete.pack(pady=10)


    

def edit_order_button():
    window = tk.Toplevel(root)
    window.title("Edit Order")
    window.geometry("750x550")

    current_order = None

    tk.Label(
        window,
        text="Enter Order ID",
        font=("Arial", 12, "bold")
    ).pack(anchor="w", padx=20, pady=5)

    edit_entry = tk.Entry(
        window,
        width=30,
        font=("Arial", 12)
    )
    edit_entry.pack(padx=20, pady=5)

    tk.Label(window, text="Customer").pack(anchor="w", padx=20)
    customer_edit = tk.Entry(window, width=40)
    customer_edit.pack(padx=20, pady=5)



    tk.Label(window, text="Product").pack(anchor="w", padx=20)
    product_edit = tk.Entry(window, width=40)
    product_edit.pack(padx=20, pady=5)

    tk.Label(window, text="Quantity").pack(anchor="w", padx=20)
    quantity_edit = tk.Entry(window, width=40)
    quantity_edit.pack(padx=20, pady=5)

    def search_order():
        nonlocal current_order

        order_id = edit_entry.get().strip()

        orders = n8n.load_orders()

        for order in orders:
            if order_id.strip().upper() == order[0].strip().upper():

                current_order = order

                customer_edit.delete(0, tk.END)
                customer_edit.insert(0, order[1])

                product_edit.delete(0, tk.END)
                product_edit.insert(0, order[2])

                quantity_edit.delete(0, tk.END)
                quantity_edit.insert(0, order[3])
                save_btn.config(state="normal")

                return

        messagebox.showerror("Error", "Order not found",parent=window)

    def save_changes():
        nonlocal current_order

        if current_order is None:
            messagebox.showerror("Error", "Search an order first.",parent=window)
            return

        new_customer = customer_edit.get().strip()
        if new_customer == "":
            messagebox.showerror(
        "Error",
        "Customer name cannot be empty.",parent=window
    )
            return
        new_product = product_edit.get().strip().lower()

        if new_product not in n8n.products:
            messagebox.showerror("Error","Invalid product.\nAvailable products:\n- shirt\n- t-shirt\n- hoodie\n- pants",parent=window
    )
            return
        try:
            new_quantity = int(quantity_edit.get())
            if new_quantity <= 0:
                messagebox.showerror(
                    "Error",
                    "Quantity must be greater than 0.",parent=window
    )
                return
            
        except ValueError:
            messagebox.showerror("Error", "Quantity must be a number.",parent=window)
            return

        # Recalculate total based on the (possibly new) product/quantity
        new_total = n8n.prices[new_product] * new_quantity

        orders = n8n.load_orders()
        order_id = current_order[0]

        for i, order in enumerate(orders):
            if order[0].strip().upper() == order_id.strip().upper():
                orders[i] = [
                    order_id,
                    new_customer,
                    new_product,
                    str(new_quantity),
                    str(new_total)
        ]
                break

        response = messagebox.askokcancel(
        "Confirm",
        "Save these changes?",parent=window
        )

        if not response:
            return

        n8n.save_all_orders(orders)
        current_order = orders[i]

        messagebox.showinfo("Success", "Order updated successfully!",parent=window)
        # window.destroy()

    search_btn = tk.Button(
        window,
        text="Search",
        font=("Arial", 12, "bold"),
        command=search_order
        
    )
    search_btn.pack(pady=10)

    save_btn = tk.Button(
        window,
        text="Save Changes",
        font=("Arial", 12, "bold"),
        command=save_changes,
        state='disabled'
    )
    save_btn.pack(pady=10)

    
# -------------------------
# Widgets
# -------------------------




title = tk.Label(
    root,
    text="AI Customer Order Management",
    font=("Arial", 24, "bold")
)
title.pack(pady=20)

message_label = tk.Label(
    root,
    text="Customer Message:",
    font=("Arial", 14)
)
message_label.pack(anchor="w", padx=20)

message_entry = tk.Entry(
    root,
    width=60,
    font=("Arial", 12)
)
message_entry.pack(padx=20, pady=10)

customer_label = tk.Label(
    root,
    text="Customer Name:",
    font=("Arial", 14)
)
customer_label.pack(anchor="w", padx=20)

customer_entry = tk.Entry(
    root,
    width=60,
    font=("Arial", 12)
)
customer_entry.pack(padx=20, pady=10)


button_frame = tk.Frame(root)

button_frame.pack(pady=20)


analyze_button = tk.Button(button_frame,
  
    text="Analyze Order",
    font=("Arial", 12, "bold"),
    width=20,
    command=analyze_order
)
analyze_button.grid(row=0, column=0, padx=10, pady=10)

reply_box = tk.Text(
    root,
    width=60,
    height=12,
    font=("Arial", 12),
    state="disabled"
)
reply_box.pack(pady=20)

confirm_button = tk.Button(
    button_frame,
    text="Confirm Order",
    font=("Arial", 12, "bold"),
    width=20,
    command=confirm_order_gui,
    state="disabled"
)
confirm_button.grid(row=0, column=1, padx=10, pady=10)

cancel_button = tk.Button(
    button_frame,
    text="Cancel",
    font=("Arial", 12, "bold"),
    width=20,
    command=cancel_order
)
cancel_button.grid(row=0, column=2, padx=10, pady=10)



view_button=tk.Button(
    button_frame,
    text="View Orders",
    font=("Arial",12,"bold"),
    width=20,
    command=view_orders

)
view_button.grid(row=0, column=3, padx=10, pady=10)

sarch_customer=tk.Button(
    button_frame,
    text="search customer",
    font=("Arial",12,"bold"),
    width=20,
    command=open_search_customer
)
sarch_customer.grid(row=1, column=0, padx=10, pady=10)


search_product_button = tk.Button(
    button_frame,
    text="Search Product",
    font=("Arial",12,"bold"),
    width=20,
    command=open_search_product
)
search_product_button.grid(row=1, column=1, padx=10, pady=10)


delete_button=tk.Button(

    button_frame,
    text="Delete Order",
    font=("Arial",12,"bold"),
    width=20,

    command=delete_button_order
)
delete_button.grid(row=1, column=2, padx=10, pady=10)


edit_order_btn=tk.Button(

    button_frame,
    
    text="Edit Order",
    font=("Arial",12,"bold"),
    width=20,
    
    command=edit_order_button


)

edit_order_btn.grid(row=1, column=3, padx=10, pady=10)


root.mainloop()