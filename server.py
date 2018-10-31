from config import PORT, MAX_CONNECTION, MAX_BUFFER_SIZE
import logger
import socket
import sys
import urllib.request
import signal


class ProxyServer:
    def run(self):
        try:
            self.setup_signal_handler()

            # my_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            my_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

            logger.log('Proxy launched')
            logger.log('Creating server...')

            my_socket.bind(('127.0.0.1', PORT))
            logger.log('Binding socket to port ' + str(PORT) + '...')

            my_socket.listen(MAX_CONNECTION)
            logger.log('Listening for incoming requests...\n')

        except Exception as e:
            logger.log(e)
            sys.exit(2)

        while True:
            try:
                conn, addr = my_socket.accept()
                data = conn.recv(MAX_BUFFER_SIZE)
                logger.log('Accept a request from client!')
                logger.log('Client sent request to proxy with headers:')
                logger.log('Connect to from ' + str(addr) + '\n')
                logger.log_header(data)

                try:
                    req_type, path = self.get_request_path(data)
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

    def send_request_to_host(self, path):
        req = urllib.request.Request(path)
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

    def get_request_path(self, req):
        lines = req.splitlines()
        first_line = str(lines[0])
        elems = first_line.split()
        return elems[0], elems[1]


server = ProxyServer()
server.run()
# server.send_request_to_host()
