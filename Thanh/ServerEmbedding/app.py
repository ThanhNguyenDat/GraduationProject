from flask import Flask, render_template, request, redirect, url_for, flash, jsonify
# from sqlalchemy import create_engine
# from sqlalchemy.orm import sessionmaker
# from database_setup import Base, Controll
from src.util.connectdb import ConnectDB

Connect = ConnectDB()
Connect.create_table()

app = Flask(__name__,
            static_url_path='',
            static_folder='src/static',
            template_folder='src/templates', )

@app.route('/')
def include_example():
    return render_template('home_page.html')

@app.route('/controll')
def controll():
    result = Connect.show_data()
    # get the lastest result from database
    result = result[-1]
    print("result: ", result)
    return render_template('./control/index.html', result=result)

@app.route('/defaultpoints')
def defaultpoints():
    results = Connect.show_data()
    # get the lastest result from database
    # result = result[-1]
    print("result: ", results)
    return render_template('./defaultpoints/index.html', results=results)


if __name__ == '__main__':
    app.run(host='0.0.0.0')
