from sympy.parsing.sympy_parser import *
from sympy import *
import PySimpleGUI as sg
from PIL import Image
import os
import io
from predict_fnc import prediction
from IPython.display import display, Latex
import matplotlib.pyplot as plt

file_types = [("JPEG (*.jpg)", "*.jpg"),
              ("All files (*.*)", "*.*")]


transformations = standard_transformations + (implicit_multiplication, implicit_application, convert_equals_signs)

sg.theme('LightGreen3')

menu_def = [
    ['Help', ['About...', 'Formulas']],
]

sg.set_options(font=('Arial Bold', 16))

right_click_menu = ['', ['Copy']]

left_column = [
[
    sg.Text("Choose file"),
    sg.Input(size=(15, 1), key="-FILE-"),
    sg.FileBrowse(file_types=file_types, button_text='...'),
    sg.Button("OK"),
    ],
    [sg.Image(key="-IMAGE-")],
]

right_column = [
    [sg.Text('Predicted expression:')],
    [sg.InputText('', key='expression', size=(30,1))],
    [sg.Button('To LaTeX', key='translate')],
    [sg.Output(size=(30,3), key='output', right_click_menu=right_click_menu)],
    [sg.Image(key='-IMG-')]
]

def main():

    

    layout = [
        [sg.Menu(menu_def, tearoff=False)],
        [
            sg.Column(left_column, element_justification='center'),
            sg.VSeparator(),
            sg.Column(right_column, element_justification='center')
            ]
    ]
    window = sg.Window('LaTeX', layout, element_padding=(10,10), resizable=True, margins=(0,0))

    while True:
        event, values = window.read()

        if event == sg.WINDOW_CLOSED:
            break

        if event == "OK":
            filename = values["-FILE-"]
            if os.path.exists(filename):
                image = Image.open(values["-FILE-"])
                image.thumbnail((400, 400))
                bio = io.BytesIO()
                image.save(bio, format="PNG")
                window["-IMAGE-"].update(data=bio.getvalue())
   
                window['expression'].update(prediction(filename))
                
        if event == 'translate':
            try:
                window['output'].update('')
                window['output'].update(latex(parse_expr(values['expression'], 
                                       transformations = transformations, 
                                       evaluate=False)))
                
                tex = '$'+latex(parse_expr(values['expression'], 
                                        transformations = transformations, 
                                        evaluate=False))+'$'

                fig = plt.figure()
                ax = fig.add_axes([0,0,1,1])
                ax.set_axis_off()
                t = ax.text(0.5, 0.5, tex,
                        horizontalalignment='center',
                        verticalalignment='center',
                        fontsize=20, color='black')
                ax.figure.canvas.draw()
                bbox = t.get_window_extent()
                fig.set_size_inches(bbox.width/80,bbox.height/80) # dpi=80
                plt.savefig('latex.png', dpi=300)

                image = Image.open('latex.png')
                image.thumbnail((400, 400))
                bio = io.BytesIO()
                image.save(bio, format="PNG")
                window["-IMG-"].update(data=bio.getvalue())             

            except:
                print('Cинтаксическая ошибка. Попробуйте исправить выражение.')

        
        if event == 'About...':
            sg.popup('About this app:', 'Version 1.0', 'Developed by: K.Pakhomova')

        if event =='Formulas':
            sg.popup('Trigonometry: sin(x+pi/3)',
            'Limit: Limit(Expression, variable, ->)', 'Power: x**2', 'Division: a/b', title='Formulas')
        
        
        if event == 'Copy':
            widget = window.find_element_with_focus().widget
            text = widget.selection_get()
            window.TKroot.clipboard_clear()
            window.TKroot.clipboard_append(text)
            with open ('latex_expression.txt', 'a') as f:
                f.write(text+'\n'+'\n')


    window.close()


if __name__ == "__main__":
    main()