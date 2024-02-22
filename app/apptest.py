from flask import request, jsonify

# Inside your route function
data = request.get_json()
if data is None:
    return jsonify({'error': 'Failed to decode JSON object'}), 400