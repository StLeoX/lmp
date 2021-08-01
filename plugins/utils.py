def valid_c_program(program: str) -> bool:
    return len(program) != 0


# b = BPF(src_file="*.c")
def read_c_program(filepath):
    ret = ''
    with open(filepath, encoding='utf-8', mode='r') as f:
        ret = f.read()
    # 验证格式
    assert valid_c_program(ret)
    return ret
