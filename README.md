# Slotted ALOHA Performance Analysis and Simulation

This repository presents a theoretical and simulation-based study of a Slotted ALOHA communication protocol used in shared multiple access channels. The project includes detailed mathematical modeling and performance analysis, as well as a Python-based simulation tool to validate theoretical findings.

## Overview

Slotted ALOHA is a random access protocol used for data transmission in shared communication channels. This project investigates:

- System throughput (S)
- Average number of transmissions per successful packet (E(NT))
- Average packet delay (D)

under various parameters such as the number of stations (N), transmission probability (q), and backoff range (K).

## Theoretical Analysis

The analysis covers:
- Probabilities of successful transmissions
- Expected number of transmissions until success
- Maximum throughput and corresponding load values
- Performance curves (S vs. G, E(NT) vs. G, D vs. G, and D vs. S)
- Asymptotic behavior as N approaches infinity

All analytical results are derived and validated through equations and plotted graphs.

## Simulation

A custom Python simulator (`SlottedALOHASimulator.py`) models the Slotted ALOHA system with the following features:

- Per-station buffer behavior
- Packet generation with probability `p`
- Randomized backoff on collisions within range [1, K]
- Performance metrics captured across load conditions

### Simulation Parameters

- Packet length: 3600 bits
- Channel rate: 72 Mbps
- Slot time: 50 µs (based on transmission time)
- Values tested: `N = [4, 16]`, `K = [4, 10]`, plus a special case `N = 10, K = 10`

### Results

Graphs generated from the simulation include:
- Throughput vs. Load (S vs. G)
- Expected transmissions to success vs. Load (E(NT) vs. G)
- Delay vs. Load (D vs. G)
- Delay vs. Throughput (D vs. S)

These results align well with the theoretical expectations.

## How to Run the Simulation

```bash
python SlottedALOHASimulator.py
```

This will produce the performance plots and simulate the ALOHA system under the specified conditions.

## File Structure

- `SlottedALOHASimulator.py`: Source code of the simulation
- `README.md`: Project summary and instructions (this file)

## Key Takeaways

- Maximum throughput occurs around G = 1
- As system load increases, delay increases exponentially
- Analytical and simulated results converge in trends, validating the model

## License

This project is released for academic and research purposes. Please credit the source if used in publications or derivative works.
