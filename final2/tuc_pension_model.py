#!/usr/bin/env python3
from mortality import makeham_mort
from TUC_salary import TUC_final_salary
from whole_life import whole_life_insurance_epv
from whole_life import whole_life_annuity

def tuc_pension_benefit():
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
                print("Retirement Age expects a positive value greater than 30 and less than 100")
                continue
            break
        except ValueError:
            print("Retirement Age expects an integer value")
    while True:
        try:
            current_age = int(input("\nEnter Current Age:\n"))
            if current_age <= 17 or current_age >= 80 or current_age >= retirement_age:
                print("Current age expects an integer age greater than 0, less than 80, and less than the retirement age.")
                continue
            break
        except ValueError:
            print("Current age expects an integer value")
    while True:
        try:
            accrual_rate = float(input("\nEnter Accrual Rate:\n"))
            if accrual_rate <= 0 or accrual_rate >= 1:
                print("Accrual rate expects a positive non-zero value")
                continue
            break
        except ValueError:
            print("Accrual rate expects a positive non-zero integer")
    while True:
        try:
            salary1ago = float(input("\nEnter Salary one year ago:\n"))
            if salary1ago <= 0:
                print("Salary one year ago expects a non-negative integer")
                continue
            break
        except ValueError:
            print("Salary one year ago expects a non-negative integer")
    while True:
        try:
            salary2ago = float(input("\nEnter Salary two years ago:\n"))
            if salary2ago <= 0:
                print("Salary two years ago expects a non-negative integer")
                continue
            break
        except ValueError:
            print("Salary two years ago expects a non-negative integer")
    while True:
        try:
            salary3ago = float(input("\nEnter Salary three years ago:\n"))
            if salary3ago <= 0:
                print("Salary three years ago expects a non-negative integer")
                continue
            break
        except ValueError:
            print("Salary three years ago expects a non-negative integer")
    while True:
        try:
            interest_rate = float(input("\nEnter Interest Rate:\n"))
            if interest_rate < 0 or interest_rate >= 1:
                print("Interest rate expects a positive value")
                continue
            break
        except ValueError:
            print("Interest rate expects a positive float")
    while True:
        try:
            years_of_service = int(input("\nEnter Years of Service:\n"))
            if years_of_service < 0 or years_of_service > current_age:
                print("Years of service expects a positive non-zero integer less than your current age")
                continue
            break
        except ValueError:
            print("Years of service expects a positive non-zero integer")
    global last_inputs
    last_inputs = {
        "salary1ago": salary1ago,
        "salary2ago": salary2ago,
        "salary3ago": salary3ago,
        "retirement_age": retirement_age,
        "current_age": current_age,
        "accrual_rate": accrual_rate,
        "interest_rate": interest_rate,
        "years_of_service": years_of_service,

        # Needed for randomness (even though TUC doesn’t use salary_growth)
        "salary_growth": 0.0
    }
    data = last_inputs
    liability = compute_tuc_without_input(data)

    print(f"\nAccrued liability at age {current_age}: {liability:.4f}")
    return liability
# Core Calculations
def compute_tuc_without_input(data):
    # Extract inputs
    salary1ago = data["salary1ago"]
    salary2ago = data["salary2ago"]
    salary3ago = data["salary3ago"]
    retirement_age = data["retirement_age"]
    current_age = data["current_age"]
    accrual_rate = data["accrual_rate"]
    interest_rate = data["interest_rate"]
    years_of_service = data["years_of_service"]

    # Years until retirement
    years_until_retirement = retirement_age - current_age

    # Discount factor per year
    v = 1 / (1 + interest_rate)

    # Final (three-year average) salary
    final_salary = TUC_final_salary(salary3ago, salary2ago, salary1ago)

    # Base annual benefit
    base_benefit = accrual_rate * years_of_service * final_salary

    # Survival probability to retirement
    survival_prob = makeham_mort(current_age, years_until_retirement)

    # Whole life annuity at retirement
    annuity = whole_life_annuity(interest_rate, retirement_age)

    # Accrued liability at CURRENT AGE
    accrued_liability = (
        base_benefit *
        (v ** years_until_retirement) *
        survival_prob *
        annuity
    )

    return accrued_liability


if __name__ == "__main__":
    tuc_pension_benefit()

