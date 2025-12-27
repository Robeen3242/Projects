import sqlite3 
from datetime import datetime, timedelta

def set_FILENAMEsales(filename):
    global FILENAME
    FILENAME = filename
def sales_menu(user):
    """Salesperson menu
    
    Args:
        user: dict with keys 'uid' and 'role'
    """
    while True:
        print(f"""
SALES MENU (User ID: {user['uid']}) Please select an action:
    1. Check and Update Products
    2. Get Sales Report
    3. See Top-Selling Products
    4. Logout
        """)
        
        try:
            choice = int(input("> "))
            if choice == 1:
                check_update_product()
            elif choice == 2:
                sales_report()
            elif choice == 3:
                top_selling_products()
            elif choice == 4:
                print("\nLogged out successfully!")
                break
            else:
                print("Invalid choice!")
        except ValueError:
            print("Invalid input. Please enter a number.")

def check_update_product():
    """Check and update product details"""
    try:
        pid = int(input("\nEnter Product ID: ").strip())
        
        conn = sqlite3.connect(FILENAME)
        cursor = conn.cursor()
        
        cursor.execute("""
            SELECT pid, name, category, price, stock_count, descr
            FROM products
            WHERE pid = ?
        """, (pid,))
        
        product = cursor.fetchone()
        
        if not product:
            print("\nProduct not found!")
            conn.close()
            return
        
        # Display product details
        print(f"\n{'='*60}")
        print("PRODUCT DETAILS")
        print('='*60)
        print(f"Product ID: {product[0]}")
        print(f"Name: {product[1]}")
        print(f"Category: {product[2]}")
        print(f"Price: ${product[3]:.2f}")
        print(f"Stock Count: {product[4]}")
        print(f"Description: {product[5]}")
        print('='*60)
        
        # Ask if user wants to update
        update = input("\nUpdate product? (y/N): ").strip().upper()
        
        if update != 'Y':
            conn.close()
            return
        
        print("\nWhat would you like to update?")
        print("1. Price")
        print("2. Stock Count")
        print("3. Both")
        print("4. Cancel")
        
        update_choice = input("> ").strip()
        
        if update_choice == '1':
            new_price = float(input("Enter new price: "))
            if new_price < 0:
                print("Price cannot be negative!")
                conn.close()
                return
            cursor.execute("UPDATE products SET price = ? WHERE pid = ?", 
                         (new_price, pid))
            conn.commit()
            print(f"\nPrice updated to ${new_price:.2f}")
            
        elif update_choice == '2':
            new_stock = int(input("Enter new stock count: "))
            if new_stock < 0:
                print("Stock count cannot be negative!")
                conn.close()
                return
            cursor.execute("UPDATE products SET stock_count = ? WHERE pid = ?", 
                         (new_stock, pid))
            conn.commit()
            print(f"\nStock count updated to {new_stock}")
            
        elif update_choice == '3':
            new_price = float(input("Enter new price: "))
            new_stock = int(input("Enter new stock count: "))
            if new_price < 0 or new_stock < 0:
                print("Price and stock count cannot be negative!")
                conn.close()
                return
            cursor.execute("""
                UPDATE products SET price = ?, stock_count = ?
                WHERE pid = ?
            """, (new_price, new_stock, pid))
            conn.commit()
            print(f"\nPrice updated to ${new_price:.2f}")
            print(f"Stock count updated to {new_stock}")
        
        conn.close()
        
    except ValueError:
        print("Invalid input!")
    except Exception as e:
        print(f"Error: {e}")

def sales_report():
    """Generate weekly sales report for past 7 days"""
    conn = sqlite3.connect(FILENAME)
    cursor = conn.cursor()
    
    # Calculate date 7 days ago
    seven_days_ago = (datetime.now() - timedelta(days=7)).date().isoformat()
    
    # Number of distinct orders
    cursor.execute("""
        SELECT COUNT(DISTINCT ono)
        FROM orders
        WHERE odate >= ?
    """, (seven_days_ago,))
    distinct_orders = cursor.fetchone()[0]
    
    # Number of distinct products sold
    cursor.execute("""
        SELECT COUNT(DISTINCT ol.pid)
        FROM orderlines ol
        JOIN orders o ON ol.ono = o.ono
        WHERE o.odate >= ?
    """, (seven_days_ago,))
    distinct_products = cursor.fetchone()[0]
    
    # Number of distinct customers with purchases
    cursor.execute("""
        SELECT COUNT(DISTINCT cid)
        FROM orders
        WHERE odate >= ?
    """, (seven_days_ago,))
    distinct_customers = cursor.fetchone()[0]
    
    # Average amount spent per customer
    cursor.execute("""
        SELECT AVG(customer_total)
        FROM (
            SELECT o.cid, SUM(ol.qty * ol.uprice) as customer_total
            FROM orders o
            JOIN orderlines ol ON o.ono = ol.ono
            WHERE o.odate >= ?
            GROUP BY o.cid
        )
    """, (seven_days_ago,))
    avg_per_customer = cursor.fetchone()[0] or 0
    
    # Total sales amount
    cursor.execute("""
        SELECT SUM(ol.qty * ol.uprice)
        FROM orders o
        JOIN orderlines ol ON o.ono = ol.ono
        WHERE o.odate >= ?
    """, (seven_days_ago,))
    total_sales = cursor.fetchone()[0] or 0
    
    conn.close()
    
    # Display report
    print(f"\n{'='*60}")
    print("WEEKLY SALES REPORT (Last 7 Days)")
    print('='*60)
    print(f"Distinct Orders: {distinct_orders}")
    print(f"Distinct Products Sold: {distinct_products}")
    print(f"Distinct Customers: {distinct_customers}")
    print(f"Average Spent per Customer: ${avg_per_customer:.2f}")
    print(f"Total Sales Amount: ${total_sales:.2f}")
    print('='*60)
    
    input("\nPress Enter to continue...")

def top_selling_products():
    """Display top-selling products by orders and views"""
    conn = sqlite3.connect(FILENAME)
    cursor = conn.cursor()
    
    # Top products by distinct orders (with ties at position 3)
    cursor.execute("""
        SELECT p.pid, p.name, COUNT(DISTINCT ol.ono) as order_count
        FROM products p
        JOIN orderlines ol ON p.pid = ol.pid
        GROUP BY p.pid, p.name
        ORDER BY order_count DESC
    """)
    
    all_products_by_orders = cursor.fetchall()
    
    # Get top 3 with ties
    top_by_orders = []
    if len(all_products_by_orders) > 0:
        if len(all_products_by_orders) <= 3:
            top_by_orders = all_products_by_orders
        else:
            # Get first 3
            top_by_orders = all_products_by_orders[:3]
            third_count = top_by_orders[2][2]
            
            # Add all ties at position 3
            for i in range(3, len(all_products_by_orders)):
                if all_products_by_orders[i][2] == third_count:
                    top_by_orders.append(all_products_by_orders[i])
                else:
                    break
    
    # Top products by views (with ties at position 3)
    cursor.execute("""
        SELECT p.pid, p.name, COUNT(*) as view_count
        FROM products p
        JOIN viewedProduct vp ON p.pid = vp.pid
        GROUP BY p.pid, p.name
        ORDER BY view_count DESC
    """)
    
    all_products_by_views = cursor.fetchall()
    
    # Get top 3 with ties
    top_by_views = []
    if len(all_products_by_views) > 0:
        if len(all_products_by_views) <= 3:
            top_by_views = all_products_by_views
        else:
            # Get first 3
            top_by_views = all_products_by_views[:3]
            third_count = top_by_views[2][2]
            
            # Add all ties at position 3
            for i in range(3, len(all_products_by_views)):
                if all_products_by_views[i][2] == third_count:
                    top_by_views.append(all_products_by_views[i])
                else:
                    break
    
    conn.close()
    
    # Display results
    print(f"\n{'='*60}")
    print("TOP SELLING PRODUCTS")
    print('='*60)
    
    print("\nTop Products by Orders:")
    print("-" * 60)
    if top_by_orders:
        for i, product in enumerate(top_by_orders, start=1):
            print(f"{i}. {product[1]} (Product ID: {product[0]})")
            print(f"   Appears in {product[2]} distinct order(s)")
    else:
        print("No order data available")
    
    print("\nTop Products by Views:")
    print("-" * 60)
    if top_by_views:
        for i, product in enumerate(top_by_views, start=1):
            print(f"{i}. {product[1]} (Product ID: {product[0]})")
            print(f"   {product[2]} view(s)")
    else:
        print("No view data available")
    
    print('='*60)
    
    input("\nPress Enter to continue...")