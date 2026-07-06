# EZGripper DDS Interface

Generic DDS interface for SAKE Robotics EZGripper. This is the universal foundation for all EZGripper integrations across different robot platforms and DDS implementations.

## Overview

This repository provides the core hardware communication layer and generic DDS interface for EZGripper control. It is designed to be:

- **Universal Foundation**: Used by Unitree, ROS2, and other robot platforms
- **DDS-Agnostic**: Works with any DDS implementation
- **Protocol 2.0**: Modern Dynamixel SDK communication
- **Full Position & Force Control**: Dynamic force limits on every cycle

## Architecture

```
┌─────────────────────────────────────────────────┐
│        EZGripper DDS Interface (This Repo)        │
│                                                     │
│  ┌─────────────────────────────────────────────┐  │
│  │  libezgripper (Protocol 2.0 Hardware Layer)  │  │
│  │  - Dynamixel SDK wrapper                    │  │
│  │  - Gripper control logic                    │  │
│  │  - Configuration management                 │  │
│  └─────────────────────────────────────────────┘  │
│                                                     │
│  ┌─────────────────────────────────────────────┐  │
│  │  Agnostic DDS Interface (Superset)          │  │
│  │  - rt/gripper/{side}/cmd_direct              │  │
│  │  - rt/gripper/{side}/state_direct           │  │
│  │  - Full position + force control             │  │
│  └─────────────────────────────────────────────┘  │
└─────────────────────────────────────────────────┘
         │                     │
         ▼                     ▼
┌─────────────────┐  ┌─────────────────┐
│ Unitree Repo    │  │   ROS2 Driver    │
│ (Unitree-only)  │  │   (ROS2-only)    │
└─────────────────┘  └─────────────────┘
```

## Installation

### Python Package Installation

```bash
pip install git+https://github.com/SAKErobotics/ezgripper-dds-interface.git
```

### For Development

```bash
git clone https://github.com/SAKErobotics/ezgripper-dds-interface.git
cd ezgripper-dds-interface
pip install -e .
```

## Requirements

- Python 3.8+
- dynamixel-sdk>=4.0.0
- pyserial>=3.5

## Hardware Requirements

- EZGripper with Protocol 2.0 servos
- USB connection (FTDI USB-to-serial adapter)
- **Need to upgrade servos?** See [Servo Upgrade Guide](https://github.com/SAKErobotics/ezgripper_ros2_v2/blob/main/SERVO_UPGRADE.md)

## Agnostic DDS Interface

This repository provides the **Agnostic Direct Control Interface** - the superset interface that gives full position and force control independent of any robot platform.

### Topics

- **Command**: `rt/gripper/{side}/cmd_direct` - Full position and force control
- **State**: `rt/gripper/{side}/state_direct` - Real-time feedback

### Message Format

```json
{
  "position_pct": 0.0,      // 0.0 (closed) to 100.0 (fully open)
  "force_limit_pct": 25     // 0 to 100% dynamic current ceiling
}
```

### Key Features

- **Dynamic Force Control**: Adjust force limits on every cycle
- **No Fixed Limitations**: Unlike robot-specific interfaces, force is not hardcoded
- **Platform Agnostic**: Works with any robot platform or DDS implementation
- **Vision Integration**: Perfect for vision-based force adaptation

### Usage Example

```python
import json
import time
from cyclonedds.domain import DomainParticipant
from cyclonedds.topic import Topic
from cyclonedds.pub import Publisher, DataWriter
import ctypes

class GenericStringIDL(ctypes.Structure):
    _fields_ = [("data", ctypes.c_char_p)]

participant = DomainParticipant()
cmd_topic = Topic(participant, "rt/gripper/left/cmd_direct", GenericStringIDL)
publisher = Publisher(participant)
writer = DataWriter(publisher, cmd_topic)

def send_command(position_pct, force_limit_pct):
    """Send agnostic command with full position and force control"""
    payload = {
        "position_pct": position_pct,
        "force_limit_pct": force_limit_pct
    }
    msg_bytes = json.dumps(payload).encode('utf-8')
    sample = GenericStringIDL(data=msg_bytes)
    writer.write(sample)

# Example: Soft grasp for delicate object (5% force)
send_command(position_pct=0.0, force_limit_pct=5)

# Example: Firm grasp for heavy object (45% force)
send_command(position_pct=0.0, force_limit_pct=45)

# Example: Open with moderate force (100% position, 20% force)
send_command(position_pct=100.0, force_limit_pct=20)
```

## Hardware API

For direct hardware control without DDS, use the hardware API:

```python
from ezgripper_dds_interface import create_connection, create_gripper, load_config

# Create connection
connection = create_connection('/dev/ttyUSB0', 1000000)

# Load configuration
config = load_config()

# Create gripper
gripper = create_gripper(connection, 'left', [1], config)

# Calibrate
gripper.calibrate()

# Control gripper
gripper.goto_position(50, 30)  # 50% position, 30% effort

# Get position
position = gripper.get_position()
print(f"Current position: {position}%")
```

## DDS Compatibility

This interface is designed to work with any DDS implementation:

- **CycloneDDS** - Used by Unitree repository
- **FastDDS** - Used by ROS2 (default)
- **RTI Connext** - Enterprise DDS
- **OpenSplice** - Open source DDS

## Integration

This interface is used by:

### **Unitree Repository**
- Repository: https://github.com/SAKErobotics/unitree-dex1-ezgripper-driver
- Purpose: Unitree G1 robots with Dex1 interface
- DDS: CycloneDDS
- Adds: Dex1-specific DDS topics and Unitree SDK integration

### **ROS2 Driver**
- Repository: https://github.com/SAKErobotics/ezgripper_ros2_v2
- Purpose: ROS2-based robots
- DDS: FastDDS (ROS2 default)
- Adds: ROS2 topics, actions, and services

### **Custom Integrations**
- Can be used by any robot platform
- DDS-agnostic design allows flexibility
- Python API for direct integration

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

## Configuration

The interface uses a configuration file for hardware settings. The default configuration is loaded automatically, but you can provide custom configuration:

```python
from ezgripper_dds_interface import load_config

# Load default config
config = load_config()

# Or load custom config
config = load_config('/path/to/custom_config.json')
```

## Troubleshooting

### Import Errors

If you get import errors:
```bash
# Reinstall the package
pip uninstall ezgripper-dds-interface
pip install git+https://github.com/SAKErobotics/ezgripper-dds-interface.git
```

### Serial Port Issues

If you get permission denied errors:
```bash
sudo adduser $USER dialout
# Then reboot
```

### Servo Not Responding

1. Check serial port: `ls -la /dev/ttyUSB*`
2. Verify servo IDs match your hardware
3. Check baudrate (default: 1000000)
4. Ensure servos are upgraded to Protocol 2.0

## License

BSD License - See LICENSE file

## Support

- **GitHub Issues**: https://github.com/SAKErobotics/ezgripper-dds-interface/issues
- **SAKE Robotics**: https://sakerobotics.com/

## Acknowledgments

This interface incorporates the Protocol 2.0 hardware layer from the SAKE Robotics unitree-dex1-ezgripper-driver project.
