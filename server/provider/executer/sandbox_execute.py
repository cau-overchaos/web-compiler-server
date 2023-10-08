from config import flask_config
from provider import util
import os
import subprocess


def run_script(config_data):
    result = []
    language = config_data['language']
    language_version = config_data['language_version']
    executable = flask_config.Config.executable_dictionary[language]
    is_conmpiled = True
    if not executable:
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
                result.append({f'Success': 'Compile success'})
            else:
                result.append({f'Error : Compile error': [
                              f'exit code : {exit_code}', f'error code : {process.returncode} ']})
                is_conmpiled = False
        except Exception as e:
            result.append(f'Error: Exception')
            result.append(str(e))
            is_conmpiled = False
    if is_conmpiled:
        execute_result = {}
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
                    execute_result[f'Success{idx}'] = 'Execute success'
                else:
                    execute_result['Error'] = [
                        {f'Execute error at input{idx}.txt': f'exit code : {exit_code}'},
                        {f'Execute error at input{idx}.txt': f'error code : {process.returncode}'}]
                    break
            except Exception as e:
                execute_result['Error'] = 'Exception : '+str(e)
    result.append(execute_result)
    return result
