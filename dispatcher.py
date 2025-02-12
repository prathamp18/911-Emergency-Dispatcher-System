import mysql.connector
import subprocess

# Function to open a new terminal window
def open_new_terminal():
    subprocess.run(['osascript', '-e', 'tell application "Terminal" to do script "python3 /Users/prathampatel/Desktop/Dispatcher 911/dispatcher.py"'])

# Connect to MySQL
def connect_to_db():
    return mysql.connector.connect(
        host="hostname",       # Hostname
        user="username",   # Your MySQL username
        password="your password", # Your MySQL password
        database="dispatcher_db"  # The database name
    )

# Set up the database and tables
def setup_database():
    conn = connect_to_db()
    cursor = conn.cursor()

    # Create the Incidents table
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS Incidents (
        id INT AUTO_INCREMENT PRIMARY KEY,
        caller_name VARCHAR(100) NOT NULL,
        phone VARCHAR(15) NOT NULL,
        location VARCHAR(255) NOT NULL,
        type VARCHAR(50) NOT NULL,
        severity INT NOT NULL,
        status VARCHAR(20) DEFAULT 'Pending'
    )
    """)

    # Create the Responders table
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS Responders (
        id INT AUTO_INCREMENT PRIMARY KEY,
        name VARCHAR(100) NOT NULL,
        role VARCHAR(50) NOT NULL,
        status VARCHAR(20) DEFAULT 'Available'
    )
    """)

    conn.commit()
    conn.close()
    print("Database setup complete!")

# Log an emergency call
def log_emergency_call():
    conn = connect_to_db()
    cursor = conn.cursor()

    # Collect caller details
    caller_name = input("Enter caller's name: ")
    phone = input("Enter caller's phone number: ")
    location = input("Enter incident location: ")
    incident_type = input("Enter type of incident (e.g., Fire, Medical, Police): ")
    severity = int(input("Enter severity level (1-5): "))

    # Insert the new incident into the database
    cursor.execute("""
    INSERT INTO Incidents (caller_name, phone, location, type, severity)
    VALUES (%s, %s, %s, %s, %s)
    """, (caller_name, phone, location, incident_type, severity))

    conn.commit()
    conn.close()
    print("Emergency call logged successfully!")

# View pending incidents
def view_pending_incidents():
    conn = connect_to_db()
    cursor = conn.cursor()

    # Fetch all pending incidents
    cursor.execute("SELECT * FROM Incidents WHERE status = 'Pending'")
    incidents = cursor.fetchall()

    print("\nPending Incidents:")
    for incident in incidents:
        print(f"ID: {incident[0]}, Caller: {incident[1]}, Location: {incident[3]}, Type: {incident[4]}, Severity: {incident[5]}")

    conn.close()

# Assign a responder
def assign_responder():
    conn = connect_to_db()
    cursor = conn.cursor()

    # Fetch pending incidents
    cursor.execute("SELECT * FROM Incidents WHERE status = 'Pending'")
    incidents = cursor.fetchall()

    if not incidents:
        print("No pending incidents!")
        conn.close()
        return

    print("\nPending Incidents:")
    for incident in incidents:
        print(f"ID: {incident[0]}, Location: {incident[3]}, Type: {incident[4]}, Severity: {incident[5]}")

    # Automatically match responder based on incident type
    incident_id = int(input("\nEnter Incident ID to assign to: "))
    
    # Get the incident type
    cursor.execute("SELECT type FROM Incidents WHERE id = %s", (incident_id,))
    incident_type = cursor.fetchone()[0]

    # Match incident type to responder role
    if incident_type.lower() == "police":
        role = "Police Officer"
    elif incident_type.lower() == "fire":
        role = "Firefighter"
    elif incident_type.lower() == "medical":
        role = "Paramedic"
    else:
        print("No matching responder role for this incident type!")
        conn.close()
        return

    # Fetch an available responder with the matching role
    cursor.execute("SELECT * FROM Responders WHERE role = %s AND status = 'Available'", (role,))
    responder = cursor.fetchone()

    if not responder:
        print(f"No available responders for role: {role}")
        conn.close()
        return

    # Assign responder to incident
    responder_id = responder[0]
    cursor.execute("UPDATE Responders SET status = 'Busy' WHERE id = %s", (responder_id,))
    cursor.execute("UPDATE Incidents SET status = 'In Progress' WHERE id = %s", (incident_id,))

    conn.commit()
    conn.close()
    print(f"Assigned {responder[1]} ({responder[2]}) to incident ID {incident_id}.")


# Update incident status
def update_incident_status():
    conn = connect_to_db()
    cursor = conn.cursor()

    # Fetch all incidents
    cursor.execute("SELECT * FROM Incidents")
    incidents = cursor.fetchall()

    print("\nAll Incidents:")
    for incident in incidents:
        print(f"ID: {incident[0]}, Location: {incident[3]}, Type: {incident[4]}, Status: {incident[6]}")

    # Update status
    incident_id = int(input("\nEnter Incident ID to update: "))
    new_status = input("Enter new status (Pending, In Progress, Resolved): ")

    cursor.execute("UPDATE Incidents SET status = %s WHERE id = %s", (new_status, incident_id))

    if new_status == "Resolved":
        cursor.execute("UPDATE Responders SET status = 'Available' WHERE status = 'Busy'")

    conn.commit()
    conn.close()
    print("Incident status updated successfully!")


# Main menu
def main():
    open_new_terminal()

    setup_database()

    while True:
        print("\n--- 911 Emergency Dispatcher System ---")
        print("1. Log Emergency Call")
        print("2. View Pending Incidents")
        print("3. Assign Responder")
        print("4. Update Incident Status")
        print("5. Exit")

        choice = input("Enter your choice: ")

        if choice == "1":
            log_emergency_call()
        elif choice == "2":
            view_pending_incidents()
        elif choice == "3":
            assign_responder()
        elif choice == "4":
            update_incident_status()
        elif choice == "5":
            print("Exiting the system.")
            break
        else:
            print("Invalid choice. Please try again.")

if __name__ == "__main__":
    main()




