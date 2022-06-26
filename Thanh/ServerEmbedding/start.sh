if [ -f "venv/bin/activate" ]
then
    echo virtual env already created
else
    virtualenv venv
fi
source venv/bin/activate

# Just install dependencies by default to pick up any changes
pip install -r requirements.txt
# npm install mysql

#
# run the data server
#
python main.py
