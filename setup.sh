# make sure to use python3.10
python3.10 -m venv .venv
source .venv/bin/activate

#Upgrade and install everything necessary
python -m pip install --upgrade pip
python -m pip install -r requirements.txt


#Add this command to ~/.zshrc
# alias mp4copy='cd ~/Documents/Git/mp4copy && source .venv/bin/activate && python mp4copy.py'
# Must have tkinter instaled via brew
# brew install python@3.10  python-tk@3.10 



