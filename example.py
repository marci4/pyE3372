from modem_wrapper import ModemConnector

mc = ModemConnector()

sms_list = mc.get_sms_list()

print(" == COUNT Unread")
print(mc.sms_count_unread())

print(" == FIRST SMS")
print(sms_list[0].content)
print(sms_list[0].phone_number)


print(" == READ first SMS")
print(mc.sms_set_read(sms_list[0].index))

print(" == DELETE first SMS")
print(mc.sms_delete(sms_list[0].index))
