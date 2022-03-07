import boto3
from boto3.dynamodb.conditions import Key
from boto3.dynamodb.conditions import Attr
import pprint

dynamodb = boto3.resource('dynamodb')
table = dynamodb.Table('pgcpsdb')


query = table.scan(
    FilterExpression = Attr('pkey').gte(1)
)
