# make sure to use python3.10
python3.10 -m venv .venv
source .venv/bin/activate

#Upgrade and install everything necessary
python -m pip install --upgrade pip
python -m pip install -r requirements.txt

# Install rsync from HomeBrew
brew cleanup -v
brew update -v
brew install rsync -v
brew install python@3.10 python-tk@3.10 -v 


#Add this command to ~/.zshrc
echo "alias mp4copy='cd ~/Documents/Git/mp4copy && source .venv/bin/activate && python mp4copy.py'" >> ~/.zshrc

source ~/.zshrc



