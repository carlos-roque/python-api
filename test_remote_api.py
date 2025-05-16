#!/usr/bin/env python3
import requests
import sys
import json
from datetime import datetime

# Default values for the remote API
API_URL = 'http://24.59.50.128:9002/api/process'
TOKEN = 'carlos89-api-token'
HEALTH_URL = 'http://24.59.50.128:9002/api/health'

def test_health():
    """Test the health endpoint of the API"""
    print(f"\n🔍 Testing API health at: {HEALTH_URL}")
    try:
        response = requests.get(HEALTH_URL, timeout=10)
        
        print(f"Status Code: {response.status_code}")
        if response.status_code == 200:
            print("Response:")
            print(json.dumps(response.json(), indent=2))
            print("\n✅ Health check passed!")
            return True
        else:
            print(f"\n❌ Health check failed with status code: {response.status_code}")
            if response.text:
                print(f"Response: {response.text}")
            return False
            
    except requests.exceptions.ConnectionError:
        print(f"\n❌ Connection error! Could not connect to {HEALTH_URL}")
        print("Please check if:")
        print("  - The server is running")
        print("  - The port forwarding is correctly set up")
        print("  - There are no firewall rules blocking the connection")
        return False
    except requests.exceptions.Timeout:
        print(f"\n❌ Connection timed out when trying to reach {HEALTH_URL}")
        return False
    except Exception as e:
        print(f"\n❌ Unexpected error during health check: {str(e)}")
        return False

def test_process_endpoint():
    """Test the process endpoint of the API with sample parameters"""
    print(f"\n🔍 Testing API endpoint at: {API_URL}")
    print(f"Using token: {TOKEN[:4]}...{TOKEN[-4:]}")
    
    # Sample parameters to test with
    params = {
        'param1': 'test_value1',
        'param2': 'test_value2',
        'param3': 'test_value3',
        'timestamp': datetime.now().isoformat()
    }
    
    # Set authorization header with bearer token
    headers = {
        'Authorization': f'Bearer {TOKEN}'
    }
    
    try:
        start_time = datetime.now()
        # Make GET request to API
        response = requests.get(API_URL, params=params, headers=headers, timeout=10)
        end_time = datetime.now()
        
        # Calculate response time
        response_time = (end_time - start_time).total_seconds() * 1000  # in milliseconds
        
        # Print response status and content
        print(f"Status Code: {response.status_code}")
        print(f"Response Time: {response_time:.2f} ms")
        
        if response.status_code == 200:
            print("Response:")
            print(json.dumps(response.json(), indent=2))
            
            # Check if the response contains the expected parameters
            json_response = response.json()
            expected_keys = ['status', 'message', 'received_params_count', 'processed_data', 'timestamp']
            missing_keys = [key for key in expected_keys if key not in json_response]
            
            if not missing_keys:
                print("\n✅ Test passed! All expected response parameters are present.")
                return True
            else:
                print(f"\n❌ Test failed! Missing keys in response: {missing_keys}")
                return False
        else:
            print("\n❌ Test failed with unexpected status code!")
            if response.text:
                print(f"Response: {response.text}")
            return False
            
    except requests.exceptions.ConnectionError:
        print(f"\n❌ Connection error! Could not connect to {API_URL}")
        print("Please check if:")
        print("  - The server is running")
        print("  - The port forwarding is correctly set up")
        print("  - There are no firewall rules blocking the connection")
        return False
    except requests.exceptions.Timeout:
        print(f"\n❌ Connection timed out when trying to reach {API_URL}")
        return False
    except Exception as e:
        print(f"\n❌ Unexpected error: {str(e)}")
        return False

if __name__ == '__main__':
    print("=" * 60)
    print(f"🌐 Remote API Test - {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print("=" * 60)
    
    # Allow overriding defaults from command line arguments
    if len(sys.argv) > 1:
        base_url = sys.argv[1]
        if not base_url.endswith('/'):
            base_url += '/'
        API_URL = f"{base_url}api/process"
        HEALTH_URL = f"{base_url}api/health"
    
    if len(sys.argv) > 2:
        TOKEN = sys.argv[2]
    
    # First test the health endpoint
    health_status = test_health()
    
    # Only test the process endpoint if health check passed
    if health_status:
        process_status = test_process_endpoint()
    else:
        print("\n⚠️ Skipping process endpoint test since health check failed.")
        process_status = False
    
    print("\n" + "=" * 60)
    print("📊 Test Summary:")
    print(f"Health Check: {'✅ Passed' if health_status else '❌ Failed'}")
    if health_status:
        print(f"Process Endpoint: {'✅ Passed' if process_status else '❌ Failed'}")
    print("=" * 60)
    
    # Exit with appropriate status code
    sys.exit(0 if (health_status and process_status) else 1) 