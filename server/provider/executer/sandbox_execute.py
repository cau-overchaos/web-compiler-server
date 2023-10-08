from config import flask_config
from provider import util
import os
import subprocess


def run_script(config_data):
    result = []
    language_name = config_data['language']
    language_version = config_data['version']
    executable = flask_config.Config.executable_dictionary[language_name]
    is_conmpiled = True
    if not executable:
        try:
            script_file = os.path.join(
                flask_config.Config.ROOT_PATH, 'scripts/compile.sh')  # 실행할 스크립트 파일의 경로

            # arguments를 전달
            additional_args = [flask_config.Config.CODE_FOLDER,
                               language_name + language_version,
                               config_data['code_file_name'],
                               config_data['code_file_name'].split('.')[0],
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
                result.append(f'Success : Compile success')
            else:
                result.append(
                    f'Error : Compile error (exit code : {exit_code})')
                result.append(
                    f'Error : Compile error (error code : {process.returncode})')
                is_conmpiled = False
        except Exception as e:
            result.append(f'Error: Exception')
            result.append(str(e))
            is_conmpiled = False
    if is_conmpiled:
        try:
            script_file = os.path.join(
                flask_config.Config.ROOT_PATH, 'scripts/execute.sh')  # 실행할 스크립트 파일의 경로

            # arguments를 전달
            print(config_data['code_file_name'] if executable else config_data['code_file_name'].split('.')[
                0])
            additional_args = [flask_config.Config.CODE_FOLDER,
                               flask_config.Config.RESULTS_FOLDER,
                               language_name,
                               str(config_data['memory_limit']),
                               str(config_data['time_limit']),
                               config_data['code_file_name'] if executable else config_data['code_file_name'].split('.')[
                                   0],
                               'input.txt',
                               'output.txt',
                               'answer.txt',
                               ]

            # 쉘 명령 실행하면서 결과를 파일로 저장
            with open(os.path.join(flask_config.Config.RESULTS_FOLDER, 'execute.txt'), 'w') as output_file:
                # 스크립트와 추가 arguments를 함께 전달
                command = ['sh', script_file] + additional_args
                process = subprocess.Popen(
                    command, stdout=output_file, stderr=subprocess.PIPE, universal_newlines=True)
                _, stderr = process.communicate()

            exit_code = int(util.read_specific_line(os.path.join(
                flask_config.Config.RESULTS_FOLDER, 'execute.txt'), 4)[12:])

            if process.returncode == 0 and exit_code == 0:
                result.append(f'Success : Execute success')
            else:
                result.append(
                    f'Error : Compile error (exit code : {exit_code})')
                result.append(
                    f'Error : Compile error (error code : {process.returncode})')
        except Exception as e:
            result.append(f'Error: Exception')
            result.append(str(e))

    return result
