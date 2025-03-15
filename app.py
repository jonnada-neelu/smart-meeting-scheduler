# Application
from datetime import datetime, timedelta
import calendar

class SmartMeetingScheduler:
    def __init__(self):
        self.working_hours = ("9 AM", "5 PM")  
        self.public_holidays = {
            "2025-01-01", "2025-12-25"  
        }
        self.schedule = {}     
    def is_working_day(self, date_str):
        date_obj = datetime.strptime(date_str, "%Y-%m-%d")
        return date_obj.weekday() < 5 and date_str not in self.public_holidays

    def convert_to_24_hour(self, time_str):
        return datetime.strptime(time_str, "%I %p").hour

    def convert_to_12_hour(self, hour):
        return datetime.strptime(str(hour), "%H").strftime("%I %p")

    def schedule_meeting(self, user, date_str, start_time, end_time):
        start_hour = self.convert_to_24_hour(start_time)
        end_hour = self.convert_to_24_hour(end_time)

        working_start = self.convert_to_24_hour(self.working_hours[0])
        working_end = self.convert_to_24_hour(self.working_hours[1])

        if not self.is_working_day(date_str):
            return "Cannot schedule on weekends or public holidays."
        
        if start_hour < working_start or end_hour > working_end:
            return "Meeting must be within working hours."
        
        if user not in self.schedule:
            self.schedule[user] = []
        
        new_meeting = (start_hour, end_hour)
        for existing_meeting in self.schedule[user]:
            if not (new_meeting[1] <= existing_meeting[0] or new_meeting[0] >= existing_meeting[1]):
                return "Meeting time overlaps with an existing meeting."
        
        self.schedule[user].append(new_meeting)
        self.schedule[user].sort()
        return "Meeting scheduled successfully."
    
    def get_available_slots(self, user, date_str):
        if not self.is_working_day(date_str):
            return "No available slots on weekends or public holidays."
        
        booked_slots = self.schedule.get(user, [])
        available_slots = []
        
        current_time = self.convert_to_24_hour(self.working_hours[0])
        for start, end in sorted(booked_slots):
            if current_time < start:
                available_slots.append((self.convert_to_12_hour(current_time), self.convert_to_12_hour(start)))
            current_time = end
        
        working_end = self.convert_to_24_hour(self.working_hours[1])
        if current_time < working_end:
            available_slots.append((self.convert_to_12_hour(current_time), self.convert_to_12_hour(working_end)))
        
        return available_slots if available_slots else "No available slots."
    
    def view_scheduled_meetings(self, user):
        meetings = self.schedule.get(user, [])
        if not meetings:
            return "No meetings scheduled."

        formatted_meetings = [(self.convert_to_12_hour(start), self.convert_to_12_hour(end)) for start, end in meetings]
        return formatted_meetings

scheduler = SmartMeetingScheduler()
print(scheduler.schedule_meeting("Neelu", "2025-03-20", "9 AM", "11 AM"))
print(scheduler.get_available_slots("Neelu", "2025-03-20"))
print(scheduler.view_scheduled_meetings("Neelu"))
