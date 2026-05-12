import ctypes
import json
import os
from http.server import BaseHTTPRequestHandler, HTTPServer
from urllib.parse import urlparse, parse_qs

lib_path = os.path.abspath('./svinocheck.so')
c_lib = ctypes.CDLL(lib_path)

c_lib.init_db.argtypes = [ctypes.c_char_p]
c_lib.init_db.restype = ctypes.c_int

c_lib.close_db.argtypes = []
c_lib.close_db.restype = None

c_lib.get_country_by_ip.argtypes = [ctypes.c_char_p, ctypes.c_char_p, ctypes.c_int]
c_lib.get_country_by_ip.restype = ctypes.c_int

DB_FILE = b"dbip.mmdb"
if c_lib.init_db(DB_FILE) == 0:
    print("Ошибка: Не удалось загрузить базу данных!")
    exit(1)

class IPApiHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        parsed_path = urlparse(self.path)
        query_params = parse_qs(parsed_path.query)

        target_ip = query_params.get('ip', [self.client_address[0]])[0]
        
        response_data = {"ip": target_ip}

        buffer_size = 128
        output_buffer = ctypes.create_string_buffer(buffer_size)

        is_found = c_lib.get_country_by_ip(target_ip.encode('utf-8'), output_buffer, buffer_size)

        if is_found:
            response_data["country"] = output_buffer.value.decode('utf-8')
        else:
            response_data["error"] = "IP или страна не найдены"

        self.send_response(200)
        self.send_header('Content-type', 'application/json; charset=utf-8')
        self.send_header('Access-Control-Allow-Origin', '*')
        self.end_headers()
        self.wfile.write(json.dumps(response_data, ensure_ascii=False).encode('utf-8'))

def run_server(port=6789):
    server_address = ('', port)
    httpd = HTTPServer(server_address, IPApiHandler)
    try:
        httpd.serve_forever()
    except KeyboardInterrupt:
        print("\nОстановка сервера...")
    finally:
        c_lib.close_db()
        httpd.server_close()

if __name__ == '__main__':
    run_server()