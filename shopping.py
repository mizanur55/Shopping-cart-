import json
import ast
import datetime
from dateutil import parser

class Product:
    
    def __init__(self, name, price, quantity, EAN, brand):
        self.name = name
        self.price = price
        self.quantity = quantity
        # the EAN code is the unique identifier
        self.EAN = EAN
        self.brand = brand
        
   # to_json method to convert to json format 
    def to_json(self):
        return json.dumps(self.__dict__)
    

class Clothing(Product):
    def __init__(self, name, price, quantity, EAN, brand, size, material):
        super().__init__(name, price, quantity, EAN, brand)
        self.size = size
        self.material = material
        
    
class Food(Product):
    #inherited from Product superclass and not Clothing. size and material excluded.
    def __init__(self, name, price, quantity, EAN, brand, expiry_date, gluten_free, suitable_for_vegans):
        super().__init__(name, price, quantity, EAN, brand)
        self.expiry_date = expiry_date
        self.gluten_free = gluten_free
        self.suitable_for_vegans = suitable_for_vegans
    
    
class Electronics(Product):
    #refurbished(is the item refurbished?) and released_this_year(was it relesed this year?)
    # are the two additional atrributes.
    def __init__(self,name, price, quantity, EAN, brand, refurbished, released_this_year):
        super().__init__(name, price, quantity, EAN, brand)
        self.refurbished = refurbished
        self.released_this_year = released_this_year



class ShoppingCart():
    def __init__(self):
        self.json_cart = []
        self.counter = 0 
        self.EAN_record = []
    
    # we will allow products with same name
    # since they have a unique numbers(EAN).
    def addproduct(self, p):
        self.counter += 1
        print(f"product '{p['name']}' has been added to the cart.")
        return self.json_cart.append(p)
        
    def removeProduct(self, p):
        self.counter -= 1
        print(f"product '{p['name']}' has been removed from the cart.")
        return self.json_cart.remove(p)
    
    def getContents(self):
        if self.json_cart:
            subtotal = 0
            total_item_price = 0
            print("This is the total of the expenses:")
            # this sorts the products by the product name
            sorted_cart = sorted(self.json_cart, key=lambda product:product['name'])
            subtotal=0
            for index, product in enumerate(sorted_cart):
                product_total = product['price']*product['quantity']
                subtotal += product_total
                print(f"{index+1} - {product['quantity']} * {product['name'].capitalize()} "
                      f"= £{product_total}")
            print(f"Total = £{subtotal}")
        else:
            print("The Shopping cart is empty. Please add shopping items to see the cart")     
            
    def changeProductQuantity(self, p, q):
        print(f"The quantity of '{p['name']}' has now been changed to {q}.")
        p['quantity'] = q
        
                   
# ------Helper Functions---------------------------------
# here are some utility fuctions and variables that will act as helper functions
ShoppingCart = ShoppingCart()

# used for returning a dictionary 
def return_dict(value):
    #convert to JSON
    value_json = value.to_json()
    #coverting it from str to dict object
    value_dict = ast.literal_eval(value_json)
    return value_dict

#check if the input is a 'yes' or 'no'.
def boolean_check(question):
    while True:
            output = input(str(question)).lower().strip()
            if output == 'yes' or output=='no':
                return output
                break
            else:
                print("Please answer with words 'Yes' or 'No'")

# checks date is valid               
def date_checker(question):
    while True:
        date = input(question)
        if (len(str(date)) == 8 or len(str(date))==10): #ensures currect length
            try:
                date = parser.parse(date, dayfirst=True)
                date = date.strftime('%d/%m/%y')
                return date
                break
            except ValueError:
                print("Date not valid. Please enter valid date")
        else:
            print("Date not valid. Please enter the date in 'mm/dd/yyyy'"\
            "or 'mm/dd/yy' format.")

#checks a number is positive
def check_number(question, num_type):
    # check if number is positive
    positive = False
    while positive==False:
        try:
            if num_type.lower()=="int":
                answer = int(input(str(question)))
            elif num_type.lower()=="float":
                answer = float(input(str(question)))
            if float(answer) > 0:
                return answer
                positive=True
            else:
                print("Please enter a positive number.")
        except ValueError:
            print("Your entry is not valid. Please try again")

#checks the EAN code is correct
def check_EAN(question, task):
    while True:
        EAN = check_number(str(question),'int')
        # we have to check that our unique identifier(EAN code) is 13 digits long
        if len(str(EAN).strip()) == 13:
            if str(task).lower()=="add":
                # check the EAN already exists. if it does then use it.
                if not any(product['EAN'] == EAN for product in ShoppingCart.json_cart):
                    return EAN
                    break  
                else:
                    print("Sorry, this EAN code has already been used. use another one")
            if str(task).lower()=="remove":
                return EAN
        else:
            print(f"The unique identifier(EAN) must be 13 digit "
                  f"sequence(only digits between 0 to 9 are allowed)")



#---------------------------------------------------------------------------------------------------    
print('The program has started.')
print('Insert your next command (H for help):')
terminated = False
while not terminated:
    c = str(input("Type your next Command: ")).strip()
    if c.upper() == 'T':
        break
    elif c.upper() == 'H':
       print('''The prgramme supports the following Commands:
         [A] - Add a new product to the cart
         [R] - Remove a product from the cart
         [S] - Print a summary of the cart
         [Q] - Change the quantity of a product
         [E] - Export a JSON version of the cart
         [T] - Terminate the program
         [H] - List the supported commands''')
    else:
        if c.upper() == 'A':
            print("Adding a new product:")
    
            while True:
                product = str(input("Insert it's type: ")).lower().strip()
                if product in ['clothing','food', 'electronics']: 
                    while True:
                        name = str(input("Insert it's name: ")).lower().strip()
                        #do not allow empty name input
                        if name: break
        #------------------------
                    #Price error handling- price has to be float
                    price = check_number("insert it's price: ",'float')
        #-------------------------------           
                    # quantity error handling- quantitiy has to be int
                    quantity = check_number("insert it's quantity: ",'int')
        #-------------------------------  
                    # getting the EAN number.
                    EAN = check_EAN("insert it's EAN code: ", "add")
         #-------------------------------  
                    while True:
                        brand = str(input("insert it's brand: "))
                        if brand:
                            break #does not allow empty input
         #-------------------------------           
                    if product.lower() == 'clothing':
                    # for the size and material I have allowed the user
                    # freedom to choose without restricting it to few choices
                    #this is because the size and matrial vary greatly in population
                        while True:
                            size = str(input("insert it's size: ")).strip()
                            if size: break
                        while True:
                            material = str(input("insert it's material: ")).strip()
                            if material: break 
                        clothing = Clothing(name,price,quantity,EAN,brand,size,material)
                        clothing = return_dict(clothing)
                        ShoppingCart.addproduct(clothing)
                        break
                        
                    elif product.lower() == 'food':
                        exp_date = date_checker("insert it's Expiry date(ddmmyy): ")
                        gluten_free = boolean_check("Is it Gluten free?: ")
                        suitable_for_vegans = boolean_check("Is it suitable for Vegans?: ")
                        food = Food(name,price,quantity,EAN,brand,exp_date, gluten_free, 
                                    suitable_for_vegans)
                        food = return_dict(food)
                        ShoppingCart.addproduct(food)
                        break
                        
                    elif product.lower() == 'electronics':
                        refurbished = boolean_check("Is it refurbished?: ").strip()
                        released_this_year = boolean_check("Was it relesed this year?: ")
                        electronics = Electronics(name,price,quantity,EAN,brand,refurbished,released_this_year)
                        electronics = return_dict(electronics)
                        ShoppingCart.addproduct(electronics)
                        break
               
                else:
                    print("The Product type you entered in not valid. Please enter a valid Product type"\
                        " like 'clothing','food' or 'electronics'")
                    False

                    
        elif c.upper() == 'R':
            # to ensure that we are removing the exact product without ambiguity
            # we will match both the name and the EAN code of the product
                product_name = str(input("What is the name of the product you want to remove?: ")).lower().strip()
                product_EAN = check_EAN("What is the EAN code of the product you want to remove?: ","remove")
                #match the name and EAN code of the product
                if not any(product['name'] == product_name for product in ShoppingCart.json_cart):
                         print(f"there is no product with the name '{product_name}'. type 'R' to remove an item") 
                if not any(product['EAN'] == product_EAN for product in ShoppingCart.json_cart):
                        print(f"there is no product with EAN code:'{product_EAN}'. type 'R' to remove an item")
                for product in ShoppingCart.json_cart:
                    if product["name"]==product_name and product["EAN"]==product_EAN:
                        ShoppingCart.removeProduct(product)
                        

            
        elif c.upper() == 'S':
            ShoppingCart.getContents()
        
        #for Q will do the same as R. we will match the name and the EAN number to avoid ambiguity.
        elif c.upper() == 'Q':
            p = str(input("What is the name of the product you want to change quantity of?")).lower().strip()
            # error handeling for new quantity
            q= check_number("What is the new quantity?: ",'int') 
            product_EAN = check_EAN("What is the EAN code of the to product you want change quantity of?: ","remove")  
            if not any(product['name'] == p for product in ShoppingCart.json_cart):
                     print(f"there is no product called '{p}'. type 'Q' to change the quantity of an item.")

            if not any(product['EAN'] == product_EAN for product in ShoppingCart.json_cart):
                    print(f"there is no product with EAN code: '{product_EAN}'. " 
                          f"Type 'Q' to change the quantity of an item.")

            for product in ShoppingCart.json_cart:
                if product["name"]==p and product["EAN"]==product_EAN:
                    ShoppingCart.changeProductQuantity(product, q)


        elif c.upper() == 'E':
            # export the shopping cart content in JSON format nicely
            print(json.dumps(ShoppingCart.json_cart,indent=1))
                    
        else:
            print('Command not recognised. Please try again')
         
            
print("Goodbye.")  
