# Python File Transfer App

The Flask File Transfer App is a web application built with Flask that allows users to transfer files between devices over a local network. It provides a simple and convenient way to upload and download files securely.

## Features

- **Upload Files**: Users can upload multiple files from their devices to the server.
- **Download Files**: Users can browse and download files stored on the server to their devices.
- **QR Code Integration**: The server generates a QR code containing the URL for easy access to the application.

## Installation

### Prerequisites

- Python 3.x
- pip (Python package installer)

### Steps

1. Clone the repository:

   ```bash
   git clone https://github.com/hanklokyaw/file_receive_over_wifi.git
   ```

2. Navigate to the project directory:

   ```bash
   cd file_receive_over_wifi
   ```

3. Install dependencies:

   ```bash
   pip install -r requirements.txt
   ```

### Usage

1. Run the Flask application:

   ```bash
   python main.py
   ```

2. Access the application in your web browser at such as `http://192.168.1.100:5000`

3. Send Files:

   - Navigate to the "Send" page.
   - Select one or multiple files from your device.
   - Click the "Send" button to send the selected files to the server.

4. Receive Files:

   - Navigate to the "Receive" page.
   - Browse the list of files available on the server.
   - Click on a file name to download it to your device.
  
5. QR Code:

   - Upon running the server, a QR code containing the server URL will be displayed.
   - Scan the QR code with your device to access the application.
  
### Contributing

Contributions are welcome! Please feel free to open an issue or submit a pull request for any improvements or features you'd like to add.

### License

This project is licensed under the MIT License.
