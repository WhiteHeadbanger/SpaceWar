# Funcion para ordenar el stack
# Se necesita refactor pero por ahora funciona

def utility(stack):
    if len(stack) < 2:
        return stack
    set_aux = []
    for i in stack:
        set_aux.append(i[2])
    _set = set(set_aux)
    _list = list(_set)

    stack_aux1 = [x for x in stack if x[2] == _list[0]]
    stack_aux2 = [x for x in stack if x[2] == _list[1]]
    res = []

    if len(stack_aux1) > len(stack_aux2):
        big = 1
    elif len(stack_aux1) < len(stack_aux2):
        big = 2
    elif len(stack_aux1) == len(stack_aux2):
        big = None
    if big == None:
        for item1, item2 in zip(stack_aux1, stack_aux2):
            res.append(item1)
            res.append(item2)
    if big == 1:
        res_len = len_1 - len_2
        new_aux = stack_aux1[-res_len:]
        for i in new_aux:
            res.append(i)
    elif big == 2:
        new_aux = stack_aux1[-res_len:]
        for i in new_aux:
            res.append(i)
    return res

