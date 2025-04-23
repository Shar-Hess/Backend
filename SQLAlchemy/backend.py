import functools


logged_in = True

def only_strings(func):
    @functools.wraps(func)
    def decorator_wrapper(*args, **kwargs):
        new_list = args[0]

        for idx, element in enumerate(new_list):
            new_list[idx] = str(element)
        args = (new_list,)

        return func(*args, **kwargs)

    return decorator_wrapper

def auth_logged_in(func):
    @functools.wraps(func)
    def decorator_wrapper(*args, **kwargs):
        if logged_in == False:
            return print("Please Login")
        else: 
            return func(*args, **kwargs)
    return decorator_wrapper


def print_args(func):
    @functools.wraps(func)
    def decorator_wrapper(*args, **kwargs):
        print(func.__name__)
        for idx, e in enumerate(args):
            print(f'{idx}: {e}')
        return func(*args, **kwargs)
    return decorator_wrapper

@auth_logged_in
def sum_num(*args):
    return sum(list(args))

@auth_logged_in
def concatenate_str(*args):
    return " ".join(args)

@auth_logged_in
def sort_list(*args):
    return sorted(list(args))

# print(sum_num(1,2,3))
# print(concatenate_str("hello", "world"))
# print(sort_list(32, 14, 27, 60))

@only_strings
def string_joined(list_of_strings):
    new_list = list_of_strings

    return ",".join(new_list)

lst = ["one", "two", "three", "four", "five", 3]
# print(string_joined(lst))
# print(lst)

def only_strings(func):
    @functools.wraps(func)
    def decorator_wrapper(*args, **kwargs):
        for key in kwargs:
            kwargs[key] = str(kwargs[key])
        return func(*args, **kwargs)
    return decorator_wrapper

@only_strings
def convert_to_str( **kwargs):
    new_list = []

    for val in kwargs.values():
        new_list.append(val)

    return ", ".join(new_list)

joined_str = convert_to_str(kw1=1, kw2="two", kw3=3, kw4="four")
print(joined_str)
print(type(joined_str))