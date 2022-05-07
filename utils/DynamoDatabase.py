import os
import boto3


class DynamoDatabase:
    def __init__(self):
        try:
            self.client = boto3.client(
                'dynamodb',
                aws_access_key_id=os.getenv('AWS_ACCESS_KEY_ID'),
                aws_secret_access_key=os.getenv('AWS_SECRET_ACCESS_KEY')
            )
            self.resource = boto3.resource(
                'dynamodb',
                aws_access_key_id=os.getenv('AWS_ACCESS_KEY_ID'),
                aws_secret_access_key=os.getenv('AWS_SECRET_ACCESS_KEY')
            )

            self.table_name = 'artists_top_wow_songs'

            self.table = self.resource.Table(self.table_name)

            self.create_tables()
        except Exception as e:
            print(e)

    def create_tables(self):
        try:
            existing_tables = self.client.list_tables()['TableNames']

            if self.table_name not in existing_tables:
                self.client.create_table(
                    AttributeDefinitions=[
                        {
                            'AttributeName': 'search_term',
                            'AttributeType': 'S',
                        }
                    ],
                    KeySchema=[
                        {
                            'AttributeName': 'search_term',
                            'KeyType': 'HASH',
                        }
                    ],
                    ProvisionedThroughput={
                        'ReadCapacityUnits': 5,
                        'WriteCapacityUnits': 5,
                    },
                    TableName=self.table_name,
                )
        except Exception as e:
            print(e)

    def set_item(self, search_term, item_data):
        try:
            response = self.table.update_item(
                Key={
                    'search_term': search_term
                },
                UpdateExpression="set artist_data=:s",
                ExpressionAttributeValues={
                    ":s": item_data
                }
            )

            return response
        except Exception as e:
            print(e)

            return None
