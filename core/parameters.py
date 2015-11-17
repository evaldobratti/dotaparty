from models import Parameter


class AbstractParameterManagement(object):

    def __init__(self, parameter_name, default_value):
        self.__parameter_name = parameter_name
        self.__default_value = default_value

    def _get_parameter(self):
        try:
            return Parameter.objects.get(name=self.__parameter_name)
        except Parameter.DoesNotExist:
            return Parameter.objects.create(name=self.__parameter_name,
                                            value=self.default_value())

    def value(self):
        return self._get_parameter().value

    def reset(self):
        parameter = self._get_parameter()
        parameter.reset()
        parameter.save()

    def default_value(self):
        return self.__default_value


class ParameterListManagement(AbstractParameterManagement):

    def __init__(self, parameter_name, default_value):
        super(ParameterListManagement, self).__init__(parameter_name, default_value)

    def value(self):
        return eval(self._get_parameter().value)

    def add_value(self, account_id):
        value = self.value()
        if account_id in value:
            return

        value.append(account_id)

        parameter = self._get_parameter()
        parameter.value = str(value)
        parameter.save()

    def default_value(self):
        return str(super(ParameterListManagement, self).default_value())


class SimpleParameterManagement(AbstractParameterManagement):

    def __init__(self, parameter_name, default_value):
        super(SimpleParameterManagement, self).__init__(parameter_name, default_value)

    def set_value(self, value):
        parameter = self._get_parameter()
        parameter.value = str(value)
        parameter.save()


INTERESTED_ACCOUNTS_IDS = ParameterListManagement('InterestedAccountsIds', [])
LAST_MATCH_SEQ_NUM = SimpleParameterManagement('LastMatchSeqNum', None)




