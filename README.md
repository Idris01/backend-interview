# Api Documentation
## Introduction
This project involves setting up some api backend using AWS lambda,
DynamoDb, API Gateway

## Description
Following are the description of activites carried out to complete the project;
1. Create DynamoDb Table
  This involve the creation of the database tables on an AWS cloud service. The tables created are `users` and `products` tables. For the
  `users` table, there
    - Primary partition key field namely `id`, it is a UUID field, this must be unique
    - Secondary Sort key field namely `userName`.
For the `products` table there is
    - Primary partition key field namely `id`

2. Create the Lambda function that serves as the backend for the application.

3. Create IAM roles that grants the lambda function permissions to access the the dynamodb database.

4. Create routes for our api endpoints using API Gateway, these routes triggers the lamda function to handle the requests.

The API GATEWAY base url:
> BASE_URL= https://b629zknkqa.execute-api.us-east-1.amazonaws.com

## API Endpoints
### `/create-user'
Create a new user

- Sample request

```
curl -X POST https://b629zknkqa.execute-api.us-east-1.amazonaws.com/create-user \
-H "Content-Type: application/json" \
-d '{
    "activateUser": false,
    "currency": "NGN",
    "lastName": "Lamidi ",
    "email": "lamiditemitope31@email.com" ,
    "firstName": "Temitope ",
    "phone": "7043330737",
    "role": "seller",
    "userName": "temi247"
    }'
```

- Sample Response
```
    {
    "id": "d6b007579dcf4bd7a59ca9e4751fffe8",
    "activateUser": false,
    "currency": "NGN",
    "lastName": "Lamidi ",
    "email": "lamiditemitope31@email.com" ,
    "firstName": "Temitope ",
    "phone": "7043330737",
    "role": "seller",
    "createdAt":"1707660898612681",
    "userName": "temi247",
    }
```

### `/get-user/{id}`
Get user by `id`
- Sample request
```
curl -X GET https://b629zknkqa.execute-api.us-east-1.amazonaws.com/get-user/d6b007579dcf4bd7a59ca9e4751fffe8
```

- Sample response
```
{
    "id": "d6b007579dcf4bd7a59ca9e4751fffe8",
    "activateUser": false,
    "currency": "NGN",
    "lastName": "Lamidi ",
    "email": "lamiditemitope31@email.com" ,
    "firstName": "Temitope ",
    "phone": "7043330737",
    "role": "seller",
    "createdAt":"1707660898612681",
    "userName": "temi247"
}
```
### `/get-user/{userName}`
Get user by `userName`
- Sample request
```
curl -X GET https://b629zknkqa.execute-api.us-east-1.amazonaws.com/get-user/temi247
```

- Sample response
```
{
    "id": "d6b007579dcf4bd7a59ca9e4751fffe8",
    "activateUser": false,
    "currency": "NGN",
    "lastName": "Lamidi ",
    "email": "lamiditemitope31@email.com" ,
    "firstName": "Temitope ",
    "phone": "7043330737",
    "role": "seller",
    "createdAt":"1707660898612681",
    "userName": "temi247"
}
```

### `/update-user/{id}`
Update user with `id`
- Sample request
```
curl -X PATCH https://b629zknkqa.execute-api.us-east-1.amazonaws.com/update-user/d6b007579dcf4bd7a59ca9e4751fffe8   \
-d '{
    "activateUser": true,
    "role": "buyer",
    "userName": "temi2478"
}'
```

- Sample response
```
{
    "id": "d6b007579dcf4bd7a59ca9e4751fffe8",
    "activateUser": true,
    "currency": "NGN",
    "lastName": "Lamidi ",
    "email": "lamiditemitope31@email.com" ,
    "firstName": "Temitope ",
    "phone": "7043330737",
    "role": "buyer",
    "createdAt":"1707660898612681",
    "userName": "temi2478"
}
```

### `/create-product`
Create new product on the products table

- Sample Request 

```
curl -X POST https://b629zknkqa.execute-api.us-east-1.amazonaws.com/create-product  \
-H "Content-Type: application/json" \
-d '{
    "category": "627cc555046919d2a6f21662",
    "city": "Abuja",
    "count": 10,
    "country": "Nigeria",
    "description": "Banana Flavour Minimum Order Quantity - 10pcs",
    "images": [
    {
    "public_id": "n4t5ccur0shvzrnwlkoy",
    "url": "https://res.cloudinary.com/tinkokooffice/image/upload/v1685421283/n4t5ccur0shvzrnwlkoy.jpg"
    }
    ],
    "price": "1000",
    "productName": "L&Z Yoghurt ",
    "quantity": 100,
    "subCategory": "hLBxpm6XoCWvhQQdsmRjQPZL",
    "sellerId": "634084c8fd2c16ba75c006e8",
    "weight": "500"
    }'
```
- Sample Response

```
    {
    "id": "e5b107579dcf4bd7a59ca9e4751fffe1",
    "createdAt":"1707660898612681",
    "category": "627cc555046919d2a6f21662",
    "city": "Abuja",
    "count": 10,
    "country": "Nigeria",
    "description": "Banana Flavour Minimum Order Quantity - 10pcs",
    "images": [
    {
    "public_id": "n4t5ccur0shvzrnwlkoy",
    "url": "https://res.cloudinary.com/tinkokooffice/image/upload/v1685421283/n4t5ccur0shvzrnwlkoy.jpg"
    }
    ],
    "price": "1000",
    "productName": "L&Z Yoghurt ",
    "quantity": 100,
    "subCategory": "hLBxpm6XoCWvhQQdsmRjQPZL",
    "sellerId": "634084c8fd2c16ba75c006e8",
    "weight": "500"
    }
```

### `/list-product`
Get the list of all products

- Sample Request

```

curl -X POST https://b629zknkqa.execute-api.us-east-1.amazonaws.com/list-product
```

- Sample Response

```
{
    "LastEvaluatedKey": {
        "id": "e5b107579dcf4bd7a59ca9e4751fffe1"
    },
    "statusCode": 200,
    "length": 10,
    "items": [
    {
    "id": "e5b107579dcf4bd7a59ca9e4751fffe1",
    "createdAt":"1707660898612681",
    "category": "627cc555046919d2a6f21662",
    "city": "Abuja",
    "count": 10,
    "country": "Nigeria",
    "description": "Banana Flavour Minimum Order Quantity - 10pcs",
    "images": [
    {
    "public_id": "n4t5ccur0shvzrnwlkoy",
    "url": "https://res.cloudinary.com/tinkokooffice/image/upload/v1685421283/n4t5ccur0shvzrnwlkoy.jpg"
    }
    ],
    "price": "1000",
    "productName": "L&Z Yoghurt ",
    "quantity": 100,
    "subCategory": "hLBxpm6XoCWvhQQdsmRjQPZL",
    "sellerId": "634084c8fd2c16ba75c006e8",
    "weight": "500"
    }
    ...
    ]
}
```
