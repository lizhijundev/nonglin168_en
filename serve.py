#!/usr/bin/env python3
"""
Simple HTTP server for serving the static website locally
Usage: python serve.py [port]
Default port: 8000
"""

import http.server
import socketserver
import sys
import os

# Change to the directory containing this script
os.chdir(os.path.dirname(os.path.abspath(__file__)))

# Get port from command line argument or use default
PORT = int(sys.argv[1]) if len(sys.argv) > 1 else 8000

class MyHTTPRequestHandler(http.server.SimpleHTTPRequestHandler):
    def end_headers(self):
        # Add CORS headers for local development
        self.send_header('Access-Control-Allow-Origin', '*')
        self.send_header('Access-Control-Allow-Methods', 'GET, POST, OPTIONS')
        self.send_header('Access-Control-Allow-Headers', 'Content-Type')
        super().end_headers()

    def log_message(self, format, *args):
        # Custom log format
        print(f"[{self.log_date_time_string()}] {format % args}")

try:
    with socketserver.TCPServer(("", PORT), MyHTTPRequestHandler) as httpd:
        print(f"🚀 Server starting at http://localhost:{PORT}")
        print(f"📁 Serving directory: {os.getcwd()}")
        print(f"🌐 Main page: http://localhost:{PORT}/index.html")
        print("Press Ctrl+C to stop the server")
        httpd.serve_forever()
except KeyboardInterrupt:
    print("\n👋 Server stopped by user")
except OSError as e:
    if e.errno == 48:  # Address already in use
        print(f"❌ Port {PORT} is already in use. Try a different port:")
        print(f"   python serve.py {PORT + 1}")
    else:
        print(f"❌ Error: {e}")
