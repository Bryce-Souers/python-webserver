# Python Webserver
Barebones web-server and client that communicate using the HTTP protocol.
Any browser can communicate with the server as it recognizes the browser HTTP requests.

### Examples
Extensive examples can be seen in `examples.pdf`.

### Getting Started
`$ python3 webserver.py port` - Start webserver on port

Then, in your browser, go to your local IP address and the port the server is binded to and request `HelloWorld.html` (http://192.168.X.XX/HelloWorld.html for example). The webserver will accept your connection and recognize the HTTP request.

Alternatively the python client can be used: `python3 web_client.py host_ip port file`
