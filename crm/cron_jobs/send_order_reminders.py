from gql import gql, Client
from gql.transport.requests import RequestsHTTPTransport
import datetime

# Setup GraphQL transport
transport = RequestsHTTPTransport(
    url="http://localhost:8000/graphql",
    verify=True,
    retries=3,
)

# Initialize client
client = Client(transport=transport, fetch_schema_from_transport=True)

# Define query
query = gql("""
query {
  ordersWithinLastWeek {
    id
    customer {
      email
    }
  }
}
""")

# Execute query
result = client.execute(query)
orders = result.get("ordersWithinLastWeek", [])

# Write results to log
timestamp = datetime.datetime.now().strftime("%d/%m/%Y-%H:%M:%S")
with open("/tmp/order_reminders_log.txt", "a") as f:
    for order in orders:
        f.write(f"{timestamp} Order {order['id']} reminder for {order['customer']['email']}\n")

print("Order reminders processed!")
