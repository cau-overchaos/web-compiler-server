from config import flask_config
from provider import util
import os
import subprocess


def code_compile(config_data):
    result = {}
    language_version = config_data['language_version']

    try:
        script_file = os.path.join(
            flask_config.Config.ROOT_PATH, 'scripts/compile.sh')  # 실행할 스크립트 파일의 경로

        # arguments를 전달
        additional_args = [flask_config.Config.CODE_FOLDER,
                           language_version,
                           config_data['code_file_name'],
                           'main',
                           ]

        # 쉘 명령 실행하면서 결과를 파일로 저장
        with open(os.path.join(flask_config.Config.RESULTS_FOLDER, 'stdout.txt'), 'w') as output_file, \
                open(os.path.join(flask_config.Config.RESULTS_FOLDER, 'stderr.txt'), 'w') as stderr_file:
            # 스크립트와 추가 arguments를 함께 전달
            command = ['sh', script_file] + additional_args
            process = subprocess.Popen(
                command, stdout=output_file, stderr=stderr_file, universal_newlines=True)
            _, stderr = process.communicate()

        exit_code = int(util.read_specific_line(os.path.join(
            flask_config.Config.RESULTS_FOLDER, 'stdout.txt'), 3)[12:])

        if exit_code == 0:
            result['Success'] = 'Compile success'
        else:
            result['Error'] = [
                {'Compile error': f'exit code : {exit_code}'},
                {'Compile error': f'error code : {process.returncode}'}]
    except Exception as e:
        result['Error'] = 'Exception : ' + str(e)
    return result
