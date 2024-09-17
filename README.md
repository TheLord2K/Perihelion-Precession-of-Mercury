# Perihelion Precession of Mercury 🌌

## Overview
This project analyzes the precession of Mercury’s perihelion, a phenomenon critical to validating Einstein's theory of general relativity. The program computes and visualizes the precession using Python, leveraging advanced numerical methods and data from real astronomical observations.

## Scientific Background
Mercury's orbit around the Sun is elliptical, with its closest point (perihelion) shifting over time. This shift, or precession, is influenced by the gravitational interactions of other planets and the curvature of spacetime around the Sun. By analyzing historical data, scientists calculated an unexplained precession rate of 43 arcseconds per century—precisely predicted by general relativity.

## Methodology
1. **Data Processing**: The dataset consists of perihelion coordinates for Mercury, gathered over centuries. I processed this data using NumPy, computing vector lengths and angles to accurately determine the precession rate.
   
2. **Numerical Calculations**: Vector dot products and trigonometric functions are employed to derive the angle of precession. The simulation closely matches established values from astronomical data.

3. **Visualization**: Using Matplotlib, I plotted the precession over time, including both actual and theoretical data for comparison. This visual representation underscores the accuracy of the general relativity prediction.

## Technologies Used
- **Programming Language**: Python
- **Libraries**: NumPy, SciPy, Matplotlib

## Achievements
- Verified Einstein’s theory by precisely calculating Mercury’s precession within a margin of error consistent with historical data.
- Demonstrated a deep understanding of numerical modeling and data analysis in a real-world scientific application.

## How to Run
1. Clone the repository:
   ```bash
   git clone https://github.com/TheLord2K/mercury-precession-analysis.git
