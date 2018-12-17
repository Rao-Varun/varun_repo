"""
Program for Server application which handles multiple client at once.
"""
from server.server_manager import ServerManager


if __name__ == "__main__":
    ServerManager().perform_server_application()