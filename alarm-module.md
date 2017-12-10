# Alarm Module

### Description:
You can create an alarm with a name and time. The system will follow it's local time and then start beeping and flashing once the alarm triggers.
Trigger can only be turned off by voice command.
### Specific Creation:
You can create an alarm by saying one of the commands in the Command.txt file. It will then ask for a name and a time to set.
```
Person: Can you create an alarm
- AI asks for name -
Person: School
- AI asks for time -
Person: 7am
- AI creates alarm based on info then displays dashboard
```
### Quick Creation:
You can create an alarm by saying "quick alarm" immediately followed by a time. It will then create the alarm and set a default "Alarm" name to it
```
Person: quick alarm 5pm
- AI creates 5pm alarm labeled 'Alarm' then displays dashboard
```
### Alarm Trigger:
When the alarm goes off, it will beep and flash the alarm time. Can only be turned off by saying a command in the Command.txt file.
```
- Alarm goes off
Person: Turn off alarm
- AI turns off alarm and displays dashboard
```
### Delete All:
By saying a specific command in the Command.txt file, the system will delete all alarms.
```
Person: Delete all alarms
- AI deletes all alarms and displays dashboard
```
### Specific Delete:
By saying a specific command in the Command.txt file, the system will delete a specific alarm. It will ask for the name of the alarm you want to delete right after.
```
Person: Delete a specific alarm
- AI asks for alarm name
Person: School
- AI deletes alarm and displays dashboard
```
