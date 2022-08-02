import os
import re
import time

import pytest

import exec_cmd


def remove(dirname: str):
    files_output = os.listdir(os.path.abspath(dirname))
    if files_output is not None:
        for file in files_output:
            os.remove(os.path.abspath(os.path.join(dirname, file)))


@pytest.fixture()
def init():
    # проверка наличия директорий
    requests_dirs = ['input', 'output', 'log']
    dir_content = os.listdir(os.curdir)
    file_dic = dict()
    for file in dir_content:
        for exp in requests_dirs:
            if re.fullmatch(exp, file):
                if file_dic.get(file):
                    file_dic[file] += 1
                else:
                    file_dic[file] = 1
    for dir in requests_dirs:
        if not file_dic.get(dir):
            os.mkdir(dir)
    # очистка всех файлов в директориях
    for dir in requests_dirs:
        remove(os.path.abspath(dir))
    yield


@pytest.mark.skip()
def test_exec_cmd():
    pass


def test_simple_log(init):
    log_file_name = 'log/log_file_name.txt'
    log_file = exec_cmd.LogFile(cmd='ls', log_file=os.path.abspath(log_file_name))
    list_dir_log = os.listdir('log')
    for file in list_dir_log:
        if file == os.path.basename(log_file_name):
            assert file == os.path.basename(log_file_name)
            break
    else:
        assert '' == log_file_name
    for i in range(1, 11):
        log_file.write2log('\n' + str(i) + ' st message')
    log_file = open(log_file_name, 'r')
    print(log_file.read())


def test_create_log_file():
    log_dir = 'log'
    log_file = exec_cmd.LogFile(cmd='ls', log_file=os.path.abspath(log_dir))
    list_dir_log = os.listdir(log_dir)
    date = time.strftime('%d_%m_%Y')
    log_file_name = date + '.log'
    for file in list_dir_log:
        if file == log_file_name:
            assert file == log_file_name
            break
    else:
        assert '' == log_file_name
    for i in range(1, 11):
        log_file.write2log('\n' + str(i) + ' st message')
    log_file.close()
    log_file = open(os.path.join(log_dir, log_file_name), 'r')
    print(log_file.read())


def test_add_data2exist_log():
    log_dir = 'log'
    cmd = 'cd'
    date = time.strftime('%d_%m_%Y')
    time_date = time.strftime("\n\tDate: %Y-%m-%d \tTime: %H:%M:%S")
    log_file_name = date + '.log'
    add_message = f'\n\n------------------\nadding message'
    full_add_message = f'\n-----------------------------------------------------------\nLogging command \"{cmd}\"{time_date} \n-----------------------------------------------------------\n' + add_message
    exp_val = open(os.path.join(log_dir, log_file_name), 'r').read() + full_add_message
    print(exp_val)
    log_file = exec_cmd.LogFile(cmd=cmd, log_file=os.path.abspath(log_dir))
    log_file.write2log(add_message)
    log_file.close()
    log_file = open(os.path.join(log_dir, log_file_name), 'r')
    assert log_file.read() == exp_val

def test_error_create_log():
    log_dir='/home/fake_log_dir/fake_log_name.log'
    cmd = 'df -h'
    log_file = exec_cmd.LogFile(cmd=cmd, log_file=os.path.abspath(log_dir))


@pytest.mark.skip()
def test_add_text2log(test_simple_log):
    pass


@pytest.mark.skip()
def test_test(init):
    assert 42 == 42


if __name__ == '__main__':
    pass
