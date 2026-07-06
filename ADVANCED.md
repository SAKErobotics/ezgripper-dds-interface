# Advanced Documentation

This document contains detailed API reference, DDS interface specifications, and advanced configuration options.

## API Reference

### Hardware Functions

```python
from ezgripper_dds_interface import create_connection, create_gripper, load_config

# Create hardware connection
connection = create_connection(port='/dev/ttyUSB0', baudrate=1000000)

# Create gripper instance
gripper = create_gripper(connection, name='left', servo_ids=[1], config=None)

# Hardware operations
gripper.calibrate()           # Calibrate gripper
gripper.open()                 # Open gripper
gripper.goto_position(pos, effort)  # Move to position
gripper.get_position()         # Get current position
gripper.get_temperatures()     # Get servo temperatures
```

### DDS Interface Functions

```python
from ezgripper_dds_interface.interface import EZGripperDDSInterface, create_dds_interface

# Create DDS interface
interface = create_dds_interface(port='/dev/ttyUSB0', baudrate=1000000)

# Add gripper
interface.add_gripper(side='left', servo_ids=[1])

# Process commands
interface.process_command(side='left', command={'action': 'goto_position', 'parameters': {...}})

# Get state
interface.get_state(side='left')

# Get telemetry
interface.get_telemetry(side='left')
```

## DDS Interface

### Agnostic Direct Control Interface

**Topics:**
- **Command**: `rt/gripper/{side}/cmd_direct`
- **State**: `rt/gripper/{side}/state_direct`

**Message Format:**
```json
{
  "position_pct": 0.0,      // 0.0 (closed) to 100.0 (fully open)
  "force_limit_pct": 25     // 0 to 100% dynamic current ceiling
}
```

**Key Features:**
- Dynamic force control on every cycle
- Platform-agnostic
- Works with any DDS implementation

## DDS Compatibility

This interface works with any DDS implementation:
- **CycloneDDS** - Used by Unitree repository
- **FastDDS** - Used by ROS2 (default)
- **RTI Connext** - Enterprise DDS
- **OpenSplice** - Open source DDS

## Configuration

### Custom Configuration

```python
from ezgripper_dds_interface import load_config

# Load default config
config = load_config()

# Or load custom config
config = load_config('/path/to/custom_config.json')
```

### Serial Port Configuration

```python
connection = create_connection(
    port='/dev/ttyUSB0',      # Serial port
    baudrate=1000000          # Baudrate (default: 1 Mbps)
)
```

## Integration

This interface is used by:

### **Unitree Repository**
- Repository: https://github.com/SAKErobotics/unitree-dex1-ezgripper-driver
- Purpose: Unitree G1 robots
- DDS: CycloneDDS

### **ROS2 Driver**
- Repository: https://github.com/SAKErobotics/ezgripper_ros2_v2
- Purpose: ROS2-based robots
- DDS: FastDDS

### **Custom Integrations**
- Any robot platform
- DDS-agnostic design
- Python API for direct integration

## Architecture

```
┌─────────────────────────────────────────────────┐
│        EZGripper DDS Interface                  │
│                                                     │
│  ┌─────────────────────────────────────────────┐  │
│  │  libezgripper (Protocol 2.0 Hardware Layer)  │  │
│  └─────────────────────────────────────────────┘  │
│                                                     │
│  ┌─────────────────────────────────────────────┐  │
│  │  Agnostic DDS Interface                      │  │
│  └─────────────────────────────────────────────┘  │
└─────────────────────────────────────────────────┘
         │                     │
         ▼                     ▼
┌─────────────────┐  ┌─────────────────┐
│ Unitree Repo    │  │   ROS2 Driver    │
└─────────────────┘  └─────────────────┘
```
