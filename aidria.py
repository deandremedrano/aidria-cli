#!/usr/bin/env python3
"""
AIdria CLI — Apple QA Command Line Tool
A powerful terminal-based QA engineering assistant for Apple engineers.
Author: Deandre Medrano

Usage:
  aidria test "Mail app"
  aidria audit "Safari login screen"
  aidria feedback "bug description"
  aidria matrix "feature1, feature2, feature3"
  aidria xctest "User Authentication"
  aidria predict "code change description"
  aidria convert "plain english requirement"
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
VERSION = "1.3.0"

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

def ask_ai(system_prompt: str, user_message: str, stream: bool = True, model: str = "mistral-nemo:latest") -> str:
    try:
        response = requests.post(
            OLLAMA_URL,
            json={
                "model": model,
                "messages": [
                    {"role": "system", "content": system_prompt},
                    {"role": "user", "content": user_message}
                ],
                "stream": stream
            },
            stream=stream,
            timeout=180
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

# ── Banner & UI ─────────────────────────────────────────────────────────────────

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
    reports_dir = os.path.expanduser("~/aidria-reports")
    os.makedirs(reports_dir, exist_ok=True)
    filepath = os.path.join(reports_dir, filename)
    with open(filepath, "w") as f:
        f.write(content)
    return filepath

# ── Commands ────────────────────────────────────────────────────────────────────

def cmd_feedback(description: str, save: bool = True):
    """Generate a perfectly formatted Apple Feedback Assistant report."""
    print_banner()
    print_divider("APPLE FEEDBACK ASSISTANT")

    system = """You are a senior Apple QA engineer with 15 years of experience writing exceptionally detailed and impactful bug reports for Apple's Feedback Assistant. You know exactly what Apple engineers need to see to reproduce, understand, and fix issues.

Your feedback reports are so detailed and well-written that Apple engineers can reproduce the issue in under 2 minutes.

Generate a complete Apple Feedback Assistant report in this exact format:

================================================================================
APPLE FEEDBACK ASSISTANT REPORT
Submitted via: Feedback Assistant (feedbackassistant.apple.com)
Reporter: Deandre Medrano
================================================================================

FEEDBACK TYPE
-------------
Bug Report

PRODUCT
-------
[Affected Apple product — e.g. macOS 26.5, iOS 18.4, Safari 18]

TITLE
-----
[Clear, specific one-line title — what breaks, where, and under what condition]

DESCRIPTION
-----------
[2-3 sentences clearly describing what the bug is, when it occurs, and why it matters to users]

STEPS TO REPRODUCE
------------------
Be extremely specific. Include exact UI element names, button labels, and menu paths.

1. [Very specific step with exact UI element names]
2. [Exact step]
3. [Exact step]
4. [Exact step]
5. [Exact step — what triggers the bug]

EXPECTED BEHAVIOR
-----------------
[What should happen — be specific about the correct behavior]

ACTUAL BEHAVIOR
---------------
[Exactly what happens instead — be precise about the incorrect behavior]

FREQUENCY
---------
[Always / Most of the time (>75%) / Sometimes (25-75%) / Rarely (<25%)]
[Any pattern or conditions that affect frequency]

IMPACT
------
Severity: [Critical / High / Medium / Low]

[Who is affected — all users, specific configurations, etc.]
[What workflow is blocked or degraded]
[Business impact if applicable]

ENVIRONMENT
-----------
OS:              macOS [version] ([build number if known])
Device:          [Device model]
Chip:            [Apple Silicon / Intel]
RAM:             [Amount]
App Version:     [If applicable]
Network:         [WiFi / Ethernet / Offline if relevant]
Reproducible on: [List of devices/OS versions if tested on multiple]

ADDITIONAL CONTEXT
------------------
[Any additional technical details, patterns noticed, workarounds discovered, or related issues]

WORKAROUND
----------
[If a workaround exists, describe it clearly. If none, state "No workaround found."]

ATTACHMENTS RECOMMENDED
-----------------------
[ ] Screen recording showing the issue occurring
[ ] Screenshot of the actual behavior
[ ] Console logs from the time of the issue (Console.app)
[ ] Sysdiagnose (if crash or system-level issue)
[ ] Sample of affected file (if file-related issue)

SUGGESTED FIX AREA
------------------
[Your technical hypothesis about where the bug likely lives in the codebase or system]

================================================================================
FEEDBACK PORTFOLIO NOTE
This report was prepared using AIdria CLI — Apple QA Feedback Portfolio Tool
Built by Deandre Medrano | github.com/deandremedrano
================================================================================"""

    sysinfo = get_system_info()

    print_step("Generating Apple Feedback Assistant report...")
    print(dim("  Crafting detailed reproduction steps"))
    print(dim("  Auto-detecting system environment"))
    print(dim("  Optimizing for Apple engineer readability\n"))

    user_message = f"""Generate a detailed Apple Feedback Assistant report for this issue:

ISSUE DESCRIPTION:
{description}

REPORTER ENVIRONMENT:
- OS: macOS {sysinfo['os_version']}
- Machine: {sysinfo['machine']} (Apple Silicon M3)
- RAM: 16GB
- Browser: {sysinfo['browser']}
- Python: {sysinfo['python']}
- Date: {sysinfo['date']}

Make this report so detailed and clear that an Apple engineer can reproduce it in under 2 minutes. Be specific about UI element names, exact steps, and technical details."""

    content = ask_ai(system, user_message)

    if save:
        timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
        safe_name = description[:30].lower().replace(" ", "_").replace('"', "")
        filename = f"feedback_{safe_name}_{timestamp}.txt"
        filepath = save_report(content, filename)
        print(f"\n{green('✓')} Feedback report saved to: {bold(filepath)}")
        print(dim("  Copy and paste this into feedbackassistant.apple.com"))
        print(dim("  Attach screen recording and console logs for best results"))

    print_divider()
    print_success("Apple Feedback report generated")
    print(dim("  Submit at: feedbackassistant.apple.com"))
    print(dim("  Tip: Attach a screen recording to dramatically increase response rate"))


def cmd_convert(requirement: str, save: bool = False):
    """Natural Language Test Converter."""
    print_banner()
    print_divider("NATURAL LANGUAGE TEST CONVERTER")

    system = """You are an elite Apple QA automation engineer with 15 years of experience writing XCTest and XCUITest code at Apple.

Convert plain English product requirements into complete, production-ready XCTest Swift code.

Always use this exact file structure:

//
//  [FeatureName]Tests.swift
//  Generated by AIdria CLI — Natural Language Test Converter
//  Requirement: "[original requirement]"
//  Generated: [date]
//  Engineer: Deandre Medrano
//

import XCTest

// MARK: - [Feature Name] Tests
// Requirement: [restate the plain English requirement]

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

    // MARK: - Happy Path Tests
    func test[HappyPath]() throws {
        // Requirement: [which part this covers]
        // Arrange
        // Act
        // Assert
    }

    // MARK: - Edge Case Tests
    func test[EdgeCase]() throws {
        // Arrange
        // Act
        // Assert
    }

    // MARK: - Negative Tests
    func test[Negative]() throws {
        // Arrange
        // Act
        // Assert
    }

    // MARK: - Accessibility Tests
    func test[Feature]IsAccessible() throws {
        // Arrange
        // Act
        // Assert
    }

    // MARK: - Performance Tests
    func test[Feature]Performance() throws {
        measure {
        }
    }
}"""

    print_step("Parsing plain English requirement...")
    print(dim(f"  Input: \"{requirement}\""))
    print(dim("  Converting to XCTest Swift using Qwen2.5 Coder\n"))
    print(dim("  Extracting testable behaviors..."))
    print(dim("  Generating happy path, edge cases, negative tests...\n"))

    sysinfo = get_system_info()

    content = ask_ai(system, f"""Convert this plain English requirement to complete XCTest Swift code:

REQUIREMENT: "{requirement}"

Generate comprehensive XCTest code covering happy path, edge cases, negative tests, accessibility, and performance.
Date: {sysinfo['date']}
Engineer: Deandre Medrano""", model="qwen2.5-coder:latest")

    if save:
        timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
        safe_name = requirement[:30].lower().replace(" ", "_").replace('"', "")
        filename = f"xctest_converted_{safe_name}_{timestamp}.swift"
        filepath = save_report(content, filename)
        print(f"\n{green('✓')} XCTest file saved to: {bold(filepath)}")
        print(dim("  Add this .swift file to your Xcode project to run the tests"))
    else:
        print(f"\n{yellow('Tip:')} Run with {cyan('--save')} to export as a .swift file")

    print_divider()
    print_success("Requirement converted to XCTest Swift code")


def cmd_predict(change_description: str, save: bool = False):
    """Defect Prediction Engine."""
    print_banner()
    print_divider("DEFECT PREDICTION ENGINE")

    system = """You are a world-class Apple QA lead with 20 years of experience predicting software defects.

Analyze code changes and predict defects. Format exactly like this:

## Defect Prediction Report
**Change:** [brief summary]
**Analysis Date:** [today]
**Analyst:** AIdria Defect Prediction Engine v1.3.0
**Overall Risk Level:** [Critical/High/Medium/Low]
**Confidence Score:** [X]%

---

### Risk Analysis by Area

| Area | Risk Level | Probability | Impact | Reasoning |
|------|------------|-------------|--------|-----------|

---

### Critical Test Cases to Run Immediately

| Priority | Test | Area | Why It Must Run |
|----------|------|------|-----------------|

---

### Hidden Dependencies & Blast Radius

1. **[Dependency 1]** — [Why affected]
2. **[Dependency 2]** — [Why affected]
3. **[Dependency 3]** — [Why affected]

---

### Historical Defect Patterns

- [Pattern 1]
- [Pattern 2]
- [Pattern 3]

---

### Regression Risk Score

| Component | Before Change | After Change | Delta |
|-----------|---------------|--------------|-------|

---

### QA Recommendation

**Release Confidence:** [X]% — [DO NOT RELEASE / RELEASE WITH CAUTION / SAFE TO RELEASE]

**Minimum testing required:**
- [ ] [Test 1]
- [ ] [Test 2]
- [ ] [Test 3]

**Estimated testing time:** [X hours]
**Recommended team size:** [X engineers]

---

### Executive Summary

[2-3 sentences]"""

    print_step("Analyzing code changes for defect prediction...")
    print(dim("  Running pattern analysis"))
    print(dim("  Calculating blast radius and hidden dependencies"))
    print(dim("  Generating risk scores\n"))

    sysinfo = get_system_info()
    content = ask_ai(system, f"Analyze this code change:\n\n{change_description}\n\nDate: {sysinfo['date']}\nAnalyst: Deandre Medrano")

    if save:
        timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"defect_prediction_{timestamp}.md"
        filepath = save_report(content, filename)
        print(f"\n{green('✓')} Prediction report saved to: {bold(filepath)}")

    print_divider()
    print_success("Defect prediction complete")


def cmd_test(app_name: str, save: bool = False):
    print_banner()
    print_divider(f"TEST PLAN — {app_name.upper()}")

    system = """You are a senior Apple QA engineer. Generate a comprehensive test plan.

## Test Plan: [App Name]
**Generated:** [date]
**Engineer:** Deandre Medrano

### Functional Tests
| ID | Test Case | Steps | Expected | Severity |
|----|-----------|-------|----------|----------|

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


def cmd_audit(target: str, save: bool = False):
    print_banner()
    print_divider(f"ACCESSIBILITY AUDIT — {target.upper()}")

    system = """You are an Apple accessibility expert. Audit against WCAG 2.1 and Apple HIG.

## Accessibility Audit: [Target]
**Date:** [date]
**Auditor:** Deandre Medrano

### Score: [X]/100 — Grade: [A/B/C/D/F]
[Summary]

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
[Assessment]

### Top 5 Recommendations
1.
2.
3.
4.
5.

### Testing Checklist
- [ ] VoiceOver navigation
- [ ] Dynamic Type scaling
- [ ] Color contrast ratios
- [ ] Touch target sizes (44x44pt minimum)
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


def cmd_matrix(features_input: str, save: bool = False):
    print_banner()
    print_divider("TEST MATRIX BUILDER")

    system = """You are a senior Apple QA engineer. Generate a test coverage matrix.

## Test Coverage Matrix
**Generated:** [date]
**Engineer:** Deandre Medrano

### Device Coverage

| Feature | iPhone 15 | iPhone 16 | iPad Air | MacBook Pro | Apple Watch | Vision Pro |
|---------|-----------|-----------|----------|-------------|-------------|------------|

Legend: ● Required | ◐ Recommended | ○ Optional | — Not Applicable

### OS Version Coverage

| Feature | iOS 17 | iOS 18 | macOS 14 | macOS 15 | watchOS 10 |
|---------|--------|--------|----------|----------|------------|

### Risk Assessment
| Feature | Risk Level | Justification |
|---------|------------|---------------|

### Testing Priority Order
1.
2.
3.

### Estimated Testing Time
- Total test cases: [number]
- Estimated time: [hours]
- Recommended team size: [number]"""

    print_step("Building test matrix...")
    print(dim("  Mapping across Apple devices and OS versions\n"))

    content = ask_ai(system, f"Generate a test matrix for:\n\n{features_input}")

    if save:
        timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"test_matrix_{timestamp}.md"
        filepath = save_report(content, filename)
        print(f"\n{green('✓')} Matrix saved to: {bold(filepath)}")

    print_divider()
    print_success("Test matrix generated")


def cmd_xctest(feature: str, save: bool = False):
    print_banner()
    print_divider(f"XCTEST GENERATOR — {feature.upper()}")

    system = """You are an expert Apple QA automation engineer.
Generate complete production-ready XCTest Swift code.

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

    func test[Name]() throws {
        // Arrange
        // Act
        // Assert
    }
}"""

    print_step(f"Generating XCTest code for {bold(feature)}...")
    print(dim("  Using Apple's native XCTest framework\n"))

    content = ask_ai(system, f"Generate complete XCTest Swift code to test: {feature}", model="qwen2.5-coder:latest")

    if save:
        timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"xctest_{feature.lower().replace(' ', '_')}_{timestamp}.swift"
        filepath = save_report(content, filename)
        print(f"\n{green('✓')} XCTest file saved to: {bold(filepath)}")

    print_divider()
    print_success(f"XCTest code generated for {feature}")


def cmd_brief():
    print_banner()
    print_divider("MORNING QA BRIEFING")

    system = """You are a senior Apple QA lead giving a morning briefing.

## Morning QA Briefing
**Date:** [today]
**Prepared by:** AIdria CLI

### Good Morning, Deandre 👋

### Today's QA Focus Areas
[3-4 specific areas]

### Apple QA Best Practices Reminder
[One practical tip]

### Today's Testing Checklist
- [ ] [Task 1]
- [ ] [Task 2]
- [ ] [Task 3]
- [ ] [Task 4]
- [ ] [Task 5]

### Interview Tip of the Day
[One Apple QA interview tip]

### Motivational Note
[One sentence]

---
*Generated by AIdria CLI — Private · Local · Secure*"""

    sysinfo = get_system_info()
    print_step("Generating your morning briefing...")
    print(dim(f"  {sysinfo['date']}\n"))

    content = ask_ai(system, f"Generate a morning QA briefing for {sysinfo['date']}. Deandre is preparing for Apple QA engineering roles.")

    print_divider()
    print_success("Have a productive day, Deandre!")


def cmd_help():
    print_banner()
    print(f"""  {bold('COMMANDS')}

  {cyan('aidria test')} {yellow('"App Name"')}                Generate a complete test plan
  {cyan('aidria audit')} {yellow('"Target"')}                 Run an accessibility audit
  {cyan('aidria feedback')} {yellow('"Bug description"')}     Generate Apple Feedback Assistant report
  {cyan('aidria matrix')} {yellow('"Feature list"')}          Build a test coverage matrix
  {cyan('aidria xctest')} {yellow('"Feature"')}               Generate XCTest Swift code
  {cyan('aidria predict')} {yellow('"Code change"')}          Predict defects from code changes
  {cyan('aidria convert')} {yellow('"Plain English req"')}    Convert requirement to XCTest code
  {cyan('aidria brief')}                         Get your morning QA briefing
  {cyan('aidria help')}                          Show this help message

  {bold('OPTIONS')}

  {cyan('--save')}    Save output to ~/aidria-reports/

  {bold('EXAMPLES')}

  {dim('$ aidria test "Mail app" --save')}
  {dim('$ aidria audit "Safari" --save')}
  {dim('$ aidria feedback "Safari crashes when opening PDF on macOS 26.5" --save')}
  {dim('$ aidria matrix "Face ID, Push Notifications, Dark Mode"')}
  {dim('$ aidria xctest "User Authentication" --save')}
  {dim('$ aidria predict "Refactored Mail compose window" --save')}
  {dim('$ aidria convert "Users should be able to log in with Face ID" --save')}
  {dim('$ aidria brief')}

  {bold('FEEDBACK PORTFOLIO')}

  {dim('All feedback reports saved to: ~/aidria-reports/')}
  {dim('Submit at: feedbackassistant.apple.com')}
  {dim('Tip: Attach a screen recording to increase Apple response rate')}

  {bold('MODELS')}

  {dim('Coding tasks  → Qwen2.5 Coder (xctest, convert)')}
  {dim('QA tasks      → Mistral Nemo 12B (test, audit, feedback, predict, brief)')}

  {bold('ABOUT')}

  {dim(f'AIdria CLI v{VERSION}')}
  {dim('Built by Deandre Medrano')}
  {dim('Powered by local AI running on your Mac')}
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
    parser.add_argument("--save", action="store_true")

    args = parser.parse_args()
    cmd = args.command.lower()
    target = args.target
    save = args.save

    commands = {
        "test":     lambda: cmd_test(target, save) if target else print_error('Example: aidria test "Mail app"'),
        "audit":    lambda: cmd_audit(target, save) if target else print_error('Example: aidria audit "Safari"'),
        "feedback": lambda: cmd_feedback(target, save) if target else print_error('Example: aidria feedback "Safari crashes when opening PDF"'),
        "matrix":   lambda: cmd_matrix(target, save) if target else print_error('Example: aidria matrix "Face ID, Dark Mode"'),
        "xctest":   lambda: cmd_xctest(target, save) if target else print_error('Example: aidria xctest "User Authentication"'),
        "predict":  lambda: cmd_predict(target, save) if target else print_error('Example: aidria predict "Refactored Mail compose window"'),
        "convert":  lambda: cmd_convert(target, save) if target else print_error('Example: aidria convert "Users should be able to log in with Face ID"'),
        "brief":    lambda: cmd_brief(),
        "help":     lambda: cmd_help(),
        "--help":   lambda: cmd_help(),
        "-h":       lambda: cmd_help(),
    }

    action = commands.get(cmd)
    if action:
        action()
    else:
        print_error(f"Unknown command: {cmd}")
        print(dim("  Run 'aidria help' to see available commands"))
        sys.exit(1)


if __name__ == "__main__":
    main()