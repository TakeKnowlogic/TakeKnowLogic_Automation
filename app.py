import os
from flask import Flask, render_template, request, redirect
import mysql.connector
import smtplib
from email.mime.text import MIMEText
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Flask app
app = Flask(__name__)
app.secret_key = os.environ.get("SECRET_KEY", "takeknowlogic-secret-key")

# Database configuration from environment variables
DB_CONFIG = {
    "host": os.environ.get("DB_HOST"),
    "user": os.environ.get("DB_USER"),
    "password": os.environ.get("DB_PASSWORD"),
    "database": os.environ.get("DB_NAME")
}

# Gmail credentials from environment variables
GMAIL_USER = os.environ.get("GMAIL_USER")
GMAIL_PASS = os.environ.get("GMAIL_PASS")


# ================= EMAIL FUNCTIONS =================
def send_admin_email(name, email, phone, message):
    """Send an email to admin when a new contact form is submitted."""
    try:
        msg = MIMEText(f"""
New Contact Enquiry

Name: {name}
Email: {email}
Phone: {phone}

Message:
{message}
""")
        msg["Subject"] = "New Enquiry | TakeKnowLogic"
        msg["From"] = GMAIL_USER
        msg["To"] = GMAIL_USER

        server = smtplib.SMTP("smtp.gmail.com", 587)
        server.starttls()
        server.login(GMAIL_USER, GMAIL_PASS)
        server.send_message(msg)
        server.quit()
    except Exception as e:
        print("ERROR sending admin email:", e)


def send_auto_reply(name, to_email):
    """Send an automatic reply to the user."""
    try:
        msg = MIMEText(f"""
Dear {name},

Thank you for contacting TakeKnowLogic Automation.
We will contact you shortly.

Regards,
TakeKnowLogic Automation
""")
        msg["Subject"] = "Enquiry Received"
        msg["From"] = GMAIL_USER
        msg["To"] = to_email

        server = smtplib.SMTP("smtp.gmail.com", 587)
        server.starttls()
        server.login(GMAIL_USER, GMAIL_PASS)
        server.send_message(msg)
        server.quit()
    except Exception as e:
        print("ERROR sending auto-reply:", e)


# ================= ROUTES =================

# ROOT ROUTE
@app.route("/")
def root():
    return redirect("/contact")


@app.route("/services")
def services():
    return render_template("services.html")


@app.route("/solutions")
def solutions():
    return render_template("solutions.html")


@app.route("/technologies")
def technologies():
    return render_template("technologies.html")


@app.route("/contact", methods=["GET", "POST"])
def contact():
    if request.method == "POST":
        name = request.form.get("name")
        email = request.form.get("email")
        phone = request.form.get("phone")
        message = request.form.get("message")

        try:
            # Save inquiry to database
            conn = mysql.connector.connect(**DB_CONFIG)
            cursor = conn.cursor()
            cursor.execute(
                "INSERT INTO contact_inquiries (name,email,phone,message) VALUES (%s,%s,%s,%s)",
                (name, email, phone, message)
            )
            conn.commit()
            cursor.close()
            conn.close()

            # Send emails
            send_admin_email(name, email, phone, message)
            send_auto_reply(name, email)

            return render_template("contact.html", success=True)

        except Exception as e:
            print("ERROR:", e)
            return render_template("contact.html", error=True)

    return render_template("contact.html")


# ================= RUN APP =================
if __name__ == "__main__":
    port = int(os.environ.get("PORT", 10000))
    app.run(host="0.0.0.0", port=port, debug=True)
