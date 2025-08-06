import os
from http.server import BaseHTTPRequestHandler, HTTPServer
import threading

def run_health_server():
    port = int(os.getenv('PORT', 5000))
    class Handler(BaseHTTPRequestHandler):
        def do_GET(self):
            if self.path == '/':
                self.send_response(200)
                self.send_header('Content-type', 'text/plain')
                self.end_headers()
                self.wfile.write(b"Annie Music Bot is Operational")
            else:
                self.send_response(404)
                self.end_headers()

    server = HTTPServer(('0.0.0.0', port), Handler)
    print(f"Starting health server on port {port}")
    server.serve_forever()

# Start the server in a separate thread
def start():
    thread = threading.Thread(target=run_health_server)
    thread.daemon = True
    thread.start()

# Call start when this module is imported
start()
