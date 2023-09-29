import pandas as pd
from datetime import datetime, timedelta

# Function to calculate the time difference between two timestamps
def calculate_time_difference(start_time, end_time):
    return (end_time - start_time).total_seconds() / 3600  # Convert to hours

# Function to check if an employee has worked for 7 consecutive days
def has_worked_consecutive_days(records, index, num_days=7):
    current_employee = records.iloc[index]
    current_date = current_employee['Time'].date()
    
    for i in range(1, num_days):
        prev_employee = records.iloc[index - i]
        prev_date = prev_employee['Time'].date()
        
        if pd.notna(current_date) and pd.notna(prev_date) and (current_date - prev_date).days != 1:
            return False
    
    return True

# Function to check if an employee has less than 10 hours between shifts but greater than 1 hour
def has_short_break(records, index, min_break=1, max_break=10):
    current_employee = records.iloc[index]
    current_end_time = current_employee['Time Out']
    
    for i in range(1, index + 1):
        prev_employee = records.iloc[index - i]
        prev_end_time = prev_employee['Time Out']
        
        if pd.notna(current_end_time) and pd.notna(prev_end_time):
            time_difference = calculate_time_difference(prev_end_time, current_end_time)
            if min_break < time_difference < max_break:
                return True
    
    return False

# Function to check if an employee has worked for more than 14 hours in a single shift
def has_long_shift(record, max_shift_hours=14):
    shift_duration = calculate_time_difference(record['Time'], record['Time Out'])
    return shift_duration > max_shift_hours

# Read the Excel file and parse records using pandas
file_path = 'C:\\Users\\pujar\\Downloads\\Assignment_Timecard.xlsx'  # Replace with your Excel file path
df = pd.read_excel(file_path)

# Keep track of employees who meet each condition
consecutive_days_employees = set()
short_break_employees = set()
long_shift_employees = set()

# Iterate over the records and check conditions
for i in range(7, len(df)):
    if has_worked_consecutive_days(df, i):
        consecutive_days_employees.add((df.at[i, 'Employee Name'], df.at[i, 'Position ID']))
    
    if has_short_break(df, i):
        short_break_employees.add((df.at[i, 'Employee Name'], df.at[i, 'Position ID']))
    
    if has_long_shift(df.iloc[i]):
        long_shift_employees.add((df.at[i, 'Employee Name'], df.at[i, 'Position ID']))

# Print the results for each condition
print("Employees who have worked for 7 consecutive days:")
for employee in consecutive_days_employees:
    print(f"Employee Name: {employee[0]}, Position: {employee[1]}")

print("\nEmployees who have less than 10 hours between shifts but greater than 1 hour:")
for employee in short_break_employees:
    print(f"Employee Name: {employee[0]}, Position: {employee[1]}")

print("\nEmployees who have worked for more than 14 hours in a single shift:")
for employee in long_shift_employees:
    print(f"Employee Name: {employee[0]}, Position: {employee[1]}")
