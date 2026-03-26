from flask import Flask, render_template, render_template_string, request, redirect, session, url_for
import sqlite3

def init_db():
    conn = sqlite3.connect('login.db')
    cursor = conn.cursor()
    cursor.execute('CREATE TABLE IF NOT EXISTS user (id INTEGER PRIMARY KEY, username TEXT, password TEXT)')
    cursor.execute('SELECT count(*) FROM user')
    if cursor.fetchone()[0] == 0:
        cursor.execute("INSERT INTO user (username, password) VALUES ('admin', 'admin')")
        cursor.execute("INSERT INTO user (username, password) VALUES ('guest', 'guest')")
        cursor.execute("INSERT INTO user (username, password) VALUES ('chiehhhhh', '12345')")
        conn.commit()
    conn.close()

mock_db_products = {
    114518: {"name": "RTX 5090", "price": "$70000", "description": "社費加起來都買不起一張嗚嗚嗚", "public": True},
    114516: {"name": "HP 16GB DDR5 4800 ECC RAM (for Z2) PC用記憶體", "price": "$1000000000", "description": "最近很貴的東西", "public": True},
    114512: {"name": "扁平鯊", "price": "$999999999", "description": "付不起也可以用RAM pay", "public": True},
    114514: {"name": "flag", "price": "$0", "description": "ZLCSC{Kn0nk.kNonK...I_DoOR!}", "public": False}
}

app = Flask(__name__)
app.secret_key = "super_secret_lab_key" # 必須設定這個才能使用 session
app.config['FLAG'] = "ZLCSC{simple_SST1...It'5_1nTeRES71n9___Ri9h7?}"

# ==========================================
# HTML Template
# ==========================================
def get_base_html(content):
    return f"""
    <!DOCTYPE html>
    <html lang="zh-TW">
    <head>
        <meta charset="UTF-8">
        <title>ZLCSC SHOP</title>
        <style>
            body {{ font-family: Arial, sans-serif; margin: 0; padding: 20px; background-color: #f4f4f9; }}
            .navbar {{ background-color: #333; padding: 15px; color: white; display: flex; justify-content: space-between; align-items: center; border-radius: 5px; }}
            .navbar a {{ color: white; text-decoration: none; margin-right: 15px; font-weight: bold; }}
            .search-bar {{ padding: 5px; }}
            .container {{ margin-top: 20px; background: white; padding: 20px; border-radius: 5px; box-shadow: 0 2px 5px rgba(0,0,0,0.1); }}
            .product-card {{ border: 1px solid #ddd; padding: 15px; margin-bottom: 10px; border-radius: 5px; background-color: #fff; }}
            .btn {{ padding: 8px 15px; background-color: #4CAF50; color: white; border: none; border-radius: 4px; cursor: pointer; text-decoration: none; }}
            .btn:hover {{ background-color: #45a049; }}
            .error {{ color: red; font-weight: bold; }}
        </style>
    </head>
    <body>
        <div class="navbar">
            <div>
                <a href="/home">ZLCSC SHOP</a>
                <a href="/logout">Log Out</a>
            </div>
            <div>
                <form action="/search" method="GET" style="margin: 0;">
                    <input type="text" name="q" class="search-bar" placeholder="search">
                    <button type="submit">搜尋</button>
                </form>
            </div>
        </div>
        <div class="container">
            {content}
        </div>
    </body>
    </html>
    """

# ==========================================
# SQL Injection
# ==========================================
@app.route('/', methods=['GET', 'POST'])
def index():
    username = None
    password = None
    message = None

    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')

        if username and password:
            conn = sqlite3.connect('login.db')
            cursor = conn.cursor()
            cursor.execute(f"SELECT * FROM user WHERE username = '{username}' AND password = '{password}'")
            result = cursor.fetchone()
            conn.close()

            if result:
                session['username'] = result[1]
                
                if username == 'admin':
                    return redirect('/admin')
                else:
                    return redirect('/home')
            else:
                message = "fail."

    return render_template('index.html', username=username, password=password, message=message)

@app.route('/logout')
def logout():
    session.pop('username', None)
    return redirect('/')

# ==========================================
# Admin
# ==========================================
@app.route('/admin')
def admin():
    return render_template('admin.html')

@app.route('/home')
def home():
    if 'username' not in session: return redirect('/')
    content = f"<h2>Welcome to ZLCSC SHOP, {session['username']}!</h2><p>Please choose the products you want to purchase:</p>"
    content += "<div style='display: flex; gap: 15px; flex-wrap: wrap;'>"
    
    for pid, p in mock_db_products.items():
        if p['public']:
            content += f"""
            <div class="product-card" style="width: 250px;">
                <h3>{p['name']}</h3>
                <p style="color: green; font-weight: bold;">{p['price']}</p>
                <a href="/product/{pid}" class="btn">View Product Details</a>
            </div>
            """
    content += "</div>"
    
    return render_template_string(get_base_html(content))

# ==========================================
# IDOR
# ==========================================
@app.route('/product/<int:product_id>')
def product_detail(product_id):
    if 'username' not in session: return redirect('/')
    
    product = mock_db_products.get(product_id)
    if not product:
        return render_template_string(get_base_html("<h2>❌ Product not found.</h2>"))
    
    content = f"""
    <h2>Product Details (Product ID: {product_id})</h2>
    <div class="product-card" style="border-left: 5px solid {'#4CAF50' if product['public'] else 'red'};">
        <h2>{product['name']}</h2>
        <p style="font-size: 20px; color: green; font-weight: bold;">{product['price']}</p>
        <p><strong>Product Description:</strong> {product['description']}</p>
        <br>
        <a href="/buy/{product_id}" class="btn">敗</a>
    </div>
    <br>
    <a href="/home">Return to Shop</a>
    """
    return render_template_string(get_base_html(content))

@app.route('/buy/<int:product_id>')
def buy(product_id):
    if 'username' not in session: return redirect('/')
    
    product = mock_db_products.get(product_id)
    if not product: return redirect('/home')
    
    content = f"""
    <h2>Purchase Successful!</h2>
    <div class="product-card">
        <p>Thank you for your purchase, you have successfully placed an order for: <strong>{product['name']}</strong></p>
        <p>Charged: {product['price']}</p>
        <p>The product will be shipped within 3-5 business days.</p>
    </div>
    <a href="/home" class="btn">Continue Shopping</a>
    """
    return render_template_string(get_base_html(content))

# ==========================================
# SSTI
# ==========================================
@app.route('/search')
def search():
    query = request.args.get('q', '')

    result_content = f"""
    <h2>Search Results</h2>
    <p>The keyword you searched for is: <strong style="color: blue;">{query}</strong></p>
    <p>Sorry, no products found related to your search.</p>
    <a href="/home">Return to Shop</a>
    """
    final_html = get_base_html(result_content)
    return render_template_string(final_html)

# ==========================================
# robots
# ==========================================
@app.route('/robots.txt')
def robots():
    return "User-agent: *\nDisallow: /secret\n", 200, {'Content-Type': 'text/plain'}

@app.route('/secret')
def secret():
    return "ZLCSC{0h_oh???OHHHHHH!!!u_r_My_fL0weR~~~}", 200, {'Content-Type': 'text/plain'}

if __name__ == '__main__':
    init_db()
    app.run(debug=True, port=5000)