-------------
Alarm System
TODO: Fix specific alarm creation
-------------
- Generic Creation
You can create an alarm by saying a generic command from the command.txt file
It will redirect to AlarmRequestView and ask for a name
It will redirect to AlarmRequestNameView set the name and ask for a time
It will redirect to AlarmRequestTimeView set the time and redirect to the dashboard
- Specific Creation
You can create an alarm by saying a specific command from the command.txt file followed by a time
It will parse the time with dateutil.parser and create an alarm then redirect to dashboard
- Alarm Goes Off
If an alarm is currently going off it switches the profile.alarm_active to true
This means that only specific commands can turn off the alarm which are in the command.txt file
If the AlarmCommandRouter gets a valid command it routes to DisableAlarmView and disables the profile.alarm_active, makes the alarm.enabled false and redirects to dashboard
- Delete All
You can delete all alarms by saying a specific command from the command.txt file
It will redirect to the DeleteAllAlarmView and delete all alarms then redirect back to the dashboard
- Delete Specific
You can delete a specific alarm by saying a specific command from the command.txt file
It will redirect to the DeleteAlarmRequestView which will ask for a name of the alarm
It will then redirect to DeleteSpecificAlarmView which will delete all alarms with that name
-------------
Sleep System
-------------
- Enable
You can make the A.I. sleep by saying a specific command from the command.txt file
It will set profile.sleep_active to true which means it will not listen to anything except specific commands to turn it off
- Disable
You can wake up the A.I. by saying a specific command from the command.txt file
It will set profile.sleep_active to false
-------------
Reminder System
TODO: Use global name instead of request.session
TODO: Remove specific reminders
-------------
- Generic Creation
You can create an reminder by saying a generic command from the command.txt file
It will redirect to ReminderRequestView and ask for a name
It will redirect to ReminderView set the name and redirect to the dashboard
- Delete All
You can delete all reminders by saying a specific command from the command.txt file
It will redirect to the DeleteAllReminderView and delete all alarms then redirect back to the dashboard
- Delete First
You can delete a specific alarm by saying a specific command from the command.txt file
It will redirect to the DeleteFirstReminderView which will delete the first reminder on the list and redirect to the dashboard
- Delete Last
You can delete a specific alarm by saying a specific command from the command.txt file
It will redirect to the DeleteLastReminderView which will delete the last reminder on the list and redirect to the dashboard
-------------
Email System
TODO: Display email that they want
-------------
- Dashboard
Number of unread emails get displayed on the dashboard
- Viewing Unread List
You can view a list of unread emails by saying a specific command from the command.txt file
If you wish to view the email you need to remember the unread emails's ID that it was assigned
-------------
Apple System
TODO: Display map of phone
TODO: Add iCal functionality
TODO: Add Gallery functionality
-------------
- Find My iPhone
You can ask a specific command to find your iphone. It will search through all apple devices and find the first device labeled iphone
It will then get all information related to it and display it on the page.
You will then be asked if you want to ping your iphone. If it hears yes, it will ping it. Any other response will end the conversation.
