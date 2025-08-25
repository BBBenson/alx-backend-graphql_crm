import requests
import datetime

url = "http://localhost:8000/graphql"
query = """
query {
  ordersWithinLastWeek {
    id
    customer {
      email
    }
  }
}
"""

response = requests.post(url, json={'query': query})
orders = response.json().get("data", {}).get("ordersWithinLastWeek", [])

timestamp = datetime.datetime.now().strftime("%d/%m/%Y-%H:%M:%S")
with open("/tmp/order_reminders_log.txt", "a") as f:
    for order in orders:
        f.write(f"{timestamp} Order {order['id']} reminder for {order['customer']['email']}\n")

print("Order reminders processed!")
