import boto3

bedrock = boto3.client(
    "bedrock-runtime",
    region_name="us-east-1"
)

response = bedrock.converse(
    modelId="global.amazon.nova-2-lite-v1:0",
    messages=[
        {
            "role": "user",
            "content": [
                {"text": "Explain Amazon Nova 2 in simple terms"}
            ]
        }
    ]
)

print(response["output"]["message"]["content"][0]["text"])


