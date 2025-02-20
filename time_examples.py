import requests
import json
import base64
from flask import Flask, jsonify, make_response
from datetime import datetime, timezone

app = Flask(__name__)

API_KEY = 'mGwU4AoN95zL5iOg03-c'
BASE_URL = 'https://060helpdesk.freshservice.com/api/v2'

def get_ticket_count():
    # Create proper Basic Auth string
    auth_string = base64.b64encode(f"{API_KEY}:X".encode()).decode()
    
    headers = {
        'Authorization': f'Basic {auth_string}',
        'Content-Type': 'application/json'
    }
    
    priorities = [1, 2, 3, 4]
    ticket_counts = {}
    total_tickets = 0
    
    for priority in priorities:
        url = f"{BASE_URL}/tickets/filter?query=\"priority:{priority}\""
        
        try:
            response = requests.get(url, headers=headers)
            
            if response.status_code == 200:
                data = response.json()
                total = data.get('total', 0)
                ticket_counts[f"priority:{priority}"] = total
                total_tickets += total
                print(f"\n>>> Total Tickets Found for Priority {priority}: {total} <<<\n")
            else:
                ticket_counts[f"priority:{priority}"] = 0
                
        except Exception as e:
            ticket_counts[f"priority:{priority}"] = 0

    ticket_counts["total"] = total_tickets
    return ticket_counts

def get_overdue_tickets():
    # Create proper Basic Auth string
    auth_string = base64.b64encode(f"{API_KEY}:X".encode()).decode()
    
    headers = {
        'Authorization': f'Basic {auth_string}',
        'Content-Type': 'application/json'
    }
    
    url = f"{BASE_URL}/tickets"
    
    try:
        response = requests.get(url, headers=headers)
        
        if response.status_code == 200:
            data = response.json()
            overdue_tickets = [ticket for ticket in data['tickets'] if ticket['status'] == 2]
            total = len(overdue_tickets)
            print(f"\n>>> Total Overdue Tickets: {total} <<<\n")
            return {"overdue": total}
        else:
            return {"overdue": 0}
            
    except Exception as e:
        return {"overdue": 0}

def get_today_tickets():
    auth_string = base64.b64encode(f"{API_KEY}:X".encode()).decode()
    headers = {
        'Authorization': f'Basic {auth_string}',
        'Content-Type': 'application/json'
    }
    
    url = f"{BASE_URL}/tickets"
    today = datetime.now(timezone.utc).strftime("%Y-%m-%d")
    
    try:
        response = requests.get(url, headers=headers)
        if response.status_code == 200:
            data = response.json()
            today_tickets = []
            
            for ticket in data['tickets']:
                due_date = ticket.get('due_by', '').split('T')[0]  # Get just the date part
                if due_date == today:
                    today_tickets.append({
                        'id': ticket['id'],
                        'subject': ticket['subject'],
                        'due_by': due_date
                    })
                    print(f"\nTicket Due Today:")
                    print(f"ID: {ticket['id']}")
                    print(f"Subject: {ticket['subject']}")
                    print(f"Due Date: {due_date}")
            
            print(f"\nTotal tickets due today ({today}): {len(today_tickets)}")
            return {"due_today": len(today_tickets), "due_today_tickets": today_tickets}
        else:
            print(f"Error fetching tickets: {response.status_code}")
            return {"due_today": 0, "due_today_tickets": []}
            
    except Exception as e:
        print(f"Error in get_today_tickets: {str(e)}")
        return {"due_today": 0, "due_today_tickets": []}

@app.route('/tickets/count')
def ticket_count():
    ticket_data = get_ticket_count()
    overdue_data = get_overdue_tickets()
    today_data = get_today_tickets()
    
    # Combine all data
    ticket_data.update(overdue_data)
    ticket_data.update(today_data)
    ticket_data["last_updated"] = datetime.now(timezone.utc).strftime("%Y-%m-%d %H:%M:%S")
    
    response = make_response(jsonify(ticket_data))
    response.headers.add('Access-Control-Allow-Origin', '*')
    response.headers.add('Access-Control-Allow-Headers', 'Content-Type')
    return response

@app.route('/')
def home():
    return 'Ticket API is running'

if __name__ == '__main__':
    app.run(port=5000, debug=True)
