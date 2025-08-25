from celery import shared_task
from gql.transport.requests import RequestsHTTPTransport
from gql import gql, Client
from datetime import datetime
import requests

@shared_task
def generate_crm_report():
    # Setup GraphQL transport
    transport = RequestsHTTPTransport(
        url="http://localhost:8000/graphql",
        verify=True,
        retries=3,
    )
    client = Client(transport=transport, fetch_schema_from_transport=True)

    # GraphQL query
    query = gql("""
    query {
      totalCustomers
      totalOrders
      totalRevenue
    }
    """)

    result = client.execute(query)

    customers = result.get("totalCustomers", 0)
    orders = result.get("totalOrders", 0)
    revenue = result.get("totalRevenue", 0)

    # Log report
    timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    with open("/tmp/crm_report_log.txt", "a") as f:
        f.write(f"{timestamp} - Report: {customers} customers, {orders} orders, {revenue} revenue\n")

    return {"customers": customers, "orders": orders, "revenue": revenue}
