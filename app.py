import os
from flask import Flask, render_template, request
import mysql.connector
import smtplib
from email.mime.text import MIMEText
from dotenv import load_dotenv

# ================= LOAD ENV =================
load_dotenv()

# ================= FLASK APP =================
app = Flask(__name__)
app.secret_key = os.environ.get("SECRET_KEY", "takeknowlogic-secret-key")

# ================= DATABASE CONFIG =================
DB_CONFIG = {
    "host": "localhost",
    "user": "root",
    "password": "Tkla@123",  # change if needed
    "database": "takeknowlogic_db",
}
# ================= EMAIL CONFIG =================
GMAIL_USER = "tkla3006@gmail.com"
GMAIL_PASS = "jtxahtythdyprdkg"

# ================= EMAIL FUNCTIONS =================
def send_admin_email(name, email, phone, message):
    try:
        msg = MIMEText(f"""
New Contact Enquiry

Name   : {name}
Email  : {email}
Phone  : {phone}

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
    try:
        msg = MIMEText(f"""
Dear {name},

Thank you for contacting TakeKnowLogic Automation.
Our team will get back to you shortly.

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

@app.route("/")
def home():
    return render_template("index.html")


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
            conn = mysql.connector.connect(**DB_CONFIG)
            cursor = conn.cursor()

            cursor.execute(
                """
                INSERT INTO contact_inquiries (name, email, phone, message)
                VALUES (%s, %s, %s, %s)
                """,
                (name, email, phone, message),
            )

            conn.commit()
            cursor.close()
            conn.close()

            send_admin_email(name, email, phone, message)
            send_auto_reply(name, email)

            return render_template("contact.html", success=True)

        except Exception as e:
            print("ERROR:", e)
            return render_template("contact.html", error=True)

    return render_template("contact.html")
@app.route("/technology/<name>")
def technology_detail(name):

    tech_data = {
        "plc": {
            "title": "Programmable Logic Controller (PLC)",
            "description": "PLC is an industrial digital computer used for automation of machinery and production systems.",
            "points": [
                "Siemens PLC Programming",
                "Allen Bradley PLC",
                "Delta PLC",
                "Modbus Communication",
                "Industrial Automation Solutions"
            ]
        },
        "hmi": {
            "title": "Human Machine Interface (HMI)",
            "description": "HMI provides a graphical interface for operators to monitor and control industrial processes.",
            "points": [
                "Siemens HMI",
                "Weintek HMI",
                "SCADA Integration",
                "Real-Time Monitoring"
            ]
        },
        "energy": {
            "title": "Energy Meter Technologies",
            "description": "Advanced energy meters used for monitoring voltage, current, power, and consumption.",
            "points": [
                "3-Phase Energy Monitoring",
                "Power Factor Analysis",
                "Modbus Energy Meters",
                "Data Logging Systems"
            ]
        },
        "iot": {
            "title": "IoT & Cloud Technologies",
            "description": "Industrial IoT systems for remote monitoring and cloud-based analytics.",
            "points": [
                "MQTT Communication",
                "Cloud Dashboards",
                "Remote Monitoring",
                "Data Analytics"
            ]
        },
        "predictive": {
            "title": "Predictive Maintenance",
            "description": "AI-based monitoring to predict machine failures before breakdown.",
            "points": [
                "Vibration Monitoring",
                "Temperature Analysis",
                "Fault Detection",
                "Condition Monitoring"
            ]
        },
        "dashboard": {
            "title": "Dashboard & Reporting",
            "description": "Custom dashboards for industrial data visualization and reporting.",
            "points": [
                "Real-Time Charts",
                "PDF Reports",
                "Historical Data",
                "KPI Monitoring"
            ]
        },
        "server": {
            "title": "Server & Deployment",
            "description": "Deployment of industrial applications on secure servers.",
            "points": [
                "Flask Deployment",
                "Gunicorn",
                "Linux Server Setup",
                "Database Integration"
            ]
        },
        "security": {
            "title": "Security Systems",
            "description": "Industrial cybersecurity and access control systems.",
            "points": [
                "User Authentication",
                "Role-Based Access",
                "Secure Communication",
                "Data Encryption"
            ]
        }
    }

    tech = tech_data.get(name)

    if not tech:
        return "Technology not found", 404

    return render_template("technology_detail.html", tech=tech)

@app.route("/solution/<name>")
def solution_detail(name):

    solution_data = {

        "energy": {
            "title": "Energy Monitoring System",
            "description": "Complete industrial energy monitoring solution for real-time power tracking.",
            "points": [
                "Real-time Energy Monitoring",
                "Power Quality Analysis",
                "Historical Reports",
                "Load Analysis & Optimization"
            ]
        },

        "repairing": {
            "title": "Repairing Solutions",
            "description": "Professional repair and maintenance services for industrial automation systems.",
            "points": [
                "PLC Repair",
                "HMI Troubleshooting",
                "Panel Maintenance",
                "On-site Support"
            ]
        },

        "predictive": {
            "title": "Predictive Maintenance",
            "description": "Advanced monitoring to detect issues before machine breakdown.",
            "points": [
                "Vibration Monitoring",
                "Temperature Tracking",
                "Fault Detection",
                "Downtime Reduction"
            ]
        },

        "iot": {
            "title": "IoT Solutions",
            "description": "Industrial IoT solutions for smart monitoring and cloud integration.",
            "points": [
                "Remote Monitoring",
                "Cloud Dashboard",
                "Real-Time Alerts",
                "Data Analytics"
            ]
        },

        "machine": {
            "title": "Machine Automation",
            "description": "Automation of industrial machines for improved efficiency and productivity.",
            "points": [
                "PLC Programming",
                "Sensor Integration",
                "Motor Control",
                "Production Optimization"
            ]
        },

        "commissioning": {
            "title": "Quick Commissioning",
            "description": "Fast and reliable commissioning of industrial automation systems.",
            "points": [
                "System Testing",
                "On-site Configuration",
                "Performance Validation",
                "Operational Training"
            ]
        },

        "automation": {
            "title": "Automation Solutions",
            "description": "Complete end-to-end automation solutions for industries.",
            "points": [
                "Control Panel Design",
                "SCADA Systems",
                "Industrial Networking",
                "Customized Automation"
            ]
        }

    }

    solution = solution_data.get(name)

    if not solution:
        return "Solution not found", 404

    return render_template("solution_detail.html", solution=solution)
# ================= SERVICES ROUTE (FINAL WORKING VERSION) =================
@app.route("/services/<path:slug>")
def service_router(slug):

    services_data = {

        # ================= INDUSTRIAL AUTOMATION =================
        "industrial-automation": {
            "title": "Industrial Automation",
            "description": "Complete industrial automation solutions including PLC, HMI and control systems.",
            "sub_services": {
                "plc-programming": {
                    "title": "PLC Programming",
                    "description": "Professional PLC programming for industrial automation.",
                    "points": [
                        "Siemens PLC",
                        "Allen Bradley PLC",
                        "Delta PLC",
                        "Modbus Communication",
                        "Machine Logic Development"
                    ]
                },
                "hmi-development": {
                    "title": "HMI Development",
                    "description": "Advanced HMI and SCADA development.",
                    "points": [
                        "Siemens HMI",
                        "Weintek HMI",
                        "SCADA Integration",
                        "Real-Time Monitoring"
                    ]
                },
                "control-panel-design": {
                    "title": "Control Panel Design",
                    "description": "Industrial control panel design & engineering.",
                    "points": [
                        "Electrical Drawing",
                        "Panel Fabrication",
                        "Component Selection",
                        "Testing & Validation"
                    ]
                },
                "system-integration": {
                    "title": "System Integration",
                    "description": "Complete automation system integration.",
                    "points": [
                        "PLC-HMI Integration",
                        "Network Configuration",
                        "Field Device Integration"
                    ]
                }
            }
        },

        # ================= ROBOTICS =================
        "robotics": {
            "title": "Robotics",
            "description": "Industrial robotics integration solutions.",
            "sub_services": {
                "robot-programming": {
                    "title": "Robot Programming",
                    "description": "Industrial robot programming.",
                    "points": [
                        "Pick & Place Robots",
                        "Welding Robots",
                        "Material Handling"
                    ]
                },
                "robot-integration": {
                    "title": "Robot Integration",
                    "description": "Robot system integration services.",
                    "points": [
                        "PLC Integration",
                        "Vision System",
                        "Safety Configuration"
                    ]
                },
                "robot-commissioning": {
                    "title": "Robot Commissioning",
                    "description": "On-site robot commissioning.",
                    "points": [
                        "System Testing",
                        "Calibration",
                        "Performance Validation"
                    ]
                }
            }
        },

        # ================= IOT =================
        "iot-data-analytics": {
            "title": "IoT & Data Analytics",
            "description": "Industrial IoT and smart monitoring systems.",
            "sub_services": {
                "iot-solutions": {
                    "title": "Industrial IoT Solutions",
                    "description": "Smart IoT integration solutions.",
                    "points": [
                        "Remote Monitoring",
                        "Cloud Connectivity",
                        "Real-Time Alerts"
                    ]
                },
                "cloud-dashboards": {
                    "title": "Cloud Dashboards",
                    "description": "Real-time monitoring dashboards.",
                    "points": [
                        "Data Visualization",
                        "KPI Monitoring",
                        "Custom Reports"
                    ]
                },
                "data-analytics": {
                    "title": "Data Analytics & Reporting",
                    "description": "Industrial data analytics solutions.",
                    "points": [
                        "Historical Reports",
                        "Trend Analysis",
                        "Performance Optimization"
                    ]
                },
                "predictive-maintenance": {
                    "title": "Predictive Maintenance",
                    "description": "Machine health monitoring solutions.",
                    "points": [
                        "Vibration Monitoring",
                        "Temperature Tracking",
                        "Failure Prediction"
                    ]
                }
            }
        },

        # ================= INSTALLATION & COMMISSIONING =================
        "installation-commissioning": {
            "title": "Installation & Commissioning",
            "description": "Complete installation and commissioning services.",
            "sub_services": {
                "supply-automation-hardware": {
                    "title": "Supply of Automation Hardware",
                    "description": "Supply of PLC, HMI and automation components.",
                    "points": [
                        "PLC & HMI Supply",
                        "Sensors & Drives",
                        "Industrial Components"
                    ]
                },
                "electrical-installation": {
                    "title": "Electrical Installation",
                    "description": "Professional electrical installation.",
                    "points": [
                        "Panel Installation",
                        "Cable Laying",
                        "Power Distribution"
                    ]
                },
                "testing-commissioning": {
                    "title": "Testing & Commissioning",
                    "description": "System testing and validation.",
                    "points": [
                        "Load Testing",
                        "Performance Validation",
                        "Safety Checks"
                    ]
                }
            }
        },

        # ================= MAINTENANCE & REPAIR =================
        "maintenance-repair": {
            "title": "Maintenance & Repair",
            "description": "Reliable maintenance and repair services.",
            "sub_services": {
                "equipment-repair": {
                    "title": "Industrial Equipment Repair",
                    "description": "Repair services for automation equipment.",
                    "points": [
                        "PLC Repair",
                        "HMI Troubleshooting",
                        "Drive Repair"
                    ]
                },
                "amc-services": {
                    "title": "AMC Services",
                    "description": "Annual maintenance contracts.",
                    "points": [
                        "Preventive Maintenance",
                        "Scheduled Inspection"
                    ]
                },
                "troubleshooting-support": {
                    "title": "Troubleshooting & Support",
                    "description": "Quick breakdown support.",
                    "points": [
                        "Remote Support",
                        "On-site Diagnosis"
                    ]
                }
            }
        },

        # ================= TRAINING =================
        "training": {
            "title": "Training Programs",
            "description": "Professional automation training.",
            "sub_services": {
                "plc-training": {
                    "title": "PLC Training",
                    "description": "Hands-on PLC training program.",
                    "points": [
                        "Basic to Advanced PLC",
                        "Practical Sessions",
                        "Live Projects"
                    ]
                },
                "hmi-training": {
                    "title": "HMI Training",
                    "description": "Professional HMI training.",
                    "points": [
                        "Screen Design",
                        "Alarm Setup",
                        "Communication Setup"
                    ]
                }
            }
        }

    }

    parts = slug.strip("/").split("/")

    # MAIN SERVICE
    if len(parts) == 1:
        service = services_data.get(parts[0])
        if not service:
            return "Service not found", 404
        return render_template("service_detail.html", service=service)

    # SUB SERVICE
    if len(parts) == 2:
        service = services_data.get(parts[0])
        if not service:
            return "Service not found", 404

        sub_service = service.get("sub_services", {}).get(parts[1])
        if not sub_service:
            return "Sub Service not found", 404

        return render_template("service_detail.html", service=sub_service)

    return "Invalid URL", 404
# ================= RUN APP =================
if __name__ == "__main__":
    port = int(os.environ.get("PORT", 10000))
    app.run(host="0.0.0.0", port=port, debug=False)
