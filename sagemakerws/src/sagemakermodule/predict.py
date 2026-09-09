import json
import boto3

ENDPOINT_NAME = "bmw-parts-demand-endpoint"

runtime = boto3.client(
    "sagemaker-runtime",
    region_name="us-east-1",
)

payload = {
    "instances": [
        [1, 100, 80, 75, 500, 1.2, 7]
    ]
}

response = runtime.invoke_endpoint(
    EndpointName=ENDPOINT_NAME,
    ContentType="application/json",
    Accept="application/json",
    Body=json.dumps(payload),
)

print(response["Body"].read().decode("utf-8"))