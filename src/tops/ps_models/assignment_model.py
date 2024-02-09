def load():
    return {
        'base_mva': 50,
        'f': 50,
        'slack_bus': 'B3',

        #'base_mva': system base/nominal complex power in [MVA].
        #'f': system frequency in [Hz].
        #'slack_bus': reference busbar with zero phase angle.

        'buses': [
            ['name',    'V_n'],
            ['B1',         10],
            ['B2',        245],
            ['B3',        245],
        ],

        #'V_n': base/nominal voltage in [kV].

        'lines': [
            ['name',  'from_bus', 'to_bus',   'length',   'S_n',  'V_n',  'unit', 'R',    'X',   'B'],
            ['L2-3',        'B2',     'B3',        250,      50,    245,    'PF',   0,    0.4,     0],
        ],

        #'length': total line length in [km].
        #'S_n': base/nominal complex power in [MVA].
        #'V_n': base/nominal voltage in [kV].
        #'unit': chosen unit for jacobian admittance calculation (leave it as 'PF').
        #'R': line resistance in [Ohm/km].
        #'X': line reactance in [Ohm/km].
        #'B': line susceptance in [Ohm/km].

        'transformers': [
            ['name', 'from_bus', 'to_bus', 'S_n', 'V_n_from', 'V_n_to', 'R', 'X'],
            ['T1',         'B1',     'B2',    50,         10,      245,   0, 0.1],
        ],

        #'S_n': base/nominal complex power in [MVA].
        #'V_n_from': base/nominal voltage on the 'from_bus' side in [kV].
        #'V_n_to': base/nominal voltage on the 'to_bus' side in [kV].
        #'R': transformer resistance in [pu].
        #'X': transformer reactance in [pu].

        'loads': [
            ['name', 'bus', 'P', 'Q', 'model'],
            ['L1',    'B2',  25,   0,     'Z'],
        ],

        #'P': active power delivered to the load in [MW].
        #'Q': reactive power delivered to the load in [MVAr].
        #'model': modelling of load voltage dependence (leave it as 'Z').

        'generators': {
            'GEN': [
                ['name',   'bus',  'S_n',  'V_n',    'P',    'V',      'H',    'D',    'X_d',  'X_q',  'X_d_t',    'X_q_t',    'X_d_st',   'X_q_st',   'T_d0_t',   'T_q0_t',   'T_d0_st',  'T_q0_st'],
                ['G1',      'B1',     50,     10,     40,   0.93,      3.1,      0,     2.27,   2.12,    0.544,      0.522,        0.11,      0.07,        2.01,         50,           1,        0.5],
                ['IB',      'B3',  10000,    245,    -15,  0.898,     10.0,      0,      1.0,   0.80,      0.3,       0.80,         0.2,       0.23,          8,      10000,        0.03,       0.07],
            ],
        }
    }
        #For 'IB': change only 'V_n', 'P' and 'V' if necessary. Other parameters should be left as they are.

        #'S_n': base/nominal complex power in [MVA].
        #'V_n': base/nominal voltage in [kV].
        #'P': active power produced by the generator in [MW].
        #'V': generator terminal voltage in [pu].
        #'H': inertia constant in [MWs/MVA].
        #'D': damping constant in [pu/pu].
        #'X_d'/'X_q': synchronous d-axis/q-axis reactance in [pu].
        #'X_d_t'/'X_q_t': transient d-axis/q-axis reactance in [pu].
        #'X_d_st'/'X_q_st': subtransient d-axis/q-axis reactance in [pu].
        #'T_d0_t'/'T_q0_t': open-circuit d-axis/q-axis transient time constant in [s].
        # 'T_d0_st'/'T_q0_st': open-circuit d-axis/q-axis subtransient time constant in [s]