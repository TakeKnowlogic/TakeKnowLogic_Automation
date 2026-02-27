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
GMAIL_USER = "info.tkla@gmail.com"
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
    "title": "Programmable Logic Controllers (PLC)",
    "description": "Programmable Logic Controllers (PLCs) are industrial-grade control systems used for reliable automation of machinery, process plants, and manufacturing systems.",
    "points": [
        "Siemens PLC (TIA Portal & Step 7)",
        "Allen-Bradley PLC (Studio 5000 / RSLogix)",
        "Delta & Mitsubishi PLC Platforms",
        "Ladder Logic & Structured Text Programming",
        "Modbus, Profinet & Ethernet/IP Communication",
        "Process & Machine Control Automation"
    ]
},
       "hmi": {
    "title": "Human Machine Interface (HMI)",
    "description": "HMI system provide real-time visualization, control, and monitoring of industrial processes through intuitive graphical interfaces.",
    "points": [
        "Siemens HMI Configuration",
        "Weintek HMI Development",
        "Alarm & Event Management",
        "Real-Time Process Visualization",
        "Remote Monitoring Capability"
    ]
},
        "energy": {
    "title": "Energy Metering & Power Monitoring Technologies",
    "description": "Advanced energy metering technologies for monitoring electrical parameters, analyzing power quality, and optimizing industrial energy consumption.",
    "points": [
        "3-Phase Energy Monitoring Systems",
        "Voltage, Current & Power Factor Analysis",
        "Modbus & TCP/IP Energy Meters",
        "Power Quality & Harmonics Monitoring",
        "Energy Data Logging & Reporting",
        "Demand & Load Analysis"
    ]
},
"iot": {
    "title": "Industrial IoT & Cloud Integration",
    "description": "Industrial IoT technologies enabling secure data acquisition, cloud connectivity, and intelligent analytics for smart factory environments.",
    "points": [
        "MQTT & Industrial Communication Protocols",
        "Cloud-Based Dashboards",
        "Remote Equipment Monitoring",
        "Edge Gateway Integration",
        "Real-Time Alerts & Notifications",
        "Industrial Data Analytics"
    ]
},
        "predictive": {
    "title": "Predictive Maintenance Technologies",
    "description": "Condition-based monitoring technologies designed to predict potential machine failures and improve equipment reliability.",
    "points": [
        "Vibration Monitoring Systems",
        "Temperature & Current Analysis",
        "Machine Health Diagnostics",
        "Condition Monitoring Sensors",
        "Early Fault Detection Algorithms",
        "Downtime Prevention Strategies"
    ]
},
"dashboard": {
    "title": "Industrial Dashboards & Reporting Systems",
    "description": "Custom-built industrial dashboards and reporting platforms for real-time performance monitoring and data-driven decision-making.",
    "points": [
        "Real-Time Data Visualization",
        "KPI & OEE Monitoring",
        "Automated PDF & Excel Reports",
        "Historical Data Trend Analysis",
        "Energy & Production Analytics",
        "Customizable User Interface"
    ]
},
       "server": {
    "title": "Industrial Server & Application Deployment",
    "description": "Secure deployment of industrial monitoring and automation applications on robust server infrastructures.",
    "points": [
        "Industrial Application Hosting",
        "Linux-Based Server Configuration",
        "Secure Database Integration",
        "Cloud & On-Premise Deployment",
        "System Backup & Recovery Planning",
        "High Availability Architecture"
    ]
},
        "security": {
    "title": "Industrial Cybersecurity & System Protection",
    "description": "Comprehensive cybersecurity solutions designed to protect industrial automation systems and critical infrastructure.",
    "points": [
        "Role-Based Access Control (RBAC)",
        "Secure Communication Protocols",
        "Data Encryption & Protection",
        "User Authentication Systems",
        "Network Security Configuration",
        "Industrial Firewall Integration"
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
    "title": "Energy Monitoring & Management System",
    "description": "Advanced industrial energy monitoring solution designed to track, analyze, and optimize power consumption across facilities for improved efficiency and cost reduction.",
    "points": [
        "Real-Time Voltage, Current & Power Monitoring",
        "Power Quality & Harmonics Analysis",
        "Energy Consumption Trend Reports",
        "Maximum Demand Monitoring",
        "Load Analysis & Optimization",
        "Automated Energy Performance Reports"
    ]
},

        "repairing": {
    "title": "Industrial Automation Repair & Refurbishment",
    "description": "Comprehensive repair and refurbishment solutions for industrial automation systems to restore performance and minimize downtime.",
    "points": [
        "PLC Diagnostics & Repair",
        "HMI Troubleshooting",
        "Drive & VFD Repair",
        "Control Panel Fault Rectification",
        "Component Replacement & Testing",
        "On-Site & Remote Technical Support"
    ]
},

        "predictive": {
    "title": "Predictive Maintenance Solution",
    "description": "Data-driven predictive maintenance system utilizing condition monitoring and analytics to detect potential equipment failures before breakdown occurs.",
    "points": [
        "Vibration & Condition Monitoring",
        "Temperature & Current Analysis",
        "Machine Health Diagnostics",
        "Early Fault Detection Alerts",
        "Downtime Reduction Strategies",
        "Maintenance Planning Optimization"
    ]
},

        "iot": {
    "title": "Industrial IoT & Smart Monitoring Solutions",
    "description": "Integrated Industrial IoT solutions enabling remote monitoring, cloud connectivity, and intelligent data-driven decision-making.",
    "points": [
        "Remote Equipment Monitoring",
        "Cloud-Based Data Logging",
        "Real-Time Alerts & Notifications",
        "Custom KPI Dashboards",
        "Edge Device & Gateway Integration",
        "Secure Industrial Communication"
    ]
},

        "machine": {
    "title": "Machine Automation Solutions",
    "description": "Comprehensive automation of industrial machines to improve productivity, efficiency, and operational reliability.",
    "points": [
        "Custom PLC Programming",
        "Sensor & Actuator Integration",
        "Motor & Drive Control Systems",
        "Production Line Automation",
        "Cycle Time Optimization",
        "Machine Performance Monitoring"
    ]
},
"commissioning": {
    "title": "System Commissioning & Validation",
    "description": "Professional commissioning services ensuring reliable startup, validation, and performance optimization of industrial automation systems.",
    "points": [
        "System Functional Testing",
        "On-Site Configuration & Setup",
        "Performance Validation & Tuning",
        "Safety & Compliance Verification",
        "Documentation & Handover Support",
        "Operator Training & Guidance"
    ]
},
"automation": {
    "title": "End-to-End Industrial Automation Solutions",
    "description": "Complete automation solutions covering design, engineering, integration, and lifecycle support for industrial facilities.",
    "points": [
        "Control Panel Engineering & Design",
        "PLC, HMI & SCADA Systems",
        "Industrial Networking & Communication",
        "Process Automation Solutions",
        "Customized System Integration",
        "Industry 4.0 Ready Architecture"
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
                    "description": "Professional PLC programming services for machine automation, process control, and industrial systems using industry-standard platforms.",
                    "points": [
                        "Siemens PLC (TIA Portal)",
                        "Allen-Bradley PLC (Studio 5000)",
                        "Delta & Mitsubishi PLC",
                        "Ladder Logic & Structured Text Programming",
                        "Modbus / Ethernet Communication Integration",
                        "Machine Logic Development & Optimization"
                    ]
                },
                "hmi-development": {
                    "title": "HMI Development",
                    "description": "Advanced HMI interface development for real-time monitoring, control, and visualization of industrial processes.",
                    "points": [
                        "Siemens HMI Configuration",
                        "Weintek HMI Development",
                        "Alarm & Event Management",
                        "Real-Time Data Visualization",
                        "Remote Monitoring Setup"
                    ]
                },
                "control-panel-design": {
                    "title": "Control Panel Design",
                    "description": "Industrial control panel design, engineering, and documentation compliant with safety and industry standards.",
                    "points": [
                       "Electrical Schematic Design",
                       "Panel Layout & GA Drawings",
                       "Component Selection & Sizing",
                       "PLC & Drive Panel Design",
                       "Testing & Factory Acceptance Test (FAT)"
                    ]
                },
                "system-integration": {
                    "title": "System Integration",
                    "description": "Complete automation system integration ensuring seamless communication between PLC, HMI, drives, and field instruments.",
                    "points": [
                        "PLC-HMI Integration",
                        "Industrial Network Configuration",
                        "Field Instrument Integration",
                        "VFD & Servo Drive Integration",
                        "System Testing & Validation"
                    ]
                }
            }
        },

        # ================= ROBOTICS =================
        "robotics": {
            "title": "Robotics",
            "description": "Industrial robotics automation solutions including robot programming, integration, and commissioning for manufacturing and material handling applications.",
            "sub_services": {
                "robot-programming": {
                    "title": "Robot Programming",
                    "description": "Industrial robot programming.",
                    "points": [
                       "Pick & Place Automation",
                       "Welding & Assembly Applications",
                       "Material Handling Systems",
                       "Robot Path Optimization",
                       "Cycle Time Improvement"
                    ]
                },
                "robot-integration": {
                    "title": "Robot Integration",
                    "description": "Integration of robotic systems with PLC-controlled automation lines and safety systems.",
                    "points": [
                        "PLC & Robot Communication Setup",
                        "Vision System Integration",
                        "Safety Interlocking Configuration",
                        "Conveyor Synchronization"
                    ]
                },
                "robot-commissioning": {
                    "title": "Robot Commissioning",
                    "description": "On-site robot commissioning.",
                    "points": [
                        "System Testing",
                        "Calibration",
                        "Performance Validation",
                        "Operator Training Support"
                    ]
                }
            }
        },

        # ================= IOT =================
        "iot-data-analytics": {
            "title": "IoT & Data Analytics",
            "description": "Industrial IoT solutions enabling real-time monitoring, cloud connectivity, and data-driven decision-making for smart factories.",
            "sub_services": {
                "iot-solutions": {
                    "title": "Industrial IoT Solutions",
                    "description": "Smart industrial IoT integration for remote monitoring and digital transformation.",
                    "points": [
                       "Remote Equipment Monitoring",
                       "Cloud-Based Data Logging",
                       "Real-Time Alerts & Notifications",
                       "Industrial Gateway Integration",
                       "Edge Device Configuration"
                    ]
                },
                "cloud-dashboards": {
                    "title": "Cloud Dashboards",
                    "description": "Custom cloud dashboards for KPI monitoring and performance tracking.",
                    "points": [
                        "Live Data Visualization",
                        "KPI & OEE Monitoring",
                        "Custom Industrial Reports",
                        "Energy Consumption Dashboards"
                    ]
                },
                "data-analytics": {
                    "title": "Data Analytics & Reporting",
                    "description": "Advanced industrial data analytics for performance improvement and operational insights.",
                    "points": [
                         "Historical Trend Analysis",
                         "Downtime Analysis",
                         "Production Efficiency Reports",
                         "Energy Performance Analysis"
                    ]
                },
                "predictive-maintenance": {
                    "title": "Predictive Maintenance",
                    "description": "Condition-based monitoring and predictive maintenance solutions to reduce unexpected breakdowns.",
                    "points": [
                        "Vibration Monitoring",
                        "Temperature & Current Analysis",
                        "Machine Health Diagnostics",
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
                    "description": "Supply of industrial-grade automation hardware and electrical components.",
                    "points": [
                        "PLC & HMI Supply",
                        "Sensors & Drives",
                        "Industrial Components"
                    ]
                },
                "electrical-installation": {
                    "title": "Electrical Installation",
                    "description": "Professional electrical installation services for industrial automation systems.",
                    "points": [
                      "Panel Installation & Wiring",
                      "Cable Laying & Termination",
                      "Power Distribution Setup",
                      "Earthing & Safety Compliance"
                    ]
                },
                "testing-commissioning": {
                    "title": "Testing & Commissioning",
                    "description": "System validation and commissioning to ensure reliable plant operations.",
                    "points": [
                     "Functional Testing",
                     "Load Testing",
                     "Performance Validation",
                     "Safety & Compliance Checks"
                    ]
                }
            }
        },

        # ================= MAINTENANCE & REPAIR =================
        "maintenance-repair": {
            "title": "Maintenance & Repair",
            "description": "Comprehensive maintenance and repair services to ensure uninterrupted industrial operations.",
            "sub_services": {
                "equipment-repair": {
                    "title": "Industrial Equipment Repair",
                    "description": "Repair and refurbishment services for industrial automation equipment.",
                    "points": [
                        "PLC Troubleshooting & Repair",
                        "HMI Diagnostics",
                        "VFD & Drive Repair",
                        "Control Panel Fault Analysis"
                    ]
                },
                "amc-services": {
                    "title": "AMC Services",
                    "description": "Structured annual maintenance contracts for preventive and corrective maintenance.",
                    "points": [
                        "Preventive Maintenance",
                        "Scheduled Inspections",
                        "Software Backup & Updates",
                        "Priority Breakdown Support"
                    ]
                },
                "troubleshooting-support": {
                    "title": "Troubleshooting & Support",
                    "description": "Fast and reliable breakdown support for industrial automation systems.",
                    "points": [
                       "Remote Technical Support",
                       "On-Site Diagnosis",
                       "Emergency Response Service"
                    ]
                }
            }
        },

        # ================= TRAINING =================
        "training": {
            "title": "Training Programs",
            "description": "Professional industrial automation training programs focused on practical and industry-oriented learning.",
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
