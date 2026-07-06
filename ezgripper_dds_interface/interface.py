#!/usr/bin/env python3
"""
Generic EZGripper DDS Interface

Provides a DDS-agnostic interface for EZGripper control.
This can be adapted to work with different DDS implementations.
"""

import json
from typing import Dict, Any, Optional
import sys
import os

# Add libezgripper to path
libezgripper_path = os.path.join(os.path.dirname(__file__), '..', '..', 'libezgripper')
sys.path.insert(0, libezgripper_path)

from libezgripper import create_connection, create_gripper, load_config


class EZGripperDDSInterface:
    """Generic DDS interface for EZGripper control"""

    def __init__(self, port: str = '/dev/ttyUSB0', baudrate: int = 1000000):
        """Initialize DDS interface with hardware connection"""
        self.port = port
        self.baudrate = baudrate
        self.grippers: Dict[str, Any] = {}
        self.config = load_config()
        self.connection = None

    def connect(self):
        """Establish hardware connection"""
        self.connection = create_connection(self.port, self.baudrate)

    def add_gripper(self, side: str, servo_ids: list):
        """Add a gripper instance"""
        if not self.connection:
            self.connect()
        
        gripper = create_gripper(self.connection, side, servo_ids, self.config)
        self.grippers[side] = gripper
        
        # Calibrate and open
        gripper.calibrate()
        gripper.open()

    def process_command(self, side: str, command: Dict[str, Any]) -> Dict[str, Any]:
        """Process DDS command and return response"""
        if side not in self.grippers:
            return {'error': f'Gripper {side} not found'}
        
        gripper = self.grippers[side]
        action = command.get('action', 'goto_position')
        params = command.get('parameters', {})
        
        try:
            if action == 'goto_position':
                position = params.get('position', 50)
                effort = params.get('effort', 30)
                gripper.goto_position(position, effort)
                return {'status': 'success', 'action': action}
            
            elif action == 'calibrate':
                result = gripper.calibrate()
                return {'status': 'success', 'calibrated': result}
            
            elif action == 'open':
                gripper.open()
                return {'status': 'success', 'action': action}
            
            elif action == 'get_status':
                position = gripper.get_position()
                temps = gripper.get_temperatures() if hasattr(gripper, 'get_temperatures') else []
                return {
                    'status': 'success',
                    'position': position,
                    'temperatures': temps
                }
            
            else:
                return {'error': f'Unknown action: {action}'}
        
        except Exception as e:
            return {'error': str(e)}

    def get_state(self, side: str) -> Dict[str, Any]:
        """Get current gripper state"""
        if side not in self.grippers:
            return {'error': f'Gripper {side} not found'}
        
        gripper = self.grippers[side]
        
        try:
            position = gripper.get_position()
            temps = gripper.get_temperatures() if hasattr(gripper, 'get_temperatures') else []
            
            return {
                'side': side,
                'position': position,
                'temperatures': temps,
                'status': 'active'
            }
        except Exception as e:
            return {'error': str(e)}

    def get_telemetry(self, side: str) -> Dict[str, Any]:
        """Get detailed telemetry data"""
        if side not in self.grippers:
            return {'error': f'Gripper {side} not found'}
        
        gripper = self.grippers[side]
        
        try:
            state = self.get_state(side)
            if 'error' in state:
                return state
            
            # Add additional telemetry if available
            telemetry = {
                'timestamp': time.time(),
                'state': state,
            }
            
            return telemetry
        
        except Exception as e:
            return {'error': str(e)}


import time


# Convenience functions
def create_dds_interface(port: str = '/dev/ttyUSB0', baudrate: int = 1000000) -> EZGripperDDSInterface:
    """Create DDS interface instance"""
    return EZGripperDDSInterface(port, baudrate)


def parse_dds_command(message: str) -> Dict[str, Any]:
    """Parse DDS command message"""
    try:
        return json.loads(message)
    except json.JSONDecodeError:
        return {'error': 'Invalid JSON message'}


def format_dds_state(state: Dict[str, Any]) -> str:
    """Format state for DDS transmission"""
    return json.dumps(state)


def main():
    """Main function for testing the DDS interface"""
    import sys
    
    print("EZGripper DDS Interface Test")
    print("=" * 50)
    
    try:
        # Create interface
        interface = create_dds_interface('/dev/ttyUSB0', 1000000)
        print("✓ Interface created")
        
        # Add gripper
        interface.add_gripper('left', [1])
        print("✓ Gripper added")
        
        # Test command
        command = {'action': 'get_status'}
        response = interface.process_command('left', command)
        print(f"✓ Status: {response}")
        
        # Test state
        state = interface.get_state('left')
        print(f"✓ State: {state}")
        
        print("=" * 50)
        print("Test completed successfully")
        
    except Exception as e:
        print(f"✗ Test failed: {e}")
        sys.exit(1)


if __name__ == '__main__':
    main()
