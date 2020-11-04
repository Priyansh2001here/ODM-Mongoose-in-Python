from typing import List, Any, Dict, Sequence

PRIMITIVE_TYPES = frozenset((int, str, bool, float))
SEQUENCE_TYPES = frozenset((dict, list))


def primitive_type_checker(odm_type, obj_value):
    if odm_type == type(obj_value):
        return True

    return False


def dict_check(obj_value: Dict[str, Any], odm_type):
    for key, value in obj_value.items():

        valid_value_type = odm_type[key]

        try:
            if valid_value_type in PRIMITIVE_TYPES:
                if type(value) != valid_value_type:
                    return False

            elif str(type(valid_value_type)) == "<class 'typing._GenericAlias'>":

                if valid_value_type.__origin__ == list:

                    is_valid = list_check(value, valid_value_type)
                    if not is_valid:
                        return False
        except TypeError as _:

            if type(valid_value_type) == dict:
                values = obj_value.get(key)

                is_valid = dict_check(values, valid_value_type)
                if not is_valid:
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

            if str(type(odm_value_type)) == "<class 'typing._GenericAlias'>":
                if odm_value_type.__origin__ == value_type == list:
                    is_valid = list_check(value, odm_value_type)
                    if not is_valid:
                        return False

                else:
                    return False

            elif type(odm_value_type) == value_type == dict:

                # ({'name_2': 'Priyansh'}, {'name_2': <class 'str'>})

                is_valid = dict_check(value, odm_value_type)
                if not is_valid:
                    return False

            elif odm_value_type == Any:
                continue

    return True
