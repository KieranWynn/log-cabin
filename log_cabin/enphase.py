
import enphase_api
from enphase_api import operations, config

def main():
    gateway = config.GatewayDevice(ip="10.0.4.53", serial_number=122206010064)
    d = operations.get_gateway_data(gateway)


if __name__ == "__main__":
    main()