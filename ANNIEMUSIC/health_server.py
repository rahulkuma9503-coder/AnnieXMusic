import os
import sys
from http.server import BaseHTTPRequestHandler, HTTPServer
import threading

PORT = int(os.getenv('PORT', 5000))

class HealthHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        if self.path == '/':
            self.send_response(200)
            self.send_header('Content-type', 'text/plain')
            self.end_headers()
            self.wfile.write(b"Annie Music Bot is Operational")
        else:
            self.send_response(404)
            self.end_headers()

def run_server():
    server_address = ('0.0.0.0', PORT)
    httpd = HTTPServer(server_address, HealthHandler)
    print(f"[HEALTH SERVER] Running on http://0.0.0.0:{PORT}")
    sys.stdout.flush()  # Force flush to ensure Render sees the log immediately
    httpd.serve_forever()

# Start the server in a daemon thread
thread = threading.Thread(target=run_server)
thread.daemon = True
thread.start()

# Print a message to confirm the server started
print(f"[HEALTH SERVER] Started successfully on port {PORT}")
sys.stdout.flush()
