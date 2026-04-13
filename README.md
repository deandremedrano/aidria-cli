# AIdria CLI

A powerful Apple QA engineering command line tool that generates test plans, accessibility audits, Apple Feedback Assistant reports, test matrices, XCTest code, and defect predictions — all powered by local AI running privately on your Mac.

## Commands

```bash
aidria test "Mail app"                                        # Generate complete test plan
aidria audit "Safari"                                         # Run accessibility audit
aidria feedback "Safari crashes when opening PDF"             # Generate Apple Feedback Assistant report
aidria matrix "Face ID, Dark Mode, Push Notifications"        # Build test coverage matrix
aidria xctest "User Authentication"                           # Generate XCTest Swift code
aidria predict "Refactored Mail compose window"               # Predict defects from code changes
aidria convert "Users should be able to log in with Face ID"  # Convert requirement to XCTest
aidria brief                                                  # Morning QA briefing
aidria help                                                   # Show all commands
```

## Installation

1. Clone this repository:
git clone https://github.com/deandremedrano/aidria-cli.git
cd aidria-cli

2. Install Ollama from ollama.com and pull the required models:
ollama pull mistral-nemo
ollama pull qwen2.5-coder

3. Make it available system-wide:
chmod +x aidria.py
sudo ln -s $(pwd)/aidria.py /usr/local/bin/aidria

4. Run from anywhere:
aidria brief

## Features

- Test Plan Generator — comprehensive test cases covering functional, edge case, negative, accessibility, and performance scenarios
- Accessibility Audit Runner — WCAG 2.1 and Apple HIG compliance checking
- Apple Feedback Assistant Reporter — generates detailed, professionally formatted bug reports ready to submit at feedbackassistant.apple.com, helping build a real feedback portfolio that Apple engineers can see
- Test Matrix Builder — feature vs device coverage mapping across iPhone, iPad, Mac, Apple Watch, and Vision Pro
- XCTest Generator — production-ready Swift XCTest code using Apple's native testing framework
- Natural Language Test Converter — converts plain English product requirements directly into executable XCTest Swift code
- Defect Prediction Engine — analyzes code changes and predicts which areas are most likely to contain bugs with confidence scores and blast radius analysis
- Morning Briefing — daily QA focus areas, checklists, and interview tips

## Feedback Portfolio

AIdria CLI helps you build a real Apple Feedback Assistant portfolio by generating detailed, reproducible bug reports for issues you find in Apple software.

1. Find a bug in any Apple app on your Mac
2. Run: aidria feedback "describe what you found" --save
3. Copy the generated report into feedbackassistant.apple.com
4. Attach a screen recording for best results
5. Submit — every report becomes a portfolio piece

Reports are saved to ~/aidria-reports/ automatically with --save.

## Privacy

Everything runs locally on your Mac using Ollama. No data is sent to any external server. No API keys required. No subscriptions. No data sharing.

## Save Reports

Add --save to any command to save output to ~/aidria-reports/
aidria test "Safari" --save
aidria feedback "Login button unresponsive on iPhone 16" --save
aidria xctest "Face ID Authentication" --save
aidria predict "Refactored authentication system" --save
aidria convert "Users should be able to reset their password via email" --save

## Models

- Mistral Nemo 12B — test plans, audits, feedback reports, defect prediction, briefings
- Qwen2.5 Coder — XCTest generation, natural language conversion

## Tech Stack

- Python 3.13
- Ollama (local AI runtime)
- Mistral Nemo 12B (runs locally)
- Qwen2.5 Coder (runs locally)
- Apple XCTest framework (for generated code)
- Apple Feedback Assistant (feedbackassistant.apple.com)

## Author

Built by Deandre Medrano
