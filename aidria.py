#!/usr/bin/env python3
"""
AIdria CLI — Apple QA Command Line Tool
A powerful terminal-based QA engineering assistant for Apple engineers.
Author: Deandre Medrano

Usage:
  aidria test "Mail app"
  aidria audit "Safari login screen"
  aidria radar "bug description"
  aidria matrix "feature1, feature2, feature3"
  aidria brief
  aidria help
"""

import sys
import json
import requests
import platform
import subprocess
import datetime
import argparse
import os
from typing import Optional

# ── Configuration ──────────────────────────────────────────────────────────────

OLLAMA_URL = "http://localhost:11434/api/chat"
MODEL = "mistral-nemo:latest"
VERSION = "1.0.0"

# ── Colors ─────────────────────────────────────────────────────────────────────

class C:
    BLUE    = "\033[94m"
    GREEN   = "\033[92m"
    YELLOW  = "\033[93m"
    RED     = "\033[91m"
    BOLD    = "\033[1m"
    DIM     = "\033[2m"
    RESET   = "\033[0m"
    CYAN    = "\033[96m"
    WHITE   = "\033[97m"
    MAGENTA = "\033[95m"

def blue(s):    return f"{C.BLUE}{s}{C.RESET}"
def green(s):   return f"{C.GREEN}{s}{C.RESET}"
def yellow(s):  return f"{C.YELLOW}{s}{C.RESET}"
def red(s):     return f"{C.RED}{s}{C.RESET}"
def bold(s):    return f"{C.BOLD}{s}{C.RESET}"
def dim(s):     return f"{C.DIM}{s}{C.RESET}"
def cyan(s):    return f"{C.CYAN}{s}{C.RESET}"
def magenta(s): return f"{C.MAGENTA}{s}{C.RESET}"

# ── System Info ─────────────────────────────────────────────────────────────────

def get_system_info():
    info = {
        "os": platform.system(),
        "os_version": platform.mac_ver()[0] if platform.system() == "Darwin" else platform.version(),
        "machine": platform.machine(),
        "python": sys.version.split()[0],
        "date": datetime.datetime.now().strftime("%B %d, %Y at %I:%M %p")
    }
    try:
        result = subprocess.run(
            ["/Applications/Google Chrome.app/Contents/MacOS/Google Chrome", "--version"],
            capture_output=True, text=True
        )
        info["browser"] = result.stdout.strip()
    except:
        info["browser"] = "Chrome not detected"
    return info

# ── AI Engine ───────────────────────────────────────────────────────────────────

def ask_ai(system_prompt: str, user_message: str, stream: bool = True) -> str:
    """Call local Ollama AI model."""
    try:
        response = requests.post(
            OLLAMA_URL,
            json={
                "model": MODEL,
                "messages": [
                    {"role": "system", "content": system_prompt},
                    {"role": "user", "content": user_message}
                ],
                "stream": stream
            },
            stream=stream,
            timeout=120
        )

        if stream:
            full_content = ""
            for line in response.iter_lines():
                if line:
                    try:
                        data = json.loads(line)
                        if data.get("message", {}).get("content"):
                            chunk = data["message"]["content"]
                            full_content += chunk
                            print(chunk, end="", flush=True)
                    except:
                        pass
            print()
            return full_content
        else:
            data = response.json()
            return data["message"]["content"]

    except requests.exceptions.ConnectionError:
        print(red("\n✗ Cannot connect to Ollama. Make sure Ollama is running."))
        print(dim("  Start Ollama from your menu bar or run: ollama serve"))
        sys.exit(1)

# ── Banner ──────────────────────────────────────────────────────────────────────

def print_banner():
    print(f"""
{bold(blue('  AIdria CLI'))} {dim(f'v{VERSION}')}
  {dim('Apple QA Command Line Tool by Deandre Medrano')}
""")

def print_divider(title: str = ""):
    width = 60
    if title:
        padding = (width - len(title) - 2) // 2
        print(f"\n{dim('─' * padding)} {cyan(title)} {dim('─' * padding)}\n")
    else:
        print(dim("─" * width))

def print_step(step: str):
    print(f"\n{blue('◆')} {bold(step)}")

def print_success(msg: str):
    print(f"{green('✓')} {msg}")

def print_warning(msg: str):
    print(f"{yellow('⚠')} {msg}")

def print_error(msg: str):
    print(f"{red('✗')} {msg}")

def save_report(content: str, filename: str) -> str:
    """Save report to file."""
    reports_dir = os.path.expanduser("~/aidria-reports")
    os.makedirs(reports_dir, exist_ok=True)
    filepath = os.path.join(reports_dir, filename)
    with open(filepath, "w") as f:
        f.write(content)
    return filepath

# ── Commands ────────────────────────────────────────────────────────────────────

def cmd_test(app_name: str, save: bool = False):
    """Generate a complete test plan for an Apple app."""
    print_banner()
    print_divider(f"TEST PLAN — {app_name.upper()}")

    system = """You are a senior Apple QA engineer with 15 years of experience.
Generate a comprehensive, professional test plan. Format exactly like this:

## Test Plan: [App Name]
**Generated:** [date]
**Engineer:** Deandre Medrano

### Functional Tests
| ID | Test Case | Steps | Expected | Severity |
|----|-----------|-------|----------|----------|
| TC001 | [name] | [steps] | [expected] | Critical/High/Medium/Low |

### Edge Cases
| ID | Test Case | Steps | Expected | Severity |
|----|-----------|-------|----------|----------|

### Negative Tests
| ID | Test Case | Steps | Expected | Severity |
|----|-----------|-------|----------|----------|

### Accessibility Tests
| ID | Test Case | Steps | Expected | Severity |
|----|-----------|-------|----------|----------|

### Performance Tests
| ID | Test Case | Steps | Expected | Severity |
|----|-----------|-------|----------|----------|

### Summary
- Total tests: [number]
- Critical: [number]
- High: [number]
- Medium: [number]
- Low: [number]
- Automation candidates: [list]"""

    print_step(f"Generating test plan for {bold(app_name)}...")
    print(dim("  Running on Mistral Nemo 12B locally\n"))

    content = ask_ai(system, f"Generate a comprehensive test plan for Apple's {app_name} app.")

    if save:
        timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"test_plan_{app_name.lower().replace(' ', '_')}_{timestamp}.md"
        filepath = save_report(content, filename)
        print(f"\n{green('✓')} Report saved to: {bold(filepath)}")

    print_divider()
    print_success(f"Test plan generated for {app_name}")
    print(dim(f"  Tip: Run {cyan('aidria radar')} to file a bug report for any failures"))


def cmd_audit(target: str, save: bool = False):
    """Run an accessibility audit."""
    print_banner()
    print_divider(f"ACCESSIBILITY AUDIT — {target.upper()}")

    system = """You are an Apple accessibility expert with 15 years of experience.
Perform a detailed accessibility audit against WCAG 2.1 and Apple Human Interface Guidelines.

Format exactly like this:

## Accessibility Audit: [Target]
**Date:** [date]
**Auditor:** Deandre Medrano

### Score: [X]/100 — Grade: [A/B/C/D/F]
[One sentence summary]

### Critical Violations
| ID | WCAG | Issue | Element | Fix |
|----|------|-------|---------|-----|

### High Priority Issues
| ID | WCAG | Issue | Element | Fix |
|----|------|-------|---------|-----|

### Passing Criteria
| Criterion | Status | Notes |
|-----------|--------|-------|

### Apple HIG Compliance
[Assessment of Apple Human Interface Guidelines compliance]

### Top 5 Recommendations
1. [Most critical fix]
2.
3.
4.
5.

### Testing Checklist
- [ ] VoiceOver navigation
- [ ] Dynamic Type scaling
- [ ] Color contrast ratios
- [ ] Touch target sizes (minimum 44x44pt)
- [ ] Keyboard navigation
- [ ] Reduce Motion support
- [ ] High Contrast mode"""

    print_step(f"Running accessibility audit for {bold(target)}...")
    print(dim("  Checking WCAG 2.1 + Apple HIG compliance\n"))

    content = ask_ai(system, f"Perform a comprehensive accessibility audit for: {target}")

    if save:
        timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"accessibility_audit_{target.lower().replace(' ', '_')}_{timestamp}.md"
        filepath = save_report(content, filename)
        print(f"\n{green('✓')} Report saved to: {bold(filepath)}")

    print_divider()
    print_success(f"Accessibility audit complete for {target}")


def cmd_radar(description: str, save: bool = True):
    """File a Radar bug report."""
    print_banner()
    print_divider("RADAR BUG REPORT")

    system = """You are a senior Apple QA engineer. Generate a professional Radar-style bug report.

Format exactly like this:

================================================================================
RADAR BUG REPORT
Apple QA Portfolio | Filed by Deandre Medrano
================================================================================

SUMMARY
-------
[One clear sentence describing the bug]

METADATA
--------
Radar ID:    FB[8 random digits]
Date:        [today]
Reporter:    Deandre Medrano
Severity:    [Critical/High/Medium/Low]
Priority:    [P1/P2/P3/P4]
Status:      Open
Component:   [affected component]

STEPS TO REPRODUCE
------------------
1. [Step 1]
2. [Step 2]
3. [Step 3]

EXPECTED RESULT
---------------
[What should happen]

ACTUAL RESULT
-------------
[What actually happens]

IMPACT
------
[Who is affected and how severely]

POSSIBLE ROOT CAUSE
-------------------
[Technical hypothesis]

RECOMMENDED FIX
---------------
[Suggested investigation area]

ATTACHMENTS NEEDED
------------------
[ ] Screenshot
[ ] Screen recording
[ ] Console logs
[ ] Crash report

================================================================================"""

    sysinfo = get_system_info()

    print_step("Generating Radar bug report...")
    print(dim("  Auto-detecting system environment\n"))
    print(dim(f"  OS: macOS {sysinfo['os_version']} | Machine: {sysinfo['machine']} | Browser: {sysinfo['browser']}\n"))

    user_message = f"""Generate a Radar bug report for this issue:

{description}

Environment:
- OS: macOS {sysinfo['os_version']}
- Machine: {sysinfo['machine']} (Apple Silicon)
- Browser: {sysinfo['browser']}
- Date: {sysinfo['date']}"""

    content = ask_ai(system, user_message)

    if save:
        timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"radar_{timestamp}.txt"
        filepath = save_report(content, filename)
        print(f"\n{green('✓')} Radar saved to: {bold(filepath)}")
        print(dim("  Ready to paste into Apple Feedback Assistant or Jira"))

    print_divider()
    print_success("Radar report filed successfully")


def cmd_matrix(features_input: str, save: bool = False):
    """Build a test matrix for features across Apple devices."""
    print_banner()
    print_divider("TEST MATRIX BUILDER")

    system = """You are a senior Apple QA engineer. Generate a test coverage matrix.

Format exactly like this:

## Test Coverage Matrix
**Generated:** [date]
**Engineer:** Deandre Medrano

### Device Coverage

| Feature | iPhone 15 | iPhone 16 | iPad Air | MacBook Pro | Apple Watch | Vision Pro |
|---------|-----------|-----------|----------|-------------|-------------|------------|
| [feature] | ● Required | ● Required | ◐ Recommended | ○ Optional | — N/A | — N/A |

Legend: ● Required | ◐ Recommended | ○ Optional | — Not Applicable

### OS Version Coverage

| Feature | iOS 17 | iOS 18 | macOS 14 | macOS 15 | watchOS 10 |
|---------|--------|--------|----------|----------|------------|

### Risk Assessment
| Feature | Risk Level | Justification |
|---------|------------|---------------|

### Testing Priority Order
1. [Highest priority feature and why]
2.
3.

### Estimated Testing Time
- Total test cases: [number]
- Estimated time: [hours]
- Recommended team size: [number]"""

    print_step("Building test matrix...")
    print(dim("  Mapping coverage across Apple devices and OS versions\n"))

    content = ask_ai(system, f"Generate a test matrix for these features:\n\n{features_input}")

    if save:
        timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"test_matrix_{timestamp}.md"
        filepath = save_report(content, filename)
        print(f"\n{green('✓')} Matrix saved to: {bold(filepath)}")

    print_divider()
    print_success("Test matrix generated")


def cmd_brief():
    """Generate a morning QA briefing."""
    print_banner()
    print_divider("MORNING QA BRIEFING")

    system = """You are a senior Apple QA lead giving a morning briefing to your team.
Generate an inspiring, practical morning QA briefing.

Format like this:

## Morning QA Briefing
**Date:** [today]
**Prepared by:** AIdria CLI

### Good Morning, Deandre 👋

### Today's QA Focus Areas
[3-4 specific areas to focus on today based on common Apple QA priorities]

### Apple QA Best Practices Reminder
[One practical tip relevant to Apple QA engineering]

### Today's Testing Checklist
- [ ] [Task 1]
- [ ] [Task 2]
- [ ] [Task 3]
- [ ] [Task 4]
- [ ] [Task 5]

### Interview Tip of the Day
[One specific tip for Apple QA interviews]

### Motivational Note
[One sentence of genuine encouragement]

---
*Generated by AIdria CLI — Private · Local · Secure*"""

    sysinfo = get_system_info()
    print_step("Generating your morning briefing...")
    print(dim(f"  {sysinfo['date']}\n"))

    content = ask_ai(system, f"Generate a morning QA briefing for today, {sysinfo['date']}. Deandre is preparing for Apple QA engineering roles.")

    print_divider()
    print_success("Have a productive day, Deandre!")


def cmd_xctest(feature: str, save: bool = False):
    """Generate XCTest code for a feature."""
    print_banner()
    print_divider(f"XCTEST GENERATOR — {feature.upper()}")

    system = """You are an expert Apple QA automation engineer.
Generate complete, production-ready XCTest code in Swift.

Always use this structure:

import XCTest

final class [FeatureName]Tests: XCTestCase {

    var app: XCUIApplication!

    override func setUpWithError() throws {
        continueAfterFailure = false
        app = XCUIApplication()
        app.launch()
    }

    override func tearDownWithError() throws {
        app = nil
    }

    // MARK: - Tests
    func test[TestName]() throws {
        // Arrange
        // Act
        // Assert
    }
}

Write complete test functions with proper XCTest assertions. Include UI tests using XCUIApplication. Add comments explaining each test."""

    print_step(f"Generating XCTest code for {bold(feature)}...")
    print(dim("  Using Apple's native XCTest framework\n"))

    content = ask_ai(system, f"Generate complete XCTest Swift code to test: {feature}")

    if save:
        timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"xctest_{feature.lower().replace(' ', '_')}_{timestamp}.swift"
        filepath = save_report(content, filename)
        print(f"\n{green('✓')} XCTest file saved to: {bold(filepath)}")
        print(dim("  Add this file to your Xcode project to run the tests"))

    print_divider()
    print_success(f"XCTest code generated for {feature}")


def cmd_help():
    """Show help information."""
    print_banner()
    print(f"""  {bold('COMMANDS')}

  {cyan('aidria test')} {yellow('"App Name"')}          Generate a complete test plan
  {cyan('aidria audit')} {yellow('"Target"')}           Run an accessibility audit
  {cyan('aidria radar')} {yellow('"Bug description"')}  File a Radar bug report
  {cyan('aidria matrix')} {yellow('"Feature list"')}    Build a test coverage matrix
  {cyan('aidria xctest')} {yellow('"Feature"')}         Generate XCTest Swift code
  {cyan('aidria brief')}                   Get your morning QA briefing
  {cyan('aidria help')}                    Show this help message

  {bold('OPTIONS')}

  {cyan('--save')}    Save output to ~/aidria-reports/

  {bold('EXAMPLES')}

  {dim('$ aidria test "Mail app"')}
  {dim('$ aidria test "Safari" --save')}
  {dim('$ aidria audit "https://apple.com"')}
  {dim('$ aidria radar "Login button unresponsive on iPhone 16"')}
  {dim('$ aidria matrix "Face ID, Push Notifications, Dark Mode"')}
  {dim('$ aidria xctest "User Authentication" --save')}
  {dim('$ aidria brief')}

  {bold('ABOUT')}

  {dim(f'AIdria CLI v{VERSION}')}
  {dim('Built by Deandre Medrano')}
  {dim('Powered by Mistral Nemo 12B running locally on your Mac')}
  {dim('Private · Secure · No cloud · No data sharing')}
""")


# ── Main ────────────────────────────────────────────────────────────────────────

def main():
    parser = argparse.ArgumentParser(
        prog="aidria",
        description="AIdria CLI — Apple QA Command Line Tool",
        add_help=False
    )
    parser.add_argument("command", nargs="?", default="help")
    parser.add_argument("target", nargs="?", default="")
    parser.add_argument("--save", action="store_true", help="Save output to file")

    args = parser.parse_args()
    cmd = args.command.lower()
    target = args.target
    save = args.save

    if cmd == "test":
        if not target:
            print_error("Please specify an app name. Example: aidria test \"Mail app\"")
            sys.exit(1)
        cmd_test(target, save)

    elif cmd == "audit":
        if not target:
            print_error("Please specify a target. Example: aidria audit \"Safari\"")
            sys.exit(1)
        cmd_audit(target, save)

    elif cmd == "radar":
        if not target:
            print_error("Please describe the bug. Example: aidria radar \"Login button unresponsive\"")
            sys.exit(1)
        cmd_radar(target, save)

    elif cmd == "matrix":
        if not target:
            print_error("Please list features. Example: aidria matrix \"Face ID, Dark Mode, Push Notifications\"")
            sys.exit(1)
        cmd_matrix(target, save)

    elif cmd == "xctest":
        if not target:
            print_error("Please specify a feature. Example: aidria xctest \"User Authentication\"")
            sys.exit(1)
        cmd_xctest(target, save)

    elif cmd == "brief":
        cmd_brief()

    elif cmd in ["help", "--help", "-h"]:
        cmd_help()

    else:
        print_error(f"Unknown command: {cmd}")
        print(dim("  Run 'aidria help' to see available commands"))
        sys.exit(1)


if __name__ == "__main__":
    main()