import json
import boto3
import uuid
from datetime import datetime
from decimal import Decimal

dynamodb = boto3.resource('dynamodb')
dynamodb_client = boto3.client('dynamodb')
users_table = dynamodb.Table('users')
products_table = dynamodb.Table('products')


def lambda_handler(event, context):
    """Called when the route is triggered
    """
    route_key = event.get('routeKey')   # get the endpoint
    
    if route_key == 'GET /get-user/{idOrUsername}':
        # get the user either with id or username
        id_or_username = event.get('pathParameters')['idOrUsername']
        
        try:
            query = f"SELECT * FROM users WHERE id = '{id_or_username}' OR userName = '{id_or_username}'"
            response = dynamodb_client.execute_statement(Statement=query)
            response_item = response.get("Items")
            if response_item:
                response_item = response_item[0]
            else:
                return generateResponse(404, dict(message="user not found"))
                
            formated_data = {}
            for key, value in response_item.items():
                formated_data[key] = list(value.values())[0]
            return generateResponse(200, formated_data)
            
        except Exception as error:
            return generateResponse(400, dict(error=str(error)))
        
    elif route_key == 'POST /create-user':
        # create a new user
        try:
            data = json.loads(event.get('body'))
            if not data.get('id'):  # id not in the request body
                data['id'] = str(uuid.uuid4()).replace('-','')
                data['createdAt'] = f"{int(datetime.now().timestamp() * 1e6)}"
            response = users_table.put_item(Item=data, ReturnValues='ALL_OLD')
            return generateResponse(200, data)
        except Exception as error:
            return generateResponse(400, dict(error=str(error)))
    
    elif route_key == 'PATCH /update-user/{id}':
        # update a given user
        try:
            data = json.loads(event.get('body'))
            item_key= event.get('pathParameters')['id']
            user_name = data.get('userName')
            key_dict =  { 'id':f"{item_key}"}
            attributes_values = {}
            attributes_names = {}
            update_expression = "SET"
            for index, item in enumerate(list(data.items())):
                this_name = f"#attrName{index}"
                this_val = f":attrValue{index}"
                attributes_names[this_name] = item[0]
                attributes_values[this_val] = item[1]
                update_expression += f" {this_name} = {this_val}" if update_expression == 'SET' else f", {this_name} = {this_val}"
                
            #return generateResponse(202, attributes_values) 
            response = users_table.update_item(
                Key=key_dict,
                UpdateExpression=update_expression,
                ExpressionAttributeNames=attributes_names,
                ExpressionAttributeValues=attributes_values,
                ReturnValues='ALL_OLD'
                )
            new_data = response.get('Attributes')
            new_data.update(data)
            return generateResponse(202, new_data)
        except Exception as error:
            return generateResponse(404, dict(error=str(error)))
            
    elif route_key == 'POST /create-product':
        # create a new product
        try:
            data = json.loads(event.get('body'))
            if not data.get('id'):
                data['id'] = str(uuid.uuid4()).replace('-','')
                data['createdAt'] =  f"{int(datetime.now().timestamp() * 1e6)}"
                response = products_table.put_item(Item=data, ReturnValues='ALL_OLD')
                return generateResponse(200, data)
        except Exception as error:
            return generateResponse(400, dict(error=str(error)))
            
    elif route_key == 'GET /list-product':
        # list all products
        response_keys = {"LastEvaluatedKey", 'Items'}
        try:
            response = products_table.scan()
            response_items_keys = set(response.keys())
            keys = response_keys.intersection(response_items_keys)
            new_response = {}
            for key in list(keys):
                new_response[key] = response.get(key)
            new_response['statusCode'] = 200
            new_response['length'] = response.get("Count")
            return generateResponse(200, new_response)
        except Exception as error:
            return generateResponse(400, dict(message=str(error)))
    
def generateResponse(status_code, body=None):
    response = {
        'statusCode': status_code,
        'headers': {
            'ContentType': 'application/json',
            'Access-Control-Allow-Origin': '*'
        }
    }
    if body is not None:
        response['body'] = json.dumps(body, cls=CustomEncoder)
    return response

class CustomEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, Decimal):
            return int(obj)
        return json.JSONEncoder.default(self, obj)