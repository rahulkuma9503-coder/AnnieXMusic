import os
import sys
import socket
from threading import Thread

PORT = int(os.getenv('PORT', 10000))  # Render's default is 10000 [citation:3]

def bind_port_immediately():
    try:
        # Create a minimal HTTP server
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.bind(('0.0.0.0', PORT))
        s.listen(5)
        print(f"[PORT BINDER] Immediate port binding to 0.0.0.0:{PORT}")
        sys.stdout.flush()
        
        # Simple response handler
        while True:
            conn, addr = s.accept()
            conn.send(b"HTTP/1.1 200 OK\r\n\r\nBot is starting...")
            conn.close()
    except Exception as e:
        print(f"[PORT BINDER ERROR] {str(e)}")
        sys.stdout.flush()

# Start in a dedicated thread immediately
Thread(target=bind_port_immediately, daemon=True).start()
