---

# LAN MDH Streams

**LAN MDH Streams** is a fun project designed to stream music within a LAN environment. This project uses the `Flask` library and `socketio` for live broadcasting, thanks to the idea from [@romulan-overlord](https://github.com/romulan-overlord). The live broadcast only transmits the timestamps of the audio, which clients use to synchronize playback.

## Features

- **Local Streaming**: Streams audio over a local area network (LAN).
- **Live Broadcasting**: Uses `Flask` and `socketio` for real-time updates.
- **Timestamp Synchronization**: Clients receive and follow audio timestamps to ensure synchronized playback.

## Live Demo

- You can try out a live demo of the project at LAN MDH Streams Live.

## Installation

1. **Clone the Repository**

    ```bash
    git clone https://github.com/njeeevan2216/LAN-MDH-Streams.git
    ```

2. **Navigate to the Project Directory**

    ```bash
    cd LAN-MDH-Streams
    ```

3. **Install Dependencies**

    ```bash
    pip install -r requirements.txt
    ```

## Usage

1. **Start the Server**

    ```bash
    python app.py
    ```

2. **Connect to the Server**

    - Ensure the server and client are on the same LAN.
    - Enter the server's IP address in the client's browser.

## Notes

- The live broadcast only includes audio timestamps.
- Ensure your firewall allows the necessary ports for `Flask` and `socketio`.

## Contributing

Feel free to contribute by opening issues or submitting pull requests.

## Acknowledgements

- Thanks to [@romulan-overlord](https://github.com/romulan-overlord) for the idea of using `socketio` for live broadcasting.