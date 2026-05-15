# DCA3 - Semiconductor Wafer Handling Software with Full HSMS/GEM Integration

**DCA3** is a modern rewrite of the DCA semiconductor handling system using the original DCA-The-New-Batch as visual and functional template.

## Features
- Tkinter GUI (same look & feel)
- Full HSMS (SEMI E37), SECS-II, GEM (SEMI E30) integration via secsgem
- Wafer/cassette management
- Robot & camera control
- Production logging and recovery
- GEM compliance: events, variables, alarms, control states

## Quick Start
1. `pip install -r requirements.txt`
2. Copy `.env.example` to `.env` and configure
3. `python -m dca3.main`

## Development
See `docs/development.md` and `CHANGELOG.md`.
