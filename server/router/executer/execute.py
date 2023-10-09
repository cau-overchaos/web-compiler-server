from flask import jsonify, request, Blueprint, send_file
from config import flask_config
from provider import util, json_util
from provider.executer import sandbox_execute
import os
import json

execute = Blueprint('execute', __name__)


@execute.route('/executer', methods=['POST'])
def execute_route():
    # json 파일 받기
    json_file = request.get_json()

    # 응답 없으면 에러
    if not json_file:
        return jsonify({
            'status': 'Error',
            'message': 'No files were uploaded.',
        }), 400

    # json 파일 파싱
    json_data_dict = json_util.save_json(json_file)

    language_version_error = util.check_language_version(
        json_data_dict['language'])
    if language_version_error != 0:
        util.clean_dir(flask_config.Config.CODE_FOLDER)
        util.clean_dir(flask_config.Config.RESULTS_FOLDER)
        return jsonify({
            'status': 'Error',
            'message': 'language did not exist.',
        }), language_version_error

    # sandbox로 execute
    result = sandbox_execute.run_script(json_data_dict)
    print(result)

    # 컴파일 실패
    if 'Error' in result[0]:
        return jsonify({
            'status': 'Fail',
            'message': 'Compile fail.',
            'data': {
                'Compile fail': result[0]
            }
        }), 400

    # 실행 실패
    if 'Error' in result[1]:
        return jsonify({
            'status': 'Fail',
            'message': 'Execute fail.',
            'data': {
                'Execute fail': result[1]
            }
        }), 400

    # 출력 결과
    output_data = []
    usage_list = []
    for idx in range(json_data_dict['input_num']):
        output_data.append(util.read_file(os.path.join(
            flask_config.Config.RESULTS_FOLDER, f'output{idx}.txt')))
        usage = util.read_specific_line(os.path.join(
            flask_config.Config.RESULTS_FOLDER, f'execute{idx}.txt'), 3)[21:-3]
        usage_dict = {}
        for dct in usage.split(','):
            key_item = dct.split(':')
            usage_dict[key_item[0].strip()] = key_item[1].strip()
        usage_list.append(usage_dict)

    # 결과 전송
    return jsonify({
        'status': 'Success',
        'message': 'Compile and Execute Success',
        'data': {
            'output_num': json_data_dict['input_num'],
            'output': output_data,
            'resource': usage_list
        }
    }), 200
