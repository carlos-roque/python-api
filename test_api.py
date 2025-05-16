import requests
import sys

# Default values
API_URL = 'http://localhost:5000/api/process'
TOKEN = 'carlos89-api-token'

def test_api():
    # Sample parameters
    params = {
        'param1': 'value1',
        'param2': 'value2',
        'param3': 'value3',
        'param4': 'value4',
        'param5': 'value5',
        'param6': 'value6',
        'param7': 'value7',
        'param8': 'value8',
        'param9': 'value9',
        'param10': 'value10'
    }
    
    # Set authorization header with bearer token
    headers = {
        'Authorization': f'Bearer {TOKEN}'
    }
    
    try:
        # Make GET request to API
        response = requests.get(API_URL, params=params, headers=headers)
        
        # Print response status and content
        print(f'Status Code: {response.status_code}')
        print('Response:')
        print(response.json())
        
        # Check if the response contains the expected 5 parameters
        if response.status_code == 200:
            json_response = response.json()
            expected_keys = ['status', 'message', 'received_params_count', 'processed_data', 'timestamp']
            missing_keys = [key for key in expected_keys if key not in json_response]
            
            if not missing_keys:
                print('\nTest passed! All expected response parameters are present.')
            else:
                print(f'\nTest failed! Missing keys in response: {missing_keys}')
        else:
            print('\nTest failed! Unexpected status code.')
            
    except requests.exceptions.RequestException as e:
        print(f'\nError making request: {e}')
    except Exception as e:
        print(f'\nUnexpected error: {e}')

if __name__ == '__main__':
    # Allow overriding defaults from command line arguments
    if len(sys.argv) > 1:
        API_URL = sys.argv[1]
    if len(sys.argv) > 2:
        TOKEN = sys.argv[2]
        
    print(f'Testing API at: {API_URL}')
    print(f'Using token: {TOKEN[:4]}...{TOKEN[-4:]}')
    test_api() 