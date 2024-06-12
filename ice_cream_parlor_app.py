import streamlit as st
import sqlite3

# Database connection and functions
def create_tables():
    conn = sqlite3.connect('ice_cream_parlor.db')
    c = conn.cursor()
    c.execute('''
    CREATE TABLE IF NOT EXISTS SeasonalFlavors (
        id INTEGER PRIMARY KEY,
        name TEXT NOT NULL,
        ingredients TEXT NOT NULL
    )
    ''')
    c.execute('''
    CREATE TABLE IF NOT EXISTS IngredientInventory (
        id INTEGER PRIMARY KEY,
        name TEXT NOT NULL,
        quantity INTEGER NOT NULL
    )
    ''')
    c.execute('''
    CREATE TABLE IF NOT EXISTS CustomerSuggestions (
        id INTEGER PRIMARY KEY,
        flavor_suggestion TEXT NOT NULL,
        allergy_concern TEXT
    )
    ''')
    c.execute('''
    CREATE TABLE IF NOT EXISTS Allergens (
        id INTEGER PRIMARY KEY,
        name TEXT NOT NULL
    )
    ''')
    conn.commit()
    conn.close()

def add_seasonal_flavor(name, ingredients):
    conn = sqlite3.connect('ice_cream_parlor.db')
    c = conn.cursor()
    c.execute('INSERT INTO SeasonalFlavors (name, ingredients) VALUES (?, ?)', (name, ingredients))
    conn.commit()
    conn.close()

def add_ingredient(name, quantity):
    conn = sqlite3.connect('ice_cream_parlor.db')
    c = conn.cursor()
    c.execute('INSERT INTO IngredientInventory (name, quantity) VALUES (?, ?)', (name, quantity))
    conn.commit()
    conn.close()

def add_customer_suggestion(flavor_suggestion, allergy_concern=None):
    conn = sqlite3.connect('ice_cream_parlor.db')
    c = conn.cursor()
    c.execute('INSERT INTO CustomerSuggestions (flavor_suggestion, allergy_concern) VALUES (?, ?)', (flavor_suggestion, allergy_concern))
    conn.commit()
    conn.close()

def add_allergen(name):
    conn = sqlite3.connect('ice_cream_parlor.db')
    c = conn.cursor()
    c.execute('INSERT INTO Allergens (name) VALUES (?)', (name,))
    conn.commit()
    conn.close()

def get_seasonal_flavors():
    conn = sqlite3.connect('ice_cream_parlor.db')
    c = conn.cursor()
    c.execute('SELECT * FROM SeasonalFlavors')
    flavors = c.fetchall()
    conn.close()
    return flavors

def get_ingredients():
    conn = sqlite3.connect('ice_cream_parlor.db')
    c = conn.cursor()
    c.execute('SELECT * FROM IngredientInventory')
    ingredients = c.fetchall()
    conn.close()
    return ingredients

def get_allergens():
    conn = sqlite3.connect('ice_cream_parlor.db')
    c = conn.cursor()
    c.execute('SELECT * FROM Allergens')
    allergens = c.fetchall()
    conn.close()
    return allergens

def search_flavors(search_term):
    conn = sqlite3.connect('ice_cream_parlor.db')
    c = conn.cursor()
    c.execute('SELECT * FROM SeasonalFlavors WHERE name LIKE ?', ('%' + search_term + '%',))
    flavors = c.fetchall()
    conn.close()
    return flavors

# Predefined seasonal and regular flavors
flavor_options = [
    "Vanilla", "Chocolate", "Strawberry", "Mint Chocolate Chip", "Cookie Dough",
    "Pumpkin Spice", "Peppermint", "Eggnog", "Mango", "Blueberry"
]

# Predefined ingredients
ingredient_options = [
    "Milk", "Sugar", "Cream", "Vanilla Extract", "Chocolate Chips",
    "Strawberries", "Blueberries", "Mint", "Cookie Dough", "Pumpkin"
]

# Streamlit app
st.title("Ice Cream Parlor Management System")

# Create tables if they don't exist
create_tables()

# Tabs for different functionalities
tab1, tab2, tab3, tab4 = st.tabs(["Add Entries", "View Entries", "Search Flavors", "Cart"])

# Add Entries tab
with tab1:
    st.header("Add Entries")
    entry_type = st.selectbox("Choose entry type", ["Seasonal Flavor", "Ingredient", "Customer Suggestion", "Allergen"])

    if entry_type == "Seasonal Flavor":
        name = st.selectbox("Choose flavor", flavor_options)
        ingredients = st.text_input("Ingredients (comma-separated)")
        if st.button("Add Flavor"):
            add_seasonal_flavor(name, ingredients)
            st.success("Flavor added successfully!")
    
    elif entry_type == "Ingredient":
        name = st.selectbox("Choose ingredient", ingredient_options)
        quantity = st.number_input("Quantity", min_value=0, step=1)
        if st.button("Add Ingredient"):
            add_ingredient(name, quantity)
            st.success("Ingredient added successfully!")
    
    elif entry_type == "Customer Suggestion":
        flavor_suggestion = st.text_input("Flavor Suggestion")
        allergy_concern = st.text_input("Allergy Concern (optional)")
        if st.button("Add Suggestion"):
            add_customer_suggestion(flavor_suggestion, allergy_concern)
            st.success("Suggestion added successfully!")
    
    elif entry_type == "Allergen":
        name = st.text_input("Allergen Name")
        if st.button("Add Allergen"):
            add_allergen(name)
            st.success("Allergen added successfully!")

# View Entries tab
with tab2:
    st.header("View Entries")
    view_type = st.selectbox("Choose entry type to view", ["Seasonal Flavors", "Ingredients", "Allergens"])

    if view_type == "Seasonal Flavors":
        flavors = get_seasonal_flavors()
        for flavor in flavors:
            st.write(f"ID: {flavor[0]}, Name: {flavor[1]}, Ingredients: {flavor[2]}")
    
    elif view_type == "Ingredients":
        ingredients = get_ingredients()
        for ingredient in ingredients:
            st.write(f"ID: {ingredient[0]}, Name: {ingredient[1]}, Quantity: {ingredient[2]}")
    
    elif view_type == "Allergens":
        allergens = get_allergens()
        for allergen in allergens:
            st.write(f"ID: {allergen[0]}, Name: {allergen[1]}")

# Search Flavors tab
with tab3:
    st.header("Search Flavors")
    search_term = st.text_input("Enter search term")
    if st.button("Search"):
        flavors = search_flavors(search_term)
        for flavor in flavors:
            st.write(f"ID: {flavor[0]}, Name: {flavor[1]}, Ingredients: {flavor[2]}")

# Cart tab
with tab4:
    st.header("Cart")
    cart = st.session_state.get('cart', [])
    flavor_to_add = st.selectbox("Choose flavor to add to the cart", flavor_options)
    if st.button("Add to Cart"):
        cart.append(flavor_to_add)
        st.session_state['cart'] = cart
        st.success("Added to cart!")
    st.write("Cart contents:")
    for item in cart:
        st.write(item)
