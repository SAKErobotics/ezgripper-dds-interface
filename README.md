# EZGripper DDS Interface

Generic DDS interface for SAKE Robotics EZGripper. Universal foundation for all EZGripper integrations.

## ⚠️ Protocol 2.0 Required

**Your EZGripper servos must be upgraded to Protocol 2.0 to use this interface.**

**How to Check**: If your servos are using Protocol 1.0, this interface will not work.

**How to Upgrade**: See [Servo Upgrade Guide](SERVO_UPGRADE.md)

## Quick Start

### Installation

```bash
pip install git+https://github.com/SAKErobotics/ezgripper-dds-interface.git
```

### Basic Usage

```python
from ezgripper_dds_interface import create_connection, create_gripper, load_config

# Create connection
connection = create_connection('/dev/ttyUSB0', 1000000)

# Create gripper
gripper = create_gripper(connection, 'left', [1], None)

# Calibrate and control
gripper.calibrate()
gripper.goto_position(50, 30)  # 50% position, 30% effort
```

### DDS Usage

```python
import json
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

# Send command with position and force
payload = {"position_pct": 0.0, "force_limit_pct": 25}
msg_bytes = json.dumps(payload).encode('utf-8')
sample = GenericStringIDL(data=msg_bytes)
writer.write(sample)
```

## Requirements

- Python 3.8+
- EZGripper with Protocol 2.0 servos

**Need to upgrade servos?** See [Servo Upgrade Guide](https://github.com/SAKErobotics/ezgripper_ros2_v2/blob/main/SERVO_UPGRADE.md)

## Troubleshooting

### Permission Denied

```bash
sudo adduser $USER dialout
# Then reboot
```

### Import Errors

```bash
pip uninstall ezgripper-dds-interface
pip install git+https://github.com/SAKErobotics/ezgripper-dds-interface.git
```

## Advanced Documentation

- [Advanced API Reference](ADVANCED.md) - Detailed API documentation
- [DDS Interface Details](ADVANCED.md#dds-interface) - DDS topics and message formats
- [Configuration](ADVANCED.md#configuration) - Advanced configuration options

## License

BSD License - See LICENSE file

## Support

- **GitHub Issues**: https://github.com/SAKErobotics/ezgripper-dds-interface/issues
- **SAKE Robotics**: https://sakerobotics.com/
