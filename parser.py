def get_request_path(req):
    lines = req.splitlines()
    first_line = str(lines[0])
    elems = first_line.split()
    return elems[0], elems[1]


def get_host(req):
    lines = req.splitlines()
    host = ""
    for l in lines:
        str_line = l.decode('utf8')
        elements = str_line.split()
        # print(elements)
        if elements[0] == 'Host:':
            host = elements[1]
            break
    return host
