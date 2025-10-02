# SkyMind_Sim: G-HMADRL Simulation Framework

**Version:** 0.1.0 (Fidelity: Basic Visualization)
**Last Updated:** 1404/07/10

## Project Goal

This project aims to implement and simulate the G-HMADRL (Graph-based Hierarchical Multi-Agent Deep Reinforcement Learning) framework for UAV-assisted Mobile Edge Computing, as outlined in the comprehensive roadmap.

---

## Current Status & Progress

We are currently in **Phase 2: Basic Physics & Manual Control**.

### Roadmap Progress Tracker

- [x] **Phase 1: Visualization & Core Engine (Completed)**
  - [x] Setup Python environment (`venv`, `pygame`).
  - [x] Implemented modular project structure.
  - [x] Created `Environment` class for Pygame management.
  - [x] Created `Simulation` class for main loop orchestration.
  - [x] Implemented `AssetLoader` for resource management.
  - [x] Implemented basic `Drone` sprite class.
  - [x] **Key Achievement:** Resolved critical integration bugs, resulting in a stable visual foundation.
- [ ] **Phase 2: Basic Physics & Manual Control (In Progress)**
  - [ ] Implement Drone movement via keyboard input.
  - [ ] Define boundaries for the simulation area.
  - [ ] Implement basic physics (velocity, acceleration).
- [ ] **Phase 3: Core Simulation Logic**
  - [ ] Implement `UE`, `GBS` classes.
  - [ ] Implement `TaskGenerator`.
  - [ ] Implement mathematical models (Communication, Computation, Energy).
- [ ] **Phase 4: AI Integration (DRL)**
  - [ ] ...

---

## Project Log & Key Decisions

*   **1404/07/10:**
    *   **Activity:** Defined a collaboration protocol to ensure project continuity. Established the `README.md` as the project's single source of truth.
    *   **Decision:** We will follow a structured approach starting each session by reviewing the `README.md`.
*   **1404/07/08 (Example):**
    *   **Activity:** Successfully fixed the `pygame.error: cannot convert without pygame.display initialized` bug.
    *   **Decision:** The `Environment` must be instantiated before any assets that require display conversion are loaded. This architectural decision was critical.
*   **... (older entries)**

---

## How to Run

1.  Ensure you have Python 3.8+ installed.
2.  Setup the virtual environment: `python -m venv venv`
3.  Activate it: `source venv/Scripts/activate` (on Windows)
4.  Install dependencies: `pip install -r requirements.txt`
5.  Run the simulation: `python -m skymind_sim.main`
