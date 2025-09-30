import subprocess 

def test1():
    """Check when print is inside the docstring
    """
    res = subprocess.run(['python3', "../default/print_check/check_prints.py", "./data/check_prints/print_in_docstring.py"], capture_output=True, text=True)
    log_output = res.stderr.strip()
    print(log_output)
    assert log_output == ""
    
def test2():
    """Check when print is outside the docstring
    """
    res = subprocess.run(['python3', "../default/print_check/check_prints.py", "./data/check_prints/print_outside_docstring.py"], capture_output=True, text=True)
    log_output = res.stderr.strip()
    assert log_output == "WARNING:__main__:Found some print statements in file './data/check_prints/print_outside_docstring.py'"

def test3():
    """Check when print is outside and inside the docstring
    """
    res = subprocess.run(['python3', "../default/print_check/check_prints.py", "./data/check_prints/print_in_both.py"], capture_output=True, text=True)
    log_output = res.stderr.strip()
    assert log_output == "WARNING:__main__:Found some print statements in file './data/check_prints/print_in_both.py'"

