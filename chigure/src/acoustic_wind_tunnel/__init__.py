"""
Acoustic Wind Tunnel Package
=============================

Zero-cost wind tunnel using ultrasonic acoustic streaming.
"""

from .hardware import (
    AcousticWindTunnelHardware,
    UltrasonicSpeakerArray,
    MicrophoneArray,
    SpeakerArrayConfig,
    MicrophoneArrayConfig
)

from .acoustic_streaming import AcousticStreamingPhysics

from .velocimetry import CrossCorrelationVelocimetry

from .s_entropy_acoustic import SAcousticMapper

from .calibration import AcousticCalibration, CalibrationPoint

from .grandwave_integration import AcousticGrandWaveConnector


__all__ = [
    # Hardware
    'AcousticWindTunnelHardware',
    'UltrasonicSpeakerArray',
    'MicrophoneArray',
    'SpeakerArrayConfig',
    'MicrophoneArrayConfig',
    
    # Physics
    'AcousticStreamingPhysics',
    
    # Velocimetry
    'CrossCorrelationVelocimetry',
    
    # S-entropy
    'SAcousticMapper',
    
    # Calibration
    'AcousticCalibration',
    'CalibrationPoint',
    
    # GrandWave Integration
    'AcousticGrandWaveConnector'
]

