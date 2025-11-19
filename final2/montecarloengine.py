from mpi4py import MPI
import numpy as np
from tuc_pension_model import compute_tuc_without_input
from puc_pension_model import compute_puc_without_input

def sim_one_trial(method, base_inputs):
	#Runs ONE monte carlo trial


	data = dict(base_inputs)

	#Salary randomness
	if "salary_growth" in data:
		data["salary_growth"] += np.random.normal(0, 0.01)


	#Interest randomness
	if "interest_rate" in data:
		data["interest_rate"] += np.random.normal(0, 0.005)

	if method == "PUC":
		return compute_puc_without_input(data)
	elif method == "TUC":
		return compute_tuc_without_input(data)
	else:
		raise ValueError("Invalid method passed")

def mpi_monte_carlo(method, base_inputs, n_trials):
	#Parallel monte carlo with MPI

	comm = MPI.COMM_WORLD
	rank = comm.Get_rank()
	size = comm.Get_size()


	trials_per_rank = n_trials // size

	if rank == 0:
		print(f"\nRunning {n_trials} Monte Carlo simulations across {size} MPI ranks...")
		

	#run local simulations
	local_results = np.zeros(trials_per_rank)


	for i in range(trials_per_rank):
		local_results[i] = sim_one_trial(method, base_inputs)

	gathered = comm.gather(local_results, root=0)

	if rank == 0:
		all_results = np.concatenate(gathered)



		return {
			"mean":round(float(np.mean(all_results)), 2),
			"std":round(float(np.std(all_results)), 2),
			"min":round(float(np.min(all_results)), 2),
			"max":round(float(np.max(all_results)), 2),
			"count":len(all_results)
		}
	
	return None




