"""
Optical Spectrometer Hardware
==============================

LED light source + diffraction grating + camera sensor.

Hardware:
- RGB LED (470nm blue, 525nm green, 625nm red)
- DVD diffraction grating (1.6 μm spacing)
- Webcam or smartphone camera
- Trans-Planckian clock for timing
"""

import numpy as np
from typing import Dict, Tuple, Optional
from dataclasses import dataclass
import sys
sys.path.append('../../grand_unification')
from clock_synchronization import HardwareClockSync


@dataclass
class LEDConfig:
    """LED light source configuration"""
    wavelengths: Tuple[float, float, float] = (470e-9, 525e-9, 625e-9)  # meters
    max_intensity: float = 1.0
    pulse_duration: float = 0.001  # seconds
    

@dataclass
class GratingConfig:
    """Diffraction grating configuration"""
    groove_spacing: float = 1.6e-6  # meters (DVD: 1.6 μm)
    order: int = 1  # First order diffraction
    

@dataclass
class CameraConfig:
    """Camera sensor configuration"""
    resolution: Tuple[int, int] = (1920, 1080)
    exposure_time: float = 0.01  # seconds
    gain: float = 1.0
    

class LEDLightSource:
    """
    RGB LED light source for sample illumination
    """
    
    def __init__(self, config: LEDConfig):
        """Initialize LED source"""
        self.config = config
        self.clock = HardwareClockSync()
        
    def illuminate_sample(self,
                         wavelength_index: int,
                         intensity: float,
                         duration: float) -> Dict:
        """
        Illuminate sample with specific LED
        
        Args:
            wavelength_index: 0=blue, 1=green, 2=red
            intensity: 0-1
            duration: seconds
            
        Returns:
            Illumination parameters
        """
        if wavelength_index not in [0, 1, 2]:
            raise ValueError("wavelength_index must be 0, 1, or 2")
            
        wavelength = self.config.wavelengths[wavelength_index]
        
        # Record timing
        t_start = self.clock.get_time()
        
        # In real implementation, would control LED hardware
        # Here we simulate
        
        t_end = self.clock.get_time()
        actual_duration = t_end - t_start
        
        return {
            'wavelength': wavelength,
            'wavelength_nm': wavelength * 1e9,
            'intensity': intensity,
            'duration': actual_duration,
            't_start': t_start,
            't_end': t_end,
            'color': ['blue', 'green', 'red'][wavelength_index]
        }
        
    def multi_wavelength_sequence(self,
                                 intensities: Tuple[float, float, float],
                                 duration_each: float) -> Dict:
        """
        Sequential illumination with all wavelengths
        
        Args:
            intensities: (blue, green, red) intensities
            duration_each: Duration for each (seconds)
            
        Returns:
            Sequence results
        """
        results = []
        
        for idx, intensity in enumerate(intensities):
            result = self.illuminate_sample(idx, intensity, duration_each)
            results.append(result)
            
        return {
            'sequence': results,
            'total_duration': sum(r['duration'] for r in results)
        }


class DiffractionGrating:
    """
    Diffraction grating (DVD) for wavelength separation
    """
    
    def __init__(self, config: GratingConfig):
        """Initialize grating"""
        self.config = config
        
    def calculate_diffraction_angle(self, wavelength: float) -> float:
        """
        Calculate diffraction angle for wavelength
        
        Args:
            wavelength: Wavelength (meters)
            
        Returns:
            Diffraction angle (radians)
        """
        # Grating equation: d sin(θ) = m λ
        # θ = arcsin(m λ / d)
        
        m = self.config.order
        d = self.config.groove_spacing
        
        sin_theta = m * wavelength / d
        
        if abs(sin_theta) > 1:
            raise ValueError(f"Wavelength {wavelength*1e9:.1f} nm cannot diffract")
            
        theta = np.arcsin(sin_theta)
        
        return theta
        
    def wavelength_to_pixel_position(self,
                                    wavelength: float,
                                    camera_distance: float,
                                    pixel_size: float) -> int:
        """
        Calculate pixel position for wavelength
        
        Args:
            wavelength: Wavelength (meters)
            camera_distance: Distance to camera (meters)
            pixel_size: Camera pixel size (meters)
            
        Returns:
            Pixel position
        """
        theta = self.calculate_diffraction_angle(wavelength)
        
        # Position on sensor
        x = camera_distance * np.tan(theta)
        
        # Pixel position
        pixel = int(x / pixel_size)
        
        return pixel


class CameraSensor:
    """
    Camera sensor for capturing spectrum
    """
    
    def __init__(self, config: CameraConfig):
        """Initialize camera"""
        self.config = config
        self.clock = HardwareClockSync()
        
    def capture_frame(self, exposure_time: Optional[float] = None) -> Dict:
        """
        Capture single frame
        
        Args:
            exposure_time: Optional exposure override (seconds)
            
        Returns:
            Frame data
        """
        if exposure_time is None:
            exposure_time = self.config.exposure_time
            
        t_start = self.clock.get_time()
        
        # In real implementation, would capture from camera
        # Here we simulate a blank frame
        frame = np.zeros(self.config.resolution, dtype=np.uint16)
        
        t_end = self.clock.get_time()
        
        return {
            'frame': frame,
            'timestamp': t_start,
            'exposure_time': exposure_time,
            'duration': t_end - t_start,
            'resolution': self.config.resolution
        }
        
    def capture_spectrum_series(self,
                               n_frames: int,
                               exposure_time: float) -> Dict:
        """
        Capture series of frames for averaging
        
        Args:
            n_frames: Number of frames
            exposure_time: Exposure time (seconds)
            
        Returns:
            Averaged spectrum
        """
        frames = []
        timestamps = []
        
        for _ in range(n_frames):
            result = self.capture_frame(exposure_time)
            frames.append(result['frame'])
            timestamps.append(result['timestamp'])
            
        # Average frames
        averaged = np.mean(frames, axis=0).astype(np.uint16)
        
        return {
            'averaged_frame': averaged,
            'n_frames': n_frames,
            'timestamps': np.array(timestamps),
            'exposure_time': exposure_time
        }


class OpticalSpectrometerHardware:
    """
    Complete optical spectrometer system
    """
    
    def __init__(self,
                 led_config: Optional[LEDConfig] = None,
                 grating_config: Optional[GratingConfig] = None,
                 camera_config: Optional[CameraConfig] = None):
        """Initialize spectrometer hardware"""
        
        self.led = LEDLightSource(led_config or LEDConfig())
        self.grating = DiffractionGrating(grating_config or GratingConfig())
        self.camera = CameraSensor(camera_config or CameraConfig())
        
        # Optical setup parameters (typical values)
        self.camera_distance = 0.10  # 10 cm
        self.pixel_size = 5e-6  # 5 μm typical webcam pixel
        
    def measure_sample_spectrum(self,
                               sample_id: str,
                               wavelength_index: int = 0,
                               led_intensity: float = 1.0,
                               n_averages: int = 10,
                               exposure_time: float = 0.01) -> Dict:
        """
        Measure absorption/transmission spectrum of sample
        
        Args:
            sample_id: Sample identifier
            wavelength_index: LED to use (0=blue, 1=green, 2=red)
            led_intensity: LED intensity (0-1)
            n_averages: Number of frames to average
            exposure_time: Camera exposure (seconds)
            
        Returns:
            Spectrum data
        """
        # Illuminate sample
        illumination = self.led.illuminate_sample(
            wavelength_index,
            led_intensity,
            duration=exposure_time * n_averages
        )
        
        # Capture spectrum
        spectrum = self.camera.capture_spectrum_series(
            n_averages,
            exposure_time
        )
        
        return {
            'sample_id': sample_id,
            'illumination': illumination,
            'spectrum_frame': spectrum['averaged_frame'],
            'n_averages': n_averages,
            'exposure_time': exposure_time,
            'wavelength': illumination['wavelength'],
            'wavelength_nm': illumination['wavelength_nm']
        }
        
    def calibrate_wavelength_axis(self) -> Dict:
        """
        Calibrate pixel position to wavelength mapping
        
        Returns:
            Calibration parameters
        """
        # Known LED wavelengths
        wavelengths = np.array(self.led.config.wavelengths)
        wavelengths_nm = wavelengths * 1e9
        
        # Calculate expected pixel positions
        pixel_positions = []
        for wl in wavelengths:
            pixel = self.grating.wavelength_to_pixel_position(
                wl,
                self.camera_distance,
                self.pixel_size
            )
            pixel_positions.append(pixel)
            
        pixel_positions = np.array(pixel_positions)
        
        # Fit linear calibration
        # pixel = a * wavelength + b
        coeffs = np.polyfit(wavelengths_nm, pixel_positions, deg=1)
        
        return {
            'wavelengths_nm': wavelengths_nm,
            'pixel_positions': pixel_positions,
            'calibration_coeffs': coeffs,
            'pixel_per_nm': coeffs[0]
        }
