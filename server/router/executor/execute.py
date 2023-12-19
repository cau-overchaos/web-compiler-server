from flask import request, Blueprint
from config import flask_config
from provider import util, json_util, compile_code, error_msg
from provider.executor import sandbox_execute
import os

execute = Blueprint('execute', __name__)


@execute.route('/executor', methods=['POST'])
def execute_route():
    # json 파일 받기
    json_file = request.get_json()

    # 응답 없으면 에러
    if not json_file:
        return error_msg.error_message('error', 'No files were uploaded', 'null', 400)

    # 언어 일치 여부 검사
    language_version_error = util.check_language_version(
        json_file['language'])
    if language_version_error:
        util.clean_dir(flask_config.Config.CODE_FOLDER)
        util.clean_dir(flask_config.Config.RESULTS_FOLDER)
        return error_msg.error_message('error', 'Language did not exist', 'null', 400)

    # json 파일 파싱
    json_data_dict = json_util.save_json(json_file)

    # sandbox로 compile
    if not flask_config.Config.executable_dictionary[json_data_dict['language']]:
        result = compile_code.code_compile(json_data_dict)
        print(result)

        # 컴파일 실패
        if 'compile_fail' in result['resultType']:
            return error_msg.error_message('success', 'Compile fail', result, 200)

    # sanbox로 execute
    result = sandbox_execute.execute_code(json_data_dict)
    print(result)

    # 결과 전송
    return sandbox_execute.return_result(json_data_dict)
