# -*- coding: utf-8 -*-
"""
Created on Fri Aug 19 22:52:54 2022

@author: KatRia
"""
from optparse import Values
import openpyxl
import PySimpleGUI as sg
import pandas as pd
from pandas import *
import numpy as np

sg.theme('Default1')

'''###---READ USER ACCOUNT INFO---###'''
df = pd.read_excel('ivcbcm_db.xlsx')

'''###---USER LOGIN---###'''
def login():
    layout = [
        [sg.Text('Username:', size=(15,1), text_color='#181E50', font=("", 15, 'bold')), sg.InputText(key='username')],
        [sg.Text('Password:', size=(15,1), text_color='#181E50', font=("", 15, 'bold')), sg.InputText(key='password', password_char='\u25CF')],
        [sg.Button('Submit', key='submit_login', size=(6,1), mouseover_colors=('white', '#181E50'), border_width=2,font=("", 12, 'bold')),
         sg.Button('back',size=(6,1), mouseover_colors=('white', '#181E50'), border_width=2,font=("", 12, 'bold')), 
        # sg.Button('forgot password',key='fg_pw',size=(15,1), mouseover_colors=('white', '#181E50'), border_width=2,font=("", 12, 'bold')) 
         ],
    ]
    return sg.Window("USER LOGIN", layout, finalize=True, element_justification='c')
    
'''###--USER SIGNUP---###'''
def signup():
    layout = [
        [sg.Text('Employee ID:', size=(15,1), text_color='#181E50', font=("", 15, 'bold')), sg.InputText(key='employee_id')],
        [sg.Text('Nickname:', size=(15,1), text_color='#181E50', font=("", 15, 'bold')), sg.InputText(key='nickname')],
        [sg.Text('Username:', size=(15,1), text_color='#181E50', font=("", 15, 'bold')), sg.InputText(key='username')],
        [sg.Text('Password:', size=(15,1), text_color='#181E50', font=("", 15, 'bold')), sg.InputText(key='password', password_char='\u25CF')],
        [sg.Text('Confirm Password:', size=(15,1), text_color='#181E50', font=("", 15, 'bold')), sg.InputText(key='conf_password', password_char='\u25CF')],
        [sg.Button('Submit', key='submit_signup',size=(6,1), mouseover_colors=('white', '#181E50'), border_width=2,font=("", 12, 'bold') ), 
         sg.Button('back',size=(6,1), mouseover_colors=('white', '#181E50'), border_width=2,font=("", 12, 'bold')) ],
    ]
    return sg.Window("USER SIGNUP", layout, finalize=True, element_justification='c')

'''###---FORGOT PASSWORD (MIGHT ADD FOR FUTURE REF)---###'''
'''def forgot_pw():
    layout = [
        [sg.Text('Employee ID:', size=(20,1), text_color='#181E50', font=("", 15, 'bold')), sg.InputText(key='employee_id')],
        [sg.Text('Username:', size=(20,1), text_color='#181E50', font=("", 15, 'bold')), sg.InputText(key='username', password_char='\u25CF')],
        [sg.Button('Submit', key='submit_change', size=(6,1), mouseover_colors=('white', '#181E50'), border_width=2,font=("", 15, 'bold'))]
    ]
    return sg.Window("FORGOT PASSWORD", layout, finalize=True, element_justification='c')'''

'''###---HOME (LOGIN/SIGNUP)---###'''
def home():
    layout = [
        [sg.Image('ivc_logo.png')], 
        [sg.Text('BAGUIO CENTERMALL', text_color='#181E50', pad=(0,20),font=("", 15, 'bold'))],
        [sg.Button('Login', size=(6,1), mouseover_colors=('white', '#181E50'), border_width=2,font=("", 15, 'bold'))], 
        [sg.Button('Signup', size=(6,1), mouseover_colors=('white', '#181E50'), border_width=2,font=("", 15, 'bold'))],
    ]
    return sg.Window("IVC-BCM INDIVIDUAL SALES", layout, finalize=True, element_justification='c')

window1, window2, window3 = home(), None, None  

'''###---USER SALES DATA---###'''
def data_input():
    '''###---READ USER ACCOUNT---###'''
    df = pd.read_excel('ivcbcm_db.xlsx', index_col = False)
    '''###--LOCATE INPUT USERNAME AND PASSWORD---###'''
    locate_un = df.loc[df['username'] == username]
    locate_pw = df.loc[df['password'] == password]
    '''###---LOCATE USERNAME AND PASSWORD'S EMPLOYEE ID---###'''
    un_id = locate_un['employee_id'].values
    pw_id = locate_pw['employee_id'].values
    '''###---CONVERTED EMPLOYEE ID INTO A PASSABLE/ CALLABLE STRING---###'''
    #converted to string
    user_id = ' '.join(map(str, un_id))
    
    '''###--CHECK IF USERNAME AND PASSWORD'S EMPLOYEE ID ARE EQUAL; IF EQUALM LOCATE THE NICKNAME---###'''
    if un_id == pw_id:
        user_nickname = locate_un['nickname'].values
        u_nick = ' '.join(map(str, user_nickname))

        '''###---READ EXCEL DATA IN ACCORDANCE WITH THEIR USER ID---###'''
        #FOR DROPDOWN DATE
        df = pd.read_excel('indiv_sales_summary.xlsx', sheet_name= user_id)
        date_list = df['MONTH, YR'].values.tolist()

        '''###---USER SALES DATA UI---###'''
        def user_sales_data():  
            sg.theme('DarkBlue3')
            layout = [
                [sg.Text('EMPLOYEE SALES DATA',size=(30,1),font=("", 20, 'bold'), justification='center', relief=sg.RELIEF_SOLID)],
                #name/ nickname
                [sg.Text('NAME:', size=(5,1), pad=(2,15),font=("",12,'bold')), sg.InputText(u_nick, key='user_name', disabled=True, size=(15,1), font=("",12,'bold')), 
                    sg.Text('EMPLOYEE ID:', size=(12,1),font=("",12,'bold')), sg.InputText(user_id, key='user_id', disabled=True, size=(15,1), font=("",12,'bold'))
                ],
                #dropdown for month, year
                [sg.Text('MO,YR:', size=(10,1), pad=(5,5), font=("",12,'bold')), sg.Combo(date_list,key='date', enable_events=True, size=(20, 1), font=("",12,'bold')), 
                    sg.Button('retrieve', key='retrieve', size=(6,1), mouseover_colors=('white', '#181E50'), border_width=2,font=("", 12, 'bold'))],
                #total sales
                [sg.Text('TOTAL SALES:', size=(20,1), pad=(5,5), font=("",12,'bold')), sg.InputText(key='total_sales', disabled=True, size=(25,1), font=("",12,'bold'))],
                #equivalent of total sales
                [sg.Text('SALES EQUIVALENT:', size=(20,1), pad=(5,5),font=("",12,'bold')), sg.InputText(key='equivalent', disabled=True, size=(25,1), font=("",12,'bold'))],
                #grand total
                [sg.Text('GRAND TOTAL:', size=(20,1), pad=(5,5),font=("",12,'bold')), sg.InputText(key='grand_total', disabled=True, size=(25,1), font=("",12,'bold'))],

                [sg.Text('_'  * 72)],
                [sg.Text('ADD-ONS', size=(20,1), pad=(5,5),font=("",15,'bold'))],
                #frames
                [sg.Text('FRAMES:', key='FRAMES', size=(20,1), pad=(5,5),font=("",12,'bold')), sg.InputText(key='frames',disabled=True, size=(25,1), font=("",12,'bold'))],
                #lens
                [sg.Text('LENS:', key='LENS', size=(20,1), pad=(5,5),font=("",12,'bold')), sg.InputText(key='lens',disabled=True, size=(25,1), font=("",12,'bold'))],
                #contact lens
                [sg.Text('CONTACT LENS:', key='CONTACT LENS', size=(20,1), pad=(5,5),font=("",12,'bold')), sg.InputText(key='cl',disabled=True, size=(25,1), font=("",12,'bold'))],
                #sodexho
                [sg.Text('SODEXHO:', key='SODEXHO', size=(20,1), pad=(5,5),font=("",12,'bold')), sg.InputText(key='sodexho',disabled=True, size=(25,1), font=("",12,'bold'))],
                [sg.Text(' '  * 20)],
                [sg.Button('Logout', size=(6,1), mouseover_colors=('white', '#181E50'), border_width=2,font=("", 15, 'bold'))],
            ]
            return sg.Window("IVC-BCM EMPLOYEE SALES DATA", layout, finalize=True, element_justification='c')
        
        user_sales_data()

    '''###---IF USERNAME AND PASSWORD'S EMPLOYEE ID DOES NOT MATCH, MEANING INCORRECT INPUT---###'''
    if (un_id != pw_id) or (pw_id != un_id):
        sg.popup('ERROR! INCORRECT USERNAME OR PASSWORD')
 
 
'''###---LOGGING OUT EXCEPTION---###'''
def logging_out():
    layout = [
        [sg.Text('Are you sure you want to log-out of your account?', text_color='#181E50', pad=(0,20),font=("", 15, 'bold'))],
        [sg.Button('Yes', size=(6,1), mouseover_colors=('white', '#181E50'), border_width=2,font=("", 15, 'bold')), 
        sg.Button('No', size=(6,1), mouseover_colors=('white', '#181E50'), border_width=2,font=("", 15, 'bold'))],
    ]
    return sg.Window("IVC-BCM INDIVIDUAL SALES", layout, finalize=True, element_justification='c')

'''###---WHILE STATEMENT FOR CODE'S FUNCTIONALITY---###'''
while True:
    window, event, values = sg.read_all_windows()
    if event == sg.WIN_CLOSED or event == 'Close':
        window.close()
        if window == window2:     #if closing win2, mark as closed
            window2 == None
        if window == window3:     #if closing win3, mark as closed
            window3 == None
        if window == window1:     #if closing win1, exit program
            quit()
    #LOGIN FUNCTION
    if event == 'Login':
        login()
    #SIGNUP FUNCTION
    if event == 'Signup':
        signup()
    #VALIDATION FOR SUBMITTING SIGNUP INFORMATION
    if event == 'submit_signup':
        employee_id, nickname, username, password, conf_password = values['employee_id'], values['username'], values['nickname'], values['password'], values['conf_password']    

        if employee_id == '':
            sg.popup('Error! Input Text must not be empty!')
        else:
            try: 
                value = int(employee_id)
            except: 
                sg.popup('ERROR! Must be an Integer or Number!')
        
        if (nickname == '' and username == '') or (nickname == '' or username ==''):
            sg.popup('Error! Input Text must not be empty!')

        if (password == '' and conf_password == '') or (password == '' or conf_password ==''):
            sg.popup('Error! Input Text must not be empty!')
        else:
            if (conf_password != password) and (password != '' and conf_password !=''):
                sg.popup('ERROR! Password does not match!')
            if (conf_password == password) and (password != '' and conf_password !='') and (employee_id!='' and nickname!='' and username!=''):
                sg.popup('WELCOME! ' + nickname + '. \n You have successfully Created an Account!',  text_color='#181E50',font=("", 15, 'bold'))
                
        if employee_id not in df.values:
            df = df.append(values, ignore_index = True)
            df.to_excel('ivcbcm_db.xlsx', index = False)
        
    #VALIDATION FOR SUBMITTING LOGIN INFORMATION     
    if event == 'submit_login':
        username, password = values['username'], values['password']

        if (username == '' and password ==''):
            sg.popup('ERROR! Input Text must not be empty!')

        if (username == ''):
            window['username'].update(background_color='red')  
        if (password == ''):
            window['password'].update(background_color='red')

        if username != '':
            window['username'].update(background_color='white')
        if password != '':
            window['password'].update(background_color='white')

        #data validate if exists in database  ... and if not...  
        if username not in df.values or password not in df.values :
            sg.popup('ERROR! user does not exist!')
        else:
            data_input()

    #FUTURE REFERENCE FOR CHANGE PASSWORD/ FORGOT PASSWORD
    '''if event == 'submit_change':
        employee_id, username = values['employee_id'], values['username']

        if (password == '' and username == '') or (password == '' or username ==''):
            sg.popup('Error! Input Text must not be empty!')

        if employee_id in df.values and username in df.values:
            print('yes')
    '''            
        
    #CLOSE WINDOW IF BUTTON BACK
    if event == 'back':
        window.close()              

    #CALL LOGOUT FUNCTION TO PERFORM CERTAIN ACTION VALIDATIONS
    if event == 'Logout':
        logging_out()
    #CLOSE ENTIRE SYSTEM/ PROGRAM
    if event == 'Yes':
        break
    #CLOSES LOGGING OUT VALIDATION WINDOW
    if event == 'No':
        window.close()

    #WHEN BUTTON RETRIEVE IS CLICKED
    if event == 'retrieve':
        #GET MONTH, YR
        month = values['date']
        #print('date chosen: ', month)

        #GET USER ID
        user_id = values['user_id']
        #print('user id: ', user_id)

        #READ EMPLOYEE SALES DATA AGAIN FROM THEIR SHEET ID
        df1 = pd.read_excel('indiv_sales_summary.xlsx', sheet_name=user_id)
        
        #LOCATE THE SELECTED MONTH, AND GET ENTIRE ROW OF DATA
        locate_date = df1.loc[df1['MONTH, YR'] == month]
        #print(locate_date)
        
        #LOCATE THE VALUES PER COLUMN, AND SAVED IN A VARIABLE
        total_sales = locate_date['TOTAL SALES'].values
        equivalent = locate_date['EQUIVALENT'].values
        grand_total = locate_date['GRAND TOTAL'].values
        frames = locate_date['FRAMES'].values
        lens = locate_date['LENS'].values
        contact_lens = locate_date['CONTACT LENS'].values
        sodexho = locate_date['SODEXHO'].values

        #CONVERTED CELL VALUES INTO STRINGS
        ts = ' '.join(map(str, total_sales))
        e = ' '.join(map(str, equivalent))
        gt = ' '.join(map(str, grand_total))
        f = ' '.join(map(str, frames))
        l = ' '.join(map(str, lens))
        c_l = ' '.join(map(str, contact_lens))
        s = ' '.join(map(str, sodexho))
    
        #UPDATE WINDOW FROM USER SALES DATA BASED ON RETRIEVED SALES VALUE FROM THE CHOSEN MONTH, YR
        window['total_sales'].update(value=ts)
        window['equivalent'].update(value=e)
        window['grand_total'].update(value=gt)
        window['frames'].update(value=f)
        window['lens'].update(value=l)
        window['cl'].update(value=c_l)
        window['sodexho'].update(value=s)

window.close()  














