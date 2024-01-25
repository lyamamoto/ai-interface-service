from flask import Blueprint, Response, request
from flask_cors import CORS, cross_origin
import json

from app import AuthException
from app.service import AssistantService, CoreService

assistant_controller = Blueprint('assistant', __name__)
cors = CORS(assistant_controller)

# Services
core_service = CoreService()
assistant_service = AssistantService()

@assistant_controller.route('/assistant/new', methods=['POST'])
@cross_origin()
def create_service_context():
    try:
        auth_token = request.headers.get("Authorization")
        customer_id = core_service.map_auth_token_to_customer_id(auth_token)

        data = request.json
        assistant = assistant_service.create_assistant(customer_id, data["name"], data["context"])
        response_data = assistant.id
        return Response(json.dumps(response_data), status=200, mimetype='application/json')

    except AuthException:
        return Response("", status=401)

    except Exception as e:
        return Response(str(e), status=500)

@assistant_controller.route('/thread/new', methods=['POST'])
@cross_origin()
def start_chat():
    try:
        auth_token = request.headers.get("Authorization")
        customer_id = core_service.map_auth_token_to_customer_id(auth_token)

        data = request.json
        thread = assistant_service.start_thread(data["assistant_id"], customer_id)
        response_data = thread.id
        return Response(json.dumps(response_data), status=200, mimetype='application/json')

    except AuthException:
        return Response("", status=401)

    except Exception as e:
        return Response(str(e), status=500)

@assistant_controller.route('/customer/new', methods=['POST'])
@cross_origin()
def register_new_customer():
    try:
        data = request.json
        customer = core_service.register_new_customer(data['name'])
        auth_token = core_service.generate_auth_token(customer.id)
        response_data = {'customer_id': customer.id, 'auth_token': auth_token}
        return Response(json.dumps(response_data), status=200, mimetype='application/json')

    except Exception:
        return Response("", status=400)

@assistant_controller.route('/assistant', methods=['GET'])
@cross_origin()
def get_all_assistants():
    try:
        auth_token = request.headers.get("Authorization")
        customer_id = core_service.map_auth_token_to_customer_id(auth_token)

        assistants = assistant_service.get_all_assistants_by_customer(customer_id)
        response_data = [assistant.id for assistant in assistants]
        return Response(json.dumps(response_data), status=200, mimetype='application/json')

    except AuthException:
        return Response("", status=401)

    except Exception as e:
        return Response(str(e), status=500)

@assistant_controller.route('/assistant/name/<name>', methods=['GET'])
@cross_origin()
def get_assistant_by_name(name):
    try:
        auth_token = request.headers.get("Authorization")
        customer_id = core_service.map_auth_token_to_customer_id(auth_token)

        assistant = assistant_service.get_assistant_by_name(customer_id, name)
        if assistant:
            response_data = assistant.id
            return Response(json.dumps(response_data), status=200, mimetype='application/json')
        else:
            return Response("", status=404)

    except AuthException:
        return Response("", status=401)

    except Exception:
        return Response("", status=500)