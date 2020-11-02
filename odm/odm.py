from typing import List, Any, Dict, Sequence

PRIMITIVE_TYPES = frozenset((int, str, bool, float))
SEQUENCE_TYPES = frozenset((dict, list))


def list_check(odm_list: Sequence[Any], odm_type):
    """
    :param odm_list: takes all the list values example [1,2,3,4]
    :param odm_type: takes what type of list is this example List[int]
    :return:
    """

    valid_odm_types: tuple = odm_type.__dict__.get('__args__')

    # print(f'odm list {odm_list} and odm type {odm_type} valid odm types {valid_odm_types}')

    print(f'agrguments {odm_list} {odm_type}')

    for i in odm_list:
        if type(i) not in valid_odm_types:
            if str(type(valid_odm_types[0])) == "<class 'typing._GenericAlias'>":
                valid = valid_odm_types[0].__dict__.get('__args__')
                print('validdddddddddddddddddddddddddddd -> ', valid, valid_odm_types[0])

                return False

            return False
        return True


def check(my_odm: Dict[Any, Any], my_obj: Dict[Any, Any]):
    for name, value in my_obj.items():

        value_type = my_odm[name]
        obj_value_type = type(value)

        if obj_value_type not in PRIMITIVE_TYPES and obj_value_type not in SEQUENCE_TYPES:
            return False

        if obj_value_type == list and value_type.__origin__ == list:
            is_valid = list_check(value, value_type)
            if not is_valid:
                return False
            return True

        if obj_value_type != value_type:
            return False

    return True
