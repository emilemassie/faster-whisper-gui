import os
import sys
import time
from datetime import datetime

from PyQt6 import QtWidgets, QtCore, QtGui, uic
from PyQt6.QtCore import QThread, pyqtSignal, QObject

# Define application directory
app_dir = os.path.dirname(__file__)
sys.path.append(os.path.join(app_dir, 'penv', 'lib', 'python3.9', 'site-packages'))
sys.path.append(os.path.join(app_dir, 'penv', 'Lib', 'site-packages'))
sys.path.append(os.path.join(app_dir, 'nv_bin'))
print('Application directory:', app_dir)

def seconds_to_hhmmss(seconds):
    hours = int(seconds // 3600)
    minutes = int((seconds % 3600) // 60)
    remaining_seconds = int(seconds % 60)
    return f"{hours:02}:{minutes:02}:{remaining_seconds:02}"

class Worker(QObject):
    finished = pyqtSignal()
    progress = pyqtSignal(str)

    def __init__(self, main_app, audio_file, transcript_folder, model_size, beam_size):
        super().__init__()
        self.main_app = main_app
        self.audio_file = audio_file
        self.transcript_folder = transcript_folder
        self.model_size = model_size
        self.beam_size = beam_size

    def run(self):
        self.main_app.stopped = False
        audio_path = self.audio_file
        transcript_dir = self.transcript_folder
        model_size = self.model_size
        beam_size = self.beam_size

        self.progress.emit('Initializing Whisper model...')
        from faster_whisper import WhisperModel


        if all(model_size not in string for string in self.main_app.get_downloaded_faster_whisper_models()):
            self.progress.emit('Downloading Model, This may take a while...')
        else:
            pass

        if self.main_app.mode_list.currentText() == 'GPU (CUDA) - int8':
            model = WhisperModel(model_size, device="cuda", compute_type="int8_float16")    
        elif self.main_app.mode_list.currentText() == 'GPU (CUDA) - float16':
            model = WhisperModel(model_size, device="cuda", compute_type="int8")
        elif self.main_app.mode_list.currentText() == 'CPU - int8':
            model = WhisperModel(model_size, device="cpu", compute_type="int8")
        else:
            model = WhisperModel(model_size, device="cpu", compute_type="int8")

        self.progress.emit('Transcription started...\n')

        audio_file = os.path.basename(audio_path)
        start_time = time.time()
        start_datetime = datetime.now().strftime('%Y-%m-%d %H:%M:%S')

        transcript_file = os.path.join(transcript_dir, f"{os.path.splitext(audio_file)[0]}.txt")
        self.progress.emit(f"Transcribing : {audio_file}")
        self.progress.emit(f"Transcript file :{transcript_file}")

        segments, info = model.transcribe(audio_path, beam_size=beam_size)

        with open(transcript_file, 'a', encoding='utf-8') as f:
            header = (
                f"---------------------------------------------\n"
                f"File: {audio_file}\n"
                f"Transcription started: {start_datetime}\n"
                f"Model Size: {model_size}\n"
                f"Detected language: '{info.language}' with probability {info.language_probability:.2f}\n"
                "---------------------------------------------\n"
            )
            f.write(header)
            for line in header.split('\n'):
                self.progress.emit(line)

            for segment in segments:
                segment_line = f"[{seconds_to_hhmmss(segment.start)} -> {seconds_to_hhmmss(segment.end)}] {segment.text}"
                f.write(segment_line + '\n')
                
                end_time = time.time()
                elapsed_time = end_time - start_time
                start_time = time.time()
                self.progress.emit(f'[Operation Time : {elapsed_time:.2f}s] - {segment_line}')
                if self.main_app.stopped:
                    self.main_app.convert_button.setEnabled(True)
                    self.main_app.convert_button.setText('Transcribe')
                    self.main_app.update_log('Conversion stopped', 'red')
                    self.finished.emit()
                    break

class FastWhisperGui(QtWidgets.QWidget):
    def __init__(self):
        super().__init__()
        self.root_folder = os.path.dirname(__file__)

        self.audio_file = None
        self.transcript_folder = None
        self.stopped = True

        parent_folder = os.path.dirname(__file__)
        uic.loadUi(os.path.join(parent_folder,'FastWhisperGui.ui'), self)
        self.setWindowIcon(QtGui.QIcon(os.path.join(parent_folder, 'icon.ico')))

        self.thread = QThread()

        self.setWindowTitle('Fast Whisper')
        self.update_log('Fast Whisper initialized', 'green')

        self.convert_button.setEnabled(False)
        self.convert_button.released.connect(self.convert_audio)
        self.trans_button.clicked.connect(self.select_transcript_file)
        self.file_button.clicked.connect(self.select_audio_file)

        # Add models to model list
        for model in ['tiny','base', 'small', 'medium', 'large-v1', 'large-v2']:
            self.model_list.addItem(model)
        self.model_list.setCurrentText('medium')

        self.mode_list.addItems(['CPU - int8','GPU (CUDA) - float16', 'GPU (CUDA) - int8'])
        print(self.get_downloaded_faster_whisper_models())

    def seconds_to_hhmmss(self, seconds):
        hours = int(seconds // 3600)
        minutes = int((seconds % 3600) // 60)
        remaining_seconds = int(seconds % 60)
        return f"{hours:02}:{minutes:02}:{remaining_seconds:02}"

    def get_downloaded_faster_whisper_models(self):
        # Path to Hugging Face cache directory
        base_dir = os.path.expanduser("~/.cache/huggingface/hub/")
        if not os.path.exists(base_dir):
            return []

        # List all downloaded models
        return [name for name in os.listdir(base_dir) if os.path.isdir(os.path.join(base_dir, name))]

    def update_log(self, message, color=None):

        if color:
            self.logs.append(f'<p style="color:{color};">'+message+'</p> ')
        else:
            self.logs.append(message)  # Append message to log view

        scroll_bar = self.logs.verticalScrollBar()
        scroll_bar.setValue(scroll_bar.maximum())
        #self.logs.moveCursor(QtGui.QTextCursor.MoveOperation.End)

    def check_if_can_convert(self):
        if not self.audio_file:
            self.convert_button.setEnabled(False)
            return False
        if not self.transcript_folder:
            self.convert_button.setEnabled(False)
            return False

        self.convert_button.setEnabled(True)
        return True
    
    
    def select_audio_file(self):
        file, _ = QtWidgets.QFileDialog.getOpenFileName(self, "Select Audio File")
        if file:
            self.audio_file = file
            self.audio_file_path.setText(file)
        else:
            self.transcript_folder = None
        self.check_if_can_convert()

    def select_transcript_file(self):
        folder = QtWidgets.QFileDialog.getExistingDirectory(self, f"Select Transcript Directory")
        if folder:
            self.transcript_folder = folder
            self.trans_text.setText(folder)
        else:
            self.transcript_folder = None
        self.check_if_can_convert()

    def convert_audio(self):
        if self.stopped:
            self.stopped = False
            self.convert_button.setText('Stop')
            self.thread = QThread()
            self.worker = Worker(
                self,
                self.audio_file,
                self.transcript_folder,
                self.model_list.currentText(),
                self.beam_size.value()
            )
            self.worker.moveToThread(self.thread)
            self.thread.started.connect(self.worker.run)
            self.worker.finished.connect(self.thread.quit)
            self.worker.finished.connect(self.worker.deleteLater)
            self.thread.finished.connect(self.thread.deleteLater)
            self.worker.progress.connect(self.update_log)
            self.thread.start()
            return
        elif self.stopped == False:
            self.stopped = True
            self.convert_button.setText('Stopping...')
            self.convert_button.setEnabled(False)
            self.worker.finished.emit()
            return

if __name__ == '__main__':
    app = QtWidgets.QApplication(sys.argv)
    FWG = FastWhisperGui()
    FWG.show()
    sys.exit(app.exec())
