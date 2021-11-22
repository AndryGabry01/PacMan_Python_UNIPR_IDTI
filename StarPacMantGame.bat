@echo off
pip install -r ./requirements.txt >> nul && (
  Echo "Install/Update requirements"
) || (
    Echo "failed requirements Installd/Updated or execute pip command... I still try to start the game"
)
python "./PacManGui.py" >> nul && (
  Echo "StartGame"
) || (
    Echo "failed start Game"
)
pause