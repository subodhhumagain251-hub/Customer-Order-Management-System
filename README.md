# Customer Order Management System

A desktop-based Customer Order Management System built with **Python** and **Tkinter**. This application allows users to manage customer orders through a simple graphical user interface (GUI).

## Features

- Add new customer orders
- View all orders
- Search orders by Customer Name
- Search orders by Product Name
- Edit existing orders
- Delete orders with confirmation
- Input validation
- Case-insensitive search and order lookup
- Automatic total price calculation
- Order data stored in CSV format

## Technologies Used

- Python 3
- Tkinter (GUI)
- CSV File Handling
- MessageBox
- ttk.Treeview

## Project Structure

```
Customer-Order-Management-System/
│
├── gui.py
├── n8n.py
├── orders.csv
├── README.md
```

## How It Works

### Add Order
- Enter a customer's order.
- The system validates the input.
- The order is saved into `orders.csv`.

### Search Order
Orders can be searched using:
- Customer Name
- Product Name

### Edit Order
- Search an order by Order ID.
- Modify Customer Name, Product, or Quantity.
- The total price is recalculated automatically.
- Updated data is saved to the CSV file.

### Delete Order
- Search using the Order ID.
- Confirmation dialog appears before deletion.
- The selected order is removed from the CSV file.

### View Orders
Displays every saved order in a table using `ttk.Treeview`.

## Validation

The application validates:

- Customer name cannot be empty
- Product must exist
- Quantity must be greater than zero
- Quantity must be numeric
- Invalid Order IDs are rejected

## Sample Products

- Shirt
- T-shirt
- Hoodie
- Pants

## Future Improvements

- Replace CSV with SQLite database
- AI-powered order recommendations
- PDF invoice generation
- Sales dashboard
- User login system
- Export reports
- Deploy as a web application

## Learning Outcomes

This project helped me practice:

- Python programming
- Tkinter GUI development
- CRUD operations (Create, Read, Update, Delete)
- CSV file handling
- Input validation
- Event-driven programming
- Debugging and problem solving

## Screenshots

*(Add screenshots of your application here.)*

## Author

**Subodh Humagain**

B.Sc. Computational Mathematics

Python | AI Automation | GUI Development

---

This project was developed as part of my learning journey to strengthen my Python programming, GUI development, and software development skills.
