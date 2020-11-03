from typing import List, Any, Dict, Sequence

PRIMITIVE_TYPES = frozenset((int, str, bool, float))
SEQUENCE_TYPES = frozenset((dict, list))


def primitive_type_checker(odm_type, obj_value):
    if odm_type == type(obj_value):
        return True

    return False


def dict_check(obj_value: Dict[str, Any], odm_type):
    # print(f'args {obj_value, odm_type}')

    valid_key_type, valid_value_type = odm_type.__args__
    print(valid_key_type, valid_value_type)

    if valid_value_type not in PRIMITIVE_TYPES or valid_key_type not in PRIMITIVE_TYPES:
        return False

    for key, value in obj_value.items():

        value_type = type(value)
        if value_type not in PRIMITIVE_TYPES and value_type not in SEQUENCE_TYPES:
            return False

        else:
            # odm_value_type = odm_type[key]
            # print(f'valid odm type {odm_value_type} odm type in args {odm_type}')
            # print(f'key -> {key} value {value} dict {odm_type.__args__} orignin {odm_type.__origin__}')
            if type(key) != valid_key_type or value_type != valid_value_type:
                return False

    return True


def list_check(obj_value: Sequence[Any], odm_type):
    """
    :param obj_value: takes all the list values example [1,2,3,4]
    :param odm_type: takes what type of list is this example List[int]
    :return:
    """
    args_type = odm_type.__args__[0]

    if str(type(args_type)) == "<class 'typing._GenericAlias'>":

        if args_type.__origin__ == list:

            for i in obj_value:
                is_valid = list_check(i, args_type)

                if not is_valid:
                    return False
            return True

    elif args_type in PRIMITIVE_TYPES:

        try:
            for i in obj_value:
                is_valid = primitive_type_checker(args_type, i)
                if not is_valid:
                    return False

        except TypeError as _:
            return False

        # if args_type != type(obj_value):
        #     return False

        return True


def check(my_odm: Dict[Any, Any], my_obj: Dict[Any, Any]):
    for key, value in my_obj.items():

        value_type = type(value)

        if value_type in PRIMITIVE_TYPES:

            is_valid = primitive_type_checker(my_odm[key], value)

            if not is_valid:
                return False

        if value_type in SEQUENCE_TYPES:

            odm_value_type = my_odm[key]
            if odm_value_type.__origin__ == value_type == list:
                is_valid = list_check(value, odm_value_type)
                if not is_valid:
                    return False

            elif odm_value_type.__origin__ == value_type == dict:
                is_valid = dict_check(value, odm_value_type)
                if not is_valid:
                    return False

            else:
                return False

    return True


d = {
    'name': Dict[str, int]
}

da = {
    'name': {
        'name_2': 'Priyansh'
    }
}

print(check(d, da))
