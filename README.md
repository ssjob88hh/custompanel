# Custom Panel

A minimal Flask-based web panel for managing Nginx server blocks on Ubuntu.

## Features

- List existing server block configurations.
- Add new domains with document roots.
- Remove domains.
- Reload Nginx after changes.

This panel stores configuration files in the `nginx_conf` directory by default.
It also maintains an `enabled` directory that simulates the `sites-enabled`
folder used by Nginx.

## Installation

1. Install Python dependencies:
   ```bash
   pip install -r requirements.txt
   ```
2. Run the panel:
   ```bash
   python panel.py
   ```

The panel will be available at `http://localhost:8080`.

**Note**: Reloading Nginx requires sudo privileges. If running locally, ensure
your user has permission to reload the Nginx service.

