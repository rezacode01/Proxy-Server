# from config import PORT, MAX_CONNECTION, MAX_BUFFER_SIZE, PRIVACY
import config
import logger
import socket
import sys
import urllib.request
import signal
import time
import parser

class ProxyServer:
    def run(self):
        try:
            self.setup_signal_handler()

            # my_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            my_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

            logger.log('Proxy launched')
            logger.log('Creating server...')

            my_socket.bind(('127.0.0.1', config.PORT))
            logger.log('Binding socket to port ' + str(config.PORT) + '...')

            my_socket.listen(config.MAX_CONNECTION)
            logger.log('Listening for incoming requests...\n')

        except Exception as e:
            logger.log(e)
            sys.exit(2)

        while True:
            try:
                conn, addr = my_socket.accept()
                data = conn.recv(config.MAX_BUFFER_SIZE)
                logger.log('Accept a request from client!')
                logger.log('Client sent request to proxy with headers:')
                logger.log('Connect to from ' + str(addr) + '\n')
                logger.log_header(data)

                try:
                    if self.check_restriction(data):
                        req_type, path = parser.get_request_path(data)
                        resp = self.send_request_to_host(path)
                        conn.sendto(resp, addr)

                except IndexError:
                    conn.sendto("".encode("ASCII"), addr)

                # resp_data = "reza"
                # my_socket.send(resp_data.encode("ASCII"))
            except KeyboardInterrupt as e:
                my_socket.close()
                sys.exit(0)

            except Exception as e:
                logger.log(e)
                my_socket.close()
                sys.exit(2)

    def check_restriction(self, data):
        host = parser.get_host(data)
        # host = 'acm.ut.ac.ir'
        restrict_type, delay = self.get_restriction_config(host)
        if restrict_type == config.BLOCK:
            logger.log('Requested host(' + host + ')  is BLOCKED')
            return False
        elif restrict_type == config.SLOW:
            logger.log('Requested host(' + host + ') has SLOW restriction for ' + str(delay) + 'ms')
            time.sleep(delay / 1000)    # delay is in ms
            return True
        else:
            return True

    def get_restriction_config(self, host):
        rstr_enable = config.RESTRICTION['enable']
        targets = config.RESTRICTION['targets']

        if rstr_enable:
            for t in targets:
                if t['URL'] == host:
                    if t['restrictType'] == config.BLOCK:
                        return t['restrictType'], 0
                    elif t['restrictType'] == config.SLOW:
                        return t['restrictType'], t['delay']
        return None, 0

    def get_user_agent(self):
        hide_user_agent = config.PRIVACY['enable']
        if hide_user_agent:
            return config.PRIVACY['userAgent']
        return ""

    def send_request_to_host(self, path):
        req = urllib.request.Request(path)
        req.add_header('user-agent', self.get_user_agent())
        # req.add_header()
        # logger.log_header(req.headers)
        # print(req.headers)
        with urllib.request.urlopen(req) as response:
            the_page = response.read()
            logger.log_header(str(response.info()))
        return the_page

    def setup_signal_handler(self):
        signal.signal(signal.SIGINT, self.signal_handler)  # Handle Ctrl-C
        if hasattr(signal, "SIGBREAK"):
            # Handle Ctrl-Break e.g. under Windows
            signal.signal(signal.SIGBREAK, self.signal_handler)

    def signal_handler(self, signnum, frame):
        sys.exit(0)



server = ProxyServer()
server.run()
# server.send_request_to_host()
