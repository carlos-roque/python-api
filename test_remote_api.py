#!/usr/bin/env python3
import requests
import sys
import json
import socket
import argparse
from datetime import datetime

# Default values for the remote API
PUBLIC_API_URL = 'http://24.59.50.128:9002/api/process'
PUBLIC_HEALTH_URL = 'http://24.59.50.128:9002/api/health'
TOKEN = 'carlos89-api-token'

def get_local_ip():
    """Get the local IP address of the machine"""
    try:
        # Create a socket to determine the local IP address
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        # Doesn't need to be reachable
        s.connect(('8.8.8.8', 1))
        local_ip = s.getsockname()[0]
        s.close()
        return local_ip
    except Exception:
        return '127.0.0.1'  # Return localhost if unable to determine

def test_health(url, timeout=10):
    """Test the health endpoint of the API"""
    print(f"\n🔍 Testing API health at: {url}")
    try:
        response = requests.get(url, timeout=timeout)
        
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
        print(f"\n❌ Connection error! Could not connect to {url}")
        print("Please check if:")
        print("  - The server is running")
        print("  - The port forwarding is correctly set up")
        print("  - There are no firewall rules blocking the connection")
        return False
    except requests.exceptions.Timeout:
        print(f"\n❌ Connection timed out when trying to reach {url}")
        return False
    except Exception as e:
        print(f"\n❌ Unexpected error during health check: {str(e)}")
        return False

def test_process_endpoint(url, token, timeout=10):
    """Test the process endpoint of the API with sample parameters"""
    print(f"\n🔍 Testing API endpoint at: {url}")
    print(f"Using token: {token[:4]}...{token[-4:]}")
    
    # Sample parameters to test with
    params = {
        'param1': 'test_value1',
        'param2': 'test_value2',
        'param3': 'test_value3',
        'timestamp': datetime.now().isoformat()
    }
    
    # Set authorization header with bearer token
    headers = {
        'Authorization': f'Bearer {token}'
    }
    
    try:
        start_time = datetime.now()
        # Make GET request to API
        response = requests.get(url, params=params, headers=headers, timeout=timeout)
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
        print(f"\n❌ Connection error! Could not connect to {url}")
        print("Please check if:")
        print("  - The server is running")
        print("  - The port forwarding is correctly set up")
        print("  - There are no firewall rules blocking the connection")
        return False
    except requests.exceptions.Timeout:
        print(f"\n❌ Connection timed out when trying to reach {url}")
        return False
    except Exception as e:
        print(f"\n❌ Unexpected error: {str(e)}")
        return False

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Test the Python API')
    parser.add_argument('--public', action='store_true', help='Test using public IP address')
    parser.add_argument('--vm', action='store_true', help='Test using VM local IP address')
    parser.add_argument('--url', type=str, help='Base URL to test (e.g. http://192.168.1.100:5000/)')
    parser.add_argument('--token', type=str, help='API token to use for authentication')
    parser.add_argument('--port', type=int, default=5000, help='Port number for local VM testing')
    parser.add_argument('--timeout', type=int, default=10, help='Request timeout in seconds')
    
    args = parser.parse_args()
    
    print("=" * 60)
    print(f"🌐 Python API Test - {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print("=" * 60)
    
    # Determine which URL to use
    base_url = None
    if args.url:
        base_url = args.url
        if not base_url.endswith('/'):
            base_url += '/'
    elif args.vm:
        local_ip = get_local_ip()
        base_url = f"http://{local_ip}:{args.port}/"
        print(f"Testing VM at local IP: {base_url}")
    else:  # Default to public IP test
        base_url = "http://24.59.50.128:9002/"
        print(f"Testing public endpoint: {base_url}")
    
    # Set URLs
    health_url = f"{base_url}api/health"
    api_url = f"{base_url}api/process"
    
    # Use provided token if specified
    token = args.token if args.token else TOKEN
    
    print(f"API URL: {api_url}")
    print(f"Health URL: {health_url}")
    
    # First test the health endpoint
    health_status = test_health(health_url, args.timeout)
    
    # Only test the process endpoint if health check passed
    if health_status:
        process_status = test_process_endpoint(api_url, token, args.timeout)
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