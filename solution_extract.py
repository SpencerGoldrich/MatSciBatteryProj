#Materials Science of Rechargeable Batteries Project
#By: Spencer Goldrich
#Research group: Rajat Mishra, Cara Fagerholm, Nirmal Jacob

import pybamm
import matplotlib.pyplot as plt
import numpy as np

#Can Specify cutoff voltage
Experiment = pybamm.Experiment(
    [
        ('Discharge at 1A until 3.0V')
    ]
)

#These are base parameters from the paper and our research
parameters = pybamm.ParameterValues("Ramadass2004")
parameters["Electrode height [m]"] = 0.2
parameters["Electrode width [m]"] = 0.2
parameters["Negative electrode density [kg.m-3]"] = 2199
parameters["Negative particle radius [m]"] = 2.1e-05
parameters["Positive particle radius [m]"] = 10e-6
parameters["Positive electrode density [kg.m-3]"] = 4239
parameters["Separator density [kg.m-3]"] = 916.8
parameters["Separator porosity"] = 0.39
parameters["Number of cells connected in series to make a battery"] = 15
parameters["Number of electrodes connected in parallel to make a cell"] = 71

#Test parameters from Cara's Excel work
testparams = {
    "porosity":[0.1,0.2,0.3,0.4,0.5,0.6,0.7],
    "cthick":np.multiply((10**(-6)),range(20,900,10)),
}
#These below are base cases
parameters["Positive electrode porosity"] = 0.3
parameters["Positive electrode thickness [m]"] = 80*10**(-6)

#Anode testing
def test(Experiment, parameters, testparams, ps):
    cap = []
    time = []
    j = 0
    for i in range(ps[0],ps[1]):
        j += 1
        print(j)

        #parameters["Positive electrode porosity"] = testparams['porosity'][i]
        #parameters["Positive electrode thickness [m]"] = testparams['cthick'][i]

        parameters["Positive electrode active material volume fraction"] = (1-parameters["Positive electrode porosity"])/0.737
        parameters["Negative electrode porosity"] = parameters["Positive electrode porosity"]
        parameters["Negative electrode thickness [m]"] = parameters["Positive electrode thickness [m]"]/0.939
        parameters["Negative electrode active material volume fraction"] = parameters["Positive electrode active material volume fraction"]/0.855

        sim = pybamm.Simulation(pybamm.lithium_ion.DFN(), experiment=Experiment, parameter_values=parameters)
        sim._solver.return_solution_if_failed_early = True
        sim.solve()
        sol = sim.solution

        cap.append(sol._summary_variables['Capacity [A.h]'])
        time.append(sol._summary_variables['Time [h]'])

    finalsim = sim
    return(finalsim, cap, time)

sim, cap, time = test(Experiment,parameters,testparams,[0,1])
sol = sim.solution

plt.plot(range(0,7),cap)
