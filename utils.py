# Returns a string created from the concatenation of a list
def list_to_string(received_list, separator = "\n"):
    return separator.join(received_list)


# Divides a big list to show on Discord embed (returns a list of strings)
def divide_big_list(received_list, separator = "\n", list_amount = 3):
    list_length = len(received_list)
    list_separator = list_length // list_amount

    strings_list = []

    counter = 0
    for i, element in enumerate(received_list):
        if (i == list_separator):
            counter+=1
            list_separator+=list_separator
        if (len(strings_list) <= counter):
            strings_list.append(element)
        else:
            strings_list[counter] = strings_list[counter] + separator + element
        

    return strings_list

