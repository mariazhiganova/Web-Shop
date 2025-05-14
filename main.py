from http.server import HTTPServer, BaseHTTPRequestHandler
import mimetypes


class CiteHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        # Обработка статических файлов
        if self.path.startswith('/static/'):
            self.serve_static_file()
        else:
            self.serve_html_file()

    def serve_static_file(self):
        try:
            file_path = self.path[1:]  # убираем первый слэш

            # Определяем MIME-тип
            mime_type, _ = mimetypes.guess_type(file_path)
            if not mime_type:
                mime_type = 'application/octet-stream'

            with open(file_path, 'rb') as f:
                content = f.read()

            self.send_response(200)
            self.send_header('Content-type', mime_type)
            self.end_headers()
            self.wfile.write(content)

        except FileNotFoundError:
            self.send_error(404, "File not found")

    def serve_html_file(self):
        # Сопоставление URL с файлами
        routes = {
            '/': 'html/main.html',
            '/main': 'html/main.html',
            '/categories': 'html/categories.html',
            '/orders': 'html/orders.html',
            '/contacts': 'html/contacts.html'
        }

        filename = routes.get(self.path)

        if filename:
            try:
                with open(filename, 'r', encoding='utf-8') as f:
                    content = f.read()
                self.send_response(200)
                self.send_header('Content-type', 'text/html; charset=utf-8')
                self.end_headers()
                self.wfile.write(content.encode('utf-8'))
            except FileNotFoundError:
                self.send_error(404, f"Page {filename} not found")
        else:
            self.send_error(404, "Page not found")

    def do_POST(self):
        content_length = int(self.headers['Content-Length'])
        body = self.rfile.read(content_length)
        print(body.decode('utf-8'))
        self.send_response(200)
        self.end_headers()


def run(server_class=HTTPServer, handler_class=CiteHandler):
    server_address = ('localhost', 8010)
    httpd = server_class(server_address, handler_class)
    print('Сервер запущен на http://localhost:8010')
    print('Доступные страницы:')
    print(' - http://localhost:8010/ (главная)')
    print(' - http://localhost:8010/categories')
    print(' - http://localhost:8010/orders')
    print(' - http://localhost:8010/contacts')
    httpd.serve_forever()


if __name__ == "__main__":
    # Инициализация MIME-типов
    mimetypes.add_type('text/css', '.css')
    mimetypes.add_type('application/javascript', '.js')
    mimetypes.add_type('image/jpeg', '.jpg')
    mimetypes.add_type('image/png', '.png')

    try:
        run()

    except KeyboardInterrupt:
        pass
