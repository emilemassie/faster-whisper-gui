<div align="center">
  <img width="494" alt="image" src="https://github.com/user-attachments/assets/a0362ea8-dd7e-4255-a15d-4ca81f001bd5" />
</div>
# Faster Whisper GUI

<img src=" alt="Faster Whisper GUI" style="height: 1.5em; vertical-align: middle;" /> Faster Whisper GUI

Faster Whisper GUI is a Python-based graphical user interface for the [faster-whisper](https://github.com/guillaumekln/faster-whisper) library, providing an easy way to generate transcripts from audio files.

<div align="center">
  <img width="494" alt="image" src="https://github.com/user-attachments/assets/8d499f19-74f5-4cfc-964f-7077b428f0e5" />
</div>

## Features
- Simple and intuitive interface.
- Choose your input file and output folder for transcripts.
- Select model size for transcription accuracy.
- GPU acceleration support for faster processing.

## Download
Download the latest version of Faster Whisper GUI from the [Releases](https://github.com/emilemassie/faster-whisper-gui/releases) section.

## How to Use

### Step 1: Choose Your File
Select the audio file you want to transcribe using the file picker.

### Step 2: Choose the Transcript Folder
Pick the folder where you want the generated transcript to be saved.

### Step 3: Choose the Model Size
Select the model size for transcription. Larger models are more accurate but may require more processing power.

### Step 4: Select GPU or CPU Mode
- **GPU Mode**: Choose this option if you have a GPU and want faster transcription.
- **CPU Mode**: Use this if you do not have a GPU or prefer CPU processing.

### Step 5: Start or Stop Transcription
Click the "Transcript" button to start the transcription process. You can stop it at any time by clicking the "Stop" button.

## Installation

1. Clone the repository:
   ```bash
   git clone https://github.com/your-username/faster-whisper-gui.git
   cd faster-whisper-gui
   ```

2. Install the required dependencies:
   ```bash
   pip install -r requirements.txt
   ```

3. Run the application:
   ```bash
   python app.py
   ```

## Requirements
- Python 3.9+
- Dependencies listed in `requirements.txt`
- Optional: GPU with CUDA support for GPU acceleration

## License
This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.

## Acknowledgments
This application is built on top of the [faster-whisper](https://github.com/guillaumekln/faster-whisper) library.

---

Feel free to contribute to the project or report any issues you encounter!
