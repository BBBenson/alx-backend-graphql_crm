#!/bin/bash
# Clean inactive customers (no orders in the last year)

TIMESTAMP=$(date +"%d/%m/%Y-%H:%M:%S")
COUNT=$(python manage.py shell -c "
from crm.models import Customer
from django.utils import timezone
from datetime import timedelta
cutoff = timezone.now() - timedelta(days=365)
qs = Customer.objects.filter(order__isnull=True) | Customer.objects.filter(order__date__lt=cutoff)
deleted, _ = qs.delete()
print(deleted)
")

echo "$TIMESTAMP Deleted $COUNT inactive customers" >> /tmp/customer_cleanup_log.txt
