import os
import math
import uuid
import random
import time
import re
import smtplib
from decimal import Decimal
import ssl
import csv
import io
import zipfile
import shutil
from datetime import datetime, timedelta
from email.message import EmailMessage
from flask import send_file
from functools import wraps 
from flask import Flask, render_template, request, redirect, url_for, session, flash

from flask import Flask, render_template, request, redirect, url_for, send_from_directory, jsonify, session, flash
from flask.cli import with_appcontext
import qrcode
from apscheduler.schedulers.background import BackgroundScheduler

from captcha.image import ImageCaptcha # <--- Add this
import random
import string
from flask import send_file, Response # Ensure these are imported
import requests # <--- Add this at the top

# ---------------------------------------------------------
# DATABASE IMPORT
# Ensure you have a db.py file with a get_db_conn() function
# ---------------------------------------------------------
from db import get_db_conn

# ========================================================
# CONFIGURATION
# ========================================================
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
app = Flask(
    __name__,
    template_folder=os.path.join(BASE_DIR, 'templates'),
    static_folder=os.path.join(BASE_DIR, 'static')
)
app.secret_key = os.getenv("FLASK_SECRET_KEY", "change_this_to_a_secure_random_string")
# ========================================================
# DISABLE BROWSER CACHING (Prevents Back Button Issues)
# ========================================================
@app.after_request
def add_header(response):
    """
    Add headers to both force latest content plus HTTP 1.1 'Cache-Control: no-cache'
    to tell the browser not to save the page history.
    """
    response.headers["Cache-Control"] = "no-cache, no-store, must-revalidate, public, max-age=0"
    response.headers["Pragma"] = "no-cache"
    response.headers["Expires"] = "0"
    return response
# ========================================================
# SECURITY DECORATORS
# ========================================================

def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'role' not in session:
            return redirect(url_for('login'))
        return f(*args, **kwargs)
    return decorated_function

def admin_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'role' not in session:
            return redirect(url_for('login'))
        if session.get('role') != 'admin':
            # Option: Redirect to student dashboard if they are a student trying to access admin
            if session.get('role') == 'student':
                return redirect(url_for('student_dashboard'))
            return redirect(url_for('login'))
        return f(*args, **kwargs)
    return decorated_function


# Email Configuration
SMTP_HOST = "smtp.gmail.com"
SMTP_PORT = 587
SMTP_USER = "isulibrary66@gmail.com"
SMTP_PASS = "jxlo titm azos xcez"  # App Password
MAIL_FROM = "Library <isulibrary66@gmail.com>"

# QR Code Folder
QR_FOLDER = os.path.join(app.static_folder, 'qrcodes')
os.makedirs(QR_FOLDER, exist_ok=True)

# Security & Validation
login_attempts = {}
EMAIL_RE = re.compile(r'^[^@\s]+@[^@\s]+\.[^@\s]+$')

# ========================================================
# HELPER FUNCTIONS (Email, OTP, Scheduler)
# ========================================================

def _send_email(to_addr: str, subject: str, html_body: str, text_body: str = None) -> bool:
    """Generic function to send emails via SMTP."""
    if not EMAIL_RE.match(to_addr or ""):
        return False

    # System Generated Footer
    footer_html = """
    <br><br>
    <hr style="border: 0; border-top: 1px solid #eee;">
    <p style="font-size: 12px; color: #888; font-style: italic;">
        This is a system generated email. Do not reply.
    </p>
    """
    html_body += footer_html

    msg = EmailMessage()
    msg["From"] = MAIL_FROM
    msg["To"] = to_addr
    msg["Subject"] = subject
    
    if not text_body:
        text_body = "Please enable HTML to view this email."
    
    msg.set_content(text_body)
    msg.add_alternative(html_body, subtype="html")

    try:
        ctx = ssl.create_default_context()
        with smtplib.SMTP(SMTP_HOST, SMTP_PORT) as s:
            s.starttls(context=ctx)
            s.login(SMTP_USER, SMTP_PASS)
            s.send_message(msg)
        return True
    except Exception as e:
        print(f"[Email Error] {e}")
        return False

def _send_email_with_attachment(to_addr, subject, body, attachment_bytes, filename):
    body += "\n\n---\nThis is a system generated email. Do not reply."
    
    msg = EmailMessage()
    msg["From"] = MAIL_FROM
    msg["To"] = to_addr
    msg["Subject"] = subject
    msg.set_content(body)

    # Attach ZIP
    msg.add_attachment(
        attachment_bytes,
        maintype='application',
        subtype='zip',
        filename=filename
    )

    try:
        ctx = ssl.create_default_context()
        with smtplib.SMTP(SMTP_HOST, SMTP_PORT) as s:
            s.starttls(context=ctx)
            s.login(SMTP_USER, SMTP_PASS)
            s.send_message(msg)
        return True
    except Exception as e:
        print(f"[Email Error] {e}")
        return False

def send_otp(email):
    """Generates a 6-digit OTP, saves to session, and emails it."""
    otp = str(random.randint(100000, 999999))
    session['otp'] = otp
    session['otp_time'] = time.time()
    
    subject = "Your Library OTP Code"
    html_body = f"""
    <div style="font-family: sans-serif; padding: 20px; border: 1px solid #ddd; border-radius: 10px;">
        <h2>Login Verification</h2>
        <p>Your OTP code is: <b style="font-size: 24px; color: #ff7a1a;">{otp}</b></p>
        <p>This code expires in 5 minutes.</p>
    </div>
    """
    _send_email(email, subject, html_body, f"OTP: {otp}")

def check_and_email_due_soon():
    """
    Background Job: Finds books due in < 5 hours that haven't been notified yet.
    """
    conn = get_db_conn()
    try:
        with conn.cursor() as cur:
            cur.execute("""
                SELECT
                  t.tx_id,
                  t.student_number,
                  s.student_name,
                  s.contact AS email_like,
                  t.accession_number,
                  b.title,
                  t.due_date
                FROM transactions t
                JOIN (
                    -- Get the latest transaction per book to ensure we notify the current borrower
                    SELECT accession_number, MAX(DATE) AS max_date
                    FROM transactions
                    GROUP BY accession_number
                ) last ON last.accession_number = t.accession_number AND last.max_date = t.DATE
                JOIN books b     ON b.accession_number = t.accession_number
                JOIN students s  ON s.student_number   = t.student_number
                LEFT JOIN due_soon_notifications dsn ON dsn.tx_id = t.tx_id
                WHERE b.STATUS = 'Borrowed'
                  AND t.action_type = 'borrow'
                  AND t.due_date IS NOT NULL
                  AND t.due_date BETWEEN NOW() AND DATE_ADD(NOW(), INTERVAL 5 HOUR)
                  AND dsn.tx_id IS NULL
            """)
            rows = cur.fetchall()

            sent_count = 0
            for r in rows:
                due_str = r["due_date"].strftime("%b %d, %Y %I:%M %p")
                subject = f"Reminder: '{r['title']}' is due soon"
                html = f"""
                    <p>Hi {r['student_name']},</p>
                    <p>The book <b>{r['title']}</b> (Accession: {r['accession_number']}) is due on <b style="color:red;">{due_str}</b>.</p>
                    <p>Please return it to avoid penalties.</p>
                """
                
                if _send_email(r["email_like"], subject, html):
                    # Log notification to DB so we don't send it again
                    cur.execute("""
                        INSERT IGNORE INTO due_soon_notifications (tx_id, student_number, accession_number)
                        VALUES (%s, %s, %s)
                    """, (r["tx_id"], r["student_number"], r["accession_number"]))
                    sent_count += 1
            
            if sent_count > 0:
                conn.commit()
                print(f"[Scheduler] Sent {sent_count} due-soon emails.")

    except Exception as e:
        print(f"[Scheduler Error] {e}")
    finally:
        try: conn.close()
        except: pass

# Initialize Scheduler
if os.environ.get("WERKZEUG_RUN_MAIN") == "true":
    sched = BackgroundScheduler(timezone="Asia/Manila")
    sched.add_job(check_and_email_due_soon, "interval", minutes=5, id="due_soon_email")
    sched.start()
    print("⏰ Scheduler started.")


@app.route('/captcha-image')
def captcha_image():
    image = ImageCaptcha(width=280, height=90)
    # Generate random 5 character string
    captcha_text = ''.join(random.choices(string.ascii_uppercase + string.digits, k=5))
    # Store in session to check later
    session['captcha_code'] = captcha_text
    
    # Generate image
    data = image.generate(captcha_text)
    return send_file(data, mimetype='image/png')

# ========================================================
# ROUTES: AUTHENTICATION
# ========================================================

@app.route('/')
def root():
    return redirect(url_for('login'))

@app.route('/login', methods=['GET', 'POST'])
def login():
    # --- Redirect if already logged in ---
    if 'role' in session:
        if session['role'] == 'admin':
            return redirect(url_for('index'))
        elif session['role'] == 'student':
            s_num = session.get('student', {}).get('student_number')
            if s_num:
                return redirect(url_for('student_details', student_number=s_num))

    ip = request.remote_addr
    now = datetime.now()

    # Rate Limiting Logic
    if ip not in login_attempts:
        login_attempts[ip] = {"count": 0, "lock_until": None}

    lock_until = login_attempts[ip]["lock_until"]
    if lock_until and now < lock_until:
        remaining = int((lock_until - now).total_seconds())
        return render_template("login.html", error=f"Locked. Try again in {remaining}s.")

    if request.method == 'POST':
        # --- 1. GOOGLE RECAPTCHA VERIFICATION ---
        recaptcha_response = request.form.get('g-recaptcha-response')
        
        if not recaptcha_response:
             return render_template('login.html', error="❌ Please complete the CAPTCHA.")

        # Verify with Google
        GOOGLE_SECRET_KEY = "6Le9hxYsAAAAAIU0j1hT9QK545zmJip9FyiKB43E"
        verify_url = "https://www.google.com/recaptcha/api/siteverify"
        payload = {'secret': GOOGLE_SECRET_KEY, 'response': recaptcha_response}
        
        try:
            response = requests.post(verify_url, data=payload)
            result = response.json()
            if not result.get("success"):
                return render_template('login.html', error="❌ CAPTCHA verification failed. Are you a robot?")
        except:
            return render_template('login.html', error="❌ Could not connect to CAPTCHA service.")
        # ----------------------------------------

        username = request.form.get('username', '').strip()
        password = request.form.get('password', '').strip()

        # 1. ADMIN LOGIN
        if username == 'admin' and password == 'Admin123456@':
            session['temp_user'] = username 
            session['temp_role'] = 'admin'
            send_otp(SMTP_USER) 
            login_attempts[ip] = {"count": 0, "lock_until": None}
            return redirect(url_for('verify_otp'))

        # 2. STUDENT LOGIN
        conn = get_db_conn()
        try:
            with conn.cursor() as cur:
                cur.execute("SELECT * FROM students WHERE student_number=%s AND password=%s", (username, password))
                student = cur.fetchone()

                if student:
                    student_email = student.get('contact')
                    if not student_email or '@' not in student_email:
                          return render_template('login.html', error="No email registered. Cannot send OTP.")

                    session['temp_student'] = student
                    session['temp_role'] = 'student'
                    
                    send_otp(student_email)
                    
                    login_attempts[ip] = {"count": 0, "lock_until": None}
                    return redirect(url_for('verify_otp'))
        finally:
            conn.close()

        # 3. FAILED LOGIN
        login_attempts[ip]["count"] += 1
        if login_attempts[ip]["count"] >= 3:
            login_attempts[ip]["lock_until"] = now + timedelta(seconds=90)
            return render_template("login.html", error="❌ Too many failed attempts. Locked for 90s.")
        
        return render_template('login.html', error="Invalid credentials.")

    return render_template('login.html')

@app.route('/verify-otp', methods=['GET', 'POST'])
def verify_otp():
    # Check if we are in the middle of a login attempt
    if 'temp_role' not in session:
        return redirect(url_for('login'))

    if request.method == 'POST':
        entered_otp = request.form.get('otp', '').strip()
        current_time = time.time()

        if 'otp' in session and (current_time - session.get('otp_time', 0)) < 300:
            if entered_otp == session['otp']:
                # --- SUCCESS: PROMOTE TEMP SESSION TO REAL SESSION ---
                session['role'] = session['temp_role']
                
                if session['role'] == 'admin':
                    session['user'] = session['temp_user']
                    # Cleanup temp
                    session.pop('temp_user', None)
                    session.pop('temp_role', None)
                    return redirect(url_for('index'))
                
                elif session['role'] == 'student':
                    session['student'] = session['temp_student']
                    # Cleanup temp
                    session.pop('temp_student', None)
                    session.pop('temp_role', None)
                    return redirect(url_for('student_details', student_number=session['student']['student_number']))
            else:
                return render_template('verify_otp.html', error="Incorrect OTP.")
        else:
            return render_template('verify_otp.html', error="OTP expired.")

    return render_template('verify_otp.html')

@app.route('/resend-otp', methods=['POST'])
def resend_otp():
    if session.get('role') == 'admin':
        send_otp(SMTP_USER)
    elif session.get('role') == 'student':
        send_otp(session['student']['contact'])
    return render_template('verify_otp.html', message="OTP has been resent.")

@app.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('login'))

# ========================================================
# ROUTES: BACKUP SYSTEM
# ========================================================

@app.route('/backup')

def backup_page():
    if session.get('role') != 'admin': return redirect(url_for('login'))
    stats = {'students': 0, 'books': 0, 'transactions': 0, 'payments': 0, 'qrcodes': 0}
    conn = get_db_conn()
    try:
        with conn.cursor() as cur:
            cur.execute("SELECT COUNT(*) as c FROM students"); stats['students'] = cur.fetchone()['c']
            cur.execute("SELECT COUNT(*) as c FROM books"); stats['books'] = cur.fetchone()['c']
            cur.execute("SELECT COUNT(*) as c FROM transactions"); stats['transactions'] = cur.fetchone()['c']
            cur.execute("SELECT COUNT(*) as c FROM payments"); stats['payments'] = cur.fetchone()['c']
        if os.path.exists(QR_FOLDER):
            stats['qrcodes'] = len([name for name in os.listdir(QR_FOLDER) if name.endswith('.png')])
        return render_template('backup.html', stats=stats)
    except Exception as e:
        return f"<h1>Error loading backup</h1><p>{e}</p>"
    finally: conn.close()

def generate_full_backup_zip():
    conn = get_db_conn()
    mem_file = io.BytesIO()
    
    try:
        with zipfile.ZipFile(mem_file, 'w', zipfile.ZIP_DEFLATED) as zf:
            with conn.cursor() as cur:
                conn.commit() # FORCE REFRESH
                # ✅ INCLUDED 'lost_book_resolutions' in backup list
                for table in ['students', 'books', 'transactions', 'payments', 'lost_book_resolutions']:
                    if table == 'transactions':
                        # Export relevant columns including is_penalty_paid
                        cur.execute("""
                            SELECT tx_id, student_number, accession_number, call_number, 
                                   action_type, date, due_date, returned_date, is_penalty_paid 
                            FROM transactions
                        """)
                    else:
                        cur.execute(f"SELECT * FROM {table}")
                    
                    rows = cur.fetchall()
                    si = io.StringIO()
                    if rows:
                        writer = csv.DictWriter(si, fieldnames=rows[0].keys())
                        writer.writeheader()
                        writer.writerows(rows)
                    zf.writestr(f"{table}.csv", si.getvalue())
            
            # Add QR Codes
            if os.path.exists(QR_FOLDER):
                for root, dirs, files in os.walk(QR_FOLDER):
                    for file in files:
                        file_path = os.path.join(root, file)
                        zf.write(file_path, arcname=os.path.join('qrcodes', file))
            
            zf.writestr('README.txt', f"Backup generated on {datetime.now()}")
    finally:
        conn.close()
    
    mem_file.seek(0)
    return mem_file

@app.route('/backup/download')
def download_backup():
    if session.get('role') != 'admin': return "Unauthorized", 403
    type_arg = request.args.get('type', 'all')
    timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')

    if type_arg == 'all':
        mem = generate_full_backup_zip()
        return send_file(mem, download_name=f"library_full_backup_{timestamp}.zip", as_attachment=True, mimetype='application/zip')
    
    # Single CSV Export Logic
    conn = get_db_conn()
    try:
        with conn.cursor() as cur:
            conn.commit() # Force refresh
            if type_arg == 'transactions':
                cur.execute("""
                    SELECT tx_id, student_number, accession_number, call_number, 
                           action_type, date, due_date, returned_date, is_penalty_paid 
                    FROM transactions
                """)
            # ✅ FIX: Added 'lost_book_resolutions' support
            elif type_arg in ['students', 'books', 'payments', 'lost_book_resolutions']:
                cur.execute(f"SELECT * FROM {type_arg}")
            else:
                return "Invalid table", 400

            rows = cur.fetchall()
            si = io.StringIO()
            if rows:
                writer = csv.DictWriter(si, fieldnames=rows[0].keys())
                writer.writeheader()
                writer.writerows(rows)
            
            mem = io.BytesIO()
            mem.write(si.getvalue().encode('utf-8'))
            mem.seek(0)
            
            return send_file(
                mem, 
                download_name=f"{type_arg}_backup_{timestamp}.csv", 
                as_attachment=True, 
                mimetype='text/csv'
            )
    finally:
        conn.close()

@app.route('/backup/email', methods=['POST'])
def email_backup():
    if session.get('role') != 'admin': return "Unauthorized", 403
    
    try:
        mem = generate_full_backup_zip()
        fname = f"backup_{datetime.now().strftime('%Y%m%d_%H%M%S')}.zip"
        
        if _send_email_with_attachment(
            to_addr=SMTP_USER, 
            subject="System Backup (Library)",
            body=f"Attached is the full system backup generated at {datetime.now()}.",
            attachment_bytes=mem.getvalue(),
            filename=fname
        ):
            flash("Backup emailed successfully!", "success")
        else: flash("Failed to send email.", "error")
    except Exception as e:
        flash(f"Error generating/sending backup: {e}", "error")
        
    return redirect(url_for('backup_page'))

@app.route('/backup/restore', methods=['POST'])
def restore_backup():
    if session.get('role') != 'admin': return "Unauthorized", 403
    
    if 'backup_file' not in request.files:
        flash("No file selected", "error")
        return redirect(url_for('backup_page'))
        
    file = request.files['backup_file']
    if not file.filename.endswith('.zip'):
        flash("Please upload a .zip file", "error")
        return redirect(url_for('backup_page'))

    conn = get_db_conn()
    try:
        # 1. Open Zip
        with zipfile.ZipFile(file, 'r') as zf:
            file_list = zf.namelist()
            
            # 2. Database Restore (WIPE & LOAD)
            with conn.cursor() as cur:
                # Disable FK checks to allow truncate
                cur.execute("SET FOREIGN_KEY_CHECKS = 0")
                
                # ✅ FIX: Added 'lost_book_resolutions' to restore list
                tables = ['students', 'books', 'transactions', 'payments', 'lost_book_resolutions']
                
                for table in tables:
                    csv_name = f"{table}.csv"
                    if csv_name in file_list:
                        # TRUNCATE current table
                        cur.execute(f"TRUNCATE TABLE {table}")
                        
                        # READ CSV from zip
                        with zf.open(csv_name) as f:
                            csv_text = io.TextIOWrapper(f, encoding='utf-8')
                            reader = csv.DictReader(csv_text)
                            
                            # Insert Rows
                            for row in reader:
                                cols = ', '.join(row.keys())
                                # Handle NULLs for empty strings
                                vals = [None if v == '' else v for v in row.values()]
                                placeholders = ', '.join(['%s'] * len(vals))
                                sql = f"INSERT INTO {table} ({cols}) VALUES ({placeholders})"
                                cur.execute(sql, vals)
                
                cur.execute("SET FOREIGN_KEY_CHECKS = 1")
                conn.commit()

            # 3. Restore QR Codes
            count_imgs = 0
            for member in file_list:
                if member.startswith('qrcodes/') and member.endswith('.png'):
                    img_data = zf.read(member)
                    fname = os.path.basename(member)
                    if fname:
                        with open(os.path.join(QR_FOLDER, fname), 'wb') as f_out:
                            f_out.write(img_data)
                        count_imgs += 1

        flash(f"System Restored! Database refreshed and {count_imgs} QR codes recovered.", "success")
        
    except Exception as e:
        print(e)
        flash(f"Critical Error during restore: {str(e)}", "error")
        
    finally:
        conn.close()
        
    return redirect(url_for('backup_page'))

# ========================================================
# ROUTES: ADMIN DASHBOARD & METRICS
# ========================================================

@app.route('/index')
  # <--- PROTECTS THE ROUTE
def index():
    return render_template('index.html')

@app.route('/api/metrics')
def api_metrics():
    conn = get_db_conn()
    try:
        with conn.cursor() as cur:
            cur.execute("SELECT COUNT(*) AS c FROM students")
            students = cur.fetchone()["c"]
            cur.execute("SELECT COUNT(*) AS c FROM books")
            books = cur.fetchone()["c"]
            cur.execute("SELECT COUNT(*) AS c FROM books WHERE status='Borrowed'")
            borrowed = cur.fetchone()["c"]
            cur.execute("SELECT COUNT(*) AS c FROM books WHERE status='Lost'")
            lost = cur.fetchone()["c"]
            
            # Calculate overdue based on transactions
            cur.execute("""
                SELECT COUNT(*) AS c
                FROM transactions t
                JOIN (
                    SELECT accession_number, MAX(date) AS maxd
                    FROM transactions
                    GROUP BY accession_number
                ) last ON last.accession_number = t.accession_number AND last.maxd = t.date
                WHERE t.action_type='borrow'
                  AND t.due_date < NOW()
                  AND t.returned_date IS NULL
            """)
            overdue = cur.fetchone()["c"]

        return jsonify(dict(students=students, books=books, borrowed=borrowed, lost=lost, overdue=overdue))
    finally:
        conn.close()

# ========================================================
# ROUTES: BOOKS MANAGEMENT
# ========================================================
@app.route('/books/delete/<accession_number>', methods=['POST'])
def books_delete(accession_number):
    if session.get('role') != 'admin': return "Unauthorized", 403
    
    conn = get_db_conn()
    try:
        with conn.cursor() as cur:
            cur.execute("DELETE FROM books WHERE accession_number=%s", (accession_number,))
            conn.commit()
        return redirect(url_for('books_list'))
    finally:
        conn.close()

@app.route('/books', methods=['GET'])

def books_list():
    if session.get('role') != 'admin': return redirect(url_for('login'))
    search = request.args.get('search', '').strip()
    conn = get_db_conn()
    try:
        with conn.cursor() as cur:
            base_query = "SELECT accession_number, title, author, publisher, call_number, `YEAR` as year, `STATUS` as status FROM books"
            if search:
                query = base_query + " WHERE accession_number LIKE %s OR title LIKE %s ORDER BY title"
                cur.execute(query, (f"%{search}%", f"%{search}%"))
            else:
                cur.execute(base_query + " ORDER BY title")
            books = cur.fetchall()
        return render_template('books.html', books=books, search=search)
    finally:
        conn.close()

@app.route('/books/add', methods=['POST'])
def books_add():
    if session.get('role') != 'admin': return "Unauthorized", 403
    f = request.form
    conn = get_db_conn()
    try:
        with conn.cursor() as cur:
            # 1. CHECK DUPLICATE ACCESSION NUMBER
            cur.execute("SELECT 1 FROM books WHERE accession_number=%s", (f.get('accession_number'),))
            if cur.fetchone():
                flash(f"Error: Accession Number '{f.get('accession_number')}' already exists!", "error")
                return redirect(url_for('books_list'))

            # 2. Insert if unique
            cur.execute("""
                INSERT INTO books (accession_number, title, author, publisher, year, call_number, status)
                VALUES (%s, %s, %s, %s, %s, %s, 'Available')
            """, (f.get('accession_number'), f.get('title'), f.get('author'), f.get('publisher'), f.get('year'), f.get('call_number')))
            conn.commit()
        flash("Book added successfully", "success")
        return redirect(url_for('books_list'))
    finally:
        conn.close()

@app.route('/books/import', methods=['POST'])
def books_import():
    if session.get('role') != 'admin': return "Unauthorized", 403
    if 'csv_file' not in request.files: return redirect(url_for('books_list'))
    file = request.files['csv_file']
    if file.filename == '': return redirect(url_for('books_list'))

    conn = get_db_conn()
    try:
        stream = io.StringIO(file.stream.read().decode("UTF8"), newline=None)
        csv_input = csv.DictReader(stream)
        if csv_input.fieldnames: csv_input.fieldnames = [name.strip() for name in csv_input.fieldnames]

        with conn.cursor() as cur:
            for row in csv_input:
                acc = row.get('Accession Number', '').strip()
                if not acc: continue
                
                cur.execute("SELECT 1 FROM books WHERE accession_number=%s", (acc,))
                if cur.fetchone(): continue

                cur.execute("""
                    INSERT INTO books (title, author, publisher, year, call_number, accession_number, status)
                    VALUES (%s, %s, %s, %s, %s, %s, 'Available')
                """, (row.get('Title', '').strip(), row.get('Author', '').strip(), row.get('Publisher', '').strip(), row.get('Year', '').strip(), row.get('Call Number', '').strip(), acc))
            conn.commit()
        flash("Successfully imported books.", "success")
    except Exception as e:
        flash(f"Error parsing CSV: {str(e)}", "error")
    finally:
        conn.close()
    return redirect(url_for('books_list'))

@app.route('/books/edit/<accession_number>', methods=['POST'])
def books_edit(accession_number):
    if session.get('role') != 'admin': return "Unauthorized", 403
    f = request.form
    conn = get_db_conn()
    try:
        with conn.cursor() as cur:
            cur.execute("""
                UPDATE books
                SET title=%s, author=%s, publisher=%s, year=%s, call_number=%s, status=%s
                WHERE accession_number=%s
            """, (f.get('title'), f.get('author'), f.get('publisher'), f.get('year'), f.get('call_number'), f.get('status'), accession_number))
            conn.commit()
        return redirect(url_for('books_list'))
    finally:
        conn.close()

@app.route('/api/books')
def api_books_json():
    """API for the Transaction Page Book Search"""
    limit = int(request.args.get('limit', 500))
    conn = get_db_conn()
    try:
        with conn.cursor() as cur:
            cur.execute("SELECT accession_number, title, author, publisher, YEAR as year, call_number, STATUS as status FROM books ORDER BY title LIMIT %s", (limit,))
            return jsonify({"rows": cur.fetchall()})
    finally:
        conn.close()

# ✅ OPTION 1: EXACT REPLACEMENT (Marks as Available, closes transaction)
@app.route('/books/resolve_lost/<accession_number>', methods=['POST'])
def books_resolve_lost(accession_number):
    if session.get('role') != 'admin': return "Unauthorized", 403
    conn = get_db_conn()
    try:
        with conn.cursor() as cur:
            cur.execute("SELECT title, status FROM books WHERE accession_number=%s", (accession_number,))
            book = cur.fetchone()
            if not book or book['status'] != 'Lost': 
                flash("Book not Lost.", "error")
                return redirect(url_for('books_list'))
            
            # Close original lost transaction
            cur.execute("UPDATE transactions SET returned_date=NOW() WHERE accession_number=%s AND returned_date IS NULL", (accession_number,))
            cur.execute("SELECT t.student_number, s.student_name, s.contact, t.tx_id FROM transactions t JOIN students s ON t.student_number=s.student_number WHERE t.accession_number=%s AND t.action_type='lost' ORDER BY t.date DESC LIMIT 1", (accession_number,))
            tx_info = cur.fetchone()
            
            # Make Available
            cur.execute("UPDATE books SET status='Available' WHERE accession_number=%s", (accession_number,))
            cur.execute("INSERT INTO transactions (tx_id, student_number, accession_number, action_type, date, returned_date, note, is_penalty_paid) VALUES (%s,%s,%s,'return',NOW(),NOW(),%s,1)",
                        (str(uuid.uuid4())[:12], (tx_info['student_number'] if tx_info else 'ADMIN'), accession_number, "Replacement Received (Resolved Lost Book)"))
            
            if tx_info: cur.execute("UPDATE lost_book_resolutions SET status='resolved' WHERE tx_id=%s", (tx_info['tx_id'],))
            conn.commit()
            
            if tx_info and tx_info['contact']:
                subject = "Lost Book Resolved"
                body = f"""
                    <div style="padding:20px; border:1px solid #10b981; border-radius:8px; font-family:sans-serif;">
                        <h2 style="color:#10b981;">Book Replacement Accepted</h2>
                        <p>Hi {tx_info['student_name']},</p>
                        <p>We have received the replacement for <b>{book['title']}</b> (Acc: {accession_number}) received. Record cleared.</p>
                    </div>
                """
                _send_email(tx_info['contact'], subject, body)
        flash("Book Resolved & Available", "success")
        return redirect(url_for('books_list'))
    finally: conn.close()

# ✅ OPTION 2: SIMILAR REPLACEMENT (DELETES OLD BOOK, CLOSES RECORD)
@app.route('/books/resolve_delete/<accession_number>', methods=['POST'])
def books_resolve_delete(accession_number):
    if session.get('role') != 'admin': return "Unauthorized", 403
    conn = get_db_conn()
    try:
        with conn.cursor() as cur:
            # 1. Get Book Info
            cur.execute("SELECT title, status FROM books WHERE accession_number=%s", (accession_number,))
            book = cur.fetchone()
            if not book or book['status'] != 'Lost':
                return jsonify({'success': False, 'message': 'Book not found or not lost.'})

            # 2. Close the Open "Lost" Transaction (So it leaves student dashboard)
            cur.execute("UPDATE transactions SET returned_date=NOW() WHERE accession_number=%s AND returned_date IS NULL", (accession_number,))

            # 3. Get Details for Logging
            cur.execute("SELECT t.student_number, s.student_name, s.contact, t.tx_id FROM transactions t JOIN students s ON t.student_number=s.student_number WHERE t.accession_number=%s AND t.action_type='lost' ORDER BY t.date DESC LIMIT 1", (accession_number,))
            tx_info = cur.fetchone()

            # 4. Log "Return" Transaction so history shows it was resolved
            # Note: We use the title in the note since the book row will be deleted
            note = f"Resolved (Book Deleted) - Original: {book['title']}"
            cur.execute("INSERT INTO transactions (tx_id, student_number, accession_number, action_type, date, returned_date, note, is_penalty_paid) VALUES (%s,%s,%s,'return',NOW(),NOW(),%s,1)",
                        (str(uuid.uuid4())[:12], tx_info['student_number'], accession_number, note))

            if tx_info: cur.execute("UPDATE lost_book_resolutions SET status='resolved' WHERE tx_id=%s", (tx_info['tx_id'],))

            # 5. DELETE THE BOOK
            cur.execute("SET FOREIGN_KEY_CHECKS=0")
            cur.execute("DELETE FROM books WHERE accession_number=%s", (accession_number,))
            cur.execute("SET FOREIGN_KEY_CHECKS=1")

            conn.commit()

            # 6. Email Student
            if tx_info and tx_info['contact']:
                body = f"""<p>Hi {tx_info['student_name']}, replacement for <b>{book['title']}</b> (Acc: {accession_number}) received. Record cleared.</p>"""
                _send_email(tx_info['contact'], "Lost Book Resolved", body)

        return jsonify({'success': True})
    except Exception as e:
        return jsonify({'success': False, 'message': str(e)})
    finally: conn.close()

# ========================================================
# ROUTES: STUDENTS MANAGEMENT
# ========================================================
@app.route('/students/delete/<student_number>', methods=['POST'])
def students_delete(student_number):
    if session.get('role') != 'admin': return "Unauthorized", 403
    
    conn = get_db_conn()
    try:
        with conn.cursor() as cur:
            cur.execute("DELETE FROM students WHERE student_number=%s", (student_number,))
            conn.commit()
        
        flash("Student and their history deleted successfully.", "success")
        return redirect(url_for('students_list'))
    finally:
        conn.close()

@app.route('/students', methods=['GET'])
def students_list():
    if session.get('role') != 'admin': return redirect(url_for('login'))
    search = request.args.get('search', '').strip()
    conn = get_db_conn()
    try:
        with conn.cursor() as cur:
            if search:
                cur.execute("SELECT * FROM students WHERE student_number LIKE %s ORDER BY student_name", (f"%{search}%",))
            else:
                cur.execute("SELECT * FROM students ORDER BY student_name")
            students = cur.fetchall()
        return render_template('student_add.html', students=students, search=search)
    finally:
        conn.close()

@app.route('/students/add', methods=['POST'])
def students_add():
    if session.get('role') != 'admin': return "Unauthorized", 403
    f = request.form
    
    if not re.match(r'^\d{2}-\d{4}$', f.get('student_number', '')):
        flash("Invalid Student format", "error")
        return redirect(url_for('students_list'))

    full_name = f.get('student_name', '').strip()
    first_name = full_name.split(' ')[0].lower() if full_name else 'student'
    stu_num = f.get('student_number', '')
    last_four = stu_num[-4:] if len(stu_num) >= 4 else stu_num
    generated_password = f"{first_name}{last_four}"

    conn = get_db_conn()
    try:
        with conn.cursor() as cur:
            cur.execute("SELECT 1 FROM students WHERE student_number=%s", (stu_num,))
            if cur.fetchone():
                flash("Student number already exists.", "error")
                return redirect(url_for('students_list'))

            cur.execute("""
                INSERT INTO students (student_number, student_name, course, department, contact, password)
                VALUES (%s, %s, %s, %s, %s, %s)
            """, (stu_num, full_name, f.get('course'), f.get('department'), f.get('contact'), generated_password))
            conn.commit()

            img = qrcode.make(stu_num)
            img.save(os.path.join(QR_FOLDER, f"{stu_num}.png"))

        email_addr = f.get('contact')
        if email_addr:
            _send_email(email_addr, "Welcome to Digital Access Management: Library", f"User ID: {stu_num}\nPassword: {generated_password}", f"User ID: {stu_num}, Password: {generated_password}")

        flash(f"Student added.", "success")
        return redirect(url_for('students_list'))
    finally:
        conn.close()

@app.route('/students/edit/<student_number>', methods=['POST'])
def edit_student(student_number):
    if session.get('role') != 'admin': return "Unauthorized", 403
    data = request.get_json()
    conn = get_db_conn()
    try:
        with conn.cursor() as cur:
            cur.execute("""
                UPDATE students SET student_name=%s, course=%s, department=%s, contact=%s
                WHERE student_number=%s
            """, (data.get('student_name'), data.get('course'), data.get('department'), data.get('contact'), student_number))
            conn.commit()
        return jsonify({'success': True})
    finally:
        conn.close()

@app.route('/student/dashboard')
@login_required  # <--- Requires ANY login (Admin or Student)
def student_dashboard():
    # 1. If Student: Force them to view ONLY their own data
    if session['role'] == 'student':
        target_id = session['student']['student_number']
    # 2. If Admin: They shouldn't use this route directly without an ID, 
    #    but if they do, redirect them to home or handle error
    elif session['role'] == 'admin':
        return redirect(url_for('index'))
    
    return render_template_student_logic(target_id)

# Rename your existing route to handle both cases cleanly:
@app.route('/students/details/<student_number>')
@login_required
def student_details(student_number):
    # SECURITY CHECK:
    # If logged in as Student, ensure they are only viewing THEIR OWN number.
    if session['role'] == 'student' and session['student']['student_number'] != student_number:
        return "Unauthorized Access", 403

    return render_template_student_logic(student_number)

# Helper function to reuse the logic (Paste the body of your old function here)
def render_template_student_logic(student_number):
    page = int(request.args.get('page', 1))
    per_page = 10
    offset = (page - 1) * per_page

    conn = get_db_conn()
    try:
        with conn.cursor() as cur:
            cur.execute("SELECT * FROM students WHERE student_number=%s", (student_number,))
            student = cur.fetchone()
            if not student: return "Student not found", 404

            cur.execute("SELECT COUNT(*) as total FROM transactions WHERE student_number=%s", (student_number,))
            total = cur.fetchone()['total']
            pages = max(1, math.ceil(total / per_page))

            cur.execute("""
                SELECT t.tx_id, t.accession_number, t.call_number, t.action_type, t.date, t.due_date, t.returned_date,
                       t.is_penalty_paid, t.note,
                       COALESCE(b.title, 'Unknown Book') as book_title
                FROM transactions t
                LEFT JOIN books b ON t.accession_number = b.accession_number
                WHERE t.student_number=%s
                ORDER BY t.date DESC
                LIMIT %s OFFSET %s
            """, (student_number, per_page, offset))
            transactions = cur.fetchall()

        # Decide which template to render based on role
        template = 'student_dashboard.html' if session.get('role') == 'student' else 'student_details.html'
        
        return render_template(template, student=student, transactions=transactions, page=page, pages=pages, total=total)
    finally:
        conn.close()

@app.route('/api/student/<student_number>')
def api_student(student_number):
    conn = get_db_conn()
    try:
        with conn.cursor() as cur:
            cur.execute("SELECT * FROM students WHERE student_number=%s", (student_number,))
            student = cur.fetchone()
            if not student: return jsonify({'error': 'Student not found'}), 404
            return jsonify(student)
    finally:
        conn.close()

# ========================================================
# ROUTES: TRANSACTIONS
# ========================================================

@app.route('/transaction')

def transaction_page():
    if session.get('role') != 'admin': return redirect(url_for('login'))
    return render_template('transaction.html')

@app.route('/transaction/create', methods=['POST'])
def transaction_create():
    if session.get('role') != 'admin': return "Unauthorized", 403
    data = request.get_json()
    
    s_num = data.get('student_number')
    acc_nums = data.get('accession_numbers') or [data.get('accession_number')]
    action = data.get('action_type')
    form_due_date = data.get('due_date')
    note = data.get('note')
    resolution_type = data.get('resolution_type')

    if not s_num or not acc_nums or not action:
        return jsonify({'error': 'Missing fields'}), 400

    conn = get_db_conn()
    processed_ids = []
    errors = []

    try:
        with conn.cursor() as cur:
            cur.execute("SELECT contact, student_name FROM students WHERE student_number=%s", (s_num,))
            stu = cur.fetchone()
            if not stu: return jsonify({'error': 'Student not found'}), 404

            for acc in acc_nums:
                cur.execute("SELECT status, call_number, title FROM books WHERE accession_number=%s", (acc,))
                book = cur.fetchone()
                
                if not book: 
                    errors.append(f"Book {acc} not found")
                    continue

                current_status = book['status']
                new_status = current_status
                final_due_date = None 
                paid_status = 0 

                if action == 'borrow':
                    if current_status != 'Available':
                        errors.append(f"'{book['title']}' is {current_status}")
                        continue
                    new_status = 'Borrowed'
                    final_due_date = form_due_date 
                
                elif action == 'return':
                    if current_status == 'Available':
                        errors.append(f"'{book['title']}' is already available")
                        continue
                    new_status = 'Available'
                    cur.execute("""
                        SELECT due_date, is_penalty_paid FROM transactions 
                        WHERE accession_number=%s AND action_type='borrow' AND returned_date IS NULL 
                        ORDER BY date DESC LIMIT 1
                    """, (acc,))
                    active = cur.fetchone()
                    if active: 
                        final_due_date = active['due_date']
                        paid_status = active['is_penalty_paid']

                elif action == 'lost':
                    new_status = 'Lost'
                    cur.execute("""
                        SELECT due_date, is_penalty_paid FROM transactions 
                        WHERE accession_number=%s AND action_type='borrow' AND returned_date IS NULL 
                        ORDER BY date DESC LIMIT 1
                    """, (acc,))
                    active = cur.fetchone()
                    if active: 
                        final_due_date = active['due_date']
                        paid_status = active['is_penalty_paid']

                tx_id = str(uuid.uuid4())[:12]
                cur.execute("""
                    INSERT INTO transactions 
                    (tx_id, student_number, accession_number, call_number, action_type, date, due_date, returned_date, note, is_penalty_paid)
                    VALUES (%s, %s, %s, %s, %s, NOW(), %s, %s, %s, %s)
                """, (tx_id, s_num, acc, book['call_number'], action, final_due_date, (None if action != 'return' else datetime.now()), note, paid_status))

                cur.execute("UPDATE books SET status=%s WHERE accession_number=%s", (new_status, acc))
                
                # Close borrow record if returning OR lost
                if action == 'return' or action == 'lost':
                    cur.execute("UPDATE transactions SET returned_date=NOW() WHERE accession_number=%s AND action_type='borrow' AND returned_date IS NULL", (acc,))
                
                if action == 'lost' and resolution_type:
                    cur.execute("""
                        INSERT INTO lost_book_resolutions (tx_id, student_number, accession_number, resolution_type)
                        VALUES (%s, %s, %s, %s)
                    """, (tx_id, s_num, acc, resolution_type))
                    
                    res_text = "Exact Replacement" if resolution_type == "same_book" else "Replacement with Similar Value"
                    
                    if stu['contact']:
                        subject = f"Report: Lost Book - {book['title']}"
                        body = f"""
                        <div style="padding:20px; border:1px solid #ef4444; border-radius:8px; font-family:sans-serif;">
                            <h2 style="color:#ef4444;">Lost Book Reported</h2>
                            <p>Hi {stu['student_name']},</p>
                            <p>You have reported the following book as lost:</p>
                            <p><b>Title:</b> {book['title']}<br>
                            <b>Accession Number:</b> {acc}</p>
                            <p><b>Agreed Resolution:</b> {res_text}</p>
                            <p>Please bring the replacement to the library to clear your record.</p>
                        </div>
                        """
                        _send_email(stu['contact'], subject, body)

                # Email Notifications for Borrow and Return
                if stu['contact']:
                    if action == 'borrow':
                        d_str = final_due_date
                        try: d_str = datetime.strptime(final_due_date, '%Y-%m-%dT%H:%M').strftime('%b %d, %Y %I:%M %p')
                        except: pass
                        
                        subj = f"Borrowed: {book['title']}"
                        body = f"""
                        <div style="padding:20px; border:1px solid #22c55e; border-radius:8px; font-family:sans-serif;">
                            <h2 style="color:#22c55e;">Successfully Borrowed</h2>
                            <p>Hi {stu['student_name']},</p>
                            <p>You have borrowed:</p>
                            <p><b>Title:</b> {book['title']}<br>
                            <b>Accession Number:</b> {acc}</p>
                            <p><b>Due Date:</b> {d_str}</p>
                            <p>Please return it on time to avoid penalties.</p>
                        </div>
                        """
                        _send_email(stu['contact'], subj, body)
                    
                    elif action == 'return':
                        subj = f"Returned: {book['title']}"
                        body = f"""
                        <div style="padding:20px; border:1px solid #3b82f6; border-radius:8px; font-family:sans-serif;">
                            <h2 style="color:#3b82f6;">Successfully Returned</h2>
                            <p>Hi {stu['student_name']},</p>
                            <p>You have successfully returned:</p>
                            <p><b>Title:</b> {book['title']}<br>
                            <b>Accession Number:</b> {acc}</p>
                            <p>Thank you!</p>
                        </div>
                        """
                        _send_email(stu['contact'], subj, body)

                processed_ids.append(tx_id)

            conn.commit()
            
            if not processed_ids and errors:
                return jsonify({'error': " | ".join(errors)}), 400
            
            return jsonify({'ok': True, 'tx_ids': processed_ids, 'errors': errors})

    except Exception as e:
        print(e)
        return jsonify({'error': str(e)}), 500
    finally:
        conn.close()

@app.route('/api/transactions')
def api_transactions():
    limit = int(request.args.get('limit', 200))
    s_num = request.args.get('student_number')
    conn = get_db_conn()
    try:
        with conn.cursor() as cur:
            base_query = """
                SELECT t.tx_id, t.student_number, s.student_name, 
                       COALESCE(b.title, t.accession_number) as book_title,
                       t.accession_number, t.call_number, t.action_type,
                       DATE_FORMAT(t.date, '%%Y-%%m-%%d %%H:%%i:%%s') as tx_date,
                       DATE_FORMAT(t.due_date, '%%Y-%%m-%%d %%H:%%i:%%s') as due_date,
                       DATE_FORMAT(t.returned_date, '%%Y-%%m-%%d %%H:%%i:%%s') as returned_date,
                       t.is_penalty_paid,
                       b.status as book_status,
                       t.note
                FROM transactions t
                LEFT JOIN books b ON b.accession_number = t.accession_number
                LEFT JOIN students s ON s.student_number = t.student_number
            """
            if s_num:
                cur.execute(base_query + " WHERE t.student_number=%s ORDER BY t.date DESC LIMIT %s", (s_num, limit))
            else:
                cur.execute(base_query + " ORDER BY t.date DESC LIMIT %s", (limit,))
            return jsonify({"rows": cur.fetchall()})
    finally:
        conn.close()

# ========================================================
# ROUTES: PAYMENTS & REPORTS
# ========================================================

@app.route('/payment')

def payment_page():
    if session.get('role') != 'admin': return redirect(url_for('login'))
    return render_template('payment.html')

@app.route('/api/pay', methods=['POST'])
def api_pay():
    if session.get('role') != 'admin': return "Unauthorized", 403
    data = request.get_json()
    student_number = data.get('student_number')
    amount = data.get('amount')
    
    if not student_number or not amount:
        return jsonify({'error': 'Missing data'}), 400

    conn = get_db_conn()
    try:
        with conn.cursor() as cur:
            cur.execute("""
                INSERT INTO payments (student_number, amount, payment_date)
                VALUES (%s, %s, NOW())
            """, (student_number, amount))
            
            cur.execute("""
                UPDATE transactions 
                SET is_penalty_paid = 1 
                WHERE student_number = %s AND is_penalty_paid = 0
            """, (student_number,))
            
            cur.execute("SELECT contact, student_name FROM students WHERE student_number=%s", (student_number,))
            stu = cur.fetchone()
            
            conn.commit()
            
            if stu and stu['contact']:
                subject = "Library Payment Receipt"
                html_body = f"""
                <div style="font-family: sans-serif; padding: 20px; border: 1px solid #ddd;">
                    <h2 style="color: #22c55e;">Payment Received</h2>
                    <p>Hi {stu['student_name']},</p>
                    <p>We have received a payment of <b>₱{amount}</b> for your library penalties.</p>
                    <p>Your account is now cleared.</p>
                    <p>Date: {datetime.now().strftime('%Y-%m-%d %H:%M')}</p>
                </div>
                """
                _send_email(stu['contact'], subject, html_body, f"Payment of {amount} received.")

            return jsonify({'success': True})
    except Exception as e:
        print(e)
        return jsonify({'error': str(e)}), 500
    finally:
        conn.close()

@app.route('/api/payments_history')
def api_payments_history():
    if session.get('role') != 'admin': return "Unauthorized", 403
    conn = get_db_conn()
    try:
        with conn.cursor() as cur:
            cur.execute("""
                SELECT p.payment_id, 
                       p.student_number, 
                       s.student_name, 
                       p.amount, 
                       p.payment_date
                FROM payments p
                LEFT JOIN students s ON p.student_number = s.student_number
                ORDER BY p.payment_date DESC
            """)
            rows = cur.fetchall()
            
            final_data = []
            for r in rows:
                raw_date = r.get('payment_date')
                date_str = "-"
                if raw_date:
                    if hasattr(raw_date, 'strftime'):
                        date_str = raw_date.strftime('%Y-%m-%d %H:%M:%S')
                    else:
                        date_str = str(raw_date)

                final_data.append({
                    'payment_id': r['payment_id'],
                    'student_number': r['student_number'],
                    'student_name': r['student_name'],
                    'amount': r['amount'],
                    'date': date_str
                })

            return jsonify({'data': final_data})
    finally:
        conn.close()

@app.route('/reports/transactions')

def reports_transactions():
    if session.get('role') != 'admin': return redirect(url_for('login'))
    conn = get_db_conn()
    try:
        with conn.cursor() as cur:
            cur.execute("""
                SELECT t.tx_id, t.student_number, b.title as book_title, 
                       t.action_type, t.date, 
                       lbr.resolution_type, lbr.status as resolution_status,
                       t.due_date
                FROM lost_book_resolutions lbr
                JOIN transactions t ON lbr.tx_id = t.tx_id
                LEFT JOIN books b ON t.accession_number = b.accession_number
                ORDER BY t.date DESC
            """)
            return render_template('report.html', rows=cur.fetchall())
    finally:
        conn.close()

@app.route('/scan')
def scan_page():
    return render_template('scan.html')

@app.route('/static/qrcodes/<filename>')
def serve_qr(filename):
    return send_from_directory(QR_FOLDER, filename)

@app.route('/api/book-status/<accession_number>')
def api_book_status(accession_number):
    conn = get_db_conn()
    try:
        with conn.cursor() as cur:
            # We select the LATEST transaction (ORDER BY date DESC)
            # This ensures we find the student even if the book is Lost, Returned, or Deleted.
            cur.execute("""
                SELECT s.student_name, s.student_number, s.contact, 
                       DATE_FORMAT(t.date, '%%b %%d, %%Y %%h:%%i %%p') as tx_date, 
                       DATE_FORMAT(t.due_date, '%%b %%d, %%Y %%h:%%i %%p') as due_date
                FROM transactions t
                JOIN students s ON t.student_number = s.student_number
                WHERE t.accession_number = %s
                ORDER BY t.date DESC
                LIMIT 1
            """, (accession_number,))
            
            row = cur.fetchone()
            if row:
                return jsonify(row)
            else:
                return jsonify({'error': 'No history found'}), 404
    finally:
        conn.close()


if __name__ == '__main__':
    try:
        test_conn = get_db_conn()
        print("✅ Database connection successful")
        test_conn.close()
    except Exception as e:
        print(f"❌ Database connection failed: {e}")

    app.run(debug=True, host='0.0.0.0', port=5000)