import openai

openai.api_key = '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'

messages = [ {"role": "system", "content":
			"You are a intelligent assistant."} ]
while True:
	message = input("User : ")
	if message:
		messages.append(
			{"role": "user", "content": message},
		)
		chat = openai.ChatCompletion.create(
			model="gpt-3", messages=messages
		)
	reply = chat.choices[0].message.content
	print(f"ChatGPT: {reply}")
	messages.append({"role": "assistant", "content": reply})
