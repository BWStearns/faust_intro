from typing import List, Optional, AsyncIterable
import uuid

import faust

app = faust.App("demo")

class PurchaseRecord(faust.Record, serializer="json"):
    msg_id: uuid.UUID
    customer: str
    amount: int
    note: Optional[str]

customer_table = app.Table("customer_table", default=int, partitions=1)

purchase_topic = app.topic("purchase_topic", value_type=PurchaseRecord, partitions=1)


def handle_purchase(purchase):
    customer_table[purchase.customer] = customer_table[purchase.customer] + purchase.amount
    print(f"{purchase.customer} has spent {customer_table[purchase.customer]} so far.")

@app.agent(purchase_topic)
async def purchase_processor(purchases: AsyncIterable[PurchaseRecord]):
    """Accumulate purchases."""
    async for purchase in purchases:
        print("Processing: ", purchase)
        handle_purchase(purchase)

@app.page("/customer/{customer_id}")
async def joiner_count(self, request, customer_id):
    """Endpoint to be able to check on the elements in the joiner backlog."""
    return self.json({"customer": customer_id, "total_spent": customer_table[customer_id]})
