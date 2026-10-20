SARAH AI Architect — Android Engineering Toolkit

Status: APPROVED FOR HOST-ONLY EVALUATION
Branch: "sarah/android-toolkit-evaluation-20261020"
Date: 2026-10-20
Developer workspace: SARAH MASTER DEVELOPER 3.0

1. Purpose

Establish an advanced, independently verifiable Android engineering toolkit for the SARAH AI Architect companion application.

This work must preserve the original application, independent audit evidence, signing-key custody, and existing authorization restrictions.

2. Existing Android Project

The currently inspected repository uses:

- Java-based Android source.
- Android Gradle Plugin 8.6.1.
- Compile SDK 35.
- Minimum SDK 26.
- Target SDK 35.
- "android.useAndroidX=false".

All proposed dependencies must be evaluated for compatibility before changing these settings.

3. Approved Tool Candidates

Native Android Development

- Jetpack Compose: modern native user interfaces and 2D architectural editing.
- Jetpack Room: offline architectural project storage and future owner-controlled design preferences.
- Kotlin Serialization: deterministic, versioned architectural plan data.
- SceneView / Filament: experimental interactive 3D architectural preview.
- libGDX: alternative voxel-oriented renderer, subject to comparative evaluation.

Testing and Engineering

- Robolectric: isolated JVM-based Android component testing.
- Paparazzi: screenshot-based interface regression testing.
- Maestro: future Android UI automation.
- GitHub Actions: reproducible remote builds, validation, and evidence artifacts.

These are approved for evaluation, not automatically installed, integrated, or independently qualified.

4. Proposed Architecture Studio

The future Android app should support:

1. Offline architectural project creation.
2. Editable deterministic floor plans.
3. Multiple floors and underground levels.
4. Interactive 2D visualization.
5. Interactive 3D architectural preview.
6. Versioned project saving and revisions.
7. Architectural geometry and plan validation.
8. Future owner-controlled architectural preference memory.
9. Verified inclusion of the Sarah MCADDON inside the APK, with user-initiated import.

Keep the Android application and Minecraft MCADDON as separately governed components.

5. Engineering Integration Gates

Before incorporating a dependency:

1. Verify its official source and license.
2. Confirm compatible versions and dependencies.
3. Evaluate Android performance and memory requirements.
4. Preserve existing application source.
5. Use isolated prototypes and development branches.
6. Run reproducible host-only tests.
7. Record source changes and SHA-256 integrity evidence.
8. Request independent qualification before any production or device-facing operation.

The original installed APK and its signing-certificate history must remain unchanged.

6. Governance

The following restrictions remain effective:

- M1 INCOMPLETE.
- A02 NOT AUTHORIZED.
- No historical audit finding may be closed through developer assertion alone.
- No unauthorized Android APK installation or replacement.
- No Minecraft connectivity.
- No autonomous construction or world editing.
- No unauthorized AI execution.
- No modification of independent auditor evidence.
- Article XVIII laboratory governance remains independent.

The Workbench V0.1.2.1 corrective assignment remains a separate, authorized host-only milestone.

7. First Engineering Milestone

Perform an isolated Android toolchain compatibility study.

Begin with the current Java/Gradle baseline, evaluate Kotlin and AndroidX requirements, and produce a minimal host-only prototype proposal.

Do not introduce Compose, Room, or a 3D renderer into the existing application until their compatibility has been demonstrated.

Create a separate evidence record for every successfully integrated tool.

Approval to evaluate a tool is not evidence that it has been installed, tested, or independently qualified.
