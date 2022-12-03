#Materials Science of Rechargeable Batteries Project
#By: Spencer Goldrich
#Research group: Rajat Mishra, Cara Fagerholm, Nirmal Jacob

import pybamm
import matplotlib.pyplot as plt
import numpy as np

#These are base parameters from the paper and our research
parameters = pybamm.ParameterValues("Ramadass2004")
parameters["Current function [A]"] = 2.138 #Our dim 1.4V for 1C, 0.28V for 0.2C, Their dim 2.138A for 1C and 0.4267A for 0.2C
#parameters["Electrode height [m]"] = 0.2
#parameters["Electrode width [m]"] = 0.2
parameters["Lower voltage cut-off [V]"] = 3
parameters["Negative electrode density [kg.m-3]"] = 2199
parameters["Negative particle radius [m]"] = 2.1e-05
parameters["Nominal cell capacity [A.h]"] = 2.138 #Our dim 1.4, Their dim 2.138
#parameters["Number of cells connected in series to make a battery"] = 15
#parameters["Number of electrodes connected in parallel to make a cell"] = 71
parameters["Positive electrode density [kg.m-3]"] = 4239
parameters["Separator density [kg.m-3]"] = 916.8
parameters["Separator porosity"] = 0.39


#Test parameters from Cara's Excel work
testparams = {
    "porosity":[0.1,0.2,0.3,0.4,0.5,0.6,0.7],
    "athick":np.multiply((10**(-6)),[67.40559574, 75.83129521, 86.66433738, 101.1083936, 121.3300723, 151.6625904, 202.2167872]),
    "aactivevolfrac":[0.7762910539, 0.6900364923, 0.6037819308, 0.5175273692, 0.4312728077, 0.3450182462, 0.2587636846],
    "cthick":np.multiply((10**(-6)),[63.29051709, 71.20183172, 81.37352197, 94.93577563, 113.9229308, 142.4036634, 189.8715513]),
    "cactivevolfrac":[0.6636728906, 0.5899314583, 0.516190026, 0.4424485937, 0.3687071614, 0.2949657291, 0.2212242969]
}
'''testparams = {
    "porosity":[0.4],
    "athick":np.multiply((10**(-6)),[101.1083936]),
    "aactivevolfrac":[0.5175273692],
    "cthick":np.multiply((10**(-6)),[94.93577563]),
    "cactivevolfrac":[0.4424485937]
}'''

#Can Specify cutoff voltage
Experiment = pybamm.Experiment(
    [
        ('Discharge at 1C until 3.0V')
    ]
)

#Anode testing
def test(Experiment, parameters, testparams):
    cap = []
    for i in range(0,len(testparams['porosity'])):
        parameters["Negative electrode porosity"] = testparams['porosity'][i]
        parameters["Negative electrode thickness [m]"] = testparams['athick'][i]
        parameters["Negative electrode active material volume fraction"] = testparams['aactivevolfrac'][i]
        parameters["Positive electrode porosity"] = testparams['porosity'][i]
        parameters["Positive electrode thickness [m]"] = testparams['cthick'][i]
        parameters["Positive electrode active material volume fraction"] = testparams['cactivevolfrac'][i]

        sim = pybamm.Simulation(pybamm.lithium_ion.DFN(), experiment=Experiment, parameter_values=parameters)
        sim._solver.return_solution_if_failed_early = True
        sim.solve()
        sol = sim.solution

        cap.append(sol._summary_variables['Capacity [A.h]'])

    finalsim = sim
    return(finalsim, cap)

finalsim, cap = test(Experiment,parameters,testparams)
sol = finalsim.solution
print(sol._summary_variables['Capacity [A.h]'])
print(sol._summary_variables['Positive electrode capacity [A.h]'])
print(sol._summary_variables['Negative electrode capacity [A.h]'])
#finalsim.plot()

plt.plot(range(0,7),cap)