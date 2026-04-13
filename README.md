# AIdria CLI

A powerful Apple QA engineering command line tool that generates test plans, accessibility audits, Radar bug reports, test matrices, and XCTest code — all powered by local AI running privately on your Mac.

## Commands

```bash
aidria test "Mail app"                    # Generate complete test plan
aidria audit "Safari"                     # Run accessibility audit
aidria radar "Bug description"            # File a Radar bug report
aidria matrix "Face ID, Dark Mode"        # Build test coverage matrix
aidria xctest "User Authentication"       # Generate XCTest Swift code
aidria brief                              # Morning QA briefing
aidria help                               # Show all commands
```

## Installation

1. Clone this repository:
git clone https://github.com/deandremedrano/aidria-cli.git
cd aidria-cli

2. Install Ollama from ollama.com and pull the required model:
ollama pull mistral-nemo

3. Make it available system-wide:
chmod +x aidria.py
sudo ln -s $(pwd)/aidria.py /usr/local/bin/aidria

4. Run from anywhere:
aidria brief

## Features

- Test Plan Generator — comprehensive test cases covering functional, edge case, negative, accessibility, and performance scenarios
- Accessibility Audit Runner — WCAG 2.1 and Apple HIG compliance checking
- Radar Bug Reporter — professionally formatted Radar-style bug reports with auto-detected system environment
- Test Matrix Builder — feature vs device coverage mapping across iPhone, iPad, Mac, Apple Watch, and Vision Pro
- XCTest Generator — production-ready Swift XCTest code using Apple's native testing framework
- Morning Briefing — daily QA focus areas, checklists, and interview tips

## Privacy

Everything runs locally on your Mac using Ollama. No data is sent to any external server. No API keys required. No subscriptions. No data sharing.

## Save Reports

Add --save to any command to save output to ~/aidria-reports/
aidria test "Safari" --save
aidria radar "Login button unresponsive" --save
aidria xctest "Face ID Authentication" --save

## Tech Stack

- Python 3.13
- Ollama (local AI runtime)
- Mistral Nemo 12B (runs locally)
- Apple XCTest framework (for generated code)

## Author

Built by Deandre Medrano
