# Foster DoS Attack Tool

## Description

The **Foster DoS Attack Tool** is an advanced penetration testing tool developed to simulate Denial of Service (DoS) attacks. It enables security professionals to assess the resilience of their systems by safely launching controlled DoS attacks. This tool is particularly useful for identifying potential vulnerabilities under stress.

> **Disclaimer:** This tool is strictly for educational purposes and legal penetration testing. Unauthorized use is illegal and unethical. The authors are not responsible for any misuse.

## Features

- **Protocol Support**: Works with HTTP, TCP, and UDP protocols.
- **Custom Payloads**: Customize payloads to target specific vulnerabilities.
- **Multi-threading**: Supports concurrent requests with customizable threads.
- **Logging**: Comprehensive logging for analysis and documentation.
- **Rate Limiting**: Control the rate of requests to manage impact.

## Installation

1. **Clone the repository**:
   ```bash
  https://github.com/Lucifer-0217/Fostter.git
   ```

2. **Install dependencies**:
   Ensure that all required Python packages are installed:
   ```bash
   pip install -r requirements.txt
   ```

3. **Run the tool**:
   Execute the following command:
   ```bash
   python foster.py --target [TARGET_IP] --port [TARGET_PORT] --protocol [PROTOCOL]
   ```

## Usage

The following commands are available to test the tool against a target:

### 1. **Basic HTTP Flood Test**:
   ```bash
   python foster.py -u https://example.com -T 10 -s 150
   ```
   - **Description**: Initiates an HTTP flood attack with 10 threads and 150 sockets.

### 2. **Custom Headers HTTP Flood Test**:
   ```bash
   python foster.py -u https://example.com -T 10 -s 150 -H "Custom-Header: Value,Another-Header: AnotherValue"
   ```
   - **Description**: Adds custom headers to the requests while launching the attack.

### 3. **Random User-Agent HTTP Flood Test**:
   ```bash
   python foster.py -u https://example.com -T 10 -s 150 -ua
   ```
   - **Description**: Randomizes the User-Agent for each request sent during the attack.

### 4. **HTTPS Test with Proxy**:
   ```bash
   python foster.py -u https://example.com -T 10 -s 150 -x --proxy-host 127.0.0.1 --proxy-port 8080 --https
   ```
   - **Description**: Uses a SOCKS5 proxy and sends the requests over HTTPS.

### 5. **Verbose Mode Test**:
   ```bash
   python foster.py -u https://example.com -T 10 -s 150 -v
   ```
   - **Description**: Enables verbose logging to show detailed output.

### Command-Line Options:
- `--target`: IP or domain of the target system.
- `--port`: Port number to attack.
- `--protocol`: Protocol to be used (HTTP, TCP, UDP).
- `--threads`: Number of concurrent threads (default: 10).
- `--duration`: Attack duration in seconds (default: 60).
- `--payload`: Optional custom payload.
- `-u`: Target URL for HTTP flood.
- `-T`: Number of threads to use.
- `-s`: Number of sockets to use.
- `-H`: Comma-separated list of custom headers.
- `-ua`: Randomizes user-agents with each request.
- `-x`: Use a SOCKS5 proxy for connecting.
- `--proxy-host`: SOCKS5 proxy host.
- `--proxy-port`: SOCKS5 proxy port.
- `--https`: Use HTTPS for the requests.
- `-v`: Enable verbose logging.

### Example:

To initiate an HTTP flood attack on `192.168.1.100` over port 80 with 50 threads for 120 seconds:

```bash
python foster.py --target 192.168.1.100 --port 80 --protocol HTTP --threads 50 --duration 120
```

## Contributing

Contributions are encouraged! If you'd like to contribute, follow these steps:

1. Fork the repository.
2. Create a new branch: `git checkout -b feature-new-feature`.
3. Commit your changes: `git commit -m 'Add new feature'`.
4. Push to the branch: `git push origin feature-new-feature`.
5. Submit a pull request.

## License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for more information.

## Legal Disclaimer

Ensure that you use this tool in a legal and ethical manner. Always obtain proper authorization before performing tests. The creators are not liable for any damage caused by the misuse of this tool.

