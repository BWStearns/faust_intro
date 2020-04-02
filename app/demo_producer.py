import uuid
from random import randint

from kafka import KafkaProducer

from .demo import PurchaseRecord

customers = ["hamzah", "meher", "brian"]
notes = [None, "Foo", "Bar", "Baz", None]

producer = KafkaProducer()

def get_purchase_amount():
	return randint(1, 20)

def make_purchase(customer):
	note = notes[randint(0, 4)]
	return PurchaseRecord(uuid.uuid4(), customer, get_purchase_amount(), note)

def make_random_purchase():
	return make_purchase(customers[randint(0,2)])

def make_random_purchases(n):
	return [make_random_purchase() for x in range(n)]

def send_purchases(purchases):
	for p in purchases:
		producer.send("purchase_topic", p.dumps())
