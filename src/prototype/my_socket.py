from classic_utils import print_log
import socket
try:
	s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
	s.connect(("8.8.8.8", 80))
	localhost = s.getsockname()[0]
except Exception as _ex:
	print_log(f"[Error: Socket] {_ex}")

