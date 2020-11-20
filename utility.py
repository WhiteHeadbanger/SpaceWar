############################ EXAMPLES ############################

#stack = [("move", 1, 2), ("move", 1, 2), ("move", 1, 2), ("move", 1, 1), ("move", 1, 1), ("move", 1, 1)]  # stack_aux1 = stack_aux2
#stack = [("move", 1, 2), ("move", 1, 2), ("move", 1, 1), ("move", 1, 1), ("move", 1, 1), ("move", 1, 1)] # stack_aux1 > stack_aux1
stack = [("move", 1, 2), ("move", 1, 2), ("move", 1, 2), ("move", 1, 2), ("move", 1, 1), ("move", 1, 1)] # stack_aux1 < stack_aux2

############################ EXAMPLES ############################

def utility(original_stack):
    # If the stack only contains one actions, then return the stack without processing.
    if len(original_stack) < 2:
        return original_stack
    # Grabs the self object and creates a set of self objects. 
    set_aux = []
    for tuple_objects in original_stack:
        set_aux.append(tuple_objects[2])
    _set = set(set_aux)
    # Transforms the set into a list
    set_to_list = list(_set)

    # Iterates over original_stack and separates it in two lists, one for the first ship and the other for the other one. 
    stack_aux1 = [x for x in original_stack if x[2] == set_to_list[0]]
    stack_aux2 = [x for x in original_stack if x[2] == set_to_list[1]]

    # We want to know the lenght of the two lists because we need to iterate over the bigger one in loop() function
    len_1 = len(stack_aux1)
    len_2 = len(stack_aux2)
    
    final_stack = []
    if len_1 > len_2:
        final_stack = loop(stack_aux1, stack_aux2)
    elif len_1 < len_2:
        final_stack = loop(stack_aux2, stack_aux1)
    else:
        #If stack_aux1 = stack_aux2, zip() them and append to the final_stack list
        for item1, item2 in zip(stack_aux1, stack_aux2):
            final_stack.append(item1)
            final_stack.append(item2)
    
    return final_stack

def loop(bigger_stack, shorter_stack):
    response_list = []
    for x in range(len(bigger_stack)):
        response_list.append(bigger_stack[0])
        bigger_stack.pop(0)
        # If shorter_stack is 0, this last three lines won't be executed. 
        if len(shorter_stack) > 0:
            response_list.append(shorter_stack[0])
            shorter_stack.pop(0)
        
    return response_list
            

print(utility(stack))
