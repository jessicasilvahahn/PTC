from mqtt.messages.message import Message


class Publish(Message):

    def __init__(self):
        super().__init__()

    def mount_message(self, topic_name, value):
        if(isinstance(topic_name, str) and isinstance(value, str)):
            topic_name_size = b'\x00' + bytes(bytearray([len(topic_name)]))
            self.packet['variable_header'] = topic_name_size + \
                topic_name.encode("utf-8")

            self.packet['payload'] = value.encode("utf-8")

            remaining_size = self.get_remaining_size(
                len(self.packet['variable_header'] + self.packet['payload']))
            if(not remaining_size):
                self.packet = None
            else:
                self.packet['fixed_header'] = b'\x30' + remaining_size
        else:
            print("Topic Name or Topic aren't string\n")
            return 0
