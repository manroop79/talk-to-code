import subprocess 

def test_check_function_lens():
    '''Tests for check_function_lens
    '''
    res = subprocess.run(['python3', "../default/function_length_check/check_function_lens.py", "./data/check_function_len/func_30_line.py"], capture_output=True, text=True)
    log_output = res.stderr.strip()
    assert log_output == "INFO:__main__:Running with line limit of '40' lines"


    res = subprocess.run(['python3', "../default/function_length_check/check_function_lens.py", "./data/check_function_len/func_50_line.py"], capture_output=True, text=True)
    log_output = res.stderr.strip()
    assert log_output == "INFO:__main__:Running with line limit of '40' lines\nWARNING:__main__:Found function hello50 in file ./data/check_function_len/func_50_line.py with too many lines! (50)"

def test_check_function_lens__with_exclude():
    '''Tests for check_function_lens with --exclude argument
    '''
    res = subprocess.run(['python3', "../default/function_length_check/check_function_lens.py", "./data/check_function_len", '--exclude', 'hello50', 'hello60'], capture_output=True, text=True)
    log_output = res.stderr.strip()
    assert log_output == "INFO:__main__:Running with line limit of '40' lines"


    # will be error because we are only excluding hello60
    res = subprocess.run(['python3', "../default/function_length_check/check_function_lens.py", "./data/check_function_len", '--exclude', 'hello60'], capture_output=True, text=True)
    log_output = res.stderr.strip()
    assert log_output == "INFO:__main__:Running with line limit of '40' lines\nWARNING:__main__:Found function hello50 in file data/check_function_len/func_50_line.py with too many lines! (50)"


