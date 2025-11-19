#!/usr/bin/env python3
from mortality import makeham_mort
from PUC_salary import PUC_salary_projection
from whole_life import whole_life_insurance_epv
from whole_life import whole_life_annuity


def puc_pension_benefit():
    while True:
        try:
            current_salary = int(input("\nEnter Current Salary:\n"))
            if current_salary <= 0:
                print("Current Salary Expects a Positive Integer")
                continue
            break
        except ValueError:
            print("Current Salary Expects a Positive Integer")
            continue

    while True:
        try:
            retirement_age = int(input("\nEnter Retirement Age:\n"))
            if retirement_age <= 30 or retirement_age > 100:
                print("Retirement age expects a value greater than or equal to thirty and less than 100")
                continue
            break
        except ValueError:
            print("Retirement Age expects an integer value")

    while True:
        try:
            current_age = int(input("\nEnter Current Age:\n"))
            if current_age <= 17 or current_age >= 80 or current_age >= retirement_age:
                print("Current age expects an integer age greater than 17, less than 80, and less than the retirement age.")
                continue
            break
        except ValueError:
            print("Current age expects an integer value that's greater than 17 and less than 80")

    while True:
        try:
            accrual_rate = float(input("\nEnter Accrual Rate:\n"))
            if accrual_rate <= 0 or accrual_rate >= 1:
                print("Accrual rate expects a positive non-zero value less than one.")
                continue
            break
        except ValueError:
            print("Accrual rate expects a positive non-zero integer")

    while True:
        try:
            salary_growth = float(input("\nEnter Salary Growth Rate:\n"))
            if salary_growth < 0 or salary_growth >= 1:
                print("Salary growth expects a non-negative integer less than one.")
                continue
            break
        except ValueError:
            print("Salary growth expects a non-negative integer")

    while True:
        try:
            interest_rate = float(input("\nEnter Interest Rate:\n"))
            if interest_rate < 0 or interest_rate >= 1:
                print("Interest rate expects a positive value less than one.")
                continue
            break
        except ValueError:
            print("Interest rate expects a positive float")

    while True:
        try:
            years_of_service = int(input("\nEnter Years of Service:\n"))
            if years_of_service > current_age or years_of_service < 0:
                print("Years of service expects a positive non-zero integer that's less than your current age.")
                continue
            break
        except ValueError:
            print("Years of service expects a positive non-zero integer")

    global last_inputs
    last_inputs = {
        "current_salary": current_salary,
        "retirement_age": retirement_age,
        "current_age": current_age,
        "accrual_rate": accrual_rate,
        "salary_growth": salary_growth,
        "interest_rate": interest_rate,
        "years_of_service": years_of_service,
    }
    data = last_inputs
    liability = compute_puc_without_input(data)

    print(f"\nAccrued liability at age {current_age}: {liability:.4f}")
    return liability

# Core Calulations

def compute_puc_without_input(data):
    current_salary = data["current_salary"]
    retirement_age = data["retirement_age"]
    current_age = data["current_age"]
    accrual_rate = data["accrual_rate"]
    salary_growth = data["salary_growth"]
    interest_rate = data["interest_rate"]
    years_of_service = data["years_of_service"]

    years_until_retirement = retirement_age - current_age
    v = 1 / (1 + interest_rate)

    final_salary = PUC_salary_projection(
        current_salary,
        years_until_retirement,
        salary_growth,
    )

    base_benefit = accrual_rate * years_of_service * final_salary

    survival_prob = makeham_mort(current_age, years_until_retirement)

    annuity = whole_life_annuity(interest_rate, retirement_age)

    accrued_liability = (
        base_benefit
        * (v ** years_until_retirement)
        * survival_prob
        * annuity
    )
    return accrued_liability


if __name__ == "__main__":
    puc_pension_benefit()
