"""
Complete Hardware Setup for Thought Geometry Detection

PHYSICAL SYSTEM COMPONENTS:
===========================

1. Gas Chamber (0.5% O₂)
   - Volume: 1L cubic chamber
   - Gas mixture: 0.5% O₂, 99.5% N₂
   - Temperature control: 310K (body temperature)
   - Pressure: 1 atm

2. 3D Sensor Array
   - 64 sensors (4×4×4 grid)
   - Sensor spacing: ~5cm
   - Measures: O₂ concentration, pressure, temperature
   - Sampling rate: 1 kHz

3. Semiconductor Circuit
   - Electron source: Field emission cathode
   - Current detection: Picoammeter (fA resolution)
   - Voltage control: 0-10V variable
   - Position control: XYZ micro-positioner

4. Odorant Injection System
   - Precision syringe pump
   - Flow rate: 0.1-10 μL/min
   - Injection port: Top center
   - Multiple compound reservoirs

5. Data Acquisition System
   - Multi-channel ADC (16-bit, 1 kHz)
   - Real-time processing (FPGA or GPU)
   - Storage: High-speed SSD
   - Synchronization: Hardware trigger

CONTROL SYSTEM:
===============

Python interface to hardware via:
- Serial/USB for sensors
- DAQ card for analog signals
- Motor controllers for positioning
- GPIO for synchronization

This module provides the software interface to all hardware components.
"""

import numpy as np
from typing import Dict, Any, List, Tuple, Optional
from dataclasses import dataclass
import time
import threading
import queue

try:
    import serial
    import pyvisa
    HARDWARE_AVAILABLE = True
except ImportError:
    HARDWARE_AVAILABLE = False
    print("Warning: Hardware libraries not available. Running in simulation mode.")


@dataclass
class SensorReading:
    """Single reading from a sensor."""
    timestamp: float
    sensor_id: int
    position: np.ndarray  # [x, y, z]
    o2_concentration: float  # fraction (0.005 = 0.5%)
    pressure: float  # Pa
    temperature: float  # K


@dataclass
class CircuitState:
    """Current state of semiconductor circuit."""
    timestamp: float
    electron_position: np.ndarray  # [x, y, z] in chamber coordinates
    applied_voltage: float  # V
    measured_current: float  # A (picoamps typically)
    electron_energy: float  # eV


class GasChamberHardware:
    """
    Interface to physical gas chamber.
    
    Controls:
    - Gas composition (flow controllers)
    - Temperature (heating/cooling)
    - Pressure (vacuum pump/inlet valve)
    - Odorant injection (syringe pump)
    """
    
    def __init__(self,
                 chamber_volume_L: float = 1.0,
                 target_o2: float = 0.005,
                 target_temp_K: float = 310.0,
                 simulation_mode: bool = not HARDWARE_AVAILABLE):
        """
        Initialize gas chamber hardware.
        
        Args:
            chamber_volume_L: Chamber volume in liters
            target_o2: Target O₂ fraction (0.005 = 0.5%)
            target_temp_K: Target temperature in Kelvin
            simulation_mode: If True, simulate hardware
        """
        self.volume = chamber_volume_L
        self.target_o2 = target_o2
        self.target_temp = target_temp_K
        self.simulation_mode = simulation_mode
        
        # Hardware connections
        self.temp_controller = None
        self.flow_controllers = {}
        self.syringe_pump = None
        
        if not simulation_mode:
            self._connect_hardware()
        
        # Current state
        self.current_o2 = target_o2
        self.current_temp = target_temp_K
        self.current_pressure = 101325.0  # Pa (1 atm)
        
    def _connect_hardware(self):
        """Connect to physical hardware."""
        try:
            # Temperature controller (e.g., Eurotherm via serial)
            self.temp_controller = serial.Serial('/dev/ttyUSB0', 9600, timeout=1)
            
            # Flow controllers for O₂ and N₂ (e.g., Alicat via serial)
            self.flow_controllers['O2'] = serial.Serial('/dev/ttyUSB1', 19200, timeout=1)
            self.flow_controllers['N2'] = serial.Serial('/dev/ttyUSB2', 19200, timeout=1)
            
            # Syringe pump (e.g., Harvard Apparatus via serial)
            self.syringe_pump = serial.Serial('/dev/ttyUSB3', 9600, timeout=1)
            
            print("✓ Gas chamber hardware connected")
        except Exception as e:
            print(f"✗ Hardware connection failed: {e}")
            print("  Falling back to simulation mode")
            self.simulation_mode = True
    
    def set_o2_concentration(self, target: float):
        """
        Set O₂ concentration by adjusting flow controllers.
        
        Args:
            target: Target O₂ fraction (e.g., 0.005 for 0.5%)
        """
        if self.simulation_mode:
            self.current_o2 = target
            print(f"[SIM] O₂ concentration set to {target*100:.2f}%")
            return
        
        # Calculate flow rates
        total_flow = 1000.0  # mL/min (1 L/min total)
        o2_flow = total_flow * target
        n2_flow = total_flow * (1 - target)
        
        # Send commands to flow controllers
        self.flow_controllers['O2'].write(f"S{o2_flow:.2f}\r".encode())
        self.flow_controllers['N2'].write(f"S{n2_flow:.2f}\r".encode())
        
        self.current_o2 = target
        print(f"O₂: {o2_flow:.2f} mL/min, N₂: {n2_flow:.2f} mL/min")
    
    def set_temperature(self, target_K: float):
        """Set chamber temperature."""
        if self.simulation_mode:
            self.current_temp = target_K
            print(f"[SIM] Temperature set to {target_K:.1f} K")
            return
        
        # Send command to temperature controller
        temp_C = target_K - 273.15
        self.temp_controller.write(f"SP{temp_C:.1f}\r".encode())
        
        self.current_temp = target_K
        print(f"Temperature setpoint: {target_K:.1f} K ({temp_C:.1f}°C)")
    
    def inject_odorant(self,
                      compound_name: str,
                      volume_uL: float,
                      flow_rate_uL_min: float = 1.0):
        """
        Inject odorant compound into chamber.
        
        Args:
            compound_name: Name of compound
            volume_uL: Volume to inject (microliters)
            flow_rate_uL_min: Flow rate (μL/min)
        """
        if self.simulation_mode:
            injection_time = volume_uL / flow_rate_uL_min * 60  # seconds
            print(f"[SIM] Injecting {volume_uL:.2f} μL of {compound_name} at {flow_rate_uL_min:.2f} μL/min")
            time.sleep(min(injection_time, 0.1))  # Simulate briefly
            return
        
        # Send commands to syringe pump
        self.syringe_pump.write(f"VOL {volume_uL}\r".encode())
        self.syringe_pump.write(f"RAT {flow_rate_uL_min}\r".encode())
        self.syringe_pump.write(b"RUN\r")
        
        # Wait for injection to complete
        injection_time = volume_uL / flow_rate_uL_min * 60
        time.sleep(injection_time)
        
        print(f"Injected {volume_uL:.2f} μL of {compound_name}")


class SensorArrayHardware:
    """
    Interface to 3D sensor array.
    
    64 sensors in 4×4×4 grid measuring:
    - O₂ concentration (electrochemical sensor)
    - Pressure (MEMS sensor)
    - Temperature (thermocouple)
    """
    
    def __init__(self,
                 grid_size: Tuple[int, int, int] = (4, 4, 4),
                 spacing_cm: float = 5.0,
                 sampling_rate_Hz: float = 1000.0,
                 simulation_mode: bool = not HARDWARE_AVAILABLE):
        """
        Initialize sensor array.
        
        Args:
            grid_size: Number of sensors in each dimension
            spacing_cm: Spacing between sensors
            sampling_rate_Hz: Data acquisition rate
            simulation_mode: If True, simulate sensors
        """
        self.grid_size = grid_size
        self.n_sensors = np.prod(grid_size)
        self.spacing = spacing_cm / 100.0  # Convert to meters
        self.sampling_rate = sampling_rate_Hz
        self.simulation_mode = simulation_mode
        
        # Generate sensor positions
        self.sensor_positions = self._generate_sensor_positions()
        
        # Hardware connections
        self.daq_device = None
        
        if not simulation_mode:
            self._connect_daq()
        
        # Data acquisition thread
        self.acquiring = False
        self.data_queue = queue.Queue(maxsize=10000)
        self.acquisition_thread = None
    
    def _generate_sensor_positions(self) -> np.ndarray:
        """Generate 3D positions of all sensors."""
        nx, ny, nz = self.grid_size
        
        # Center the grid at origin
        x = np.linspace(-self.spacing*(nx-1)/2, self.spacing*(nx-1)/2, nx)
        y = np.linspace(-self.spacing*(ny-1)/2, self.spacing*(ny-1)/2, ny)
        z = np.linspace(-self.spacing*(nz-1)/2, self.spacing*(nz-1)/2, nz)
        
        xx, yy, zz = np.meshgrid(x, y, z)
        positions = np.stack([xx.flatten(), yy.flatten(), zz.flatten()], axis=1)
        
        return positions
    
    def _connect_daq(self):
        """Connect to data acquisition hardware."""
        try:
            if HARDWARE_AVAILABLE:
                rm = pyvisa.ResourceManager()
                # Connect to DAQ (e.g., National Instruments USB-6216)
                self.daq_device = rm.open_resource('DAQ::Dev1')
                print("✓ Sensor array DAQ connected")
        except Exception as e:
            print(f"✗ DAQ connection failed: {e}")
            print("  Falling back to simulation mode")
            self.simulation_mode = True
    
    def start_acquisition(self):
        """Start continuous data acquisition."""
        if self.acquiring:
            print("Already acquiring!")
            return
        
        self.acquiring = True
        self.acquisition_thread = threading.Thread(target=self._acquisition_loop)
        self.acquisition_thread.daemon = True
        self.acquisition_thread.start()
        
        print(f"✓ Started acquisition at {self.sampling_rate} Hz")
    
    def stop_acquisition(self):
        """Stop data acquisition."""
        self.acquiring = False
        if self.acquisition_thread:
            self.acquisition_thread.join(timeout=2.0)
        print("✓ Stopped acquisition")
    
    def _acquisition_loop(self):
        """Continuous acquisition loop (runs in separate thread)."""
        dt = 1.0 / self.sampling_rate
        
        while self.acquiring:
            start_time = time.time()
            
            # Read all sensors
            readings = self._read_all_sensors()
            
            # Add to queue
            try:
                self.data_queue.put(readings, block=False)
            except queue.Full:
                print("Warning: Data queue full, dropping samples")
            
            # Maintain sampling rate
            elapsed = time.time() - start_time
            sleep_time = max(0, dt - elapsed)
            time.sleep(sleep_time)
    
    def _read_all_sensors(self) -> List[SensorReading]:
        """Read all sensors and return readings."""
        timestamp = time.time()
        readings = []
        
        if self.simulation_mode:
            # Simulate sensor readings
            for i in range(self.n_sensors):
                reading = SensorReading(
                    timestamp=timestamp,
                    sensor_id=i,
                    position=self.sensor_positions[i],
                    o2_concentration=0.005 + np.random.normal(0, 0.0001),
                    pressure=101325.0 + np.random.normal(0, 10.0),
                    temperature=310.0 + np.random.normal(0, 0.1)
                )
                readings.append(reading)
        else:
            # Read from actual hardware (DAQ channels)
            # Each sensor has 3 channels: O₂, pressure, temperature
            n_channels = self.n_sensors * 3
            voltages = self.daq_device.query_ascii_values(f'READ:AI? (@0:{n_channels-1})')
            
            for i in range(self.n_sensors):
                # Convert voltages to physical units (calibration curves)
                v_o2 = voltages[i*3]
                v_press = voltages[i*3 + 1]
                v_temp = voltages[i*3 + 2]
                
                o2_conc = self._calibrate_o2(v_o2)
                pressure = self._calibrate_pressure(v_press)
                temperature = self._calibrate_temperature(v_temp)
                
                reading = SensorReading(
                    timestamp=timestamp,
                    sensor_id=i,
                    position=self.sensor_positions[i],
                    o2_concentration=o2_conc,
                    pressure=pressure,
                    temperature=temperature
                )
                readings.append(reading)
        
        return readings
    
    def _calibrate_o2(self, voltage: float) -> float:
        """Convert O₂ sensor voltage to concentration."""
        # Example calibration: 0-5V → 0-100% O₂
        # Actual calibration from sensor datasheet
        return voltage / 5.0 * 1.0
    
    def _calibrate_pressure(self, voltage: float) -> float:
        """Convert pressure sensor voltage to Pascals."""
        # Example: 0-5V → 0-200 kPa
        return voltage / 5.0 * 200000.0
    
    def _calibrate_temperature(self, voltage: float) -> float:
        """Convert thermocouple voltage to Kelvin."""
        # Type K thermocouple: ~40 μV/°C
        temp_C = voltage / 40e-6
        return temp_C + 273.15
    
    def get_latest_data(self, max_samples: int = 100) -> List[SensorReading]:
        """Get latest sensor data from queue."""
        samples = []
        try:
            for _ in range(max_samples):
                readings = self.data_queue.get(block=False)
                samples.extend(readings)
        except queue.Empty:
            pass
        return samples


class SemiconductorCircuitHardware:
    """
    Interface to semiconductor electron injection circuit.
    
    Components:
    - Field emission cathode (electron source)
    - XYZ micro-positioner (position control)
    - High-voltage power supply (0-10 kV)
    - Picoammeter (current detection, fA resolution)
    """
    
    def __init__(self,
                 position_range_mm: float = 100.0,
                 voltage_range_V: float = 10000.0,
                 current_sensitivity_A: float = 1e-15,
                 simulation_mode: bool = not HARDWARE_AVAILABLE):
        """
        Initialize semiconductor circuit hardware.
        
        Args:
            position_range_mm: XYZ positioning range
            voltage_range_V: Maximum voltage
            current_sensitivity_A: Minimum detectable current
            simulation_mode: If True, simulate hardware
        """
        self.position_range = position_range_mm / 1000.0  # Convert to meters
        self.voltage_range = voltage_range_V
        self.current_sensitivity = current_sensitivity_A
        self.simulation_mode = simulation_mode
        
        # Hardware connections
        self.positioner = None
        self.power_supply = None
        self.ammeter = None
        
        if not simulation_mode:
            self._connect_hardware()
        
        # Current state
        self.electron_position = np.array([0.0, 0.0, 0.1])  # Start 10cm above center
        self.applied_voltage = 0.0
        self.measured_current = 0.0
    
    def _connect_hardware(self):
        """Connect to circuit hardware."""
        try:
            if HARDWARE_AVAILABLE:
                rm = pyvisa.ResourceManager()
                
                # XYZ positioner (e.g., Newport ESP301)
                self.positioner = rm.open_resource('GPIB0::1::INSTR')
                
                # High-voltage power supply (e.g., Keithley 2410)
                self.power_supply = rm.open_resource('GPIB0::24::INSTR')
                
                # Picoammeter (e.g., Keithley 6485)
                self.ammeter = rm.open_resource('GPIB0::22::INSTR')
                
                print("✓ Semiconductor circuit hardware connected")
        except Exception as e:
            print(f"✗ Hardware connection failed: {e}")
            print("  Falling back to simulation mode")
            self.simulation_mode = True
    
    def move_electron(self, target_position: np.ndarray):
        """
        Move electron injection point to target position.
        
        Args:
            target_position: [x, y, z] in meters
        """
        if self.simulation_mode:
            self.electron_position = target_position.copy()
            print(f"[SIM] Electron moved to {target_position}")
            return
        
        # Send positioning commands
        x, y, z = target_position * 1000  # Convert to mm
        self.positioner.write(f'1PA{x:.3f};2PA{y:.3f};3PA{z:.3f}')
        
        # Wait for motion to complete
        time.sleep(0.5)
        
        self.electron_position = target_position
        print(f"Electron position: {target_position}")
    
    def set_voltage(self, voltage: float):
        """
        Set applied voltage for electron emission.
        
        Args:
            voltage: Voltage in V (0 to voltage_range)
        """
        voltage = np.clip(voltage, 0, self.voltage_range)
        
        if self.simulation_mode:
            self.applied_voltage = voltage
            # Simulate current (rough field emission model)
            self.measured_current = 1e-12 * (voltage / 5000.0) ** 2
            print(f"[SIM] Voltage: {voltage:.1f} V, Current: {self.measured_current*1e12:.2f} pA")
            return
        
        # Set voltage
        self.power_supply.write(f':SOUR:VOLT {voltage:.2f}')
        self.power_supply.write(':OUTP ON')
        
        time.sleep(0.1)  # Settle time
        
        # Measure current
        current_str = self.ammeter.query(':READ?')
        self.measured_current = float(current_str)
        
        self.applied_voltage = voltage
        print(f"Voltage: {voltage:.1f} V, Current: {self.measured_current*1e12:.2f} pA")
    
    def get_circuit_state(self) -> CircuitState:
        """Get current circuit state."""
        return CircuitState(
            timestamp=time.time(),
            electron_position=self.electron_position.copy(),
            applied_voltage=self.applied_voltage,
            measured_current=self.measured_current,
            electron_energy=self.applied_voltage * 1.602e-19 / 1.602e-19  # eV
        )


class IntegratedSystem:
    """
    Complete integrated hardware system.
    
    Coordinates:
    - Gas chamber
    - Sensor array
    - Semiconductor circuit
    - Data acquisition and control
    """
    
    def __init__(self, simulation_mode: bool = not HARDWARE_AVAILABLE):
        """Initialize complete system."""
        print("\n" + "="*80)
        print("INITIALIZING CONSCIOUSNESS DETECTION HARDWARE")
        print("="*80 + "\n")
        
        self.simulation_mode = simulation_mode
        
        # Initialize subsystems
        print("1. Gas Chamber...")
        self.chamber = GasChamberHardware(simulation_mode=simulation_mode)
        
        print("\n2. Sensor Array...")
        self.sensors = SensorArrayHardware(simulation_mode=simulation_mode)
        
        print("\n3. Semiconductor Circuit...")
        self.circuit = SemiconductorCircuitHardware(simulation_mode=simulation_mode)
        
        print("\n" + "="*80)
        if simulation_mode:
            print("✓ System initialized in SIMULATION MODE")
        else:
            print("✓ System initialized with PHYSICAL HARDWARE")
        print("="*80 + "\n")
    
    def startup_sequence(self):
        """Run complete startup sequence."""
        print("\n" + "="*80)
        print("SYSTEM STARTUP SEQUENCE")
        print("="*80 + "\n")
        
        # 1. Set gas composition
        print("1. Setting O₂ concentration to 0.5%...")
        self.chamber.set_o2_concentration(0.005)
        time.sleep(2.0)
        
        # 2. Set temperature
        print("\n2. Setting temperature to 310K (37°C)...")
        self.chamber.set_temperature(310.0)
        time.sleep(2.0)
        
        # 3. Start data acquisition
        print("\n3. Starting sensor data acquisition...")
        self.sensors.start_acquisition()
        time.sleep(1.0)
        
        # 4. Initialize electron position
        print("\n4. Moving electron to initial position...")
        self.circuit.move_electron(np.array([0.0, 0.0, 0.1]))
        time.sleep(0.5)
        
        # 5. Enable electron emission
        print("\n5. Enabling electron emission (5kV)...")
        self.circuit.set_voltage(5000.0)
        time.sleep(0.5)
        
        print("\n" + "="*80)
        print("✓ SYSTEM READY FOR EXPERIMENTS")
        print("="*80 + "\n")
    
    def shutdown_sequence(self):
        """Safe shutdown sequence."""
        print("\n" + "="*80)
        print("SYSTEM SHUTDOWN SEQUENCE")
        print("="*80 + "\n")
        
        # 1. Disable electron emission
        print("1. Disabling electron emission...")
        self.circuit.set_voltage(0.0)
        
        # 2. Stop data acquisition
        print("\n2. Stopping data acquisition...")
        self.sensors.stop_acquisition()
        
        # 3. Return to ambient conditions
        print("\n3. Returning to ambient conditions...")
        self.chamber.set_o2_concentration(0.21)  # Ambient air
        self.chamber.set_temperature(298.0)  # Room temp
        
        print("\n" + "="*80)
        print("✓ SYSTEM SHUTDOWN COMPLETE")
        print("="*80 + "\n")


def demonstrate_hardware():
    """Demonstrate hardware system."""
    print("\n" + "="*80)
    print("HARDWARE DEMONSTRATION")
    print("="*80 + "\n")
    
    # Initialize system
    system = IntegratedSystem(simulation_mode=True)
    
    # Startup
    system.startup_sequence()
    
    # Wait for stabilization
    print("Waiting for system stabilization...")
    time.sleep(2.0)
    
    # Test odorant injection
    print("\nTesting odorant injection...")
    system.chamber.inject_odorant("Vanillin", volume_uL=5.0, flow_rate_uL_min=1.0)
    
    # Monitor sensors
    print("\nMonitoring sensors for 3 seconds...")
    for i in range(3):
        time.sleep(1.0)
        data = system.sensors.get_latest_data(max_samples=10)
        if data:
            avg_o2 = np.mean([r.o2_concentration for r in data])
            print(f"  t={i+1}s: Average O₂ = {avg_o2*100:.3f}%")
    
    # Test electron movement
    print("\nTesting electron positioning...")
    positions = [
        np.array([0.05, 0.0, 0.1]),
        np.array([0.0, 0.05, 0.1]),
        np.array([-0.05, 0.0, 0.1]),
        np.array([0.0, 0.0, 0.1]),  # Return to center
    ]
    
    for pos in positions:
        system.circuit.move_electron(pos)
        state = system.circuit.get_circuit_state()
        print(f"  Position: {pos}, Current: {state.measured_current*1e12:.2f} pA")
        time.sleep(0.5)
    
    # Shutdown
    system.shutdown_sequence()
    
    print("\n✓ Hardware demonstration complete!")


if __name__ == "__main__":
    demonstrate_hardware()

