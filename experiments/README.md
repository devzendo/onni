This tree contains Python 3 versions of various parts of onni such as the AFSK
modem, using different designs. These are tested against the recording in the
`samples` directory. There are tests and Jupyter Notebooks here.

To recreate the virtual environment after a clone on a new system:
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt

To update the virtual environment after installing new libraries:
pip freeze > requirements.txt

To activate the virtual environment:
source venv/bin/activate

