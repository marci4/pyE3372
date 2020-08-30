from modem_wrapper import ModemConnector

mc = ModemConnector()

mc.get_sms_list()

print(mc.sms_list[0].content)
