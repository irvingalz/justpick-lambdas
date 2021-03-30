import json
import os
from datetime import datetime, timezone


import boto3


def lambda_handler(event, context):
    print(f'Event: {json.dumps(event)}')
    if ("triggerSource" in event and event["triggerSource"] == "PostConfirmation_ConfirmSignUp"):
        table_name = os.environ["TABLE_NAME"]

        dynamodb = boto3.resource('dynamodb')
        table = dynamodb.Table(table_name)

        user_attributes = event["request"]["userAttributes"]

        user = {
            "id": user_attributes["sub"],
            "created": datetime.timestamp(datetime.now(timezone.utc)),
            "email": user_attributes["email"],
            "first_name": "",
            "last_name": "",
            "phone_number": user_attributes["phone_number"],
            "profile_photo": "",
            "friends": [],
            "sessions": [],
            "active_session": ""
        }

        print(f'Adding user {user["email"]} to table {table_name}')

        try:
            resp = table.put_item(Item=user)
        except dynamodb.meta.client.exceptions as err:
            print(err)
