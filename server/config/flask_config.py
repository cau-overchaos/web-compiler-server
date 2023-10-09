import os
from dotenv import load_dotenv

load_dotenv(verbose=True)


class Config(object):
    ENV = os.getenv('ENV')
    HOST = os.getenv('HOST')
    PORT = os.getenv('PORT')
    ROOT_PATH = os.getcwd()
    CODE_FOLDER = os.path.join(ROOT_PATH, os.getenv('CODE_FOLDER'))
    RESULTS_FOLDER = os.path.join(ROOT_PATH, os.getenv('RESULTS_FOLDER'))

    # 파일 업로드를 위한 임시 디렉토리 설정
    if not os.path.exists(CODE_FOLDER):
        os.makedirs(CODE_FOLDER)

    # 결과 파일들이 저장될 디렉토리 설정
    if not os.path.exists(RESULTS_FOLDER):
        os.makedirs(RESULTS_FOLDER)

    executable_dictionary = {'c': False, 'cpp': False, 'python': True, }
    language_dictionary = {
        'c': ['c99', 'c11', 'c17'],
        'cpp': ['cpp98', 'cpp11', 'cpp14', 'cpp17', 'cpp20', 'cpp2a'],
        'python': ['python3'],
    }
    language_extension_dictionary = {
        'c': 'c',
        'cpp': 'cpp',
        'python': 'py'
    }
    CSRF_ENABLED = True


class devConfig(Config):
    DEBUG = True


class prodConfig(Config):
    DEBUG = False
