from hivemind import DHT
import requests

class DHTSingleton:
    _instance = None


    @staticmethod
    def get_public_ip():
        try:
            response = requests.get('https://api.ipify.org')
            return response.text
        except requests.RequestException:
            raise RuntimeError("Unable to get IP")
    
    def __new__(cls, dht_port):
        if cls._instance is None: #TODO allow for port change without restart by checking for new port number
            cls._instance = super(DHTSingleton, cls).__new__(cls)
            cls._instance.dht = DHT(
                host_maddrs=[f"/ip4/0.0.0.0/tcp/{dht_port}",
                            f"/ip4/{cls.get_public_ip()}/tcp/{dht_port}"],
                announce_maddrs = [f"/ip4/0.0.0.0/tcp/{dht_port}",
                            f"/ip4/{cls.get_public_ip()}/tcp/{dht_port}"],
                start=True)  # Example data store
        return cls._instance

  