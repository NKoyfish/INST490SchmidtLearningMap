import boto3
from boto3.dynamodb.conditions import Key
from boto3.dynamodb.conditions import Attr



dynamodb = boto3.resource('dynamodb')
table = dynamodb.Table('pgcpsDB')
columnName = 'section1_green_school_certification'
value = 'Yes'
    
    # return (event)
query = table.scan(
    FilterExpression = Attr(columnName).eq(value)
)
    
    # return (query['Items'])
print(query["Items"][0])