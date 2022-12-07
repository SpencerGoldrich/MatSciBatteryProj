#Materials Science of Rechargeable Batteries Project
#By: Spencer Goldrich
#Research group: Rajat Mishra, Cara Fagerholm, Nirmal Jacob

import pybamm
import matplotlib.pyplot as plt
import numpy as np

#These are base parameters from the paper and our research/analysis
parameters = pybamm.ParameterValues("Ramadass2004")
parameters["Electrode height [m]"] = 0.2
parameters["Electrode width [m]"] = 0.2
parameters["Negative electrode density [kg.m-3]"] = 2199
parameters["Negative particle radius [m]"] = 2.1e-05
parameters["Positive particle radius [m]"] = 10e-6
parameters["Positive electrode density [kg.m-3]"] = 4239
parameters["Separator density [kg.m-3]"] = 916.8
parameters["Separator porosity"] = 0.39
parameters["Positive electrode porosity"] = 0.24
parameters["Positive electrode thickness [m]"] = 81*10**(-6)

def test(Experiment, testparams, ps, experiment_type):
    if (experiment_type == "Thickness Test") or (experiment_type == "Porosity Test"):
        parameters = testparams["parameters"]
    elif experiment_type == "Cycle Test":
        parameters = testparams

    sols = []
    j = 0
    for i in range(ps[0],ps[1]):
        if experiment_type == "Porosity Test":
            parameters["Positive electrode porosity"] = testparams['porosity'][i]
        elif experiment_type == "Thickness Test":
            parameters["Positive electrode thickness [m]"] = testparams['cthick'][i]

        parameters["Positive electrode active material volume fraction"] = (1-parameters["Positive electrode porosity"])/0.737
        parameters["Negative electrode porosity"] = parameters["Positive electrode porosity"]
        parameters["Negative electrode thickness [m]"] = parameters["Positive electrode thickness [m]"]/0.939
        parameters["Negative electrode active material volume fraction"] = parameters["Positive electrode active material volume fraction"]/0.855

        sim = pybamm.Simulation(pybamm.lithium_ion.DFN(), experiment=Experiment, parameter_values=parameters)
        sim._solver.return_solution_if_failed_early = True
        sol = sim.solve()
        sols.append(sol)

        j += 1
        print(j)
    return(sols)

#Porosity and Thickness
'''
Experiment = pybamm.Experiment(
    [
    'Discharge at 0.28A until 3.0V'
    ]
)

testparams = {
    "parameters":parameters,
    "porosity":[0.2,0.22,0.24,0.26,0.28], #0.24 intial max
    "cthick":np.multiply((10**(-6)),range(150,850,100)),
}
n = len(testparams["cthick"])

sols = test(Experiment, testparams, [0,n], "Porosity Test")
pybamm.dynamic_plot(sols)
'''

#Coloumbic/Voltage/Energy Efficiencies
'''
num = 5
Experiment = pybamm.Experiment(
    [
    'Discharge at 0.28A until 3.0V',
    'Rest at 3.0V for 1 hour',
    'Charge at 0.28A until 4.2V',
    'Rest at 4.2V for 1 hour'
    ] * num
)

sols = test(Experiment, parameters, [0,1], "Cycle Test")
pybamm.dynamic_plot(sols,["Terminal voltage [V]"])

coloumbic_eff = []
voltage_eff = []
energy_eff = []
for i in range(0,num-1):
    a = 100 * sols[0].all_summary_variables[4*i + 4]['Measured capacity [A.h]'] / sols[0].all_summary_variables[4*i + 2]['Measured capacity [A.h]']
    coloumbic_eff.append(a)
    b = 100 * sols[0].all_summary_variables[4*i + 4]['Maximum voltage [V]'] / sols[0].all_summary_variables[4*i + 2]['Maximum voltage [V]']
    voltage_eff.append(b)
    energy_eff.append(100 * (b/100 * a/100))
'''

a = 1
plt.show()
