import os
import zipfile


def clean_dir(folder_path):
    for file_name in os.listdir(folder_path):
        file_path = os.path.join(folder_path, file_name)
        if os.path.isfile(file_path):
            os.remove(file_path)


def zip_results(folder_path):
    # 결과 파일들을 압축하여 results.zip 파일 생성
    with zipfile.ZipFile(os.path.join(folder_path, 'results.zip'), 'w', zipfile.ZIP_DEFLATED) as zipf:
        for root, _, files in os.walk(folder_path):
            for file in files:
                file_path = os.path.join(root, file)
                arcname = os.path.relpath(file_path, folder_path)
                zipf.write(file_path, arcname=arcname)


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
