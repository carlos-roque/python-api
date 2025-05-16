from flask import Flask, request, jsonify
import os
import logging
from datetime import datetime

app = Flask(__name__)

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Predefined bearer token
VALID_TOKEN = os.environ.get('API_TOKEN', 'carlos89-api-token')

@app.route('/api/process', methods=['GET'])
def process_request():
    # Check authorization
    auth_header = request.headers.get('Authorization')
    if not auth_header or not auth_header.startswith('Bearer '):
        return jsonify({'error': 'Missing or invalid authorization header'}), 401
    
    token = auth_header.split(' ')[1]
    if token != VALID_TOKEN:
        return jsonify({'error': 'Invalid token'}), 401
    
    # Extract up to 10 optional parameters
    param1 = request.args.get('param1')
    param2 = request.args.get('param2')
    param3 = request.args.get('param3')
    param4 = request.args.get('param4')
    param5 = request.args.get('param5')
    param6 = request.args.get('param6')
    param7 = request.args.get('param7')
    param8 = request.args.get('param8')
    param9 = request.args.get('param9')
    param10 = request.args.get('param10')
    
    # Log received parameters for debugging
    logger.info(f'Received parameters: {request.args}')
    
    # Process the request (example processing)
    # In a real application, you would implement your business logic here
    
    # Return a response with 5 parameters
    response = {
        'status': 'success',
        'message': 'Request processed successfully',
        'received_params_count': len(request.args),
        'processed_data': f'Processed data for {param1 if param1 else "unknown"}',
        'timestamp': datetime.now().isoformat()
    }
    
    return jsonify(response)

@app.route('/api/health', methods=['GET'])
def health_check():
    return jsonify({
        'status': 'healthy',
        'version': '1.0.0',
        'timestamp': datetime.now().isoformat(),
        'uptime': 'Service is up and running',
        'environment': os.environ.get('ENVIRONMENT', 'production')
    })

if __name__ == '__main__':
    # Get port from environment variable or use 5000 as default
    port = int(os.environ.get('PORT', 5000))
    # Run the Flask application
    app.run(host='0.0.0.0', port=port, debug=os.environ.get('DEBUG', 'False').lower() == 'true') 