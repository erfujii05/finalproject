def PUC_salary_projection(current_salary, years_until_retirement, salary_growth_rate):
    return (current_salary * ((1 + salary_growth_rate) ** (years_until_retirement - 1)))
