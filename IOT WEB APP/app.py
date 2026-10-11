
from http.server import HTTPServer, BaseHTTPRequestHandler
import json
import urllib.parse

# Simulated Device State
device_state = {
    "status": "OFF",
    "brightness": 0
}

class DimmerAPIHandler(BaseHTTPRequestHandler):
    def _send_response(self, status_code, data):
        self.send_response(status_code)
        self.send_header('Content-Type', 'application/json')
        self.send_header('Access-Control-Allow-Origin', '*')
        self.send_header('Access-Control-Allow-Methods', 'GET, POST, OPTIONS')
        self.send_header('Access-Control-Allow-Headers', 'Content-Type')
        self.end_headers()
        self.wfile.write(json.dumps(data).encode('utf-8'))

    def do_OPTIONS(self):
        self._send_response(200, {"message": "OK"})

    # 1. Device Status dekhne ke liye (GET /api/device)
    def do_GET(self):
        parsed_path = urllib.parse.urlparse(self.path)
        if parsed_path.path == "/api/device":
            self._send_response(200, device_state)
        else:
            self._send_response(404, {"error": "Endpoint not found"})

    # 2. Dimmer control karne ke liye (POST /api/device)
    def do_POST(self):
        parsed_path = urllib.parse.urlparse(self.path)
        if parsed_path.path == "/api/device":
            content_length = int(self.headers.get('Content-Length', 0))
            body = self.rfile.read(content_length)
            try:
                payload = json.loads(body.decode('utf-8'))
                
                # Validation rules
                if "status" in payload:
                    if payload["status"] in ["ON", "OFF"]:
                        device_state["status"] = payload["status"]
                    else:
                        self._send_response(400, {"error": "Invalid status value"})
                        return

                if "brightness" in payload:
                    val = int(payload["brightness"])
                    if 0 <= val <= 100:
                        device_state["brightness"] = val
                        if val > 0:
                            device_state["status"] = "ON"
                        else:
                            device_state["status"] = "OFF"
                    else:
                        self._send_response(400, {"error": "Brightness must be between 0 and 100"})
                        return

                self._send_response(200, {
                    "message": "Device updated successfully",
                    "current_state": device_state
                })
            except Exception as e:
                self._send_response(400, {"error": "Malformed JSON payload"})
        else:
            self._send_response(404, {"error": "Endpoint not found"})

if __name__ == "__main__":
    server = HTTPServer(('0.0.0.0', 5000), DimmerAPIHandler)
    print("IoT Dimmer API running on port 5000...")
    server.serve_forever()