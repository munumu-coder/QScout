# METRIC_DEFINITIONS.md — Canonical Metric Definitions for Q-Scout SDK

**Status:** ACTIVE
**Version:** 1.0
**Last Updated:** 2026-07-19
**Purpose:** Single source of truth for all engineering metrics in the Q-Scout project.
**Authority Level:** 3 (See [Document Hierarchy](#document-hierarchy) in QUALITY_GATES.md)

---

## **📌 CORE PRINCIPLE**

> **RULE M-001:** NEVER compare numerical values until BOTH values have been proven to use EXACTLY the same metric definition.
> Violating this rule invalidates the analysis.

---

## **📊 CANONICAL METRIC DEFINITIONS**

Each metric definition **MUST** include:
1. **Definition**: Exact meaning of the metric.
2. **Included Elements**: What is counted as part of the metric.
3. **Excluded Elements**: What is explicitly NOT part of the metric.
4. **Repository Evidence**: Files or functions used as proof.
5. **Calculation Method**: How the metric is computed.
6. **Examples**: Concrete examples for clarity.

---

### **🔹 Test-Related Metrics**

---

#### **M-001: Dedicated Unit Test**
- **Definition**: A test that verifies the correctness of a **single command's functionality** in isolation, including its payload format, action code, and validation logic.
- **Included Elements**:
  - Tests in `tests/test_actuators.py` that directly exercise a **specific actuator command** (e.g., `TestLED` for `SET_LED`).
  - Tests in `tests/test_sensors.py` that directly exercise a **specific sensor command** (e.g., `TestGetUltrasonic` for `GET_ULTRASONIC`).
  - Tests in `tests/test_protocol.py` for **command-specific** `build_*` and `parse_*` functions (e.g., `TestBuildSetLed` for `build_set_led`).
- **Excluded Elements**:
  - Integration tests (e.g., `test_facade.py`).
  - Real packet regression tests (e.g., `test_real_packets.py`).
  - Physical validation scripts (e.g., `phase3b_validation.py`).
  - Generic protocol tests (e.g., `TestChecksum`, `TestBuildPacket`).
- **Repository Evidence**:
  - `tests/test_actuators.py` (classes `TestLED`, `TestMotor`, `TestMove`, `TestBuzzer`).
  - `tests/test_sensors.py` (classes `TestGetUltrasonic`, `TestParseUltrasonicResponse`).
  - `tests/test_protocol.py` (classes `TestBuildSetLed`, `TestBuildSetMotor`, `TestBuildSetMove`, `TestBuildSetBuzzer`, `TestParseUltrasonic`, `TestParseVoltage`, `TestParseButton`, `TestParseLight`, `TestParseTempHumidity`, `TestParseGyro`).
- **Calculation Method**:
  1. For each Action code in `protocol.py`'s `Action` enum, check if there exists a test class or function **named after the command** (e.g., `TestLED` for `SET_LED`).
  2. Alternatively, check if the command's `build_*` or `parse_*` function has a dedicated test class (e.g., `TestBuildSetLed` for `build_set_led`).
- **Examples**:
  - ✅ `SET_LED` has `TestLED` in `test_actuators.py` → **Included**.
  - ✅ `GET_ULTRASONIC` has `TestGetUltrasonic` in `test_sensors.py` → **Included**.
  - ❌ `GET_COLOR` has no dedicated test class → **Excluded**.

---

#### **M-002: Indirect Test**
- **Definition**: A test that verifies a command's functionality **as part of a larger system**, but not in isolation.
- **Included Elements**:
  - Tests in `tests/test_facade.py` (e.g., `QScout.led()`, `QScout.motor()`).
  - Tests in `tests/test_real_packets.py` (real captured packet validation).
- **Excluded Elements**:
  - Dedicated Unit Tests (see **M-001**).
  - Generic protocol tests (e.g., `TestChecksum`).
- **Repository Evidence**:
  - `tests/test_facade.py`
  - `tests/test_real_packets.py`
- **Calculation Method**:
  Count the number of commands referenced in these files.
- **Examples**:
  - ✅ `GET_DEVICE_INFO` is tested in `test_real_packets.py` → **Included**.
  - ✅ `SET_LED` is tested in `test_facade.py` → **Included**.

---

#### **M-003: Protocol Test**
- **Definition**: A test that verifies the **RB protocol implementation**, including packet structure, checksums, and header validation.
- **Included Elements**:
  - Tests in `tests/test_protocol.py` for **generic protocol functions** (e.g., `build_packet`, `parse_packet`, `sum_check`).
  - Tests in `tests/test_checksum.py`.
- **Excluded Elements**:
  - Command-specific tests (see **M-001** or **M-002**).
- **Repository Evidence**:
  - `tests/test_protocol.py` (classes `TestChecksum`, `TestBuildPacket`, `TestParseFunctions`, `TestExtractPackets`, `TestOrderManager`).
  - `tests/test_checksum.py`
- **Calculation Method**:
  Count the number of protocol-level tests (not command-specific).
- **Examples**:
  - ✅ `sum_check` is tested in `test_checksum.py` → **Included**.
  - ❌ `build_set_led` is command-specific → **Excluded** (see **M-001**).

---

#### **M-004: Builder Test**
- **Definition**: A test that verifies a **command builder function** (e.g., `build_set_led`) produces the correct packet bytes.
- **Included Elements**:
  - Tests in `tests/test_protocol.py` for `build_*` functions.
  - Tests in `tests/test_real_packets.py` for builder output validation.
- **Excluded Elements**:
  - Parser tests (see **M-005**).
  - Integration tests.
- **Repository Evidence**:
  - `tests/test_protocol.py` (classes `TestBuildSetLed`, `TestBuildSetMotor`, `TestBuildSetMove`, `TestBuildSetBuzzer`).
  - `tests/test_real_packets.py` (e.g., `test_get_device_info`, `test_set_led_red`).
- **Calculation Method**:
  Count the number of `build_*` functions with tests.
- **Examples**:
  - ✅ `build_set_led` is tested in `TestBuildSetLed` → **Included**.
  - ❌ `build_set_matrix` has no test → **Excluded**.

---

#### **M-005: Parser Test**
- **Definition**: A test that verifies a **response parser function** (e.g., `parse_ultrasonic`) correctly extracts data from a packet.
- **Included Elements**:
  - Tests in `tests/test_protocol.py` for `parse_*` functions.
  - Tests in `tests/test_sensors.py` for `parse_ultrasonic_response`.
- **Excluded Elements**:
  - Builder tests (see **M-004**).
  - Integration tests.
- **Repository Evidence**:
  - `tests/test_protocol.py` (classes `TestParseUltrasonic`, `TestParseVoltage`, `TestParseButton`, `TestParseLight`, `TestParseTempHumidity`, `TestParseGyro`).
  - `tests/test_sensors.py` (class `TestParseUltrasonicResponse`).
- **Calculation Method**:
  Count the number of `parse_*` functions with tests.
- **Examples**:
  - ✅ `parse_ultrasonic` is tested in `TestParseUltrasonic` → **Included**.
  - ❌ `parse_color_rgb` has no test → **Excluded**.

---

#### **M-006: Real Packet Validation**
- **Definition**: A test that verifies a command's **packet bytes match real captured data** from the Q-Scout robot.
- **Included Elements**:
  - All tests in `tests/test_real_packets.py`.
- **Excluded Elements**:
  - Synthetic packet tests.
- **Repository Evidence**:
  - `tests/test_real_packets.py` (all test classes).
- **Calculation Method**:
  Count the number of commands with tests in `test_real_packets.py`.
- **Examples**:
  - ✅ `GET_DEVICE_INFO` has a real packet test → **Included**.
  - ❌ `GET_COLOR` has no real packet test → **Excluded**.

---

#### **M-007: Hardware Validation**
- **Definition**: A command has been **tested against the physical Q-Scout robot** and confirmed to work.
- **Included Elements**:
  - Commands listed in `CONTROL_CENTER.yaml:validation:physical_validation`.
  - Commands with `validated=True` in `command_map.py`.
- **Excluded Elements**:
  - Commands only tested in simulation or unit tests.
- **Repository Evidence**:
  - `CONTROL_CENTER.yaml:176-189` (physical_validation:commands).
  - `command_map.py` (`validated` field for each `CommandDef`).
- **Calculation Method**:
  Count the number of commands with `validated=True` in `command_map.py`.
- **Examples**:
  - ✅ `SET_LED` is in `CONTROL_CENTER.yaml:validation` → **Included**.
  - ❌ `GET_COLOR` has `validated=False` → **Excluded**.

---
---

### **🔹 Coverage Metrics**

---

#### **M-010: Command Coverage (Dedicated Unit Test)**
- **Definition**: Percentage of commands with **Dedicated Unit Tests** (see **M-001**).
- **Included Elements**:
  - Commands with Dedicated Unit Tests (**M-001**).
- **Excluded Elements**:
  - Commands with only Indirect Tests (**M-002**).
  - Commands with only Real Packet Validation (**M-006**).
- **Repository Evidence**:
  - `tests/test_actuators.py`, `tests/test_sensors.py`, `tests/test_protocol.py`.
- **Calculation Method**:
  `(Number of commands with Dedicated Unit Tests) / (Total commands in command_map.py) * 100`.
- **Examples**:
  - If 12 commands have Dedicated Unit Tests: `12/42 * 100 = 28.6%`.

---

#### **M-011: Command Coverage (Any Test)**
- **Definition**: Percentage of commands with **any test coverage** (direct or indirect).
- **Included Elements**:
  - Commands with Dedicated Unit Tests (**M-001**).
  - Commands with Indirect Tests (**M-002**).
- **Excluded Elements**:
  - Commands with no tests at all.
- **Repository Evidence**:
  - All `tests/*.py` files.
- **Calculation Method**:
  `(Number of commands with any test) / (Total commands in command_map.py) * 100`.
- **Examples**:
  - If 30 commands have any test: `30/42 * 100 = 71.4%`.

---

#### **M-012: Protocol Coverage**
- **Definition**: Percentage of protocol functions (`build_*`, `parse_*`) with tests.
- **Included Elements**:
  - All `build_*` and `parse_*` functions in `protocol.py` with tests (**M-004**, **M-005**).
- **Excluded Elements**:
  - Non-protocol functions.
- **Repository Evidence**:
  - `src/qscout/protocol.py` (functions starting with `build_` or `parse_`).
  - `tests/test_protocol.py`.
- **Calculation Method**:
  `(Number of tested protocol functions) / (Total protocol functions in protocol.py) * 100`.

---

#### **M-013: Public API Coverage**
- **Definition**: Percentage of public API methods (in `actuators.py`, `sensors.py`, `__init__.py`) with tests.
- **Included Elements**:
  - Module-level functions in `actuators.py` and `sensors.py`.
  - Methods in `Actuators`, `Sensors`, and `QScout` classes.
- **Excluded Elements**:
  - Internal/private methods (e.g., `_clamp_signed8`).
- **Repository Evidence**:
  - `src/qscout/actuators.py`, `sensors.py`, `__init__.py`.
  - `tests/test_actuators.py`, `tests/test_sensors.py`, `tests/test_facade.py`.
- **Calculation Method**:
  `(Number of tested public API methods) / (Total public API methods) * 100`.

---

#### **M-014: Physical Validation Coverage**
- **Definition**: Percentage of commands **validated against real hardware** (see **M-007**).
- **Included Elements**:
  - Commands with `validated=True` in `command_map.py`.
- **Excluded Elements**:
  - Commands not tested on hardware.
- **Repository Evidence**:
  - `command_map.py` (`validated` field).
- **Calculation Method**:
  `(Number of validated commands) / (Total commands in command_map.py) * 100`.

---

#### **M-015: SDK Completion**
- **Definition**: Percentage of **planned SDK features** that are implemented.
- **Included Elements**:
  - All 42 commands in `command_map.py`.
  - All public API methods in `actuators.py`, `sensors.py`, `__init__.py`.
  - All protocol builders and parsers in `protocol.py`.
- **Excluded Elements**:
  - Features not in the current scope (e.g., BLE backend, CLI).
- **Repository Evidence**:
  - `src/qscout/command_map.py` (42 `CommandDef` definitions).
  - `src/qscout/protocol.py` (all `build_*` and `parse_*` functions).
- **Calculation Method**:
  `(Number of implemented features) / (Total planned features) * 100`.
- **Examples**:
  - If all 42 commands are implemented: `42/42 * 100 = 100%`.

---

#### **M-016: Task Completion**
- **Definition**: Percentage of **tasks in `TASK_STATE.yaml`** that are completed.
- **Included Elements**:
  - Tasks with `status: completed` in `TASK_STATE.yaml`.
- **Excluded Elements**:
  - Pending, blocked, or obsolete tasks.
- **Repository Evidence**:
  - `project_management/TASK_STATE.yaml` (tasks:completed_tasks).
- **Calculation Method**:
  `(Number of completed tasks) / (Total tasks) * 100`.

---

#### **M-017: Documentation Coverage**
- **Definition**: Percentage of **commands documented in `CHANGELOG.md`**.
- **Included Elements**:
  - Commands mentioned in `project_management/CHANGELOG.md`.
- **Excluded Elements**:
  - Undocumented commands.
- **Repository Evidence**:
  - `project_management/CHANGELOG.md`.
- **Calculation Method**:
  `(Number of documented commands) / (Total commands in command_map.py) * 100`.

---
---

## **📌 VALIDATION WORKFLOW (MANDATORY)**

Every inconsistency analysis **MUST** execute this workflow:

### **STEP 1: Identify the Metric**
- Extract the **exact wording** from the document.
- Example: `"Commands with unit tests: 21 (50%)"`.

### **STEP 2: Locate Its Canonical Definition**
- Check `docs/METRIC_DEFINITIONS.md` for the metric.
- If the metric is undefined, **STOP** and propose a definition first.

### **STEP 3: Verify Definitions Match**
- Compare the document's definition with the canonical definition.
- If definitions differ:
  - **STOP**. Do NOT compare values.
  - Classify as **B) Different Metric Definitions**.

### **STEP 4: Recompute the Metric from Repository**
- Apply the **canonical definition** to the current repository.
- Example: For **M-010**, count commands with Dedicated Unit Tests (**M-001**).

### **STEP 5: Compare Values (Only if Definitions Match)**
- If the documented value **matches** the recomputed value → **Consistent**.
- If the documented value **differs** → Proceed to Step 6.

### **STEP 6: Classify the Inconsistency**
Use **exactly one** of these categories:

| **Category** | **Description** | **Example** |
|--------------|-----------------|-------------|
| **A) Real Repository Error** | The documented value is **factually incorrect** under the canonical definition. | Document says 21 commands have Dedicated Unit Tests, but recomputed value is 12. |
| **B) Different Metric Definitions** | The document uses a **different definition** than the canonical one. | Document includes `test_real_packets.py` as "Unit Tests". |
| **C) Historical Metric** | The metric refers to a **past state** of the repository. | Document from 2026-07-18 reports 145 tests (before T-FIX-01). |
| **D) Documentation Obsolete After Repository Evolution** | The documentation was correct **at the time of writing**, but the repository has since changed. | Document says 21 commands lack tests, but new tests were added. |
| **E) Intentional Difference** | The repository **intentionally** differs from a frozen baseline. | Baseline says architecture is frozen, but a justified improvement was approved. |

### **STEP 7: Recommend Action**
- **Category A**: Update the documentation to match the canonical metric.
- **Category B**: **DO NOT UPDATE**. Add a note clarifying the definition used.
- **Category C**: **DO NOT UPDATE**. Mark as "Historical Metric".
- **Category D**: Update the documentation **only if the metric is still relevant**.
- **Category E**: **DO NOT UPDATE**. Document the intentional difference.

---

## **📋 MANDATORY REPORT FORMAT**

Every engineering report **MUST** include the following fields:

```markdown
# [Report Title] — Verification Report

**Date:** YYYY-MM-DD
**Analyst:** [Agent Role]
**Status:** [Draft/Final]
**Metric Under Analysis:** [e.g., M-010: Command Coverage (Dedicated Unit Test)]

---

## **Definition Analysis**

| **Field**               | **Value**                                                                 |
|-------------------------|---------------------------------------------------------------------------|
| Canonical Definition    | [Link to METRIC_DEFINITIONS.md section, e.g., M-010]                     |
| Document's Definition   | [Extract exact wording or infer from context]                            |
| Definitions Match?      | ✅ Yes / ❌ No                                                             |

---

## **Repository Evidence**

| **Field**               | **Value**                                                                 |
|-------------------------|---------------------------------------------------------------------------|
| Included Elements        | [List files/functions included in the metric]                           |
| Excluded Elements        | [List files/functions excluded]                                         |
| Calculation Method       | [Describe how the metric was computed]                                   |
| Computed Value          | [e.g., "12 (28.6%)"]                                                     |

---

## **Consistency Classification**

- **Category:** [A / B / C / D / E]
- **Justification:** [Explain why this category applies]

---

## **Required Action**

- **Action:** [Update Documentation / No Action / Add Clarification / Mark as Historical]
- **Files to Modify:** [List files, if applicable]
- **Priority:** [P1 / P2 / P3]
- **Evidence References:** [List repository files/lines used as evidence]
```

---

## **📌 DOCUMENT HIERARCHY**

Order of authority (highest to lowest):

1. **Repository source code** (`src/qscout/*.py`)
2. **Repository metadata** (`pyproject.toml`, `setup.cfg`, etc.)
3. **`docs/METRIC_DEFINITIONS.md`** (This document)
4. **`project_management/QUALITY_GATES.md`**
5. **`project_management/CONTROL_CENTER.yaml`**
6. **`project_management/TASK_STATE.yaml`**
7. **Phase reports** (e.g., `docs/SDK_02_PHASE_2C_BASELINE.md`)
8. **Historical reports** (e.g., `docs/SDK_CAPABILITY_AUDIT.md`)

**Rule:** Lower levels **cannot** redefine metrics defined in higher levels.

---

## **📜 HISTORICAL METRIC RULES**

1. **Historical documents are snapshots.**
   - They represent the state of the repository **at a specific point in time**.
   - They are **NOT bugs** simply because the repository has evolved.

2. **Preservation Rule:**
   - Historical documents **MUST NOT** be rewritten to match newer definitions.
   - Instead, mark them explicitly as:
     - `Historical Metric (YYYY-MM-DD)`
     - `Historical Snapshot (Phase X)`

3. **Clarification Rule:**
   - If a historical document uses a non-canonical definition, add a note:
     ```markdown
     **Note:** This metric uses a historical definition. 
     See [M-XXX](#) in `docs/METRIC_DEFINITIONS.md` for the current canonical definition.
     ```

---

## **🔄 CONTINUOUS IMPROVEMENT**

1. **New Metrics:**
   - If a new metric is needed, **first define it in this document** before using it.
   - Follow the **canonical format** (definition, included/excluded elements, etc.).

2. **Metric Updates:**
   - If a metric definition needs to change, **update this document first**.
   - Ensure backward compatibility with historical reports.

3. **Validation:**
   - Every new metric **MUST** be validated against the repository before inclusion.

---

## **📌 CHANGELOG**

| **Date**       | **Change**                                                                 | **Author**       |
|----------------|---------------------------------------------------------------------------|------------------|
| 2026-07-19     | Initial version. Added 17 canonical metric definitions (M-001 to M-017). | opencode        |
