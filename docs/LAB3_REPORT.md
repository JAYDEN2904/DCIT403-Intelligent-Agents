# Lab 3: Goals, Events, and Reactive Behavior — Report

## Overview

Lab 3 implements **event-driven reactive behavior** using a **Finite State Machine (FSM)**. A **RescueAgent** reacts to disaster events that are triggered by **sensor reports** from a **SensorAgent**. The lab connects Lab 2 (perception) with Lab 3 (goal-based reactive behavior).

---

## Agents and Their Roles

### 1. SensorAgent (from Lab 2)

**Purpose:** Monitors a simulated disaster environment and reports conditions to the RescueAgent.

**What it does:**
- Uses a `DisasterEnvironment` that evolves over time (damage, water level, fire risk, accessibility).
- Every 2 seconds it calls `env.step()`, producing a new state.
- Builds a **percept** (JSON) with: `damage_severity`, `water_level`, `fire_risk`, `is_accessible`, `timestamp`.
- Logs each percept to a file.
- When configured with `rescue_jid`, sends each percept as an **INFORM** message to the RescueAgent via XMPP.

**Relationship:** Acts as the **event source**. Its reports are the events that drive the RescueAgent’s FSM.

---

### 2. RescueAgent (Lab 3)

**Purpose:** Responds to disaster events in a goal-directed way using an FSM.

**What it does:**
- Runs two parallel behaviours:
  1. **ReceiveSensorReportsBehaviour** — Receives INFORM messages from the SensorAgent, parses the percept, and appends it to `pending_events`.
  2. **RescueFSMBehaviour** — A finite state machine that reacts to queued events.

**Relationship:** Receives events from the SensorAgent and executes rescue goals based on severity.

---

## The Finite State Machine

The RescueAgent’s FSM cycles through four states:

```
     ┌────────────────────────────────────────────┐
     │  IDLE ──(sensor report)──► ALERT ──► RESPONDING   │
     │   ▲                              │         │
     │   └───── COMPLETED ◄─────────────┘         │
     └────────────────────────────────────────────┘
```

| State        | Behavior                                                                 |
|--------------|---------------------------------------------------------------------------|
| **IDLE**     | Waits for events. Checks `pending_events`. If empty, stays in IDLE. If not empty, pops a percept, creates a `DisasterEvent`, moves to ALERT. |
| **ALERT**    | Interprets the event and sets goals. High/critical severity → `SAVE_LIVES`, `ASSESS_DAMAGE`. Otherwise → `ASSESS_DAMAGE`, `SECURE_AREA`. Then moves to RESPONDING. |
| **RESPONDING** | Executes each goal in sequence, simulates work, sets outcome (SUCCESS/PARTIAL), then moves to COMPLETED. |
| **COMPLETED** | Logs the execution trace, clears the current event, and returns to IDLE. |

---

## Event Flow (End-to-End Process)

1. **SensorAgent** senses the environment.
2. **SensorAgent** sends an INFORM message containing the percept to `rescue@localhost`.
3. **RescueAgent’s ReceiveSensorReportsBehaviour** receives the message and appends the percept to `pending_events`.
4. **RescueAgent’s FSM** (in IDLE) checks `pending_events`, pops the first entry, and parses it into a `DisasterEvent`.
5. **DisasterEvent** infers event type (flood, fire, building_collapse, emergency) and severity (low, medium, high, critical) from the percept.
6. The FSM moves through ALERT → RESPONDING → COMPLETED, then returns to IDLE for the next event.

---

## Goals (RescueGoals)

| Goal          | Description                    |
|---------------|--------------------------------|
| `SAVE_LIVES`  | Highest-priority response      |
| `ASSESS_DAMAGE` | Inspect and assess damage    |
| `SECURE_AREA` | Make the area safe            |
| `DELIVER_AID` | Deliver aid (defined but not used) |

High/critical events use `SAVE_LIVES` and `ASSESS_DAMAGE`. Other events use `ASSESS_DAMAGE` and `SECURE_AREA`.

---

## How the Agents Relate

```
DisasterEnvironment  ──step()──►  SensorAgent
                                        │
                                        │ INFORM (percept)
                                        ▼
                         RescueAgent  ◄──  pending_events queue
                                │
                                └── FSM: IDLE → ALERT → RESPONDING → COMPLETED → IDLE
```

- **SensorAgent** is the **producer** of events.
- **RescueAgent** is the **consumer** that reacts through its FSM.
- Communication is one-way: SensorAgent → RescueAgent via XMPP INFORM messages.
- The FSM ensures reactions are ordered and goal-based rather than purely reflexive.

---

## Execution Trace

At the end of a run, the RescueAgent prints an execution trace containing:
- Cycle number
- Event description
- Goals executed
- Result (SUCCESS or PARTIAL)
- Timestamp

This supports verification and analysis of the system’s reactive behavior.
