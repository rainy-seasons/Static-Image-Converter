from http.server import BaseHTTPRequestHandler, HTTPServer
import os
import cgi
from PIL import Image
import subprocess

class RequestHandler(BaseHTTPRequestHandler):
    def _send_response(self, message):
        self.send_response(200)
        self.send_header('Content-type', 'text/html')
        self.end_headers()
        self.wfile.write(bytes(message, 'utf-8'))

    def do_GET(self):
        # Serve other static files (CSS, JS, etc.)
        if self.path.endswith('.css') or self.path.endswith('.js'):
            try:
                with open(self.path[1:], 'rb') as file:
                    self.send_response(200)
                    self.send_header('Content-type', 'text/css' if self.path.endswith('.css') else 'application/javascript')
                    self.end_headers()
                    self.wfile.write(file.read())
            except FileNotFoundError:
                self.send_response(404)
            return

        # Serve the HTML file for both '/' and '/convert'
        if self.path == '/' or self.path == '/convert':
            try:
                with open('index.html', 'r') as file:
                    self.send_response(200)
                    self.send_header('Content-type', 'text/html')
                    self.end_headers()
                    self.wfile.write(file.read().encode('utf-8'))
            except FileNotFoundError:
                self.send_response(404)
            return

        # Handle other cases with a 404 response
        self.send_response(404)
        self.end_headers()

    def do_POST(self):
        # Handle file upload and conversion
        if self.path == '/convert':
            form = cgi.FieldStorage(
                fp=self.rfile,
                headers=self.headers,
                environ={'REQUEST_METHOD': 'POST'}
            )

            # Get the uploaded file and selected file type
            file_item = form['image']
            file_type = form.getvalue('fileType')

            # Save the uploaded file
            original_image_path = os.path.join('images', file_item.filename)
            with open(original_image_path, 'wb') as file:
                file.write(file_item.file.read())

            # Convert the image using PIL
            with Image.open(original_image_path) as original_image:
                converted_image_path = os.path.join('converted_images', 'converted_image.' + file_type)
                if (file_type == "jpeg"):
                    original_image = original_image.convert('RGB')
                original_image.save(converted_image_path, format=file_type.upper())  # Convert to the selected file type

            with open(converted_image_path, 'rb') as converted_file:
                self.send_response(200)
                self.send_header('Content-type', 'application/octet-stream')
                self.send_header('Content-disposition', f'attachment; filename=converted_image.{file_type.lower()}')
                self.end_headers()
                self.wfile.write(converted_file.read())

            # Send a response to the client
            self._send_response('Conversion completed successfully')

        else:
            self.send_response(404)
            self.end_headers()

def run(server_class=HTTPServer, handler_class=RequestHandler, port=8000):
    server_address = ('', port)
    httpd = server_class(server_address, handler_class)
    print(f"Starting server on port {port}")
    httpd.serve_forever()

if __name__ == '__main__':
    run()

