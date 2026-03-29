import json, base64, boto3, datetime

s3 = boto3.client('s3')
BUCKET = 'prj-clickstream-data-lake'  # ← change this

def lambda_handler(event, context):
    records = []
    for rec in event['Records']:
        # Kinesis encodes data as base64
        payload = base64.b64decode(rec['kinesis']['data']).decode('utf-8')
        data = json.loads(payload)
        records.append(json.dumps(data))
    
    now = datetime.datetime.utcnow()
    key = f"raw/year={now.year}/month={now.month:02d}/day={now.day:02d}/{now.timestamp()}.json"
    
    s3.put_object(
        Bucket=BUCKET,
        Key=key,
        Body='\n'.join(records),
        ContentType='application/json'
    )
    return {'statusCode': 200, 'body': f'Wrote {len(records)} records'}