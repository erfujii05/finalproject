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
		print(f"\nRunning {n_trials} Monte Carlo simulations across {size} processes...")
		
	# Synchronize so all ranks start timing together
	comm.Barrier()
	t0 = MPI.Wtime()

	#run local simulations
	local_results = np.zeros(trials_per_rank)


	for i in range(trials_per_rank):
		local_results[i] = sim_one_trial(method, base_inputs)

	# Local elapsed time for this rank
	local_time = MPI.Wtime() - t0

	gathered = comm.gather(local_results, root=0)
	max_time = comm.reduce(local_time, op=MPI.MAX, root=0)

	if rank == 0:
		all_results = np.concatenate(gathered)



		return {
			"Expected Value":round(float(np.mean(all_results)), 2),
			"Standard Deviation":round(float(np.std(all_results)), 2),
			"Min Observed Accrued Liability":round(float(np.min(all_results)), 2),
			"Max Observed Accrued Liability":round(float(np.max(all_results)), 2),
			"Number of Trials":len(all_results),
			"Computation Time (Seconds)":round(float(max_time), 4)
		}
	
	return None



