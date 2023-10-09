from config import flask_config
from provider import util
import json
import os


def save_json(json_file):
    try:
        # JSON 데이터에서 필요한 값 추출
        language_version = json_file['language']
        time_limit = json_file['time_limit'] if 'time_limit' in json_file else 10
        memory_limit = json_file['memory_limit'] if 'memory_limit' in json_file else 536870912
        code = json_file['code']
        input_list = json_file['input']
        answer_list = json_file['answer'] if 'answer' in json_file else []

        # 코드 확장자 확인
        language = ''
        for lang, lang_list in flask_config.Config.language_dictionary.items():
            if language_version in lang_list:
                language = lang

        # 코드 저장
        extension_name = flask_config.Config.language_extension_dictionary[language]
        util.write_file(os.path.join(
            flask_config.Config.CODE_FOLDER, 'main.' + extension_name), code)

        # input 저장
        for idx, file in enumerate(input_list):
            util.write_file(os.path.join(
                flask_config.Config.CODE_FOLDER, f'input{idx}.txt'), file)

        # answer 저장
        for idx, file in enumerate(answer_list):
            util.write_file(os.path.join(
                flask_config.Config.CODE_FOLDER, f'answer{idx}.txt'), file)

        return {
            'language': language,
            'language_version': language_version,
            'time_limit': time_limit,
            'memory_limit': memory_limit,
            'code_file_name': 'main.' + extension_name,
            'input_num': len(input_list),
            'answer_num': len(answer_list)
        }

    except json.JSONDecodeError as e:
        print(f'JSON parsing error: {e}')
    except Exception as e:
        print(f'Error occurred: {e}')
