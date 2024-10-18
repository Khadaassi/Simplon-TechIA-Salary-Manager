import json
import csv


def extract_data():
    """
    Extracts employee data from a JSON file, organizes it by filial,
    and calculates monthly salary for each employee.

    Returns:
        filial_data(dict): Dictionary where each key is a filial, containing lists of employee data.
    """
    with open("employes_data.json", 'r') as file:
        employes_data = json.load(file)

    filial_data = {}

    for filial in employes_data:
        filial_data[filial] = {
            "name_list": [],
            "job_list": [],
            "hourly_rate_list": [],
            "weekly_hours_worked_list": [],
            "contract_hours_list": [],
            "monthly_salary_list": []
        }

        for employe in range(len(employes_data[filial])):
            name = employes_data[filial][employe]["name"]
            filial_data[filial]["name_list"].append(name)

            job = employes_data[filial][employe]["job"]
            filial_data[filial]["job_list"].append(job)

            hourly_rate = employes_data[filial][employe]["hourly_rate"]
            filial_data[filial]["hourly_rate_list"].append(hourly_rate)

            weekly_hours_worked = employes_data[filial][employe]["weekly_hours_worked"]
            filial_data[filial]["weekly_hours_worked_list"].append(weekly_hours_worked)

            contract_hours = employes_data[filial][employe]["contract_hours"]
            filial_data[filial]["contract_hours_list"].append(contract_hours)

            salary = calcul_single_monthly_rate(hourly_rate, weekly_hours_worked, contract_hours)
            filial_data[filial]["monthly_salary_list"].append(salary)

    return filial_data


def calcul_single_monthly_rate(hourly_rate, weekly_hours_worked, contract_hours):
    """
    Calculates the monthly salary for an employee based on their hourly rate,
    weekly hours worked, and contract hours.
    Args:
        Hourly_rate(list), weekly_hours_worked(list), and contract_hours(list).
    Returns:
        salary(float): Monthly salary.
    """
    if weekly_hours_worked > contract_hours:
        overtime_hours = weekly_hours_worked - contract_hours
        salary = 4 * ((contract_hours * hourly_rate) + (overtime_hours * hourly_rate * 1.5))
    elif weekly_hours_worked < contract_hours:
        non_factored_hours = contract_hours - weekly_hours_worked
        salary = 4 * ((contract_hours * hourly_rate) - (non_factored_hours * hourly_rate))
    else:
        salary = 4 * (contract_hours * hourly_rate)
    
    return salary


def calcul_stats(salary_list):
    """
    Calculates the mean, max, and min salary from a list of salaries.
    Args : 
        salary_list(list): List of salaries.
    Returns:
        tuple: (mean_salary, max_salary, min_salary)
    """
    mean_salary = sum(salary_list) / len(salary_list)
    max_salary = max(salary_list)
    min_salary = min(salary_list)

    return mean_salary, max_salary, min_salary

filial_data = extract_data()
global_salary_list = []

def print_report(filial_data, global_salary_list):
    """ 
    Prints employee salary data and statistics for each filial and globally.
    """
    
    for filial, data in filial_data.items():
        mean_salary, max_salary, min_salary = calcul_stats(data["monthly_salary_list"])

        print(f"Filial: {filial}")
        print("=" * 80)
        for i in range(len(data["name_list"])):
            print(f"{data['name_list'][i]:<20}| {data['job_list'][i]:<20}| Monthly Salary: {data['monthly_salary_list'][i]:.2f} $")
        
        print("-" * 80)
        print(f"Salary statistics for filial {filial}")
        print(f'Average salary: {mean_salary:.2f} $')
        print(f'Highest salary: {max_salary:.2f} $')
        print(f'Lowest salary: {min_salary:.2f} $', end="\n\n\n")
        
        global_salary_list.extend(data["monthly_salary_list"])

    global_mean_salary, global_max_salary, global_min_salary = calcul_stats(global_salary_list)

    print("=" * 80)
    print("Global salary statistics for TechIA")
    print(f'Global average salary: {global_mean_salary:.2f} $')
    print(f'Global highest salary: {global_max_salary:.2f} $')
    print(f'Global lowest salary: {global_min_salary:.2f} $')
    print("=" * 80)

print_report(filial_data, global_salary_list)
