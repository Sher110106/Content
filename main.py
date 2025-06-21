import pandas as pd
import numpy as np
import random
from datetime import datetime, timedelta

# Set random seed for reproducibility
np.random.seed(42)
random.seed(42)

# Define parameters for data generation
n_employees = 550

# Define lists for categorical variables
departments = ['Computer Science', 'Mathematics', 'Physics', 'Chemistry', 'Biology', 
               'English', 'History', 'Economics', 'Management', 'Civil Engineering',
               'Mechanical Engineering', 'Electrical Engineering', 'Administration', 
               'Library', 'Research & Development']

job_roles = ['Professor', 'Associate Professor', 'Assistant Professor', 'Lecturer',
             'Research Scholar', 'Lab Assistant', 'Administrative Officer', 
             'Librarian', 'Technical Staff', 'Support Staff']

education_levels = ['PhD', 'Masters', 'Bachelors', 'Diploma']

marital_status = ['Single', 'Married', 'Divorced']

gender = ['Male', 'Female']

cities = ['Mumbai', 'Delhi', 'Bangalore', 'Chennai', 'Kolkata', 'Hyderabad', 
          'Pune', 'Ahmedabad', 'Jaipur', 'Lucknow', 'Kanpur', 'Nagpur',
          'Indore', 'Bhopal', 'Visakhapatnam', 'Patna', 'Vadodara', 'Coimbatore']

# Generate employee data
data = []

for i in range(n_employees):
    emp_id = f"EMP{1000 + i}"
    
    # Demographics
    emp_age = np.random.normal(35, 8)
    emp_age = max(22, min(65, int(emp_age)))  # Cap between 22 and 65
    
    emp_gender = random.choice(gender)
    emp_marital_status = random.choice(marital_status)
    
    # Job details
    department = random.choice(departments)
    job_role = random.choice(job_roles)
    
    # Adjust job role probability based on department
    if department in ['Computer Science', 'Mathematics', 'Physics', 'Chemistry', 'Biology', 
                      'English', 'History', 'Economics']:
        job_role = random.choice(['Professor', 'Associate Professor', 'Assistant Professor', 
                                'Lecturer', 'Research Scholar'])
    elif department == 'Administration':
        job_role = random.choice(['Administrative Officer', 'Support Staff'])
    elif department == 'Library':
        job_role = 'Librarian'
    
    education = random.choice(education_levels)
    
    # Adjust education based on job role
    if job_role in ['Professor', 'Associate Professor']:
        education = 'PhD'
    elif job_role == 'Assistant Professor':
        education = random.choice(['PhD', 'Masters'])
    elif job_role == 'Lecturer':
        education = random.choice(['Masters', 'PhD'])
    
    # Experience and tenure
    years_exp = max(0, np.random.normal(8, 4))
    years_exp = min(emp_age - 22, int(years_exp))  # Can't have more experience than working age
    
    years_at_company = max(0, np.random.normal(4, 3))
    years_at_company = min(years_exp, int(years_at_company))  # Can't be at company longer than total experience
    
    # Salary (in INR per month)
    base_salary = 0
    if job_role == 'Professor':
        base_salary = np.random.normal(120000, 20000)
    elif job_role == 'Associate Professor':
        base_salary = np.random.normal(90000, 15000)
    elif job_role == 'Assistant Professor':
        base_salary = np.random.normal(70000, 10000)
    elif job_role == 'Lecturer':
        base_salary = np.random.normal(50000, 8000)
    elif job_role == 'Research Scholar':
        base_salary = np.random.normal(35000, 5000)
    else:
        base_salary = np.random.normal(40000, 8000)
    
    monthly_income = max(25000, int(base_salary))
    
    # Performance and satisfaction metrics
    job_satisfaction = random.randint(1, 4)  # 1-Low, 2-Medium, 3-High, 4-Very High
    environment_satisfaction = random.randint(1, 4)
    work_life_balance = random.randint(1, 4)
    performance_rating = random.randint(1, 4)  # 1-Poor, 2-Good, 3-Excellent, 4-Outstanding
    
    # Work conditions
    overtime = random.choice(['Yes', 'No'])
    distance_from_home = np.random.exponential(15)  # Most people live closer
    distance_from_home = min(50, int(distance_from_home))  # Cap at 50 km
    
    num_companies_worked = max(1, int(np.random.poisson(2)))  # Including current
    
    # Training and development
    training_times_last_year = random.randint(0, 6)
    years_since_last_promotion = max(0, int(np.random.exponential(3)))
    
    # Personal factors
    home_city = random.choice(cities)
    
    # Calculate attrition probability based on various factors
    attrition_prob = 0.15  # Base probability
    
    # Adjust based on job satisfaction
    if job_satisfaction == 1:
        attrition_prob += 0.3
    elif job_satisfaction == 2:
        attrition_prob += 0.1
    elif job_satisfaction == 4:
        attrition_prob -= 0.1
    
    # Adjust based on work-life balance
    if work_life_balance == 1:
        attrition_prob += 0.2
    elif work_life_balance == 4:
        attrition_prob -= 0.1
    
    # Adjust based on years at company
    if years_at_company < 2:
        attrition_prob += 0.2
    elif years_at_company > 10:
        attrition_prob -= 0.15
    
    # Adjust based on age
    if emp_age < 25:
        attrition_prob += 0.15
    elif emp_age > 50:
        attrition_prob -= 0.1
    
    # Adjust based on distance
    if distance_from_home > 30:
        attrition_prob += 0.1
    
    # Adjust based on overtime
    if overtime == 'Yes':
        attrition_prob += 0.1
    
    # Adjust based on promotion
    if years_since_last_promotion > 5:
        attrition_prob += 0.1
    
    # Ensure probability is between 0 and 1
    attrition_prob = max(0, min(1, attrition_prob))
    
    # Determine attrition
    attrition = 'Yes' if random.random() < attrition_prob else 'No'
    
    # Create employee record
    employee = {
        'EmployeeID': emp_id,
        'Age': emp_age,
        'Gender': emp_gender,
        'MaritalStatus': emp_marital_status,
        'DistanceFromHome': distance_from_home,
        'HomeCity': home_city,
        'Education': education,
        'Department': department,
        'JobRole': job_role,
        'YearsExperience': years_exp,
        'YearsAtCompany': years_at_company,
        'MonthlyIncome': monthly_income,
        'JobSatisfaction': job_satisfaction,
        'EnvironmentSatisfaction': environment_satisfaction,
        'WorkLifeBalance': work_life_balance,
        'PerformanceRating': performance_rating,
        'OverTime': overtime,
        'NumCompaniesWorked': num_companies_worked,
        'TrainingTimesLastYear': training_times_last_year,
        'YearsSinceLastPromotion': years_since_last_promotion,
        'Attrition': attrition
    }
    
    data.append(employee)

# Create DataFrame
df = pd.DataFrame(data)

# Add some additional calculated fields
df['SalaryHike'] = np.random.normal(12, 4, n_employees).round(1)  # Percentage
df['SalaryHike'] = df['SalaryHike'].clip(0, 25)  # Cap between 0 and 25%

df['StockOptionLevel'] = np.random.choice([0, 1, 2, 3], size=n_employees, p=[0.4, 0.3, 0.2, 0.1])

# Reorder columns
column_order = ['EmployeeID', 'Age', 'Gender', 'MaritalStatus', 'DistanceFromHome', 'HomeCity',
                'Education', 'Department', 'JobRole', 'YearsExperience', 'YearsAtCompany',
                'MonthlyIncome', 'SalaryHike', 'StockOptionLevel', 'JobSatisfaction',
                'EnvironmentSatisfaction', 'WorkLifeBalance', 'PerformanceRating',
                'OverTime', 'NumCompaniesWorked', 'TrainingTimesLastYear',
                'YearsSinceLastPromotion', 'Attrition']

df = df[column_order]

# Save to CSV
df.to_csv('university_hr_attrition_data.csv', index=False)

print(f"Dataset created with {len(df)} employees")
print(f"Attrition rate: {(df['Attrition'] == 'Yes').mean():.2%}")
print("\nDataset saved as 'university_hr_attrition_data.csv'")

# Display basic statistics
print("\n=== Dataset Overview ===")
print(f"Total Employees: {len(df)}")
print(f"Departments: {df['Department'].nunique()}")
print(f"Job Roles: {df['JobRole'].nunique()}")
print(f"Attrition Count: {(df['Attrition'] == 'Yes').sum()}")
print(f"Retention Count: {(df['Attrition'] == 'No').sum()}")

print("\n=== Sample Data ===")
print(df.head())

print("\n=== Column Descriptions ===")
descriptions = {
    'EmployeeID': 'Unique identifier for each employee',
    'Age': 'Employee age in years',
    'Gender': 'Employee gender (Male/Female)',
    'MaritalStatus': 'Marital status (Single/Married/Divorced)',
    'DistanceFromHome': 'Distance from home to workplace in km',
    'HomeCity': 'Employee home city',
    'Education': 'Highest education level',
    'Department': 'Department/Faculty where employee works',
    'JobRole': 'Current job role/position',
    'YearsExperience': 'Total years of work experience',
    'YearsAtCompany': 'Years worked at current university',
    'MonthlyIncome': 'Monthly salary in INR',
    'SalaryHike': 'Last salary hike percentage',
    'StockOptionLevel': 'Stock option level (0-3)',
    'JobSatisfaction': 'Job satisfaction rating (1-4)',
    'EnvironmentSatisfaction': 'Work environment satisfaction (1-4)',
    'WorkLifeBalance': 'Work-life balance rating (1-4)',
    'PerformanceRating': 'Performance rating (1-4)',
    'OverTime': 'Whether employee works overtime (Yes/No)',
    'NumCompaniesWorked': 'Number of companies worked at',
    'TrainingTimesLastYear': 'Number of training sessions attended',
    'YearsSinceLastPromotion': 'Years since last promotion',
    'Attrition': 'Whether employee left (Yes/No) - Target variable'
}

for col, desc in descriptions.items():
    print(f"{col}: {desc}")
