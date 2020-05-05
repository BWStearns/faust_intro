from typing import List, Optional, AsyncIterable
import random
import uuid

import faust
from kafka import KafkaProducer

app = faust.App("demo")
producer = KafkaProducer()

class CustomerRecord(faust.Record, serializer="json"):
    msg_id: uuid.UUID
    customer: str
    amount: int
    number_of_purchases: int
    note: Optional[str]

customer_topic = app.topic("customer_topic", value_type=CustomerRecord)

completed_customer_topic = app.topic("completed_customer_topic", value_type=CustomerRecord)

def ring_up_customer(customer):
    customer.number_of_purchases += 1
    purchase_price = random.randint(1, 100)
    customer.amount += purchase_price
    print(f"{customer.customer} spent {purchase_price}")

def customer_is_done(customer):
    return (customer.number_of_purchases > 100
        or customer.amount > 5000
        or random.randint(1, 100) == 1)


latest_customer = {}

@app.agent(customer_topic)
async def purchase_processor(customers: AsyncIterable[CustomerRecord]):
    """Process customer purchases."""
    async for customer in customers:
        latest_customer = ring_up_customer(customer)
        if customer_is_done(customer):
            print(f"{customer.customer} spent {customer.amount / customer.number_of_purchases} on average.")
            print(customer)
            producer.send("completed_customer_topic", customer.dumps())
        else:
            producer.send("customer_topic", customer.dumps())
