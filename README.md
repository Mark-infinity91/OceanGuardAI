# OceanGuardAI
### AI-Driven Marine Debris Detection and Mapping System

**BuildFest 2.0 | Problem Statement PS-17**

## Overview
OceanGuardAI is a project aimed at supporting marine debris identification, observation management, and mapping through an integrated software workflow.

## Project Goals
- Support marine debris observation and classification.
- Store observation records and associated metadata.
- Track review status for recorded observations.
- Provide a dashboard for viewing observation summaries.
- Support geographic information and CSV export for further analysis.

## Current Development Progress

### Member 1–2 Workstream
The Member 1–2 workstream has been integrated by Member 1. Final integration with the other workstream remains in progress.

### Member 3–4 Workstream
The Member 3–4 workstream includes:
- Streamlit dashboard.
- SQLite observation database.
- Observation review-status updates.
- Observation statistics and summaries.
- CSV export functionality.
- GPS-coordinate validation and update functionality.
- Database tests for key operations and validation cases.

### Current Integration Status
The two workstreams are under development and final end-to-end integration is pending. Individual components have been developed and tested, but full-system compatibility and end-to-end behavior must be verified after merging.

## Technology Stack
- Python
- Streamlit
- SQLite
- Pandas
- NumPy

## Running the Member 3–4 Dashboard
Install the dependencies:

```bash
pip install -r requirements.txt
```

Run the dashboard:

```bash
streamlit run app_member3.py
```

Run database tests:

```bash
python test_database.py
```

Run these commands from the directory containing the relevant files.

## Development Roadmap
1. Complete integration of both workstreams.
2. Resolve interface and dependency mismatches.
3. Verify end-to-end application behavior.
4. Test database persistence, review status, and CSV export in the combined application.
5. Verify which visualizations use real records and which are illustrative.
6. Prepare the final demonstration and documentation.

## Project Status
**Prototype under active development.** Individual components have been implemented; final combined-system verification is pending.
