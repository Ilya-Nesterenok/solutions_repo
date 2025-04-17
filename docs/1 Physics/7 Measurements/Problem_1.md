# Problem 1


## **Measuring Earth's Gravitational Acceleration Using a Simple Pendulum**

## **1. Theoretical Background**

A simple pendulum consists of a mass (called the bob) suspended from a fixed point by a string or rod of negligible mass. When displaced from its equilibrium position and released, the pendulum swings back and forth under the influence of gravity.

For small angular displacements (typically less than 15°), the motion of a simple pendulum approximates simple harmonic motion. The period $T$ of oscillation (the time for one complete cycle) is given by:

$$
T = 2\pi \sqrt{\frac{L}{g}}
$$

Where:
- $T$ is the period of oscillation (in seconds),
- $L$ is the length of the pendulum (in meters),
- $g$ is the acceleration due to gravity (in m/s²).

Rearranging the formula to solve for $g$:

$$
g = \frac{4\pi^2 L}{T^2}
$$

This equation allows for the experimental determination of $g$ by measuring $L$ and $T$.

---

## **2. Experimental Procedure**

### **Materials Required**
- String (1 to 1.5 meters in length)
- Small dense object (e.g., metal nut) as the pendulum bob
- Stopwatch or timer
- Ruler or measuring tape

### **Setup**
1. Attach the bob to one end of the string.
2. Secure the other end of the string to a fixed support, allowing the pendulum to swing freely.
3. Measure the length $L$ from the point of suspension to the center of mass of the bob. Record the measurement and the resolution of the measuring instrument.

### **Data Collection**
1. Displace the pendulum slightly (angle less than 15°) and release it without imparting additional force.
2. Use the stopwatch to measure the time taken for 10 complete oscillations. Record this time as $T_{10}$.
3. Repeat the measurement 10 times to obtain a set of $T_{10}$ values.

---

## **3. Data Analysis**

### **Sample Data**

Based on experimental data from Don Cross's pendulum experiment:

- **Length of pendulum**: $L = 1.634 \, \text{m}$
- **Measured period**: $T = 2.57025 \, \text{s}$
- **Uncertainty in period**: $\Delta T = 0.00123 \, \text{s}$
- **Calculated gravitational acceleration**: $g = 9.7787 \, \text{m/s}^2$
- **Uncertainty in $g$**: $\Delta g = 0.0094 \, \text{m/s}^2$

### **Calculations**

1. **Period of One Oscillation**:
    $$
    T = \frac{\overline{T_{10}}}{10}
    $$

2. **Mean Period**:
    $$
    \overline{T} = \frac{1}{n} \sum_{i=1}^{n} T_i
    $$

3. **Standard Deviation**:
    $$
    \sigma_T = \sqrt{\frac{1}{n-1} \sum_{i=1}^{n} (T_i - \overline{T})^2}
    $$

4. **Uncertainty in Mean Period**:
    $$
    \Delta T = \frac{\sigma_T}{\sqrt{n}}
    $$

5. **Gravitational Acceleration**:
    $$
    g = \frac{4\pi^2 L}{T^2}
    $$

6. **Propagation of Uncertainty in $g$**:
    $$
    \Delta g = g \cdot \sqrt{\left( \frac{\Delta L}{L} \right)^2 + \left( 2 \cdot \frac{\Delta T}{T} \right)^2}
    $$

---

## **4. Results**

Using the provided data:

- **Length**: $L = 1.634 \, \text{m}$
- **Period**: $T = 2.57025 \, \text{s}$
- **Calculated $g$**: $9.7787 \, \text{m/s}^2$
- **Uncertainty in $g$**: $\pm 0.0094 \, \text{m/s}^2$

---

## **5. Discussion**

### **Comparison with Standard Value**

The standard value of gravitational acceleration at sea level is approximately $9.80665 \, \text{m/s}^2$. The measured value of $9.7787 \, \text{m/s}^2$ is slightly lower, which could be attributed to factors such as:

- **Geographical Location**: Gravity varies with latitude and altitude.
- **Measurement Uncertainties**: Errors in timing and length measurement.
- **Air Resistance**: Not accounted for in the simple pendulum model.
- **Amplitude of Swing**: Larger amplitudes introduce non-linear effects.

### **Sources of Uncertainty**

1. **Length Measurement**: Inaccuracies in measuring from the pivot point to the center of mass of the bob.
2. **Timing**: Human reaction time when using a manual stopwatch.
3. **Environmental Factors**: Air currents and temperature variations can affect the pendulum's motion.

### **Improving Accuracy**

- Use a longer pendulum to increase the period, reducing relative timing errors.
- Employ electronic timing methods to minimize human reaction time errors.
- Conduct the experiment in a controlled environment to reduce air currents and temperature fluctuations.

---

## **6. Conclusion**

The experiment demonstrates a practical method for estimating the acceleration due to gravity using a simple pendulum. While the measured value may deviate slightly from the standard value due to various uncertainties, careful experimental design and measurement can yield results that closely approximate the true value of $g$.

---

