import requests
import datetime

def log_crm_heartbeat():
    timestamp = datetime.datetime.now().strftime("%d/%m/%Y-%H:%M:%S")
    with open("/tmp/crm_heartbeat_log.txt", "a") as f:
        f.write(f"{timestamp} CRM is alive\n")

def update_low_stock():
    url = "http://localhost:8000/graphql"
    mutation = """
    mutation {
      updateLowStockProducts {
        success
        updated
      }
    }
    """
    response = requests.post(url, json={'query': mutation})
    data = response.json().get("data", {}).get("updateLowStockProducts", {})

    timestamp = datetime.datetime.now().strftime("%d/%m/%Y-%H:%M:%S")
    with open("/tmp/low_stock_updates_log.txt", "a") as f:
        f.write(f"{timestamp} {data}\n")
