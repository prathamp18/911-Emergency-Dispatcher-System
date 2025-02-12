# 911 Emergency Dispatcher System 🚨

A CLI-based emergency response system with real-time incident tracking and responder management, built with Python and MySQL.

## Features ✨

- 📞 Log emergency calls with caller details and incident information
- 🗃️ MySQL database integration for persistent data storage
- 👮 Automated responder assignment based on incident type (Police, Fire, Medical)
- 🔄 Real-time status updates (Pending → In Progress → Resolved)
- 📊 View pending incidents and responder availability
- 🖥️ Multi-terminal simulation for dispatcher workflow

### Prerequisites
- Python 3.8+
- MySQL Server
- macOS/Linux (for terminal simulation feature)

## Main Menu Options:

📝 Log Emergency Call
📋 View Pending Incidents
👥 Assign Responder
🔄 Update Incident Status
🚪 Exit System

The system will automatically:
Create database tables on first run
Open new terminal window for dispatcher interface
Maintain responder availability status

## Database Schema 🗄️

### **Incidents Table**
| Column | Type | Description |
|--------|------|-------------|
| `id` | `INT` | Unique incident ID |
| `caller_name` | `VARCHAR(100)` | Caller's name |
| `phone` | `VARCHAR(15)` | Caller's phone number |
| `location` | `VARCHAR(255)` | Incident location |
| `type` | `VARCHAR(50)` | Incident type (Police/Fire/Medical) |
| `severity` | `INT` | Severity level (1-5) |
| `status` | `VARCHAR(20)` | Current status (Pending/In Progress/Resolved) |

### **Responders Table**
| Column | Type | Description |
|--------|------|-------------|
| `id` | `INT` | Unique responder ID |
| `name` | `VARCHAR(100)` | Responder name |
| `role` | `VARCHAR(50)` | Responder specialization (Police Officer/Firefighter/Paramedic) |
| `status` | `VARCHAR(20)` | Availability status (Available/Busy) |
