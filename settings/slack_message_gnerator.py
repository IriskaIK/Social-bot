class MessageGeneratorSlack:
	def __init__(self):
		self
	

	def create_block(self, elem, static_option):
		option = static_option.copy()
		text = option['text'].copy()
		option['value'] = elem
		
		text['text'] = elem
		v = text.copy()

		option['text'] = v

		
		return option


	def gen_type_block(self, arr_of_types, static_message, static_option, itstype, current_type, static_empty_message_category):
		print(static_message)
		if len(arr_of_types) != 0:
			if itstype:
				blocks = static_message.copy()
				blocks[0]['element']['options'] = []
				for i in arr_of_types:
					blocks[0]['element']['options'].append(self.create_block(i, static_option.copy()))
				# print(static_message)
				return blocks
			else:
				blocks = static_message.copy()
				blocks[0]['element']['options'] = []
				for i in arr_of_types:
					blocks[0]['element']['options'].append(self.create_block(i, static_option.copy()))
				blocks[2]['accessory']['text']['text'] = current_type
				return blocks
		else:
			blocks = static_empty_message_category.copy()
			blocks[1]['accessory']['text']['text'] = current_type
			return blocks


mg = MessageGeneratorSlack()