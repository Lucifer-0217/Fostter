# Foster DoS Attack Tool

## Description

The **Foster DoS Attack Tool** is an advanced denial-of-service (DoS) attack tool designed for stress testing websites and web servers. It includes support for HTTP flooding and Slowloris attacks. This tool is intended for security researchers and penetration testers to assess the robustness of their systems.

> **Disclaimer**: This tool is intended for educational purposes and legal penetration testing only. Unauthorized use of this tool is illegal and unethical. The developers are not responsible for any misuse of this tool.

## Features

- **Slowloris Attack**: Opens a large number of connections to the target web server and sends partial HTTP requests, keeping connections open to exhaust server resources.
- **HTTP Flooding**: Sends a large number of HTTP requests to a specified URL for testing server resilience.
- **Custom Headers**: Allows users to send custom headers with HTTP flood requests.
- **Proxy Support**: Supports SOCKS5 proxies for anonymization.
- **Multithreading**: Capable of launching attacks using multiple threads.
- **SSL/HTTPS Support**: Includes support for SSL/TLS connections.

## Installation

1. **Clone the repository**:
   ```bash
   git clone https://github.com/yourusername/foster-dos-tool.git
   cd foster-dos-tool
   ```

2. **Install dependencies**:
   Make sure you have Python 3 installed. Install required Python packages:
   ```bash
   pip install -r requirements.txt
   ```

## Usage

The tool can perform both Slowloris and HTTP flood attacks. Below are the usage instructions.

### Slowloris Attack

```bash
python foster_dos.py [HOST] -p [PORT] --sockets [SOCKET_COUNT] --https --sleeptime [SECONDS]
```

### HTTP Flood Attack

```bash
python foster_dos.py --url [TARGET_URL] --threads [THREAD_COUNT] --headers [CUSTOM_HEADERS]
```

### Example Commands

1. **Slowloris Attack** on a web server:
   ```bash
   python foster_dos.py example.com -p 80 --sockets 100 --https --sleeptime 60
   ```

2. **HTTP Flood** with custom headers:
   ```bash
   python foster_dos.py --url http://example.com --threads 10 --headers "User-Agent: Mozilla/5.0, Accept: text/html"
   ```

### Command-Line Arguments

- `host`: Hostname or IP of the target.
- `-p, --port`: Port of the web server (default: 80).
- `--sockets`: Number of sockets to use in the Slowloris attack (default: 50).
- `--threads`: Number of threads to use in the HTTP flood attack (default: 5).
- `--https`: Use HTTPS for the connection.
- `--sleeptime`: Time to sleep between sending headers in the Slowloris attack (default: 30 seconds).
- `--url`: Target URL for the HTTP flood attack.
- `--headers`: Custom headers to send in the HTTP flood attack (comma-separated in 'key:value' format).
- `--useproxy`: Use a SOCKS5 proxy.
- `--proxy-host`: Proxy host (default: 127.0.0.1).
- `--proxy-port`: Proxy port (default: 8080).
- `-v, --verbose`: Enable verbose logging.
- `-ua, --randuseragents`: Randomize user agents with each request.

## Proxy Usage

To route your requests through a SOCKS5 proxy, use the `--useproxy` option. Set the proxy's host and port using the `--proxy-host` and `--proxy-port` options.

Example:
```bash
python foster_dos.py example.com -p 80 --useproxy --proxy-host 192.168.1.10 --proxy-port 1080
```

## Contributing

Contributions are welcome! If you'd like to contribute, please follow these steps:

1. Fork the repository.
2. Create a new branch: `git checkout -b feature-new-feature`.
3. Make your changes and commit them: `git commit -m 'Add new feature'`.
4. Push to the branch: `git push origin feature-new-feature`.
5. Submit a pull request.

## License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for more details.

## Legal Disclaimer

This tool is intended for legal, ethical penetration testing and educational purposes only. The developers are not liable for any damage caused by the misuse of this tool.

--- 

This `README.md` file is tailored to the script, providing an overview, installation instructions, and usage examples. Let me know if you want further adjustments!
