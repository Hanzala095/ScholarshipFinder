from flask import Flask, render_template, request, redirect, session
from database.db import get_connection

app = Flask(__name__)
app.secret_key = 'your_secret_key_here'  # Change to a random secret key later

# Home page: Show all scholarships
@app.route('/')
def home():
    conn = get_connection()
    cursor = conn.cursor(dictionary=True)
    cursor.execute("SELECT * FROM scholarships")
    data = cursor.fetchall()
    cursor.close()
    conn.close()
    return render_template('index.html', scholarships=data)

# Search page: Search scholarships by eligibility, name, or provider
@app.route('/search', methods=['GET', 'POST'])
def search():
    scholarships = []
    keyword = ""

    if request.method == 'POST':
        keyword = request.form.get('keyword', '').strip()

        conn = get_connection()
        cursor = conn.cursor(dictionary=True)
        query = """
            SELECT id, name, provider, eligibility, deadline, link
            FROM scholarships
            WHERE 
                name LIKE %s OR
                provider LIKE %s OR
                eligibility LIKE %s
        """
        like_keyword = f"%{keyword}%"
        cursor.execute(query, (like_keyword, like_keyword, like_keyword))
        scholarships = cursor.fetchall()
        cursor.close()
        conn.close()

    return render_template('search.html', scholarships=scholarships, keyword=keyword)

# Admin Login Page
@app.route('/admin_login', methods=['GET', 'POST'])
def admin_login():
    error = None
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        if username == 'admin' and password == 'admin123':
            session['admin_logged_in'] = True
            return redirect('/add')
        else:
            error = "Invalid Credentials. Please try again."

    return render_template('admin_login.html', error=error)

# Admin Add Scholarship Page (Protected)
@app.route('/add', methods=['GET', 'POST'])
def add_scholarship():
    if not session.get('admin_logged_in'):
        return redirect('/admin_login')

    if request.method == 'POST':
        name = request.form['name']
        provider = request.form['provider']
        eligibility = request.form['eligibility']
        deadline = request.form['deadline']
        link = request.form['link']

        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute("""
            INSERT INTO scholarships (name, provider, eligibility, deadline, link)
            VALUES (%s, %s, %s, %s, %s)
        """, (name, provider, eligibility, deadline, link))
        conn.commit()
        cursor.close()
        conn.close()
        return redirect('/')

    return render_template('add.html')

# Save student's email for reminder
@app.route('/save_email', methods=['POST'])
def save_email():
    email = request.form['email']
    scholarship_id = request.form['scholarship_id']

    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("""
        INSERT INTO student_emails (email, scholarship_id)
        VALUES (%s, %s)
    """, (email, scholarship_id))
    conn.commit()
    cursor.close()
    conn.close()

    return redirect('/search')

# Admin Logout
@app.route('/logout')
def logout():
    session.pop('admin_logged_in', None)
    return redirect('/')

# Run the app
if __name__ == '__main__':
    app.run(debug=True)
