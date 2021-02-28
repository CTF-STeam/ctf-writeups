import re

'''
:param blob: blob of data to parse through (string)
:param group_name: A single Group name ("Green", "Red", or "Yellow",etc...)

:return: A list of all user names that are part of a given Group
'''
def ParseNamesByGroup(blob, group_name):
    x = re.findall("\[.+?\]", blob)
    #print(x)
    res = []
    for m in x:
        m = m.replace('[', '{').replace(']', '}')
        m = eval(m)
        #print(m)
        if m['Group'] == group_name:
            res.append(m['user_name'])
    return res

data = raw_input()
group_name = data.split('|')[0]
blob = data.split('|')[1]
result_names_list = ParseNamesByGroup(blob, group_name)
print(result_names_list)
