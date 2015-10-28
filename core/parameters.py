from models import Parameter


class AbstractParameterManagement(object):

    def __init__(self, parameter_name):
        self.__parameter_name = parameter_name

    def __get_parameter(self):
        return Parameter.objects.get(name=self.__parameter_name)

    def value(self):
        return self.__get_parameter().value

    def reset(self):
        parameter = self.__get_parameter()
        parameter.reset()
        parameter.save()


class ParameterListManagement(AbstractParameterManagement):

    def __init__(self, parameter_name):
        super(ParameterListManagement, self).__init__(parameter_name)

    def value(self):
        return eval(self.__get_parameter().value)

    def add_value(self, account_id):
        value = self.get_list_value()
        if account_id in value:
            return

        value.append(account_id)

        parameter = self.__get_parameter()
        parameter.value = str(value)
        parameter.save()


class SimpleParameterManagement(AbstractParameterManagement):

    def set_value(self, value):
        parameter = self.__get_parameter()
        parameter.value = str(value)
        parameter.save()


INTERESTED_ACCOUNTS_IDS = ParameterListManagement('InterestedAccountsIds')
LAST_MATCH_SEQ_NUM = SimpleParameterManagement('LastMatchSeqNum')




