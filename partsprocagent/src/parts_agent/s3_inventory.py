from io import BytesIO

import boto3
import pandas as pd

from .config import (
    AWS_REGION,
    S3_BUCKET,
    INVENTORY_KEY
)


class S3Inventory:

    def __init__(self):

        self.client = boto3.client(
            "s3",
            region_name=AWS_REGION
        )

        self.bucket = S3_BUCKET

        self.key = INVENTORY_KEY

    # ---------------------------------------------
    # Upload CSV
    # ---------------------------------------------
    def upload_csv(
        self,
        content: bytes
    ):

        self.client.put_object(
            Bucket=self.bucket,
            Key=self.key,
            Body=content,
            ContentType="text/csv"
        )

        return {
            "bucket": self.bucket,
            "key": self.key
        }

    # ---------------------------------------------
    # Check stock
    # ---------------------------------------------
    def check_inventory(
        self,
        part_number: str,
        quantity: int
    ):

        response = (
            self.client.get_object(
                Bucket=self.bucket,
                Key=self.key
            )
        )

        df = pd.read_csv(
            response["Body"]
        )

        matches = df[
            df["part_number"]
            == part_number
        ]

        if matches.empty:

            stock = 0
            part_name = None

        else:

            row = matches.iloc[0]

            stock = int(
                row["stock_quantity"]
            )

            part_name = (
                row["part_name"]
            )

        return {
            "part_number":
                part_number,
            "part_name":
                part_name,
            "stock_quantity":
                stock,
            "requested_quantity":
                quantity,
            "available":
                stock >= quantity
        }