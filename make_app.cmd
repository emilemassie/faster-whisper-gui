pyinstaller --clean --noconsole -y -n FasterWhisperGUI --onefile --icon=icon.ico --add-data ./nv_bin;. --add-data icon.ico;. --add-data FastWhisperGui.ui;. faster_whisper_gui.py
pause