# reMarkable Offline Sync Tool

This is a Python-based tool to synchronize your documents from a reMarkable tablet using its USB HTTP REST API. It is designed for users who prefer not to use cloud sync due to privacy concerns or who require a completely offline and local solution. The reMarkable API is built in and does not require any modifcation on the reMarkable (like the developer tool settings).

This tool has been tested with the reMarkable Pro (software version 3.16) but should be also compatible with the reMarkable 2.

> **Disclaimer:** This tool is in an early stage of development. Use it at your own risk.

---

## Features
- Fully offline and local syncing of documents from a reMarkable tablet.
- Creates and maintains a folder structure mirroring the reMarkable’s file system.
- Downloads documents as PDFs for offline use.
- Works with a minimal Python environment. Only the requests library needs to be installed

### Roadmap
The following features are planned for future releases:
- Faster sync by detecting and syncing only changed files.
- Deletion of local files that have been removed from the reMarkable.
- Option to upload files back to the reMarkable.
- Option to download raw `.rmdoc` files in addition to PDFs.
- Overall status output providing an overview of tracked files.
- Improved error handling.
- Code refactoring and enhancements for better robustness.
- Create binary packages to run the tool without the need to install Python locally

---

## Preparing Your reMarkable Tablet

To use this tool, the HTTP API server on your reMarkable tablet must be activated:

1. **Connect your reMarkable via USB:**
   - Plug your reMarkable tablet into your computer using a USB cable.

2. **Enable USB Web Interface:**
   - Open the settings on your reMarkable tablet.
   - Navigate to **Storage settings** and enable **USB web interface**.

3. **Note the API URL:**
   - Once the interface is enabled, you will see an HTTP address (e.g., `http://10.11.99.1`). Use this URL in your `sync_config.json` file.

---

## Installation and Setup

### 1. Clone the Repository
```bash
git clone https://github.com/yourusername/remarkable-offline-sync.git
cd remarkable-offline-sync
```

### 2. Set Up Python Environment
It is recommended to use a virtual environment:

```bash
python3 -m venv venv
source venv/bin/activate  # On Windows, use `venv\Scripts\activate`
```

Install the required dependencies:
```bash
pip install -r requirements.txt
```

### 3. Configure the Tool
Create a `sync_config.json` file in the root directory. Below is an example configuration:

```json
{
    "url": "http://10.11.99.1",
    "baseFolder": "synced_files",
    "syncDatabase": "sync_db.json"
}
```

- **`url`**: The HTTP API address of your reMarkable tablet.
- **`baseFolder`**: The local directory where files will be synced.
- **`syncDatabase`**: Will be used in the future. The file used to track changes for faster syncing.

---

## Usage

Run the tool from the command line:

### Basic Commands

1. **Sync Files**
   ```bash
   python sync_tool.py
   ```
   This will download files and folders from your reMarkable tablet to your local machine.


4. **Debug Mode**
   ```bash
   python sync_tool.py --debug
   ```
   Enables verbose debugging output.

---

## Contributing

Contributions are welcome! If you encounter issues or have suggestions for new features, feel free to open an issue or submit a pull request.

---

## License
This project is licensed under the [MIT License](LICENSE).

