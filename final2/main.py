#!/usr/bin/env python3
import tuc_pension_model
import puc_pension_model
from mpi4py import MPI
from montecarloengine import mpi_monte_carlo

def main():
	comm = MPI.COMM_WORLD
	rank = comm.Get_rank()

	method = None
	if rank == 0:
		while True:
			method = input("\nPUC, TUC, or MC (Monte Carelo) method?\n").upper()
			if method in ["TUC","PUC","MC"]:
				break
			print("Method expects either TUC, PUC, or MC (not case-sensitive)")

	method = comm.bcast(method, root=0)

	if method == "MC":
		run_mc_mode()
	elif rank == 0:
		if method == "TUC":
			tuc_pension_model.tuc_pension_benefit()
		elif method == "PUC":
			puc_pension_model.puc_pension_benefit()


def run_mc_mode():
	comm = MPI.COMM_WORLD
	rank = comm.Get_rank()
	method = None
	data = None
	n_trials = None
	

	#Rank 0 asks for user inputs
	if rank == 0:
		print("\n---Monte Carlo Mode---")
		method = input("\nSimulate using PUC or TUC?\n").upper()
		if method == "PUC":
			puc_pension_model.puc_pension_benefit()
			data = puc_pension_model.last_inputs
			n_trials = int(input("\nHow many Monte Carlo trials?\n"))
		elif method == "TUC":
			tuc_pension_model.tuc_pension_benefit()
			data = tuc_pension_model.last_inputs
			n_trials = int(input("\nHow many Monte Carlo trials?\n"))
		else:
			method = None
			data = None
			n_trials = None

	#Broadcast
	method = comm.bcast(method, root=0)
	data = comm.bcast(data, root=0)
	n_trials = comm.bcast(n_trials, root=0)

	#Runs monte carlo simulation
	results = mpi_monte_carlo(method, data, n_trials)
	
	if rank == 0:
		print("\nMonte Carlo Results\n")
		for k, v in results.items():
			print(f"{k}: {v}")






if __name__ == "__main__":
    main()			
