from flask import jsonify


def error_message(status, message, error_data, error_code):
    return jsonify({
        'status': status,
        'message': message,
        'data': {
            message: error_data
        }
    }), error_code
