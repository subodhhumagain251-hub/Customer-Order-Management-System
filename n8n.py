from email.mime import message
import os
print("File will be saved at:", os.getcwd())


def clean_message(message):
    return message.lower().replace("-",'').replace(',','').replace(".",'').replace("_","")

def detect_quantity(word,number_words):
    if word.isdigit():#so i know that sometimes we don't need to declare the parametr but correct me here 
        return int(word)
    elif word in number_words:#how does this work
        return number_words[word] #how does this work
    return None 


def build_cart(message,products,number_words): # why do we need the parameter called message here 

    cart={}
    words=message.split()
    current_quantity=1
    skip_next=False# how does this variable works and why are we using it
    for i in range(len(words)):
        if skip_next:
            skip_next=False
            continue

        word=words[i]


        qty_found=detect_quantity(word, number_words)
        if qty_found is not None :
            current_quantity=qty_found
            continue 
        for key, keywords in products.items():# what is key and keywords , here 
            if word in keywords:#what does it means??
                qty=current_quantity

                if qty==1 and i+1<len(words): # explained me fromm here , i don't understand particulary 
                    next_word=words[i+1]
                    next_qty=detect_quantity(next_word,number_words)
                    if next_qty is not None :
                        qty=next_qty
                        skip_next = True
                cart[key]=cart.get(key,0)+qty 
                current_quantity=1 
                break
    return cart           



def load_orders():
    orders=[]

    with open("orders.csv","r")as f :
        for line in f:
            line=line.strip()
            parts=line.split(",")
           
            
            orders.append(parts)
    return orders
    

    



def calculate_total(cart,prices): #also here 
    total=0  
    for item, qty in cart.items():
        total += prices.get(item,0)*qty
    return total 



def save_order(order_id, customer_name, cart, total):
    with open("orders.csv", "a") as f:
        for item, qty in cart.items():
            line = f"{order_id},{customer_name},{item},{qty},{total}\n"
            print("Writing:", line)
            f.write(line)

    print("Saved to:", os.path.abspath("orders.csv"))


    # Read the file immediately
    with open("orders.csv", "r") as f:
        print("\n----- Last 5 lines -----")
        lines = f.readlines()
        for line in lines[-5:]:
            print(line.strip())

def save_all_orders(orders):

    with open("orders.csv", "w") as f:

        for order in orders:

            line = f"{order[0]},{order[1]},{order[2]},{order[3]},{order[4]}\n"

            f.write(line)
def generate_order_id(orders):
  
    if orders==[]:
        return 'ORD001'
    else:
        last_id=orders[-1]
        last_id_number=int(last_id[0][3:])
        new_id=last_id_number+1
        converted_id=str(new_id).zfill(3)
    return f'ORD{converted_id}'

def generate_reply(cart,total):

    if not cart:
        return""" No valid products found in the order.\n
Available Products:\n
-shirt\n 
-T-shirt\n
-Hoodie\n
-Pants
"""
    
    reply="Hello! \n\n"
    reply+="Here's your order:\n"

    for item ,qty in cart.items():
        reply+=f". {item.title()} x {qty}\n"

    reply+=f"\nTotal:NPR {total}"
    #reply += "\nReply YES to confirm your order.[Y/N]"

    return reply
def search_customer(customer_name):
    orders=load_orders()
    found=False
    for items in orders:
        if items[1]==customer_name:
            found=True 
            print(items)
            print("Order ID :", items[0])
            print("Customer :", items[1])
            print("Product  :", items[2])
            print("Quantity :", items[3])
            print("Total    :", items[4])
            print("----------------------")

    if not found:
        print("No orders found for customer:",customer_name)



def search_product(product_name):
    orders=load_orders()
    found=False
    for item in orders:
        if item[2]==product_name:
            found=True 
            print(item)
            print("Order ID :", item[0])
            print("Customer :", item[1])
            print("Product  :", item[2])
            print("Quantity :", item[3])
            print("Total    :", item[4])
            print("----------------------")

    if not found:

    
        print("No orders found for product:",product_name)

def confirm_order(reply):
    

    print(reply)
    
    while True:
        answer=input("enter your choice [Y/N]:").lower()
        if answer in ('y','yes','confirm','ok'):
            return True 
        elif answer in  ("n","no","cancel"):
            return False
        else:
            print("Invalid input.Please enter Y or N ")

def place_order():

    message=input("customer said:")


    message_cleaned =clean_message(message)
    cart=build_cart(message_cleaned,products,number_words)
    total=calculate_total(cart,prices)
    if not cart:
        print(generate_reply(cart,total))
        return


    print("\n.... CART....")
    for item,qty in cart.items():
        print(item,'->',qty)


    total=calculate_total(cart,prices)
    print("\n Total price:",total)
    reply=generate_reply(cart,total)
    confirmed=confirm_order(reply)
    if confirmed:
        customer_name=input("Customer name:")

   

        orders = load_orders()

        order_id = generate_order_id(orders)
        save_order(order_id,customer_name,cart,total)
        
        print("order saved  sucessfully!")
    else:
        print('order cancelled by customer.')

    
    
def show_menu():
    print("====================================\n"
          "AI CUSTOMER ORDER MANAGEMENT\n"
          "====================================\n "
          "1. Place Order\n"
          "2. Search Customer\n"
          "3. Search Product\n"
          "4. Show All Orders\n"
          "5. Exit\n"
          "====================================\n")


products={
"shirt":["shirt","shirts"],
"t-shirt": ["tshirt", "t-shirt",],
"hoodie" : ["hoodie", "hodie", "hoddie"],
"pants": ["pants",'pant']
}

number_words = {
    "one": 1,
    "two": 2,
    "three": 3,
    "four": 4,
    "five": 5,
    "six": 6,
    "seven": 7,
    "eight": 8,
    "nine": 9,
    "ten": 10
}



#prices 
prices={
    "shirt":500,
    "t-shirt":400,
    "hoodie":1000,
    "pants":800

}
def show_all_orders():
    orders=load_orders()

    if orders == []:
        print("No orders found")
        return 
    
    for order in orders:
        print("order ID:",order[0])
        print("customer:",order[1])
        print("product:",order[2])
        print("quantity:",order[3])
        print("total:",order[4])
        print("----------------------")




if __name__ == "__main__":

    while True:
        show_menu()
        choice = input("choose an option:")

        if choice == "1":
            place_order()

        elif choice == "2":
            customer_name = input("Enter customer name: ")
            search_customer(customer_name)

        elif choice == "3":
            product_name = input("Enter product name: ")
            search_product(product_name)

        elif choice == "4":
            show_all_orders()

        elif choice == "5":
            print("Thank you!")
            break

        else:
            print("Invalid choice.")



