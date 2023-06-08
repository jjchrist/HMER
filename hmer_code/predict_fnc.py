from img_preprocess import np, img_to_lst
from keras.models import load_model
from regexpr import str_to_ltx

labels = ['!', '(', ')', '+', ',', '-', '0', '1', '2', '3', '4', '5', '6', '7', '8', '9', '=', '[', ']', 
'a', 'alpha', 'b', 'beta', 'c', 'd', 'decimal', 'delta', 'div', 'e', 'f', 'g', 'gamma', 'geq', 'gt', 'h', 
'i', 'in', 'infty', 'int', 'j', 'k', 'l', 'lambda', 'leq', 'lt', 'm', 'mu', 'n', 'neq', 'o', 'p', 'phi', 'pi', 'pm', 'q', 'r', 
'rightarrow', 's', 'sigma', 'sum', 't', 'theta', 'u', 'v', 'w', 'x', 'y', 'z', '{', '}']

def img_predict(model, image_file):
    img_arr = np.expand_dims(image_file, axis = 0)
    img_arr = img_arr.reshape((-1, 45, 45, 1))
    pred = model.predict([img_arr], verbose = None)
    res = np.argmax(pred, axis=1)
    return (str(labels[res[0]]))

def check_symbols(symbol):
    if symbol == 'div':
        return '/'
    elif symbol == 'geq':
        return '>='
    elif symbol == 'gt':
        return '>'
    elif symbol == 'leq':
        return '<='
    elif symbol == 'lt':
        return '<'
    elif symbol == 'neq':
        return '!='
    elif symbol == 'pm':
        return '+-'
    elif symbol == 'rightarrow':
        return '->'
    elif symbol == 'int':
        return  'Integral '
    elif symbol == 'infty':
        return 'oo'
    elif symbol == 'decimal':
        return '.'
    else:
        return symbol
    


def img_to_str(model, image_file):
    output = ''
    symbols = img_to_lst(image_file)
    for i in range(len(symbols)):
        symbol = img_predict(model, symbols[i][2])
        output += check_symbols(symbol)
    return output


def prediction(image):
    model = load_model('models/hmer_model.h5')
    out = img_to_str(model, image)
    return str_to_ltx(out)