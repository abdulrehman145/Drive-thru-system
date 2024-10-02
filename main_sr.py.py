import pyttsx3
import datetime
import speech_recognition as sr

# Initialize the text-to-speech engine
engine = pyttsx3.init()

# Initialize the speech recognizer
recognizer = sr.Recognizer()

# Function to speak and display text
def say_and_show(text):
    engine.say(text)
    engine.runAndWait()
    print(text)

# Function to convert speech to text
def listen_to_speech(timeout=5):
    with sr.Microphone() as source:
        recognizer.adjust_for_ambient_noise(source)  # Adjust for ambient noise
        say_and_show("Listening...")
        try:
            audio = recognizer.listen(source, timeout=timeout)
            text = recognizer.recognize_google(audio)
            print(f"You said: {text}")
            return text.lower()
        except sr.UnknownValueError:
            say_and_show("Sorry, I could not understand the audio.")
            return ""
        except sr.RequestError as e:
            say_and_show(f"Could not request results; {e}")
            return ""

# Function to save files according to dates and orders for the day
def save_file(order_summary):
    date = datetime.datetime.now().strftime('%Y-%m-%d')
    time = datetime.datetime.now().strftime('%H:%M:%S')
    filename = f"orders_{date}.txt"
    
    with open(filename, "a") as f:
        f.write(f"\n\nOrder Time: {time}\n")
        f.write(order_summary)
    
    say_and_show(f"Order saved to: {filename}")

# Function to summarize the order
def summarize_order(orders):
    summary = ""
    total_bill = 0
    for item, details in orders.items():
        summary += f"{item.capitalize()} x {details['quantity']} = {details['price'] * details['quantity']} Rs\n"
        total_bill += details['price'] * details['quantity']
    summary += f"\nTotal Bill: {total_bill} Rs"
    return summary, total_bill

# Function to display the menu
def display_menu(menu):
    say_and_show("Here is our menu:")
    for item, price in menu.items():
        say_and_show(f"{item.capitalize()} - Rs.{price}")

# Function to take orders using speech recognition
def take_order(menu):
    orders = {}
    while True:
        display_menu(menu)
        say_and_show("Please state your order.")
        order = listen_to_speech()
        if order in menu:
            quantity = int(say_and_input("How many, sir?: "))
            orders[order] = {"quantity": quantity, "price": menu[order]}
            
            say_and_show("Would you like to order something else? (yes/no)")
            more = listen_to_speech()
            if more != 'yes':
                break
        else:
            say_and_show("Sorry, we don't have that item. Please choose from the menu.")
    
    return orders

# Function to speak text and take user input
def say_and_input(text):
    engine.say(text)
    engine.runAndWait()
    return input(text)

# Main function to process the order
def process_order():
    menu = {
        "coffee": 150,
        "burger": 300,
        "drink": 70,
        "pizza": 1800
    }
    
    say_and_show("Welcome to our drive-thru!")
    orders = take_order(menu)
    
    order_summary, total_bill = summarize_order(orders)
    
    say_and_show("Here is your order summary:")
    say_and_show(order_summary)
    
    say_and_show("Would you like to confirm your order? (yes/no)")
    confirm = listen_to_speech()
    if confirm == 'yes':
        save_file(order_summary)
        say_and_show("Thank you, sir! Hope you enjoy your order.")
    else:
        say_and_show("Order cancelled. Thank you!")

# Run the order process
process_order()
