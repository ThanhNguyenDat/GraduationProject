from unittest import result
from flask import Flask, render_template, request, redirect, url_for, flash, jsonify, Response, Request
from calculate import cal_theta_1, cal_theta_2, cal_theta_3, cal_theta_4, cal_theta_5
# from sqlalchemy import create_engine
# from sqlalchemy.orm import sessionmaker
# from database_setup import Base, Controll
from src.util.connectmysql import ConnectDB
from calculate import *
import plotly
import plotly.graph_objs as go
import plotly.express as px
import json

Connect = ConnectDB()
Connect.create_table_controll()
Connect.create_table_motor_default()


# plot 3d scater from database
def plot_3d_scatter(x, y, z):
    data = [go.Scatter3d(x=x, y=y, z=z, mode='markers', marker=dict(size=1))]
    layout = go.Layout(title='3D Scatter Plot from Database')
    fig = go.Figure(data=data, layout=layout)
    return fig

server = Flask(__name__,
            static_url_path='',
            static_folder='src/static',
            template_folder='src/templates', )

@server.route('/')
def include_example():
    return render_template('home_page.html')

@server.route('/controlposition')
def controlposition():
    result = Connect.show_data()
    # get the lastest result from database
    if len(result) > 0:
        result = result[-1]
        # x = result[11]
        # y = result[12]
        # z = result[13]
        # fig = plot_3d_scatter(x, y, z)

        return render_template('./controlposition/index.html', result=result)
    else:
        return render_template('./controlposition/index.html')

@server.route('/controlposition', methods=['POST'])
def setposition():
    if request.method == 'POST':
        print("request.form: ", request.form)
        data = request.form
        

        if len(data['vitri_x']):
            vitri_x = float(data['vitri_x'])
        else:
            vitri_x = 0
        if len(data['vitri_y']):
            vitri_y = float(data['vitri_y'])
        else:
            vitri_y = 0
        if len(data['vitri_z']):
            vitri_z = float(data['vitri_z'])
        else:
            vitri_z = 0
        if len(data['phi']):
            phi = float(data['phi'])
        else:
            phi = 0
        if len(data['gramma']):
            gramma = float(data['gramma'])
        else:
            gramma = 0
        if len(data['v']):
            v = float(data['v'])
        else:
            v = 0
        
        theta_1 = cal_theta_1(vitri_y, vitri_z)
        theta_5 = cal_theta_5(gramma, theta_1)
        
        theta_2 = cal_theta_2(vitri_x, vitri_y, vitri_z, theta_1)
        theta_3 = cal_theta_3(vitri_x, vitri_y, vitri_z, theta_1, theta_2)
        theta_4 = cal_theta_4(vitri_x, vitri_y, vitri_z, theta_1, theta_2, theta_3)
        
        w_1, w_2, w_3, w_4, w_5 = 6, 7, 8, 9, 10

        data = [theta_1, theta_2, theta_3, theta_4, theta_5, w_1, w_2, w_3, w_4, w_5, vitri_x, vitri_y, vitri_z, phi, gramma, v]
        Connect.insert_data(data)
        return redirect(url_for('controlposition'))

@server.route('/controltheta')
def controltheta():
    result = Connect.show_data()
    # get the lastest result from database
    if len(result) > 0:
        result = result[-1]
    print("Len result: ", len(result))
    return render_template('./controltheta/index.html', result=result)

@server.route('/controltheta', methods=['POST'])
def settheta():
    if request.method == 'POST':
        print("request.form: ", request.form)
        data = request.form
        
        v = 6.0
        if len(data['theta_1']):
            theta_1 = float(data['theta_1'])
        else:
            theta_1 = 0
        if len(data['theta_2']):
            theta_2 = float(data['theta_2'])
        else:
            theta_2 = 0
        if len(data['theta_3']):
            theta_3 = float(data['theta_3'])
        else:
            theta_3 = 0
        if len(data['theta_4']):
            theta_4 = float(data['theta_4'])
        else:
            theta_4 = 0
        if len(data['theta_5']):
            theta_5 = float(data['theta_5'])
        else:
            theta_5 = 0

        vitri_x, vitri_y, vitri_z, phi, gramma = get_pos_p(theta_1, theta_2, theta_3, theta_4, theta_5)
        w_1, w_2, w_3, w_4, w_5 = 6, 7, 8, 9, 10

        data = [theta_1, theta_2, theta_3, theta_4, theta_5, w_1, w_2, w_3, w_4, w_5, vitri_x, vitri_y, vitri_z, phi, gramma, v]
        Connect.insert_data(data)
        return redirect(url_for('controltheta'))


@server.route('/defaultpoints')
def defaultpoints():
    results = Connect.show_data(table_name="MotorDefault")
    
    # get the lastest result from database
    # result = result[-1]
    # print("result: ", results)
    return render_template('./defaultpoints/index.html', results=results)

# edit default points with id
@server.route('/defaultpoints/edit/<int:id>', methods=['GET', 'POST'])
def edit_defaultpoints(id):
    results = Connect.show_data(table_name="MotorDefault")
    
    # get result with id
    for r in results:
        if r[0] == id:
            result = r
    
    if request.method == 'POST':
        data = request.form

        if len(data['vitri_x']):
            vitri_x = float(data['vitri_x'])
        else:
            vitri_x = 0
        if len(data['vitri_y']):
            vitri_y = float(data['vitri_y'])
        else:
            vitri_y = 0
        if len(data['vitri_z']):
            vitri_z = float(data['vitri_z'])
        else:
            vitri_z = 0
        if len(data['phi']):
            phi = float(data['phi'])
        else:
            phi = 0
        if len(data['gramma']):
            gramma = float(data['gramma'])
        else:
            gramma = 0
        if len(data['v']):
            v = float(data['v'])
        else:
            v = 0
        if len(data['position']):
            position = data['position']
        else:
            position = 0
        if len(data['velocity']):
            velocity = data['velocity']
        else:
            velocity = 0
        if len(data['description']):
            description = data['description']
        else:
            description = " "

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

@server.route('/defaultpoints/delete/<int:id>', methods=['GET', 'POST'])
def delete_defaultpoints(id):    
    Connect.delete_data_by_id(id, name_database="MotorDefault")
    return redirect(url_for('defaultpoints'))
    
@server.route('/defaultpoints/add')
def add_defaultpoints():
    return render_template('defaultpoints/add.html')

@server.route('/defaultpoints/add', methods=['POST'])
def add_position():
    if request.method == 'POST':
        data = request.form
        if len(data['vitri_x']):
            vitri_x = float(data['vitri_x'])
        else:
            vitri_x = 0
        if len(data['vitri_y']):
            vitri_y = float(data['vitri_y'])
        else:
            vitri_y = 0
        if len(data['vitri_z']):
            vitri_z = float(data['vitri_z'])
        else:
            vitri_z = 0
        if len(data['phi']):
            phi = float(data['phi'])
        else:
            phi = 0
        if len(data['gramma']):
            gramma = float(data['gramma'])
        else:
            gramma = 0
        if len(data['v']):
            v = float(data['v'])
        else:
            v = 0
        if len(data['position']):
            position = data['position']
        else:
            position = 0
        if len(data['velocity']):
            velocity = data['velocity']
        else:
            velocity = 0
        if len(data['description']):
            description = data['description']
        else:
            description = " "


        theta_1 = cal_theta_1(vitri_y, vitri_z)
        theta_5 = cal_theta_5(gramma, theta_1)

        theta_2 = cal_theta_2(vitri_x, vitri_y, vitri_z, theta_1)
        theta_3 = cal_theta_3(vitri_x, vitri_y, vitri_z, theta_1, theta_2)
        theta_4 = cal_theta_4(vitri_x, vitri_y, vitri_z, theta_1, theta_2, theta_3)
        
        w_1, w_2, w_3, w_4, w_5 = 6, 7, 8, 9, 10
        data = [theta_1, theta_2, theta_3, theta_4, theta_5, w_1, w_2, w_3, w_4, w_5, vitri_x, vitri_y, vitri_z, phi, gramma, v, position, velocity, description]
        Connect.insert_data(data, table_name="MotorDefault")
        return redirect(url_for('defaultpoints'))

@server.route('/defaultpoints/', methods=['POST'])
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
    server.run(debug=True, host='0.0.0.0')
