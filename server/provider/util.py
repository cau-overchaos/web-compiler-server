from config import flask_config
import os


def clean_dir(folder_path):
    for file_name in os.listdir(folder_path):
        file_path = os.path.join(folder_path, file_name)
        if os.path.isfile(file_path):
            os.remove(file_path)


def write_file(path, data):
    # path에 파일을 저장합니다.
    try:
        with open(path, 'w') as file:
            file.write(data)
        print(f'File saved successfully: {path}')
    except Exception as e:
        print(f'Failed to save file: {path}')
        print(f'Error message: {str(e)}')


def read_file(path):
    try:
        with open(path, 'r') as source_file:
            source_code = source_file.read()
        return source_code
    except Exception as e:
        print(f'Failed to read the file: {path}')
        print(f'Error message: {str(e)}')
        return None


def read_specific_line(file_path, line_number):
    try:
        with open(file_path, 'r') as file:
            lines = file.readlines()
            # 주의: line_number는 1부터 시작합니다.
            if 1 <= line_number <= len(lines):
                specific_line = lines[line_number - 1].strip()  # 줄 바꿈 문자 제거
                return specific_line
            else:
                return "The line number is out of the file range."
    except FileNotFoundError:
        return "File not found."


def check_language_version(language):
    if language in flask_config.Config.language_dictionary:
        return 0
    return 400
