import re


def check_pattern(patt, s):
  if re.match(patt, s) != None:
    return True
  else:
    return False

def regexFunc(st):
  # print('Input string:', st)
  patt_comma = r'(,)(?=\d+)'
  st = re.sub(patt_comma, '.', st)
  # print(st)
  split_patt = r'[-(+=\/><,.]*\w+[()]*'

  split_lst = re.findall(split_patt, st)
  # print(split_lst)

  patt1 = r'[ -=+\/][0-9]*[a-zA-Z]+[0-9]+|[0-9]*[a-zA-Z]+[0-9]+(?=[ ]*)'
  patt2 = r'[ -=+\/]*[0-9]*[a-zA-Z]+[()]*|[0-9]+[a-zA-Z]+(?!\w)(?=[ ]*)'
  patt3 = r'[ -=+\/][0-9]+[()]*(?![a-zA-Z])|[0-9]+'

  new_str = ''

  for i, s in enumerate(split_lst):
    if check_pattern(patt1, s):
      # print(s, 'is pattern 1')
      split_str = list(s)
      for j, l in enumerate(split_str):
        if (split_str[j-1].isalpha() and split_str[j].isdigit()) \
                              or (split_lst[i-1].endswith(')') \
                              and (s.isdigit() or s.isalpha()) and i>0):
          new_str += ''.join(f'**{split_str[j]}')
        
        elif j>0 and (split_str[j-1].isdigit() or split_str[j-1].isalpha())\
                            or (split_str[j-1] == ')' and split_str[j]=='('):
          new_str += ''.join(f'*{split_str[j]}')

        else:
          new_str += ''.join(l)

    elif check_pattern(patt2, s):
      # print(s, 'is pattern 2')
      split_str = list(s)
      for j, l in enumerate(split_str):

        if l.isdigit(): 
          new_str += ''.join(f'{l}*')
        
        elif (split_str[j-1] == ')' and split_str[j]=='(') \
                      or ((split_str[j-1].isdigit() or split_str[j-1].isalpha()) and split_str[j]=='(' and j>0):
          new_str += ''.join(f'*{split_str[j]}')

        elif split_lst[i-1].endswith(')') and (s.isdigit() or s.isalpha()) and i>0:
          new_str +=''.join(f'**{split_lst[i]}')

        else:
          new_str += ''.join(l)  

    elif check_pattern(patt3, s):
    
      split_str = list(s)
      for j, l in enumerate(split_str):
        if split_str[j-1] == ')' and split_str[j]=='(' \
                or ((split_str[j-1].isdigit() or split_str[j-1].isalpha())
                and split_str[j]=='(' and j>0):
          new_str += ''.join(f'*{split_str[j]}')

        elif split_lst[i-1].endswith(')') and (s.isdigit() or s.isalpha()) and i>0:
          new_str +=''.join(f'**{split_lst[i]}')

        else:
          new_str += ''.join(l)

    else:
      new_str += ''.join(s)

  return new_str


def check_expr(string):
  pattern =r'(?P<func>lim|sin|cos|tan|cot|arcsin|arccos|arctan|arccot)'
  str_split = ''
  if check_pattern(pattern, string):
    str_split = re.sub(pattern, r'\g<func> ', string)
    str_split = re.split(' ', str_split)

    for i, s in enumerate(str_split):
      if re.match(pattern, s) != None:
        a = s + ' ' + regexFunc(str_split[i+1])
        return a
  else:
    return regexFunc(string)
  

def check_lim(string):
    if check_pattern(r'lim', string):
        string = re.sub(r'lim', r'Limit', string)
        string = re.sub(r'->', ',', string)
        a = re.split(' ', string)
        str_latex= ' '
        for l in a:
            if l == 'Limit':
                str_latex += ''.join(l)
            else:
                str_latex += ''.join(f'({l})')
        return str_latex
    else:
        return string



def str_to_ltx(string):
    string = check_expr(string)
    string = check_lim(string)
    return string
