from modem_wrapper import ModemConnector

mc = ModemConnector()

mc.get_sms_list()


print(" == COUNT Unread")
print(mc.sms_count_unread())

print(" == COUNT")
print(mc.sms_count_unread())

print(mc.sms_list[0].content)
print(mc.sms_list[0].phone_number)
