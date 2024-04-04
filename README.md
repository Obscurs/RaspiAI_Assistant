# RaspiAI_Assistant

## Installation
1. Clone the repository on your raspi Desktop 
```bash
Installation:

git clone https://github.com/Obscurs/RaspiAI_Assistant.git

cd RaspiAI_Assistant
sudo apt-get update
sudo apt-get upgrade
chmod +x install_dependencies.sh
./install_dependencies.sh

python3 -m venv env
source env/bin/activate

pip install -r requirements.txt
python -m spacy download en_core_web_sm

chmod +x setupService.sh
chmod +x enableService.sh
chmod +x disableService.sh

./setupService.sh
```

Add picoVoice and ChatGPT API keys on src/config.py
