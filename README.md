# Python API with Bearer Token Authentication

This API provides a secure endpoint that accepts GET requests with up to 10 optional parameters, requires bearer token authentication, and returns 5 parameters in the response. It also integrates with the MySQL database from the FullStackMysql project.

## API Specification

### Endpoint

```
GET /api/process
```

### Authentication

This API uses Bearer Token authentication. Include the token in the Authorization header of your request:

```
Authorization: Bearer carlos89-api-token
```

### Query Parameters

The API accepts up to 10 optional query parameters:

- `param1` through `param10`

Example: `/api/process?param1=value1&param2=value2`

### Response

The API returns a JSON response with the following parameters:

1. `status`: Status of the request processing ("success" or "error")
2. `message`: A descriptive message about the result
3. `received_params_count`: The number of parameters received in the request
4. `db_info`: Information about the database connection and car count
5. `processed_data`: Information about the processed data

## Setup and Deployment

### Local Development

1. Install dependencies:
   ```
   pip install -r requirements.txt
   ```

2. Run the application:
   ```
   python app/main.py
   ```

### Docker Deployment

Build and run the application using Docker:

```
docker build -t python-api .
docker run -p 5000:5000 -e API_TOKEN=carlos89-api-token python-api
```

Or use Docker Compose:

```
docker-compose up -d
```

## Testing

Use the provided test script to verify the API's functionality:

```
python test_api.py [api_url] [token]
```

Default values:
- API URL: http://localhost:5000/api/process
- Token: carlos89-api-token

## Environment Variables

- `API_TOKEN`: The bearer token required for authentication (default: "carlos89-api-token")
- `PORT`: The port on which the application runs (default: 5000)
- `DEBUG`: Enable/disable debug mode ("True" or "False", default: "False")
- `MYSQL_HOST`: MySQL database host (default: "db")
- `MYSQL_USER`: MySQL database user (default: "root")
- `MYSQL_PASSWORD`: MySQL database password (default: "carlos89")
- `MYSQL_DATABASE`: MySQL database name (default: "cardb") 