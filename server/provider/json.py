from config import flask_config
import json


def read_json(json_file_path):
    try:
        # JSON 파일 열기
        with open(json_file_path, 'r') as json_file:
            # JSON 데이터 파싱
            json_data = json.load(json_file)

            # JSON 데이터에서 필요한 값 추출
            is_judge = json_data.get('is_judge', 0)     # 0이면 judge가 아님
            language = json_data.get('language', '')
            version = json_data.get('version', '')
            code_file_name = json_data.get('code_file_name', '')
            time_limit = json_data.get('time_limit', 0)
            memory_limit = json_data.get('memory_limit', 0)

            # 기본 1sec
            if time_limit == 0:
                time_limit = 10
            # 기본 512MB
            if memory_limit == 0:
                memory_limit = 536870912

            dict = {'is_judge': is_judge,
                    'language': language,
                    'version': version,
                    'code_file_name': code_file_name,
                    'time_limit': time_limit,
                    'memory_limit': memory_limit
                    }

            return dict

    except FileNotFoundError:
        print(f'File not found: {json_file_path}')
    except json.JSONDecodeError as e:
        print(f'JSON parsing error: {e}')
    except Exception as e:
        print(f'Error occurred: {e}')


def check_language_version(language, version):
    if language not in flask_config.Config.language_dictionary:
        return 401
    if version not in flask_config.Config.language_dictionary[language]:
        return 402
    return 0
