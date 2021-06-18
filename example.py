from modem_wrapper import ModemConnector

mc = ModemConnector()

sms_list = mc.get_sms_list()


print(" == COUNT Unread")
print(mc.sms_count_unread())

print(" == FIRST SMS")
print(sms_list[0].content)
print(sms_list[0].phone_number)
