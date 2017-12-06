# Chatbot Module

### Description:
The chatbot listens and based on replies in XML files will respond accordingly.

### Generic Replies:
Generic conversations like "hello" or "hi" will select a random reply from the XML file. This gives the AI the appearance of being unique.

### Adding Conversations:
You can add your own conversations to the chatbot. First navigate to the API/chatbot folder. Within the folder select the XML file you wish to add a conversation to.
The XML system works as follows
```
<greeting_specific>
<human id="1">good morning</human>
<human id="2">good day</human>
<human id="3">hello how are you</human>
<human id="4">what is your name</human>
<response_list>
<response id="1">Good Morning.</response>
<response id="2">Good Day.</response>
<response id="3">Hello. I am doing well. How about you?</response>
<response id="4">My name is { ai_name }</response>
</response_list>
</greeting_specific>
```
* human = Contains what the accepted human question or sentence is

* human id = Used to match to a corresponding reply

* response = Contains the reply that you want to be spoken

* response id = Must match id of human id that you want to go together

* { ai_name } = The system will replace this with the object in question. In this case it would be the name of the ai.

### Acceptable Replaceable Objects:

* { ai_name } = Name of the AI
* { ai_gender } = Gender of the AI