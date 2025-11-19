#!/usr/bin/env python3


from mortality import makeham_mort

def whole_life_insurance_epv(interest_rate, retirement_age, benefit = 1.0, max_age = 200):
	v = 1.0 / (1.0 + interest_rate)
	max_years = int(max_age - retirement_age)
	

	epv = 0.0 #Sets a base value
	for t in range(max_years):
		p_t = makeham_mort(retirement_age, t)
		p_t1 = makeham_mort(retirement_age+t,1.0)
		q_xt = 1-p_t1
		epv += (v ** (t+1)) * p_t * q_xt

	return (benefit * epv)
	
def whole_life_annuity(interest_rate, retirement_age, benefit = 1.0, max_age = 200):
	d = interest_rate / (1 + interest_rate)
	whole_life = whole_life_insurance_epv(interest_rate, retirement_age, benefit=benefit, max_age=max_age)
	
	annuity = (1.0 - whole_life) / d

	return (annuity)

if __name__ == "__main__":
	insurance = whole_life_insurance_epv(interest_rate = 0.05, retirement_age = 65)
	annuity = whole_life_annuity(interest_rate = 0.05, retirement_age = 65)

	print(f"Whole life insurance EPV: {insurance:.4f}")
	print(f"Whole life annuity value: {annuity:.4f}")
