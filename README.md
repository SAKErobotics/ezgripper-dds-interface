# EZGripper DDS Interface

Generic DDS interface for SAKE Robotics EZGripper. This is the foundation for all EZGripper integrations across different robot platforms and DDS implementations.

## Features

- **Protocol 2.0 Hardware**: Modern Dynamixel SDK communication
- **Generic DDS Interface**: Works with any DDS implementation
- **Universal Foundation**: Used by Unitree, ROS2, and other robot platforms
- **Multi-Gripper Support**: Independent gripper instances

## Installation

```bash
pip install git+https://github.com/SAKErobotics/ezgripper-dds-interface.git
```

## Dependencies

- dynamixel-sdk>=4.0.0
- pyserial>=3.5

## Usage

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
```

## DDS Interface

### Generic Topics
- `rt/ezgripper/{side}/admin` - Gripper administration commands
- `rt/ezgripper/{side}/state` - Gripper state information
- `rt/gripper/{side}/telemetry` - Telemetry data

### DDS Compatibility
This interface is designed to work with any DDS implementation:
- CycloneDDS
- FastDDS
- RTI Connext
- OpenSplice

## Integration

This interface is used by:
- **Unitree Repository**: For Unitree robots with Dex1 interface
- **ROS2 Driver**: For ROS2-based robots
- **Custom Integrations**: For other robot platforms

## License

BSD License - See LICENSE file
