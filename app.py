import os
from flask import Flask, render_template, request, redirect
import mysql.connector
from db_config import DB_CONFIG
import smtplib
from email.mime.text import MIMEText

app = Flask(__name__)
app.secret_key = "takeknowlogic-secret-key"

# ================= EMAIL FUNCTIONS =================
# (Keep them, but we will call them safely)

def send_admin_email(name, email, phone, message):
    sender = "tkla3006@gmail.com"
    password = "jtxahtythdyprdkg"  # later move to ENV variable

    msg = MIMEText(f"""
New Contact Enquiry

Name: {name}
Email: {email}
Phone: {phone}

Message:
{message}
""")

    msg["Subject"] = "New Enquiry | TakeKnowLogic"
    msg["From"] = sender
    msg["To"] = sender

    server = smtplib.SMTP("smtp.gmail.com", 587)
    server.starttls()
    server.login(sender, password)
    server.send_message(msg)
    server.quit()


def send_auto_reply(name, to_email):
    sender = "tkla3006@gmail.com"
    password = "jtxahtythdyprdkg"

    msg = MIMEText(f"""
Dear {name},

Thank you for contacting TakeKnowLogic Automation.
We will contact you shortly.

Regards,
TakeKnowLogic Automation
""")

    msg["Subject"] = "Enquiry Received"
    msg["From"] = sender
    msg["To"] = to_email

    server = smtplib.SMTP("smtp.gmail.com", 587)
    server.starttls()
    server.login(sender, password)
    server.send_message(msg)
    server.quit()


# ================= ROUTES =================

# ROOT ROUTE (VERY IMPORTANT FOR RENDER)
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


# ================= RUN APP (RENDER SAFE) =================
if __name__ == "__main__":
    port = int(os.environ.get("PORT", 10000))
    app.run(host="0.0.0.0", port=port)
