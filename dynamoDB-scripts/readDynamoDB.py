import boto3
from boto3.dynamodb.conditions import Key
from boto3.dynamodb.conditions import Attr

def lambda_handler():
    """
    Queries the database and returns all values
    """
    dynamodb = boto3.resource('dynamodb')
    table = dynamodb.Table('pgcpsDB')
    
    #returns all values with a 'pkey' greater than or equal to 1
    query = table.scan(
        FilterExpression = Attr('pkey').gte(1)
    )
    
    string = str(query["Items"])
    print(string)
    return string + "sss"

if __name__ == "__main__":
    lambda_handler()
