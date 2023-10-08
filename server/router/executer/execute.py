from flask import jsonify, request, Blueprint, send_file
from config import flask_config
from provider import util, json
from provider.executer import sandbox_execute
import os
import zipfile

execute = Blueprint('execute', __name__)


@execute.route('/executer', methods=['POST'])
def execute_route():
    # 이전에 RESULTS_FOLDER에 있는 데이터를 전부 삭제
    util.clean_dir(flask_config.Config.RESULTS_FOLDER)

    code_files = request.files.get('file')

    if not code_files:
        return jsonify({'error': 'No files were uploaded.'}), 400

    # 업로드된 압축 파일 저장
    zip_file_path = os.path.join(
        flask_config.Config.CODE_FOLDER, 'files.zip')
    code_files.save(zip_file_path)

    # 압축 파일 해제
    with zipfile.ZipFile(zip_file_path, 'r') as zipf:
        zipf.extractall(flask_config.Config.CODE_FOLDER)

    # json 파일 파싱
    config_data = json.read_json(
        os.path.join(flask_config.Config.CODE_FOLDER, 'config.json'))

    language_version_error = json.check_language_version(
        config_data['language'], config_data['version'])
    if language_version_error != 0:
        util.clean_dir(flask_config.Config.CODE_FOLDER)
        util.clean_dir(flask_config.Config.RESULTS_FOLDER)
        return jsonify({'error': 'language did not exist.' if language_version_error == 401 else 'language version did not exist.'}), language_version_error

    # sandbox로 execute
    result = sandbox_execute.run_script(config_data)
    print(result)

    # 결과 파일들을 압축
    util.zip_results(flask_config.Config.RESULTS_FOLDER)

    # 받은 파일 삭제
    util.clean_dir(flask_config.Config.CODE_FOLDER)

    # 결과 전송
    return send_file(os.path.join(flask_config.Config.RESULTS_FOLDER, 'results.zip'), as_attachment=True)
