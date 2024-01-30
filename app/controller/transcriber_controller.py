from flask import Blueprint, Response, request
from flask_cors import CORS, cross_origin
import json

from app.exceptions import AuthException
from app.service import AssemblyAITranscriberService, OpenAITranscriberService, CoreService

transcriber_controller = Blueprint('transcriber', __name__)
cors = CORS(transcriber_controller)

# Services
core_service = CoreService()
assemblyai_transcriber_service = AssemblyAITranscriberService()
openai_transcriber_service = OpenAITranscriberService()

@transcriber_controller.route('/transcription/<transcription_id>', methods=['GET'])
@cross_origin()
def get_transcription(transcription_id: str):
    try:
        auth_token = request.headers.get("Authorization")
        customer_id = core_service.map_auth_token_to_customer_id(auth_token)

        source_transcription = assemblyai_transcriber_service.get_transcription(transcription_id)
        response_data = {"id": source_transcription.id, "text": source_transcription.text}
        return Response(json.dumps(response_data), status=200, mimetype='application/json')

    except AuthException:
        return Response("", status=401)

    except Exception as e:
        return Response(str(e), status=500)

@transcriber_controller.route('/', methods=['POST'])
@cross_origin()
def transcribe():
    try:
        auth_token = request.headers.get("Authorization")
        customer_id = core_service.map_auth_token_to_customer_id(auth_token)

        data = request.json
        if not "source" in data:
            data["source"] = "assemblyai"
        if data["source"] == "openai":
            transcription = openai_transcriber_service.transcribe(customer_id, data["file_path"])
        else:
            transcription = assemblyai_transcriber_service.transcribe(customer_id, data["file_path"])
        response_data = transcription.id
        return Response(json.dumps(response_data), status=200, mimetype='application/json')

    except AuthException:
        return Response("", status=401)

    except Exception as e:
        return Response(str(e), status=500)
    
@transcriber_controller.route('/transcription/<transcription_id>/questions', methods=['POST'])
@cross_origin()
def questions(transcription_id: str):
    try:
        auth_token = request.headers.get("Authorization")
        customer_id = core_service.map_auth_token_to_customer_id(auth_token)

        data = request.json
        if not "source" in data:
            data["source"] = "assemblyai"
        if data["source"] == "openai":
            qa = assemblyai_transcriber_service.request_interpretation_about_transcription(transcription_id, data["questions"])
        else:
            qa = assemblyai_transcriber_service.request_interpretation_about_transcription(transcription_id, data["questions"])
        response_data = qa
        return Response(json.dumps(response_data), status=200, mimetype='application/json')

    except AuthException:
        return Response("", status=401)

    except Exception as e:
        return Response(str(e), status=500)