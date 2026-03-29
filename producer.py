import boto3, json, time, random
from faker import Faker
from datetime import datetime

fake = Faker()
kinesis = boto3.client('kinesis', region_name='us-east-1')
STREAM = 'prj-clickstream-events'
PAGES = ['/home', '/products', '/cart', '/checkout', '/about', '/blog']

def generate_event():
    return {
        "event_id": fake.uuid4(),
        "user_id": f"user_{random.randint(1000, 9999)}",
        "session_id": fake.uuid4(),
        "page": random.choice(PAGES),
        "referrer": random.choice(['google', 'direct', 'email', 'social']),
        "device": random.choice(['mobile', 'desktop', 'tablet']),
        "timestamp": datetime.utcnow().isoformat(),
        "duration_ms": random.randint(500, 15000)
    }

print(f"Sending events to {STREAM}... (Ctrl+C to stop)")
count = 0
while True:
    event = generate_event()
    kinesis.put_record(
        StreamName=STREAM,
        Data=json.dumps(event),
        PartitionKey=event['user_id']  # routes same user to same shard
    )
    count += 1
    print(f"  Sent #{count}: {event['user_id']} → {event['page']}")
    time.sleep(1)