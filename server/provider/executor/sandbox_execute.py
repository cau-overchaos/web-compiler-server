from flask import jsonify
from config import flask_config
from provider import util
import os
import subprocess


def execute_code(config_data):
    result = {}
    language = config_data['language']
    executable = flask_config.Config.executable_dictionary[language]

    # input 수만큼 반복
    for idx in range(config_data['input_num']):
        try:
            script_file = os.path.join(
                flask_config.Config.ROOT_PATH, 'scripts/execute.sh')  # 실행할 스크립트 파일의 경로

            # arguments를 전달
            additional_args = [flask_config.Config.CODE_FOLDER,
                               flask_config.Config.RESULTS_FOLDER,
                               language,
                               str(config_data['memory_limit']),
                               str(config_data['time_limit']),
                               config_data['code_file_name'] if executable else 'main',
                               f'input{idx}.txt',
                               f'output{idx}.txt',
                               f'answer{idx}.txt',
                               ]

            # 쉘 명령 실행하면서 결과를 파일로 저장
            with open(os.path.join(flask_config.Config.RESULTS_FOLDER, f'execute{idx}.txt'), 'w') as output_file:
                # 스크립트와 추가 arguments를 함께 전달
                command = ['sh', script_file] + additional_args
                process = subprocess.Popen(
                    command, stdout=output_file, stderr=subprocess.PIPE, universal_newlines=True)
                _, stderr = process.communicate()

            exit_code = int(util.read_specific_line(os.path.join(
                flask_config.Config.RESULTS_FOLDER, f'execute{idx}.txt'), 4)[12:])

            if exit_code == 0:
                result[f'Success{idx}'] = 'Execute success'
            else:
                result['Error'] = [
                    {f'Execute error at input{idx}.txt': f'exit code : {exit_code}'},
                    {f'Execute error at input{idx}.txt': f'error code : {process.returncode}'}]
        except Exception as e:
            result['Error'] = 'Exception : ' + str(e)
    return result


def return_result(config_data):
    # 출력 결과
    output_list = []
    message = 'Compile and Execute Success'
    resultType = 'execute_success'
    for idx in range(config_data['input_num']):
        # 출력
        output_data = util.read_file(os.path.join(
            flask_config.Config.RESULTS_FOLDER, f'output{idx}.txt'))
        # 리소스
        usage = util.read_specific_line(os.path.join(
            flask_config.Config.RESULTS_FOLDER, f'execute{idx}.txt'), 3)[21:-3]
        # exit code
        exit_code = int(util.read_specific_line(os.path.join(
            flask_config.Config.RESULTS_FOLDER, f'execute{idx}.txt'), 4)[12:])
        usage_dict = {}
        # 리소스 기록
        for dct in usage.split(','):
            key_item = dct.split(':')
            usage_dict[key_item[0].strip()] = key_item[1].strip()
        usage_dict['exit_code'] = exit_code
        if exit_code == 0:
            usage_dict['output'] = output_data
            usage_dict['errorDescription'] = None
        else:
            message = 'Excute Fail'
            resultType = 'execute_fail'
            usage_dict['errorDescription'] = util.read_specific_line(os.path.join(
                flask_config.Config.RESULTS_FOLDER, f'execute{idx}.txt'), 5)[22:-2]
            usage_dict['output'] = None
        output_list.append(usage_dict)

    return jsonify({
        'status': 'success',
        'message': message,
        'data': {
            'resultType': resultType,
            'result': output_list[0]
        }
    }), 200
