from collections import defaultdict
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import tops.dynamic as dps
import tops.solvers as dps_sol
import importlib
importlib.reload(dps)
import importlib.util
import sys


if __name__ == '__main__':

    # region Model loading and initialisation stage
    # import tops.ps_models.assignment_model as model_data
    
    # Spesifiser filsti og modulnavn
    module_path = "C:\\Users\\audun\\OneDrive - University of Bergen\\Dokumenter\\Collaborative_Python\\kraftsystem_sim\\TOPS-main\\src\\tops\\ps_models\\assignment_model.py"
    module_name = "model_data"

    # Last inn modulen
    spec = importlib.util.spec_from_file_location(module_name, module_path)
    model_data = importlib.util.module_from_spec(spec)
    sys.modules[module_name] = model_data
    spec.loader.exec_module(model_data)

# Nå kan du bruke model_data som en vanlig modul
    model = model_data.load()
    ps = dps.PowerSystemModel(model=model)  # Load into a PowerSystemModel object

    ps.power_flow()  # Power flow calculation

    ps.init_dyn_sim()  # Initialise dynamic variables
    x0 = ps.x0.copy()  # Initial states

    t = 0
    result_dict = defaultdict(list)
    t_end = 5  # Simulation time

    # Solver
    sol = dps_sol.ModifiedEulerDAE(ps.state_derivatives, ps.solve_algebraic, 0, x0, t_end, max_step=5e-3)
    # endregion

    # region Print initial conditions
    v_bus_mag = np.abs(ps.v_0)
    v_bus_angle = ps.v_0.imag / v_bus_mag
    #
    print(' ')
    print('Voltage magnitudes  (pu) = ', v_bus_mag)
    print('Voltage magnitudes  (kV) = ', v_bus_mag * [10, 245, 245])
    print(' ')
    print('Voltage angles     (rad) = ', v_bus_angle)
    print('Voltage angles (degrees) = ', v_bus_angle * [180/np.pi, 180/np.pi, 180/np.pi])
    print(' ')
    print('state description: \n', ps.state_desc)
    print('Initial values on all state variables (G1 and IB) :')
    print(x0)
    print(' ')
    # endregion

    # region Runtime variables
    # Additional plot variables
    P_m_stored = []
    P_e_stored = []
    E_f_stored = []
    v_bus = []
    I_stored = []

    event_flag1 = True #A different one for each system event
    # endregion

    # Simulation loop starts here!
    while t < t_end:
        result = sol.step()
        x = sol.y
        v = sol.v
        t = sol.t

        ################  Assignment 3 / 4: Simulation of short-circuit  ################

        #if (...):
        #    ps.y_bus_red_mod[ , ] =
        #else:
        #    ps.y_bus_red_mod[ , ] =

        ##'y_bus_red_mod' refers to the fault admittance, the inverse of fault impedance.
        ##Fault: impedance = zero --> admittance = ?

        ##[0, 0]: corresponds to 'B1' (generator bus).
        ##[1, 1]: corresponds to 'B2' (load bus).
        ##[2, 2]: corresponds to 'B3' (stiff network).

        #################################################################################

        #####  Assignment 5/6: Short-circuit with line disconnection & reconnection #####

        #if (...) and (...):
        #   (...)
        #   ps.y_bus_red_mod[ , ] =

        #if (...) and (...):
        #    (...)
        #    ps.lines['Line'].event(ps, ps.lines['Line'].par['name'][0], 'disconnect')
        #    ps.y_bus_red_mod[ , ] =

        #if (...) and (...):
        #    (...)
        #    ps.lines['Line'].event(ps, ps.lines['Line'].par['name'][0], 'connect')

        #################################################################################

        # region Store variables
        result_dict['Global', 't'].append(sol.t)
        [result_dict[tuple(desc)].append(state) for desc, state in zip(ps.state_desc, x)]
        # Store additional variables
        P_m_stored.append(ps.gen['GEN'].P_m(x, v).copy())
        P_e_stored.append(ps.gen['GEN'].P_e(x, v).copy())
        E_f_stored.append(ps.gen['GEN'].E_f(x, v).copy())

        I_gen = ps.y_bus_red_full[0, 1] * (v[0] - v[1])
        I_stored.append(np.abs(I_gen)) #Stores magnitude of armature current
        v_bus.append(np.abs(v[0])) #Stores magnitude of generator terminal voltage
        # endregion


    # Convert dict to pandas dataframe
    result = pd.DataFrame(result_dict, columns=pd.MultiIndex.from_tuples(result_dict))

    # region Plotting

    #Plotting as a function of time --> result[('Global', 't')]

    fig, ax = plt.subplots(3)
    fig.suptitle('Generator speed, power angle and electric power')
    ax[0].plot(result[('Global', 't')], result.xs(key='speed', axis='columns', level=1))
    ax[0].set_ylabel('Speed (p.u.)')
    ax[1].plot(result[('Global', 't')], result.xs(key='angle', axis='columns', level=1))
    ax[1].set_ylabel('Power angle (rad)')
    #ax[1].plot(result[('Global', 't')], np.array(P_m_stored))
    #ax[1].set_ylabel('Mech. power (p.u.)')
    ax[2].plot(result[('Global', 't')], np.array(P_e_stored)/[50, 10000])
    ax[2].set_ylabel('Elec. power (p.u.)')
    ax[2].set_xlabel('Time (s)')

    #Plotting as a function of power angle --> result.xs(key='angle', axis='columns', level=1)



    plt.figure()
    plt.plot(result[('Global', 't')], np.array(E_f_stored))
    plt.xlabel('Time (s)')
    plt.ylabel('E_q (p.u.)')
    plt.show()
    # endregion