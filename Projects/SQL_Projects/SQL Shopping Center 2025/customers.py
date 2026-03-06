import sqlite3 
from datetime import datetime

def set_FILENAME(filename):
    global FILENAME
    FILENAME = filename

def get_or_create_session(cid):
    """
    if there is a session with no end time: return session (this is the current session)
    else: make a new session
    """
    conn = sqlite3.connect(FILENAME)
    cursor = conn.cursor()
    
    # Get the latest session for this customer
    cursor.execute("""
        SELECT sessionNo FROM sessions 
        WHERE cid = ? AND end_time IS NULL
        ORDER BY sessionNo DESC LIMIT 1
    """, (cid,))
    
    result = cursor.fetchone()
    
    if result:
        session_no = result[0]
    else:
        # Create new session
        cursor.execute("""
            SELECT COALESCE(MAX(sessionNo), 0) + 1 FROM sessions WHERE cid = ?
        """, (cid,))
        session_no = cursor.fetchone()[0]
        
        cursor.execute("""
            INSERT INTO sessions (cid, sessionNo, start_time) 
            VALUES (?, ?, ?)
        """, (cid, session_no, datetime.now().isoformat()))
        conn.commit()
    
    conn.close()
    return session_no

def customer_menu(user):
    session_no = get_or_create_session(user['uid'])
    
    while True:
        print(f"""
CUSTOMER MENU (User ID: {user['uid']}) Please select an action:
    1. Search for Products
    2. View Cart
    3. My Orders
    4. Logout
        """)
        
        try:
            choice = int(input("> "))
            if choice == 1:
                search_products(user['uid'], session_no)
            elif choice == 2:
                view_cart(user['uid'], session_no)
            elif choice == 3:
                view_orders(user['uid'])
            elif choice == 4:
                # End session
                conn = sqlite3.connect(FILENAME)
                cursor = conn.cursor()
                cursor.execute("""
                    UPDATE sessions SET end_time = ? 
                    WHERE cid = ? AND sessionNo = ?
                """, (datetime.now().isoformat(), user['uid'], session_no))
                conn.commit()
                conn.close()
                print("\nLogged out successfully!")
                break
            else:
                print("Invalid choice!")
        except ValueError:
            print("Invalid input. Please enter a number.")

def search_products(uid, session_no):
    """Search for products by keyword
    
    Args:
        uid: user id
        session_no: session number
    """
    # Obtaining input from user
    keyword = input("\nEnter search keywords: ").strip()
    
    # empty search
    if not keyword:
        print("Search is empty, please try again.")
        return
    
    conn = sqlite3.connect(FILENAME)
    cursor = conn.cursor()
    
    # Log the search
    cursor.execute("""
        INSERT INTO search (cid, sessionNo, ts, query)
        VALUES (?, ?, ?, ?)
    """, (uid, session_no, datetime.now().isoformat(), keyword))
    conn.commit()
    
    keywords = keyword.split()
    conditions = []
    params = []
    for kw in keywords:
        conditions.append("(LOWER(name) LIKE LOWER(?) OR LOWER(descr) LIKE LOWER(?))")
        params.extend([f'%{kw}%', f'%{kw}%'])
    
    query = f"""
        SELECT pid, name, category, price, stock_count, descr
        FROM products
        WHERE {' AND '.join(conditions)}
    """
    
    cursor.execute(query, params)
    
    results = cursor.fetchall()
    conn.close()
    
    if not results:
        print("\nNo products found matching your search.")
        return

    page = 0
    page_size = 5
    total_pages = (len(results) + page_size - 1) // page_size
    
    # print saerch results in pages
    while True:
        print(f"\n--- Search Results (Page {page + 1} of {total_pages}) ---")
        start = page * page_size
        end = min(start + page_size, len(results))
        
        for i, product in enumerate(results[start:end], start=1):
            pid, name, category, price, stock, descr = product
            print(f"\n{i}. {name}")
            print(f"   Category: {category} | Price: ${price:.2f} | Stock: {stock}")
        
        print("\n" + "="*50)
        options = []
        if page > 0:
            options.append("P: Previous")
        if page < total_pages - 1:
            options.append("N: Next")
        options.append("1-5: Select Product")
        options.append("B: Back to Menu")
        
        print(" | ".join(options))
        choice = input("> ").strip().upper()
        
        if choice == 'N' and page < total_pages - 1:
            page += 1
        elif choice == 'P' and page > 0:
            page -= 1
        elif choice == 'B':
            break
        elif choice.isdigit() and 1 <= int(choice) <= min(5, end - start):
            product_idx = start + int(choice) - 1
            view_product_details(uid, session_no, results[product_idx])
        else:
            print("Invalid choice.")

def view_product_details(uid, session_no, product):
    """Display product details and allow adding to cart
    
    Args:
        uid: user id
        session_no: session number
        product: tuple of product data (pid, name, category, price, stock, description)
    """
    pid, name, category, price, stock, descr = product
    
    conn = sqlite3.connect(FILENAME)
    cursor = conn.cursor()
    
    # Record the view
    cursor.execute("""
        INSERT INTO viewedProduct (cid, sessionNo, ts, pid)
        VALUES (?, ?, ?, ?)
    """, (uid, session_no, datetime.now().isoformat(), pid))
    conn.commit()
    conn.close()
    # Print the view
    print(f"\n{'='*60}")
    print(f"Product: {name}")
    print(f"Category: {category}")
    print(f"Price: ${price:.2f}")
    print(f"Stock Available: {stock}")
    print(f"Description: {descr}")
    print(f"{'='*60}")
    
    if stock > 0:
        add = input("\nAdd to cart? (y/N): ").strip().upper()
        if add == 'Y':
            add_to_cart(uid, session_no, pid, stock)
    else:
        print("\nSorry, product out of stock.")

def add_to_cart(uid, session_no, pid, available_stock):
    """Add product to cart or update quantity
    
    Args:
        uid: user id
        session_no: session number
        pid: product id
        available_stock: available stock count
    """
    conn = sqlite3.connect(FILENAME)
    cursor = conn.cursor()
    
    # Check if product is already in the cart
    cursor.execute("""
        SELECT qty FROM cart
        WHERE cid = ? AND sessionNo = ? AND pid = ?
    """, (uid, session_no, pid))
    
    result = cursor.fetchone()
    
    if result:
        current_qty = result[0]
        if current_qty + 1 <= available_stock:
            cursor.execute("""
                UPDATE cart SET qty = qty + 1
                WHERE cid = ? AND sessionNo = ? AND pid = ?
            """, (uid, session_no, pid))
            print(f"\nProduct updated in cart. (Now: {current_qty + 1})")
        else:
            print(f"\nNot enough items. Only {available_stock} are available.")
    else:
        cursor.execute("""
            INSERT INTO cart (cid, sessionNo, pid, qty)
            VALUES (?, ?, ?, 1)
        """, (uid, session_no, pid))
        print("\nProduct added to cart.")
    
    conn.commit()
    conn.close()

def view_cart(uid, session_no):
    """View and manage shopping cart
    
    Args:
        uid: user id
        session_no: session number
    """
    conn = sqlite3.connect(FILENAME)
    cursor = conn.cursor()
    
    cursor.execute("""
        SELECT c.pid, p.name, p.price, c.qty, p.stock_count
        FROM cart c
        JOIN products p ON c.pid = p.pid
        WHERE c.cid = ? AND c.sessionNo = ?
    """, (uid, session_no))
    
    cart_items = cursor.fetchall()
    conn.close()
    # Check for empty cart
    if not cart_items:
        print("\nCart is empty.")
        return
    # Cart management until user does not need to manage cart anymore
    while True:
        print(f"\n{'='*70}")
        print("SHOPPING CART")
        print('='*70)
        # Display current items
        total = 0
        for i, item in enumerate(cart_items, start=1):
            pid, name, price, qty, stock = item
            subtotal = price * qty
            total += subtotal
            print(f"{i}. {name}")
            print(f"   Price: ${price:.2f} | Qty: {qty} | Subtotal: ${subtotal:.2f}")
        
        print(f"\n{'='*70}")
        print(f"Total: ${total:.2f}")
        print('='*70)
        
        print(f'''
    1. Update Quantity
    2. Remove Product
    3. Proceed to Checkout
    4. Back to Menu
        ''')
        
        choice = input("> ").strip()
        
        if choice == '1':
            update_cart_quantity(uid, session_no, cart_items)
            # After update, reload the cart
            conn = sqlite3.connect(FILENAME)
            cursor = conn.cursor()
            cursor.execute("""
                SELECT c.pid, p.name, p.price, c.qty, p.stock_count
                FROM cart c
                JOIN products p ON c.pid = p.pid
                WHERE c.cid = ? AND c.sessionNo = ?
            """, (uid, session_no))
            cart_items = cursor.fetchall()
            conn.close()
        elif choice == '2':
            remove_from_cart(uid, session_no, cart_items)
            # After removing, reload the cart
            conn = sqlite3.connect(FILENAME)
            cursor = conn.cursor()
            cursor.execute("""
                SELECT c.pid, p.name, p.price, c.qty, p.stock_count
                FROM cart c
                JOIN products p ON c.pid = p.pid
                WHERE c.cid = ? AND c.sessionNo = ?
            """, (uid, session_no))
            cart_items = cursor.fetchall()
            conn.close()
            if not cart_items:
                print("\nYour cart is now empty.")
                return
        elif choice == '3':
            checkout(uid, session_no, cart_items)
            return
        elif choice == '4':
            break
        else:
            print("Invalid choice!")

def update_cart_quantity(uid, session_no, cart_items):
    """Update quantity of a product in cart
    
    Args:
        uid: user id
        session_no: session number
        cart_items: list of cart items
    """
    try:
        item_num = int(input("\nEnter item number to update: "))
        if 1 <= item_num <= len(cart_items):
            pid, name, price, current_qty, stock = cart_items[item_num - 1]
            new_qty = int(input(f"Enter new quantity (Available: {stock}): "))
            
            if new_qty < 0:
                print("You can't have a negative quantity.")
                return
            if new_qty == 0:
                remove_from_cart(uid, session_no, cart_items)
                return
            
            if new_qty > stock:
                print(f"Sorry, there are only {stock} items.")
                return
            #Update the state of the item in cart
            conn = sqlite3.connect(FILENAME)
            cursor = conn.cursor()
            cursor.execute("""
                UPDATE cart SET qty = ?
                WHERE cid = ? AND sessionNo = ? AND pid = ?
            """, (new_qty, uid, session_no, pid))
            conn.commit()
            conn.close()
            print("\nQuantity updated!")
        else:
            print("Invalid item number!")
    except ValueError:
        print("Invalid input!")

def remove_from_cart(uid, session_no, cart_items):
    """Remove a product from cart
    
    Args:
        uid: user id
        session_no: session number
        cart_items: list of cart items
    """
    try:
        item_num = int(input("\nAre you sure you want to remove an item?(Enter item number) "))
        if 1 <= item_num <= len(cart_items):
            pid = cart_items[item_num - 1][0]
            
            conn = sqlite3.connect(FILENAME)
            cursor = conn.cursor()
            #Update the state of the item in cart
            cursor.execute("""
                DELETE FROM cart
                WHERE cid = ? AND sessionNo = ? AND pid = ?
            """, (uid, session_no, pid))
            conn.commit()
            conn.close()
            print("\nProduct removed from cart.")
        else:
            print("Invalid item number.")
    except ValueError:
        print("Invalid input.")

def checkout(uid, session_no, cart_items):
    """Process checkout and create order
    
    Args:
        uid: user id
        session_no: session number
        cart_items: list of cart items
    """
    print(f"\n{'='*70}")
    print("CHECKOUT")
    print('='*70)
    
    # Display all items being bought
    total = 0
    for item in cart_items:
        pid, name, price, qty, stock = item
        subtotal = price * qty
        total += subtotal
        print(f"{name} - Qty: {qty} x ${price:.2f} = ${subtotal:.2f}")
    
    print(f"\n{'='*70}")
    print(f"Total: ${total:.2f}")
    print('='*70)

    # Ask for address and prompt user to confirm purchase
    shipping_address = input("\nEnter address: ").strip()
    
    if not shipping_address:
        print("Shipping address is required!")
        return
    
    confirm = input("\nConfirm order? (Y/N): ").strip().upper()
    
    if confirm != 'Y':
        print("\nOrder cancelled.")
        return
    
    conn = sqlite3.connect(FILENAME)
    cursor = conn.cursor()
    
    try:
        # Get next order number
        cursor.execute("SELECT MAX(ono) FROM orders")
        max_ono = cursor.fetchone()[0]
        ono = 1 if max_ono is None else max_ono + 1
        
        # Create order
        cursor.execute("""
            INSERT INTO orders (ono, cid, sessionNo, odate, shipping_address)
            VALUES (?, ?, ?, ?, ?)
        """, (ono, uid, session_no, datetime.now().date().isoformat(), shipping_address))
        
        # Create order lines and update stock
        line_no = 1
        for item in cart_items:
            pid, name, price, qty, stock = item
            
            # Verify stock is still available
            cursor.execute("SELECT stock_count FROM products WHERE pid = ?", (pid,))
            current_stock = cursor.fetchone()[0]
            
            if current_stock < qty:
                print(f"\nError: Insufficient stock for {name}. Order cancelled.")
                conn.rollback()
                conn.close()
                return
            
            # Insert order line
            cursor.execute("""
                INSERT INTO orderlines (ono, lineNo, pid, qty, uprice)
                VALUES (?, ?, ?, ?, ?)
            """, (ono, line_no, pid, qty, price))
            
            # Update stock
            cursor.execute("""
                UPDATE products SET stock_count = stock_count - ?
                WHERE pid = ?
            """, (qty, pid))
            
            line_no += 1
        
        # Clear cart
        cursor.execute("""
            DELETE FROM cart
            WHERE cid = ? AND sessionNo = ?
        """, (uid, session_no))
        
        conn.commit()
        
        print(f"\nOrder placed successfully. Order Number: {ono}")
        print(f"Total Amount: ${total:.2f}")
        
    except Exception as e:
        conn.rollback()
        print(f"\nError processing order: {e}")
    finally:
        conn.close()

def view_orders(uid):
    """View customer's order history
    
    Args:
        uid: user id
    """
    conn = sqlite3.connect(FILENAME)
    cursor = conn.cursor()
    
    # Display all orders of the customer
    cursor.execute("""
        SELECT o.ono, o.odate, o.shipping_address,
               SUM(ol.qty * ol.uprice) as total
        FROM orders o
        JOIN orderlines ol ON o.ono = ol.ono
        WHERE o.cid = ?
        GROUP BY o.ono, o.odate, o.shipping_address
        ORDER BY o.odate DESC
    """, (uid,))
    
    orders = cursor.fetchall()
    conn.close()
    
    if not orders:
        print("\nYou have no previous orders.")
        return
    
    page = 0
    page_size = 5
    total_pages = (len(orders) + page_size - 1) // page_size
    
    while True:
        print(f"\n{'='*70}")
        print(f"MY ORDERS (Page {page + 1} of {total_pages})")
        print('='*70)
        
        start = page * page_size
        end = min(start + page_size, len(orders))
        
        for i, order in enumerate(orders[start:end], start=1):
            ono, odate, address, total = order
            print(f"\n{i}. Order #{ono}")
            print(f"   Date: {odate}")
            print(f"   Shipping: {address}")
            print(f"   Total: ${total:.2f}")
        
        print("\n" + "="*70)
        options = []
        if page > 0:
            options.append("P: Previous")
        if page < total_pages - 1:
            options.append("N: Next")
        options.append("1-5: View Order Details")
        options.append("B: Back to Menu")
        
        print(" | ".join(options))
        choice = input("> ").strip().upper()
        
        if choice == 'N' and page < total_pages - 1:
            page += 1
        elif choice == 'P' and page > 0:
            page -= 1
        elif choice == 'B':
            break
        elif choice.isdigit() and 1 <= int(choice) <= min(5, end - start):
            order_idx = start + int(choice) - 1
            view_order_details(orders[order_idx][0])
        else:
            print("Invalid choice.")

def view_order_details(ono):
    """View detailed information for a specific order
    
    Args:
        ono: order number
    """
    conn = sqlite3.connect(FILENAME)
    cursor = conn.cursor()
    
    # Get order header
    cursor.execute("""
        SELECT odate, shipping_address
        FROM orders
        WHERE ono = ?
    """, (ono,))
    
    order_header = cursor.fetchone()
    
    # Get order lines, 1-COALESCE(ol.discount,0) is to account for undiscounted items
    cursor.execute("""
        SELECT p.name, p.category, ol.qty, ol.uprice, 
               (ol.qty * ol.uprice * (1 - COALESCE(ol.discount, 0))) as line_total
        FROM orderlines ol
        JOIN products p ON ol.pid = p.pid
        WHERE ol.ono = ?
    """, (ono,))
    
    order_lines = cursor.fetchall()
    conn.close()
    
    odate, address = order_header
    #Display order details
    print(f"\n{'='*70}")
    print(f"ORDER DETAILS - Order #{ono}")
    print(f"Date: {odate}")
    print(f"Shipping Address: {address}")
    print('='*70)
    
    grand_total = 0
    for line in order_lines:
        name, category, qty, uprice, line_total = line
        grand_total += line_total
        print(f"\n{name} ({category})")
        print(f"  Quantity: {qty} x ${uprice:.2f} = ${line_total:.2f}")
    print(f"\n{'='*70}")
    print(f"Grand Total: ${grand_total:.2f}")
    print('='*70)
    
    input("\nPress 'Enter' to continue.")