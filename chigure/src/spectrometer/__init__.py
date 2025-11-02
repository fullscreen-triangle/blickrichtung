"""
Optical Imaging Spectrometer Package
=====================================

Zero-cost spectrometer using LED + DVD grating + camera.
"""

from .hardware import (
    OpticalSpectrometerHardware,
    LEDLightSource,
    DiffractionGrating,
    CameraSensor,
    LEDConfig,
    GratingConfig,
    CameraConfig
)

from .grating_calibration import (
    GratingCalibration,
    CalibrationLine
)

from .spectral_extraction import SpectralExtractor

from .absorption_analysis import AbsorptionAnalyzer

from .s_entropy_optical import SOpticalMapper

from .calibration import (
    SpectrometerCalibrator,
    SpectrometerCalibration
)

from .grandwave_integration import SpectrometerGrandWaveConnector


__all__ = [
    # Hardware
    'OpticalSpectrometerHardware',
    'LEDLightSource',
    'DiffractionGrating',
    'CameraSensor',
    'LEDConfig',
    'GratingConfig',
    'CameraConfig',
    
    # Grating calibration
    'GratingCalibration',
    'CalibrationLine',
    
    # Spectral extraction
    'SpectralExtractor',
    
    # Absorption analysis
    'AbsorptionAnalyzer',
    
    # S-entropy
    'SOpticalMapper',
    
    # System calibration
    'SpectrometerCalibrator',
    'SpectrometerCalibration',
    
    # GrandWave Integration
    'SpectrometerGrandWaveConnector'
]

