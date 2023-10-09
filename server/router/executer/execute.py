from flask import request, Blueprint
from config import flask_config
from provider import util, json_util, compile_code, error_msg
from provider.executer import sandbox_execute
import os

execute = Blueprint('execute', __name__)


@execute.route('/executer', methods=['POST'])
def execute_route():
    # json 파일 받기
    json_file = request.get_json()

    # 응답 없으면 에러
    if not json_file:
        return error_msg.error_message('Error', 'No files were uploaded.', '', 400)

    # json 파일 파싱
    json_data_dict = json_util.save_json(json_file)

    # 언어 일치 여부 검사
    language_version_error = util.check_language_version(
        json_data_dict['language'])
    if language_version_error != 0:
        util.clean_dir(flask_config.Config.CODE_FOLDER)
        util.clean_dir(flask_config.Config.RESULTS_FOLDER)
        return error_msg.error_message('Error', 'Language did not exist.', '', language_version_error)

    # sandbox로 compile
    if not flask_config.Config.executable_dictionary[json_data_dict['language']]:
        result = compile_code.code_compile(json_data_dict)
        print(result)

        # 컴파일 실패
        if 'Error' in result:
            return error_msg.error_message('Fail', 'Compile fail.', result, 400)

    # sanbox로 execute
    result = sandbox_execute.execute_code(json_data_dict)
    print(result)

    # 실행 실패
    if 'Error' in result:
        return error_msg.error_message('Fail', 'Execute fail.', result, 400)

    # 결과 전송
    return sandbox_execute.return_result(json_data_dict)
