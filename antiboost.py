# GitLab Stuff
import os

# Model Libraries
import numpy as np
from zero import Circuit
from zero.analysis import AcSignalAnalysis
from zero.data import Series, Response

# Data Libraries
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

# PyZero Code
circuit = Circuit()
frequencies = np.logspace(1, 5, 100)

## Input Comparator
circuit.add_library_opamp(name="U1", model="AD829", node1="n4", node2="n3", node3="n5")
circuit.add_resistor(name = "R1", value="1k", node1="n1", node2="n3")
circuit.add_resistor(name = "R2", value="1k", node1="n3", node2="n5")
circuit.add_resistor(name = "R3", value="1k", node1="gnd", node2="n4")
circuit.add_resistor(name = "R4", value="1k", node1="n4", node2="gnd")
circuit.add_capacitor(name = "C1", value="5p", node1="n3", node2="n5")
circuit.add_capacitor(name = "C2", value="5p", node1="gnd", node2="n4")

## Anti-Boost
circuit.add_library_opamp(name="U2", model="AD829", node1="gnd", node2="n7", node3="n8")
circuit.add_resistor(name = "R5", value="100k", node1="n5", node2="n7")
circuit.add_resistor(name = "R6", value="1k", node1="n5", node2="n6")
circuit.add_resistor(name = "R7", value="1k", node1="n7", node2="n8")
circuit.add_capacitor(name = "C5", value="2.2n", node1="n6", node2="n7")
circuit.add_capacitor(name = "C6", value="5p", node1="n7", node2="n8")

analysis = AcSignalAnalysis(circuit=circuit)
solution = analysis.calculate(frequencies=frequencies, input_type="voltage", node="n1")
nin = circuit['n1']
nout = circuit['n8']
res = solution.get_response(nin, nout)
magres = res.db_magnitude
phares = res.phase

magnitude_z = np.array(magres)
phase_z = np.array(phares)

# Plot just PyZero
#plot = solution.plot_responses(sink="n8")
#plot.show()

# Experimental Code
script_path = os.path.dirname( os.path.abspath(__file__))
#df = pd.read_excel('/home/nico/my_code/AntiBoostFull_data.xlsx') 
df = pd.read_excel( os.path.join(script_path, '../data/AntiBoostFull_data.xlsx')) # data from SR785

frequency_e = df['Frequency (Hz)'].values
magnitude_e = df['Magnitude'].values
phase_e = df['Phase'].values

# Plots
fig, (s1, s2) = plt.subplots(2, 1, sharex=True)
s1.semilogx(frequency_e, magnitude_e, 'b', label='Original Data', color='#f0a963ff')
s1.semilogx(frequency_e, magnitude_z, 'b', label="PyZero Data")
s1.set_ylabel('Magnitude(dB)')
s1.set_title('Magnitude vs Frequency')
s1.set_yticks([-40, -20, 0])
s1.grid()
s1.grid(which='minor', ls='--', alpha=0.5)
s1.legend()

s2.semilogx(frequency_e, phase_e, 'b', label='Original Data', color='#f0a963ff')
s2.semilogx(frequency_e, phase_z, 'b', label="PyZero Data")
s2.set_xlabel('Frequency (Hz)')
s2.set_ylabel('Phase (degrees)')
s2.grid()
s2.grid(which='minor', ls='--', alpha=0.5)
s2.set_title('Phase vs Frequency')
s2.set_yticks([-45, 0, 45, 90])
s2.legend()

plt.tight_layout()
plt.show()


# Residuals

residual_magnitude = magnitude_e - magnitude_z
residual_phase = phase_e - phase_z

fig, (r1, r2) = plt.subplots(2, 1, sharex=True)

r1.semilogx(frequency_e, residual_magnitude, '#f0a963ff')
r1.set_ylabel('Magnitude(dB)')
r1.set_title('Magnitude Residuals')

r2.semilogx(frequency_e, residual_phase, '#f0a963ff')
r2.set_xlabel('Frequency (Hz)')
r2.set_ylabel('Phase(degrees)')
r2.set_title('Phase Residuals')
plt.tight_layout()
plt.show()

