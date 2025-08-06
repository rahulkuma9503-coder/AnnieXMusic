import os
import sys
import socket
import threading
import time

PORT = int(os.getenv('PORT', 10000))  # Render's default port

def bind_port_immediately():
    try:
        # Create socket and bind immediately
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        s.bind(('0.0.0.0', PORT))
        s.listen(5)
        print(f"✅ [PORT BINDER] Successfully bound to 0.0.0.0:{PORT}")
        sys.stdout.flush()
        
        # Simple HTTP response handler
        while True:
            try:
                conn, addr = s.accept()
                request = conn.recv(1024)
                # Respond with minimal HTTP response
                conn.send(b"HTTP/1.1 200 OK\r\n")
                conn.send(b"Content-Type: text/plain\r\n")
                conn.send(b"Connection: close\r\n\r\n")
                conn.send(b"Bot is initializing...")
                conn.close()
            except Exception as e:
                print(f"⚠️ [PORT BINDER] Connection error: {str(e)}")
                sys.stdout.flush()
    except Exception as e:
        print(f"❌ [PORT BINDER CRITICAL] Failed to bind port: {str(e)}")
        sys.stdout.flush()
        # Attempt to restart binding
        time.sleep(2)
        bind_port_immediately()

# Start binding in a separate thread immediately
threading.Thread(target=bind_port_immediately, daemon=True).start()
