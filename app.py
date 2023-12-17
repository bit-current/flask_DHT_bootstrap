# Import the Flask module
import argparse
from dht import DHTSingleton
from flask import Flask
import requests

def get_public_ip():
    try:
        response = requests.get('https://api.ipify.org')
        return response.text
    except requests.RequestException:
        raise RuntimeError("Unable to get IP")

# Create an instance of the Flask class
app = Flask(__name__)

# Define a route for the root URL
@app.route('/')
def return_dht():
    dht_object = DHTSingleton(app.dht_serve_port)
    ip, port, p2p_key = dht_object.dht.get_visible_maddrs()[0].values()

    try: 
        getattr(app,'public_ip')
    except AttributeError: #to set the public IP for the first time
        app.public_ip = get_public_ip()
    multiaddr = f"/ipv4/{app.public_ip}/tcp/{app.dht_serve_port}/p2p/{p2p_key}"
    return multiaddr

# Check if the script is run directly (not imported)
if __name__ == '__main__':
    # Set up argument parsing
    parser = argparse.ArgumentParser(description='Flask Server Configuration')
    parser.add_argument('--flask_serve_port', type=int, default=5000, help='Port to run the Flask server on')
    # Custom placeholders for arguments
    parser.add_argument('--dht_serve_port', type=int, default=5001, help='Port to run the DHT server on')
    parser.add_argument('--host', type=str, default=5001, help='IP to host on')

    # Parse the arguments
    args = parser.parse_args()

    app.dht_serve_port = args.dht_serve_port

    # Run the Flask app on the specified port
    app.run(host=args.host, debug=True, port=args.flask_serve_port)