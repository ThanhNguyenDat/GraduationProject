from unittest import result
from flask import Flask, render_template, request, redirect, url_for, flash, jsonify
from calculate import cal_theta_1, cal_theta_2, cal_theta_3, cal_theta_4, cal_theta_5
# from sqlalchemy import create_engine
# from sqlalchemy.orm import sessionmaker
# from database_setup import Base, Controll
from src.util.connectmysql import ConnectDB

Connect = ConnectDB()
Connect.create_table_controll()
Connect.create_table_motor_default()

app = Flask(__name__,
            static_url_path='',
            static_folder='src/static',
            template_folder='src/templates', )

@app.route('/')
def include_example():
    return render_template('home_page.html')

@app.route('/controlposition')
def control():
    result = Connect.show_data()
    # get the lastest result from database
    if len(result) > 0:
        result = result[-1]
    print("Len result: ", len(result))
    return render_template('./controlposition/index.html', result=result)

@app.route('/controlposition', methods=['POST'])
def setposition():
    if request.method == 'POST':
        print("request.form: ", request.form)
        data = request.form
        vitri_x = float(data['vitri_x'])
        vitri_y = float(data['vitri_y'])
        vitri_z = float(data['vitri_z'])
        phi = float(data['phi'])
        gramma = float(data['gramma'])
        v = float(data['v'])
        theta_1 = cal_theta_1(vitri_y, vitri_z)
        theta_5 = cal_theta_5(gramma, theta_1)
        
        theta_2 = cal_theta_2(vitri_x, vitri_y, vitri_z, theta_1)
        theta_3 = cal_theta_3(vitri_x, vitri_y, vitri_z, theta_1, theta_2)
        theta_4 = cal_theta_4(vitri_x, vitri_y, vitri_z, theta_1, theta_2, theta_3)
        
        w_1, w_2, w_3, w_4, w_5 = 6, 7, 8, 9, 10

        data = [theta_1, theta_2, theta_3, theta_4, theta_5, w_1, w_2, w_3, w_4, w_5, vitri_x, vitri_y, vitri_z, phi, gramma, v]
        Connect.insert_data(data)
        return redirect(url_for('control'))

@app.route('/controltheta')
def controlltheta():
    result = Connect.show_data()
    # get the lastest result from database
    if len(result) > 0:
        result = result[-1]
    print("Len result: ", len(result))
    return render_template('./control/index_theta.html', result=result)

@app.route('/defaultpoints')
def defaultpoints():
    results = Connect.show_data(table_name="MotorDefault")
    
    # get the lastest result from database
    # result = result[-1]
    # print("result: ", results)
    return render_template('./defaultpoints/index.html', results=results)

# edit default points with id
@app.route('/defaultpoints/edit/<int:id>', methods=['GET', 'POST'])
def edit_defaultpoints(id):
    results = Connect.show_data(table_name="MotorDefault")
    
    # get result with id
    for r in results:
        if r[0] == id:
            result = r
    
    if request.method == 'POST':
        data = request.form
        vitri_x = float(data['vitri_x'])
        vitri_y = float(data['vitri_y'])
        vitri_z = float(data['vitri_z'])
        phi = float(data['phi'])
        gramma = float(data['gramma'])
        v = data['v']
        position = data['position']
        velocity = data['velocity']
        description = data['description']
        theta_1 = cal_theta_1(vitri_y, vitri_z)
        theta_5 = cal_theta_5(gramma, theta_1)
        
        theta_2 = cal_theta_2(vitri_x, vitri_y, vitri_z, theta_1)
        theta_3 = cal_theta_3(vitri_x, vitri_y, vitri_z, theta_1, theta_2)
        theta_4 = cal_theta_4(vitri_x, vitri_y, vitri_z, theta_1, theta_2, theta_3)
        
        w_1, w_2, w_3, w_4, w_5 = 6, 7, 8, 9, 10

        data = [theta_1, theta_2, theta_3, theta_4, theta_5, w_1, w_2, w_3, w_4, w_5, vitri_x, vitri_y, vitri_z, phi, gramma, v, position, velocity, description]
        Connect.update_data(id, data, name_database="MotorDefault")
        return redirect(url_for('defaultpoints'))

    return render_template('defaultpoints/edit.html', id=id, result=result)

@app.route('/defaultpoints/delete/<int:id>', methods=['GET', 'POST'])
def delete_defaultpoints(id):    
    Connect.delete_data_by_id(id, name_database="MotorDefault")
    return redirect(url_for('defaultpoints'))
    
@app.route('/defaultpoints/add')
def add_defaultpoints():
    return render_template('defaultpoints/add.html')

@app.route('/defaultpoints/add', methods=['POST'])
def add_position():
    if request.method == 'POST':
        data = request.form
        vitri_x = float(data['vitri_x'])
        vitri_y = float(data['vitri_y'])
        vitri_z = float(data['vitri_z'])
        phi = float(data['phi'])
        gramma = float(data['gramma'])
        position = data['position']
        velocity = data['velocity']
        v = data['v']
        description = data['description']
        theta_1 = cal_theta_1(vitri_y, vitri_z)
        theta_5 = cal_theta_5(gramma, theta_1)

        theta_2 = cal_theta_2(vitri_x, vitri_y, vitri_z, theta_1)
        theta_3 = cal_theta_3(vitri_x, vitri_y, vitri_z, theta_1, theta_2)
        theta_4 = cal_theta_4(vitri_x, vitri_y, vitri_z, theta_1, theta_2, theta_3)
        
        w_1, w_2, w_3, w_4, w_5 = 6, 7, 8, 9, 10
        data = [theta_1, theta_2, theta_3, theta_4, theta_5, w_1, w_2, w_3, w_4, w_5, vitri_x, vitri_y, vitri_z, phi, gramma, v, position, velocity, description]
        Connect.insert_data(data, table_name="MotorDefault")
        return redirect(url_for('defaultpoints'))

@app.route('/defaultpoints/', methods=['POST'])
def submit_position(id):
    results = Connect.show_data(table_name="MotorDefault")
    
    # get result with id
    for r in results:
        if r[0] == id:
            result = r
            
    if request.method=='POST':
        data =request.form
        print(data)
        return redirect(url_for('control'))


if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')
