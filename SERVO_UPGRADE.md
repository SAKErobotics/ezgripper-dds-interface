# Servo Protocol Upgrade Guide

Upgrade your EZGripper servos from Protocol 1.0 to Protocol 2.0 for use with the latest EZGripper drivers.

## Download Dynamixel Wizard

Download from: [Dynamixel Wizard 2.0 Installation](https://docs.robotis.com/docs/software/dynamixel_wizard_2_0/installation)

## Upgrade Process

### 1. Connect with Dynamixel Wizard

- Open Dynamixel Wizard
- Set connection options:
  - **Protocol**: 1 and 2
  - **Ports**: All ports
  - **Baud rates**: All baud rates
- Click "Connect"

### 2. Scan for Servos

- Click "Scan" to find connected servos
- Your EZGripper servos should appear in the list

### 3. Select Servo

- Click on the desired servo to select it
- Note the current protocol version

### 4. Use Recovery Function

- Click the **Recovery** button on the banner
- In the recovery dialog, select:
  - **Series**: MX Series
  - **Model**: MX-64(2.0)
  - **Firmware**: V45
- Follow the on-screen instructions to complete the recovery

### 5. Verify Upgrade

- After recovery completes, scan again
- Verify the servo now shows Protocol 2.0
- Test communication with ping

## Multiple Servos

Repeat the recovery process for each servo in your EZGripper:
- Single gripper: 1 servo
- Dual gripper: 2 servos
- Triple gripper: 3 servos

## Troubleshooting

### Servo Not Found
- Check USB connection
- Verify EZGripper is powered
- Try different USB port

### Recovery Fails
- Ensure stable power supply during recovery
- Try different USB cable
- Check servo model matches MX-64

### Communication Issues After Upgrade
- Power cycle the servo
- Reconnect in Dynamixel Wizard
- Verify baud rate is set correctly

## Need Help?

- [Dynamixel Wizard Manual](https://docs.robotis.com/docs/software/dynamixel_wizard_2_0/installation)
- [SAKE Robotics Support](https://sakerobotics.com/)
