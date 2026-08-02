# Arduino-Amplifier-Stress-Analysis-INA125-Shield
PCB design, Gerber files, stress‑analysis results, transducer shield development, and related documentation.

**Introduction**

Whether validating finite element analysis (FEA) results or designing load cells, amplifying the small voltage differential developed by a Wheatstone bridge of strain gauge/s requires the careful consideration of a number of variables.

Digital load-cell amplifiers offer several advantages for strain-gauge data logging. They provide self-centering signals, high resolution, and low-noise performance, which reduces the need for heavy analog gain and simplifies the overall design. These features make digital front-ends ideal for stable, low-frequency stress measurements.

However, digital systems also have limitations. Analog instrumentation amplifiers still offer important benefits, especially in experimental or dynamic applications. They allow real-time adjustment of gain, manual offset control, and directional biasing of the signal. Analog front-ends also support much higher sampling frequencies, which is essential for capturing dynamic strain, impact events, and fast transducer responses. For users who need flexible tuning or to make custom measurements outside the laboratory with high-speed data acquisition, analog amplifiers remain the better choice.

For transducers, strain gauges can often be arranged in a full Wheatstone bridge configuration to achieve optimal performance. However, some applications require half-bridge configurations, while many strain measurement methods require quarter-bridge configurations, by utilising strain gauge rosettes. 
In both half- and quarter-bridge designs, the remaining legs of the bridge must be completed using dummy resistors. Professional industry hardware and software - by LabView, Micro-Measurements, or Techni-Measure—provide plug-and-play solutions, whereas the independent practitioner often needs to construct the remaining circuitry and amplification stages on veroboard.

In my publication Bicycle Biomechanics: How to Build a Dynamometer, the published graphs traces were captured using the well-known HX711 digital amplifier. Because of the limitations described earlier, I wanted a analogue template that provides a genuine “plug-and-play” solution. The INA125 instrumentation amplifier-often demonstrated on forums using breadboard layouts - stands out, because it includes onboard reference voltages pins, removing the need to design separate current-source circuits for powering the Wheatstone bridge or to provide a stable reference voltages. The other advantage of the INA125 chip is that it has a through-hole version (INA125P), which allows a proof of concept to be built, and a surface-mount version (INA125U) that allows for further miniaturisation.

These breadboard examples are straightforward to follow, but as with most proof-of-concept builds, data acquisition on breadboard is inherently noisy; and although Gerber files for INA125-based shields exist online, I have not found sufficient evidence that these designs have been validated by comparing measured outputs against known inputs. This is generally acceptable when a voltage output is correlated with and applied calibration load although not as useful for stress analysis. Additionally, for half- and quarter-bridge configurations, the remaining dummy-resistor circuits still need to be assembled on veroboard.

To address these issues, I present a shield design that interfaces directly with an Arduino UNO. I also provide detailed guidance so readers can adapt the circuit to their own data-logging methods and measurement requirements.

**Methods**

To evaluate the shield, a cantilever beam was built with full-, half-, and quarter-Wheatstone-bridge strain-gauge configuration and known weights were applied to the tip so the measured strain was validated against the analytical plot. The printed circuit board (PCB) was designed using LibrePCB 2.1.1, and the schematic showing the connection to two analogue channels A0 and A1 is detailed in Figure 1. 

<img width="1263" height="881" alt="Image" src="https://github.com/user-attachments/assets/461836ef-0dc1-4c19-877a-1863a0ca5397" />

**Figure 1 Schematic of INA125 Amplifier shield**

The INA125 instrumentation amplifier includes several integrated features that allow the gain, the bridge reference voltage (fixed at 5 V on this board), and an additional reference voltage to be adjusted directly on the PCB without requiring extra peripheral circuits. As shown in Figure 1, the gain is set using an external resistor; the reference voltage is set by connecting pin 4 to pin 16 (in this case the 2.5 V reference); and pin 17 (for this PCB) is used to set the bridge-supply voltage (5 V). On the board, the reference-voltage variable-resistor pins can be connected using a jumper wire, or-if the signal requires biasing-a variable resistor can be soldered in place. Likewise, a fixed resistor can be used to set the gain, or a variable resistor can be installed; the advantage of a fixed resistor is improved precision in the known gain value (figure 2).

<img width="671" height="760" alt="Image" src="https://github.com/user-attachments/assets/b2bab40c-4d20-4865-a6f4-de634751ec42" />

**Figure 2 LibrePCB generated Image of Amplifier Shield Plugged into Arduino Uno**

The external strain gauges are connected to the circuit via terminal blocks, as shown in Figure 2. The PCB silkscreen indicates the correct termination for full-, half-, and quarter-Wheatstone-bridge configurations (Figure 3). For half- and quarter-bridge setups, dummy resistors (in this study 350 Ω Metal Film Resistor 0.4 W 0.25 %) can be soldered to the board to complete the strain-gauge circuit as required. This provides a robust method that minimises circuit noise, as it avoids completing the bridge on a separate board.

<img width="1216" height="470" alt="Image" src="https://github.com/user-attachments/assets/6fa8e500-8f47-45a0-80aa-d3b68dd3b2a4" />

**Figure 3 The Wiring of the External Wheatstone Bridge with the Amplifier Board**

The first circuit evaluated was the full Wheatstone bridge. For this test, 350 Ω Z-type strain gauges were bonded to a steel ruler approximately 35 mm from the fixed end, that was to be held with a G-clamp (Figure 3). 

<img width="1536" height="1024" alt="Image" src="https://github.com/user-attachments/assets/b68c48d2-9b5d-4a9b-9fc0-91fdbb80ae5b" />

**Figure 4 Steel Rule (300 x 25.6 x 1mm) with Bonded Zalati Strain Gauges in Full-Bridge Configuration (top-right). Flat-Bar (300 x 13 x 3mm) with Bonded Micro-Measurements CEA-00-250UW-350 Strain Gauges in quarter or Half -Bridge Configuration. In both set-ups additional gauges are mounted on the reverse side in identical positions (R2 & R3 for Full Bridge & R2 for Half Bridge).**

A non-premium gauge was chosen because this setup was expected to represent the worst-case scenario, although the limiting factor in strain-gauge performance is typically the quality of the bond. However, for the half and quarter bridge Micro-Measurements CEA-00-250UW-350 gauges were bonded to the top and underside of a steel flat-bar (Figure 3). For the quarter bridge only the topside gauge (R1) was connected and for the half bridge the topside (R1) and reverse side gauge (R2) was connected (Figure 3 & 4).

The steel ruler and steel flat-bar surfaces were prepared by sanding with 300-grit abrasive paper, cleaning with isopropanol, and applying Micro-Measurements M-Bond M-Prep Conditioner. After conditioning, the surfaces were lightly sanded again, cleaned, and treated with Micro-Measurements M-Prep Neutralizer, followed by a final alcohol wipe. The gauge locations were marked with a pencil, and Micro-Measurements PCT-3MD installation tape was used to position the strain gauges before bonding them in place with Loctite 401. Epoxy-coated wires were then soldered to the strain gauges and terminated on solder pads to allow attachment of lead wires that would interface with the shield. Finally, the bonded sight was then coated with clear silicone RTV 80050 adhesive to protect the gauges.

Two shields were assembled, as each shield supports only two channels, and the quarter- and half-bridge channels required dummy resistors to be soldered in place (Figure 5). 

<img width="1367" height="1591" alt="Image" src="https://github.com/user-attachments/assets/ff707165-f358-413d-af95-843af3e8dbd9" />

**Figure 5 The amplifier shield is plugged into the Arduino Uno, with channel A1 configured for the half-bridge circuit and channel A0 configured for the quarter-bridge connection.**

Additionally, an integrated circuit (IC) socket was used in place of soldering INA125 chip directly so that all three configurations could be evaluated using the same instrumentation amplifier. A G-clamp was used to secure both the ruler and the steel flat bar to the edge of a table, and magnets of known mass were placed on the free end of each cantilever beam (Figure 4). Because the ruler (25.6 × 1 mm cross-section) is more flexible than the steel flat bar (13 × 3 mm cross-section), the respective masses applied to the steel ruler were 6, 12, 18, 24, 30, and 36 g. Conversely, for the flat-bar cantilever beam, the respective masses applied were 24, 48, 72, 96, 120, and 144 g. In both cases, the self-weight was ignored in the sense that the settled signal position was taken as the zero reference before applying the magnets.

The Arduino boards were flashed with the example ReadAnalogVoltage code, and the Python script DataLog.py was used to plot the live display and record the strain signal. The respective captured signals (QuarterBridge.txt, HalfBridge.txt, FullBridge.txt) and scripts (QuarterBridge.py, HalfBridge.py, FullBridge.py) are provided. The following headers are given in the script so the reader can walk through the code and easily identify similarities, differences, and the main steps required.

#LOAD DATA – The text file is imported containing the timestamp and the measured voltage differential signal.

#CONSTANTS – The gain of the amplifier is set by the 100 Ω resistor (x 604 gain). The bridge excitation voltage and the strain gauge’s gauge factor (K) are used to correlate the mechanical strain with the resulting electrical signal - Equation 1 – where δL/L is the strain (ε).
 δR/R=[δL/L]K Equation 1

#REMOVE OFFSET USING REAL BASELINE – Here the signal is base-lined, meaning the amplified voltage output before the cantilever beam is loaded is used as the zero-reference position.

STRAIN FROM AMPLIFIED SIGNAL – The amplified Wheatstone bridge output voltage is now converted into strain. This is achieved by dividing the signal by the amplifier gain (604) for all beam measurements and then applying the following formula to calculate the measured strain (Equation 2-4). In all cases, the gauge factor (K) is 2, and it can be observed that the full Wheatstone bridge is four times as sensitive as the quarter bridge.

**Quater Bridge:**
 E_out=(E_exc)/4δR/R=KE_exc/4ε Equation 2
 
**half Bridge:**
 E_out=(E_exc)/2δR/R=KE_exc/2ε Equation 3
 
**Full Bridge:**
 E_out=E_excδR/R=εKE_exc Equation 4

#BEAM GEOMETRY – The beam geometry of the two cantilever beams is saved in the script and it was assumed that the possion ratio (υ) is 0.3 and the Modulus (E) is 200GPa.

#STRESS & MOMENT – The relationship between stress and strain is used to determine the surface stress, and simple bending theory is applied to determine the bending moment at the position where the strain gauge is situated (equation 5-6).

ϭ=Eε Equation 5

M/I=ϭ/y=E/R Equation 6

#SMOOTH MOMENT FOR PLATEAU DETECTION – As the title suggests, a simple moving-average filter is used to remove signal noise.

#K-MEANS PLATEAU DETECTION (TOP 10% FLAT SAMPLES) – The smoothed moment signal is analysed by computing its absolute gradient. The flattest 10% of samples are selected by applying a percentile-based threshold to the gradient values. These low-gradient samples represent regions where the moment signal is approximately constant. K-means clustering (with seven clusters) is then applied to these flat samples to identify distinct plateau levels. The median value of each cluster is used as a robust estimate of the plateau height, and the resulting plateau moments are sorted to produce the final ordered set of measured moments.

#ANALYTICAL MOMENT – The expected bending moment at the strain-gauge location is calculated analytically using the beam’s loading and geometry.

#CALIBRATION FITS – A linear fit is obtained from the measured moment values and then compared with the analytical prediction.

**Results**

Figures 6–8 present the unfiltered strain-step responses of the cantilever beams during tip loading. The data indicates that the primary disturbances arose from positioning the magnets at each step, while the symmetric loading and unloading behavior demonstrates effective strain-gauge adhesion and confirms that the hardware delivered suitable signal conditioning.

<img width="1400" height="800" alt="Image" src="https://github.com/user-attachments/assets/a6335411-6128-402e-9abe-3a6e65264620" />

**Figure 6 full-bridge cantilever response showing moment progression during loading and subsequent unloading with 6 gram progression.**

<img width="1400" height="800" alt="Image" src="https://github.com/user-attachments/assets/832fa948-fbb6-455c-9f7c-2f89553ae2e4" />

**Figure 7  half- bridge cantilever response showing moment progression during loading and subsequent unloading with 24 gram progression.**

<img width="1400" height="800" alt="Image" src="https://github.com/user-attachments/assets/d8183543-e8cc-47e7-bc30-5dce3e5b8e07" />

**Figure 8  Quarter-bridge cantilever response showing moment progression during loading and subsequent unloading with 24 gram progression.**


Figures 9–12 highlight the excellent correlation between the calculated moment (derived from the strain measurement) and the analytical estimate. This agreement validates both the test protocol and the amplifier shield.

<img width="1000" height="600" alt="Image" src="https://github.com/user-attachments/assets/8676beb7-fc2c-4d09-b3a2-bd6f9d45efa2" />

**Figure 9 Full-Bridge Calibration Curve**

<img width="1000" height="600" alt="Image" src="https://github.com/user-attachments/assets/c9c93594-2d2a-4f9f-97f8-4bdf3a334782" />

**Figure 10 Half-Bridge Calibration Curve**

<img width="1000" height="600" alt="Image" src="https://github.com/user-attachments/assets/53b98133-d127-45db-b874-a05a1d555e56" />

**Figure 11 Quarter-Bridge Calibration Curve**

**Discussion**

Independent engineers have access to a wide range of public forums discussing strain-gauge signal conditioning. Nevertheless, much of the material found in scientific publications or online communities is presented as proof-of-concept implementations on veroboards or breadboards. Given the high amplification required for strain-gauge signals, a well-designed, properly grounded PCB with appropriate termination is essential to ensure low-noise performance. Furthermore, most of these solutions are designed for strain-gauge transducers rather than the half- or quarter-bridge configurations commonly used in stress analysis. The PCB presented in this report provides a practical solution by incorporating dummy gauges. The study demonstrates that these configurations have been validated by comparing the measured output with an analytical solution.
The advantage of the INA125 instrumentation amplifier is that it requires very little additional circuitry to provide bridge-excitation voltage and signal referencing, and this formed the basis of the PCB used in the study. The cantilever-beam evaluation illustrates that both the gain and the bridge-excitation voltage are precisely controlled, and that when interfaced with an Arduino in the form of a shield, a repeatable and accurate signal is obtained. Indeed, many poor strain-gauge measurements arise from inadequate bonding or soldering, although the importance of proper signal conditioning should not be overlooked.
The results have shown that there is good correlation when placing magnet weights by hand and that the loading and unloading steps show good symmetry. However, improved accuracy could be achieved by placing and removing weights using custom tooling. Furthermore, by visual inspection of the loading and unloading steps, it can be observed that the hysteresis was minimal, but it was not the purpose of this study to statistically comment on such details or to compare the measured output against an analytical calculation.

**Conclusion**

The solution presented in Figure 1, which incorporates the INA125 instrumentation amplifier, has been validated using full-, half-, and quarter-bridge strain-gauge configurations bonded to a cantilever beam. The PCB’s measured output was compared against an analytical solution, confirming its accuracy. This work demonstrates that the building block developed here provides a repeatable, validated method suitable for both transducer applications and stress-analysis measurements.

**Contact:** anthony.crimin@hotmail.co.uk
