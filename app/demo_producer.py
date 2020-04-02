import uuid
from random import randint

from kafka import KafkaProducer, KafkaAdminClient

from .demo import PurchaseRecord

customers = ["hamzah", "meher", "brian"]

producer = KafkaProducer()

def get_purchase_amount():
	return randint(1, 20)

def make_purchase(customer):
	return PurchaseRecord(uuid.uuid4(), customer, get_purchase_amount())

def make_random_purchase():
	return make_purchase(customers[randint(0,2)])

def make_random_purchases(n):
	return [make_random_purchase() for x in range(n)]

def send_purchases(purchases):
	for p in purchases:
		producer.send("purchase_topic", p.dumps())
