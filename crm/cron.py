from gql.transport.requests import RequestsHTTPTransport
from gql import gql, Client
import datetime

def log_crm_heartbeat():
    timestamp = datetime.datetime.now().strftime("%d/%m/%Y-%H:%M:%S")
    with open("/tmp/crm_heartbeat_log.txt", "a") as f:
        f.write(f"{timestamp} CRM is alive\n")

def update_low_stock():
    # Setup GraphQL transport
    transport = RequestsHTTPTransport(
        url="http://localhost:8000/graphql",
        verify=True,
        retries=3,
    )

    # Initialize client
    client = Client(transport=transport, fetch_schema_from_transport=True)

    # Define mutation
    mutation = gql("""
    mutation {
      updateLowStockProducts {
        success
        updated
      }
    }
    """)

    # Execute mutation
    result = client.execute(mutation)
    data = result.get("updateLowStockProducts", {})

    # Log result
    timestamp = datetime.datetime.now().strftime("%d/%m/%Y-%H:%M:%S")
    with open("/tmp/low_stock_updates_log.txt", "a") as f:
        f.write(f"{timestamp} {data}\n")
