import os, sys, threading, time
from http.server import HTTPServer, CGIHTTPRequestHandler

port = 5050
webdir = '.'
if len(sys.argv) > 1:
	webdir = sys.argv[1]
if len(sys.argv) > 2:
	port = int(sys.argv[2])

def main():
	print('WEB запущен, адрес подключения: localhost:', port)
	os.chdir(webdir)

	HTTPServer(('', port), CGIHTTPRequestHandler).serve_forever()

try:
	main()
except:
	print("Error in Main")
