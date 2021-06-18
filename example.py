from modem_wrapper import ModemConnector

mc = ModemConnector()

mc.get_sms_list()


print(" == COUNT")
print(mc.sms_count())

print(" == COUNT")
print(mc.sms_count())

print(mc.sms_list[0].content)
print(mc.sms_list[0].phone_number)
