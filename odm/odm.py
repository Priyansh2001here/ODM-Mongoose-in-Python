from typing import Any, Dict, Sequence


class Validator(object):

    __PRIMITIVE_TYPES = frozenset((int, str, bool, float))
    __SEQUENCE_TYPES = frozenset((dict, list))

    @staticmethod
    def __primitive_type_checker(odm_type, obj_value):
        if odm_type == type(obj_value):
            return True

        return False

    def __dict_check(self, obj_value: Dict[str, Any], odm_type):
        for key, value in obj_value.items():

            valid_value_type = odm_type[key]

            try:
                if valid_value_type in self.__PRIMITIVE_TYPES:
                    if type(value) != valid_value_type:
                        return False

                elif str(type(valid_value_type)) == "<class 'typing._GenericAlias'>":

                    if valid_value_type.__origin__ == list:

                        is_valid = self.__list_check(value, valid_value_type)
                        if not is_valid:
                            return False
            except TypeError as _:

                if type(valid_value_type) == dict:
                    values = obj_value.get(key)

                    is_valid = self.__dict_check(values, valid_value_type)
                    if not is_valid:
                        return False

        return True

    def __list_check(self, obj_value: Sequence[Any], odm_type):
        args_type = odm_type.__args__[0]

        if str(type(args_type)) == "<class 'typing._GenericAlias'>":

            if args_type.__origin__ == list:

                for i in obj_value:
                    is_valid = self.__list_check(i, args_type)

                    if not is_valid:
                        return False
                return True

        elif args_type in self.__PRIMITIVE_TYPES:

            try:
                for i in obj_value:
                    is_valid = self.__primitive_type_checker(args_type, i)
                    if not is_valid:
                        return False

            except TypeError as _:
                return False

            return True

    def validate(self, my_odm: Dict[Any, Any], my_obj: Dict[Any, Any]):

        """
        :param my_odm: takes odm defines as dictionary
        :param my_obj: takes data that needs to be validated
        :return: returns True if types defined in odm matches data
        """

        for key, value in my_obj.items():

            value_type = type(value)

            if value_type in self.__PRIMITIVE_TYPES:

                is_valid = self.__primitive_type_checker(my_odm[key], value)

                if not is_valid:
                    return False

            if value_type in self.__SEQUENCE_TYPES:

                odm_value_type = my_odm[key]

                if str(type(odm_value_type)) == "<class 'typing._GenericAlias'>":
                    if odm_value_type.__origin__ == value_type == list:
                        is_valid = self.__list_check(value, odm_value_type)
                        if not is_valid:
                            return False

                    else:
                        return False

                elif type(odm_value_type) == value_type == dict:
                    is_valid = self.__dict_check(value, odm_value_type)
                    if not is_valid:
                        return False

                elif odm_value_type == Any:
                    continue

        return True
