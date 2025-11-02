"""
Sleep and Circadian System Oscillatory Dynamics Validator

This module validates the theoretical predictions about sleep-wake cycles,
circadian rhythms, consciousness oscillations, and sleep architecture within
the unified biological oscillations framework.

Key Validations:
1. Circadian Rhythm Oscillatory Coupling
2. Sleep Architecture Validation  
3. Consciousness State Transitions
"""

import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from scipy import signal, stats
from scipy.integrate import odeint
import pandas as pd
from typing import Dict, List, Tuple, Any
import os
from datetime import datetime

class SleepOscillatoryValidator:
    """Validates oscillatory dynamics in sleep and circadian systems"""
    
    def __init__(self, results_dir: str = "results/sleep"):
        self.results_dir = results_dir
        os.makedirs(results_dir, exist_ok=True)
        
        # Circadian rhythm parameters
        self.circadian_params = {
            'period': 24.0 * 3600,             # 24 hours in seconds
            'scn_frequency': 1.16e-5,          # Hz (24 hour period)
            'melatonin_phase': -6 * 3600,      # 6 hours before sleep
            'cortisol_phase': -1 * 3600,       # 1 hour before wake
            'core_temp_phase': -4 * 3600,      # 4 hours before wake
        }
        
        # Sleep architecture parameters
        self.sleep_params = {
            'total_sleep_time': 8 * 3600,      # 8 hours
            'sleep_onset_latency': 15 * 60,    # 15 minutes
            'wake_after_sleep_onset': 30 * 60, # 30 minutes
            'rem_percentage': 22,              # % of TST
            'deep_sleep_percentage': 15,       # % of TST
            'light_sleep_percentage': 50,      # % of TST
            'sleep_cycles': 5,                 # Number of cycles per night
        }
        
        # Sleep oscillation frequencies
        self.sleep_frequencies = {
            'circadian': 1.16e-5,              # Hz - 24 hour cycle
            'ultradian': 1.39e-4,              # Hz - ~120 minute cycles
            'delta_waves': 1.0,                 # Hz - deep sleep
            'theta_waves': 6.0,                 # Hz - REM sleep
            'alpha_waves': 10.0,                # Hz - relaxed wake
            'beta_waves': 20.0,                 # Hz - active wake
            'gamma_waves': 40.0,                # Hz - conscious awareness
            'sleep_spindles': 12.5,             # Hz - stage 2 sleep
            'k_complexes': 0.5,                 # Hz - slow wave activity
        }
        
        # Neurotransmitter parameters
        self.neurotransmitter_params = {
            'melatonin_amplitude': 10.0,        # pg/mL peak
            'cortisol_amplitude': 20.0,         # μg/dL peak  
            'adenosine_buildup_rate': 1.0,      # Relative units/hour
            'orexin_wake_level': 1.0,           # Wake promoting
            'gaba_sleep_level': 1.0,            # Sleep promoting
        }
        
        self.validation_results = {}
        
    def experiment_1_circadian_rhythm_oscillatory_coupling(self) -> Dict[str, Any]:
        """
        Experiment 1: Circadian Rhythm Oscillatory Coupling
        
        Validates multi-oscillator circadian system:
        - Suprachiasmatic nucleus (SCN) master clock
        - Peripheral tissue clocks
        - Light entrainment
        - Melatonin and cortisol rhythms
        """
        print("🕐 Experiment 1: Circadian Rhythm Oscillatory Coupling")
        
        # Simulation parameters
        duration = 3 * 24 * 3600  # 3 days in seconds
        fs = 1.0 / 3600  # 1 sample per hour
        t = np.linspace(0, duration, int(duration * fs))
        
        # Circadian oscillator system model
        def circadian_oscillator_system(state, t):
            """
            Multi-oscillator circadian system:
            - SCN master clock
            - Peripheral clocks (liver, muscle, etc.)
            - Light input and entrainment
            - Melatonin/cortisol output rhythms
            """
            (scn_phase, liver_clock, muscle_clock, melatonin_level, 
             cortisol_level, core_temp, light_input_history) = state
            
            # Light input (simplified day/night cycle with dawn/dusk transitions)
            hour_of_day = (t / 3600) % 24
            if 6 <= hour_of_day <= 18:  # Day
                light_intensity = 1000 + 500 * np.sin(np.pi * (hour_of_day - 6) / 12)  # Lux
            else:  # Night
                light_intensity = 1  # Dim light
            
            # Light entrainment of SCN
            light_entrainment_strength = 0.1
            light_phase_shift = light_entrainment_strength * light_intensity / 1000
            
            # SCN master clock (core circadian oscillator)
            scn_frequency = self.circadian_params['scn_frequency']
            scn_period_correction = light_phase_shift * np.sin(scn_phase)
            scn_phase_dot = 2 * np.pi * scn_frequency + scn_period_correction
            
            # Peripheral clock oscillators (coupled to SCN but with some autonomy)
            scn_coupling_strength = 0.3
            
            # Liver clock (metabolic rhythms)
            liver_autonomous_freq = scn_frequency * 0.98  # Slightly different period
            liver_scn_coupling = scn_coupling_strength * np.sin(scn_phase - liver_clock)
            liver_clock_dot = 2 * np.pi * liver_autonomous_freq + liver_scn_coupling
            
            # Muscle clock (physical activity rhythms)
            muscle_autonomous_freq = scn_frequency * 1.02  # Slightly different period
            muscle_scn_coupling = scn_coupling_strength * np.sin(scn_phase - muscle_clock)
            muscle_clock_dot = 2 * np.pi * muscle_autonomous_freq + muscle_scn_coupling
            
            # Melatonin production (pineal gland, suppressed by light)
            melatonin_phase = scn_phase + self.circadian_params['melatonin_phase'] / (24*3600) * 2*np.pi
            melatonin_base_production = self.neurotransmitter_params['melatonin_amplitude']
            light_suppression = 1.0 / (1.0 + (light_intensity / 100)**2)  # Suppressed by light
            
            melatonin_target = melatonin_base_production * light_suppression * (0.5 + 0.5 * np.sin(melatonin_phase))
            melatonin_dot = 0.5 * (melatonin_target - melatonin_level)  # Fast response
            
            # Cortisol production (HPA axis, peaks in morning)
            cortisol_phase = scn_phase + self.circadian_params['cortisol_phase'] / (24*3600) * 2*np.pi
            cortisol_base_production = self.neurotransmitter_params['cortisol_amplitude']
            
            cortisol_target = cortisol_base_production * (0.3 + 0.7 * np.sin(cortisol_phase))
            cortisol_dot = 0.3 * (cortisol_target - cortisol_level)  # Slower response
            
            # Core body temperature rhythm
            temp_phase = scn_phase + self.circadian_params['core_temp_phase'] / (24*3600) * 2*np.pi
            temp_baseline = 36.8  # °C
            temp_amplitude = 0.8   # °C
            
            temp_target = temp_baseline + temp_amplitude * np.sin(temp_phase)
            core_temp_dot = 0.2 * (temp_target - core_temp)
            
            # Light input history (for entrainment analysis)
            light_input_history_dot = 0.1 * (light_intensity - light_input_history)
            
            return [scn_phase_dot, liver_clock_dot, muscle_clock_dot, melatonin_dot,
                   cortisol_dot, core_temp_dot, light_input_history_dot]
        
        # Initial conditions
        initial_state = [
            0.0,    # SCN phase
            0.1,    # Liver clock phase (slightly offset)
            -0.1,   # Muscle clock phase (slightly offset)
            2.0,    # Melatonin level (pg/mL)
            5.0,    # Cortisol level (μg/dL)  
            36.5,   # Core temperature (°C)
            500     # Light input history (Lux)
        ]
        
        # Solve circadian system
        solution = odeint(circadian_oscillator_system, initial_state, t)
        scn_phase_trace = solution[:, 0]
        liver_clock_trace = solution[:, 1]
        muscle_clock_trace = solution[:, 2]
        melatonin_trace = solution[:, 3]
        cortisol_trace = solution[:, 4]
        core_temp_trace = solution[:, 5]
        light_history_trace = solution[:, 6]
        
        # Convert phases to normalized oscillations for analysis
        scn_oscillation = np.sin(scn_phase_trace)
        liver_oscillation = np.sin(liver_clock_trace)
        muscle_oscillation = np.sin(muscle_clock_trace)
        
        # Calculate circadian metrics
        # Period estimation (using autocorrelation)
        def estimate_period(signal, sampling_rate):
            """Estimate period using autocorrelation"""
            autocorr = np.correlate(signal, signal, mode='full')
            autocorr = autocorr[len(autocorr)//2:]
            
            # Find peaks in autocorrelation
            peaks, _ = signal.find_peaks(autocorr[1:], height=0.5*np.max(autocorr))
            if len(peaks) > 0:
                first_peak = peaks[0] + 1  # +1 because we started from index 1
                period = first_peak / sampling_rate
                return period
            return 24 * 3600  # Default to 24 hours
        
        scn_period = estimate_period(scn_oscillation, fs) / 3600  # Convert to hours
        melatonin_period = estimate_period(melatonin_trace, fs) / 3600
        cortisol_period = estimate_period(cortisol_trace, fs) / 3600
        
        # Phase relationships between oscillators
        from scipy.signal import hilbert
        
        # SCN-peripheral clock coupling
        scn_analytic = hilbert(scn_oscillation)
        liver_analytic = hilbert(liver_oscillation)
        muscle_analytic = hilbert(muscle_oscillation)
        
        scn_phase = np.angle(scn_analytic)
        liver_phase = np.angle(liver_analytic)
        muscle_phase = np.angle(muscle_analytic)
        
        # Phase coupling strength
        scn_liver_coupling = np.abs(np.mean(np.exp(1j * (scn_phase - liver_phase))))
        scn_muscle_coupling = np.abs(np.mean(np.exp(1j * (scn_phase - muscle_phase))))
        
        # Hormone rhythm analysis
        melatonin_max_times = []
        cortisol_max_times = []
        
        # Find peak times (simplified)
        melatonin_peaks, _ = signal.find_peaks(melatonin_trace, distance=int(20*fs))  # At least 20 hours apart
        cortisol_peaks, _ = signal.find_peaks(cortisol_trace, distance=int(20*fs))
        
        if len(melatonin_peaks) > 0:
            melatonin_max_times = t[melatonin_peaks] / 3600  # Convert to hours
        if len(cortisol_peaks) > 0:
            cortisol_max_times = t[cortisol_peaks] / 3600
        
        # Calculate phase relationships
        melatonin_cortisol_phase_diff = 0
        if len(melatonin_max_times) > 0 and len(cortisol_max_times) > 0:
            # Average phase difference between peaks
            phase_diffs = []
            for mel_time in melatonin_max_times:
                closest_cort = cortisol_max_times[np.argmin(np.abs(cortisol_max_times - mel_time))]
                phase_diff = (closest_cort - mel_time) % 24  # Modulo 24 hours
                phase_diffs.append(phase_diff)
            melatonin_cortisol_phase_diff = np.mean(phase_diffs)
        
        # Temperature rhythm coupling
        temp_scn_coupling = np.corrcoef(core_temp_trace, scn_oscillation)[0, 1]
        
        # Entrainment effectiveness (how well synchronized to 24h)
        entrainment_quality = 1.0 / (1.0 + abs(scn_period - 24.0))
        
        # Light response analysis
        light_melatonin_coupling = np.corrcoef(light_history_trace, melatonin_trace)[0, 1]
        
        # Theoretical predictions
        theoretical_predictions = {
            'expected_period_range': (23.8, 24.2),  # Hours, normal circadian period
            'scn_peripheral_coupling_min': 0.7,      # Strong coupling expected
            'melatonin_cortisol_phase_diff_range': (6, 10),  # Hours separation
            'temp_scn_coupling_min': 0.6,            # Temperature follows SCN
            'entrainment_quality_min': 0.8,          # Good 24h entrainment
            'light_melatonin_anticorrelation_max': -0.3,  # Light suppresses melatonin
        }
        
        # Validation
        validation_success = (
            theoretical_predictions['expected_period_range'][0] <= scn_period <= 
            theoretical_predictions['expected_period_range'][1] and
            scn_liver_coupling >= theoretical_predictions['scn_peripheral_coupling_min'] and
            scn_muscle_coupling >= theoretical_predictions['scn_peripheral_coupling_min'] and
            theoretical_predictions['melatonin_cortisol_phase_diff_range'][0] <= 
            melatonin_cortisol_phase_diff <= 
            theoretical_predictions['melatonin_cortisol_phase_diff_range'][1] and
            temp_scn_coupling >= theoretical_predictions['temp_scn_coupling_min'] and
            entrainment_quality >= theoretical_predictions['entrainment_quality_min'] and
            light_melatonin_coupling <= theoretical_predictions['light_melatonin_anticorrelation_max']
        )
        
        results = {
            'experiment': 'Circadian Rhythm Oscillatory Coupling',
            'validation_success': validation_success,
            'circadian_traces': {
                'time_hours': t / 3600,
                'scn_oscillation': scn_oscillation,
                'liver_oscillation': liver_oscillation,
                'muscle_oscillation': muscle_oscillation,
                'melatonin': melatonin_trace,
                'cortisol': cortisol_trace,
                'core_temperature': core_temp_trace,
                'light_exposure': light_history_trace
            },
            'period_analysis': {
                'scn_period_hours': scn_period,
                'melatonin_period_hours': melatonin_period,
                'cortisol_period_hours': cortisol_period
            },
            'coupling_analysis': {
                'scn_liver_coupling': scn_liver_coupling,
                'scn_muscle_coupling': scn_muscle_coupling,
                'temp_scn_coupling': temp_scn_coupling,
                'light_melatonin_coupling': light_melatonin_coupling
            },
            'rhythm_metrics': {
                'melatonin_cortisol_phase_diff': melatonin_cortisol_phase_diff,
                'entrainment_quality': entrainment_quality,
                'melatonin_peak_times': melatonin_max_times,
                'cortisol_peak_times': cortisol_max_times
            },
            'theoretical_predictions': theoretical_predictions
        }
        
        # Visualization
        self._plot_circadian_analysis(results)
        
        return results
    
    def experiment_2_sleep_architecture_validation(self) -> Dict[str, Any]:
        """
        Experiment 2: Sleep Architecture Validation
        
        Validates oscillatory structure of sleep:
        - Ultradian sleep cycles (~90 minutes)
        - Sleep stage transitions
        - EEG frequency band evolution
        - REM/NREM oscillations
        """
        print("💤 Experiment 2: Sleep Architecture Validation")
        
        # Simulation parameters
        sleep_duration = 8 * 3600  # 8 hours of sleep
        fs = 1.0  # 1 Hz sampling
        t = np.linspace(0, sleep_duration, int(sleep_duration * fs))
        
        # Sleep architecture model
        def sleep_architecture_system(state, t):
            """
            Multi-stage sleep architecture model:
            - Ultradian sleep cycles
            - Sleep stage progression
            - REM pressure buildup
            - EEG frequency generation
            """
            (sleep_stage, rem_pressure, delta_amplitude, theta_amplitude,
             alpha_amplitude, sigma_amplitude, homeostatic_drive) = state
            
            # Ultradian cycle (approximately 90 minutes)
            ultradian_frequency = self.sleep_frequencies['ultradian']
            ultradian_phase = ultradian_frequency * 2 * np.pi * t
            ultradian_modulation = np.sin(ultradian_phase)
            
            # Sleep homeostatic drive (Process S - decreases during sleep)
            homeostatic_decay_rate = 1.0 / (6 * 3600)  # 6 hour time constant
            homeostatic_drive_dot = -homeostatic_decay_rate * homeostatic_drive
            
            # REM pressure buildup (increases during NREM, released during REM)
            current_stage = sleep_stage
            if current_stage < 0:  # REM sleep (negative values)
                rem_pressure_change = -2.0  # REM pressure decreases during REM
            else:  # NREM sleep (positive values)
                rem_pressure_change = 0.5   # REM pressure builds during NREM
            
            rem_pressure_dot = rem_pressure_change * (1.0 - rem_pressure) if rem_pressure < 1.0 else 0
            
            # Sleep stage transitions based on ultradian cycle and pressures
            # Stage coding: 3=N3 (deep), 2=N2 (light), 1=N1 (transition), 0=wake, -1=REM
            
            cycle_position = (ultradian_modulation + 1) / 2  # 0 to 1
            
            if cycle_position < 0.3:  # Early cycle - deep sleep
                target_stage = 3 - 2 * homeostatic_drive  # Deeper when tired
            elif cycle_position < 0.6:  # Mid cycle - light NREM
                target_stage = 2
            elif cycle_position < 0.8 and rem_pressure > 0.6:  # Late cycle - REM if pressure high
                target_stage = -1
            else:  # Transition periods
                target_stage = 1
            
            sleep_stage_dot = 2.0 * (target_stage - sleep_stage)  # Smooth transitions
            
            # EEG frequency amplitudes based on sleep stage
            current_stage_rounded = np.round(sleep_stage)
            
            # Delta waves (0.5-4 Hz) - prominent in deep sleep
            if current_stage_rounded >= 2:  # NREM stages
                delta_target = (current_stage_rounded / 3) * 100  # Stronger in deeper sleep
            else:
                delta_target = 10  # Minimal delta
            delta_amplitude_dot = 0.5 * (delta_target - delta_amplitude)
            
            # Theta waves (4-8 Hz) - prominent in REM
            if current_stage_rounded == -1:  # REM
                theta_target = 80
            elif current_stage_rounded == 1:  # N1
                theta_target = 40
            else:
                theta_target = 15
            theta_amplitude_dot = 0.8 * (theta_target - theta_amplitude)
            
            # Alpha waves (8-12 Hz) - prominent in wake/drowsy
            if current_stage_rounded <= 1 and current_stage_rounded >= 0:
                alpha_target = 50
            else:
                alpha_target = 10
            alpha_amplitude_dot = 1.0 * (alpha_target - alpha_amplitude)
            
            # Sigma/spindle activity (11-15 Hz) - prominent in N2
            if current_stage_rounded == 2:
                sigma_target = 60
            else:
                sigma_target = 5
            sigma_amplitude_dot = 0.6 * (sigma_target - sigma_amplitude)
            
            return [sleep_stage_dot, rem_pressure_dot, delta_amplitude_dot,
                   theta_amplitude_dot, alpha_amplitude_dot, sigma_amplitude_dot,
                   homeostatic_drive_dot]
        
        # Initial conditions (sleep onset)
        initial_state = [
            1.0,  # Sleep stage (N1)
            0.2,  # REM pressure (low at start)
            20,   # Delta amplitude
            30,   # Theta amplitude
            40,   # Alpha amplitude
            10,   # Sigma amplitude
            0.8   # Homeostatic drive (high at sleep onset)
        ]
        
        # Solve sleep architecture system
        solution = odeint(sleep_architecture_system, initial_state, t)
        sleep_stage_trace = solution[:, 0]
        rem_pressure_trace = solution[:, 1]
        delta_amplitude_trace = solution[:, 2]
        theta_amplitude_trace = solution[:, 3]
        alpha_amplitude_trace = solution[:, 4]
        sigma_amplitude_trace = solution[:, 5]
        homeostatic_drive_trace = solution[:, 6]
        
        # Generate synthetic EEG based on sleep stages
        eeg_signal = np.zeros_like(t)
        
        for i, time_point in enumerate(t):
            # Combine frequency bands with appropriate amplitudes
            delta_component = delta_amplitude_trace[i] * np.sin(
                self.sleep_frequencies['delta_waves'] * 2 * np.pi * time_point)
            theta_component = theta_amplitude_trace[i] * np.sin(
                self.sleep_frequencies['theta_waves'] * 2 * np.pi * time_point)
            alpha_component = alpha_amplitude_trace[i] * np.sin(
                self.sleep_frequencies['alpha_waves'] * 2 * np.pi * time_point)
            sigma_component = sigma_amplitude_trace[i] * np.sin(
                self.sleep_frequencies['sleep_spindles'] * 2 * np.pi * time_point)
            
            # Add some noise
            noise_component = 5 * np.random.randn()
            
            eeg_signal[i] = (delta_component + theta_component + 
                           alpha_component + sigma_component + noise_component)
        
        # Sleep architecture analysis
        # Extract sleep cycles
        sleep_cycles = []
        current_cycle_start = 0
        
        for i in range(1, len(sleep_stage_trace)):
            # Detect cycle boundaries (return to light sleep after REM)
            if (sleep_stage_trace[i-1] < 0 and sleep_stage_trace[i] > 0 and 
                sleep_stage_trace[i] < 2):  # REM to light NREM transition
                cycle_duration = (t[i] - t[current_cycle_start]) / 60  # Minutes
                if cycle_duration > 60:  # Minimum cycle length
                    sleep_cycles.append({
                        'start_time': t[current_cycle_start] / 60,
                        'end_time': t[i] / 60,
                        'duration': cycle_duration
                    })
                    current_cycle_start = i
        
        # Sleep stage statistics
        wake_time = np.sum(sleep_stage_trace == 0) / fs / 60  # Minutes
        n1_time = np.sum((sleep_stage_trace > 0) & (sleep_stage_trace < 1.5)) / fs / 60
        n2_time = np.sum((sleep_stage_trace >= 1.5) & (sleep_stage_trace < 2.5)) / fs / 60
        n3_time = np.sum(sleep_stage_trace >= 2.5) / fs / 60
        rem_time = np.sum(sleep_stage_trace < 0) / fs / 60
        
        total_sleep_time = n1_time + n2_time + n3_time + rem_time
        
        sleep_efficiency = total_sleep_time / (sleep_duration / 60) * 100
        rem_percentage = (rem_time / total_sleep_time) * 100 if total_sleep_time > 0 else 0
        deep_sleep_percentage = (n3_time / total_sleep_time) * 100 if total_sleep_time > 0 else 0
        
        # EEG frequency band analysis
        freqs, psd = signal.welch(eeg_signal, fs=fs, nperseg=1024)
        
        # Extract power in different frequency bands
        frequency_bands = {
            'delta': (0.5, 4),
            'theta': (4, 8),
            'alpha': (8, 12), 
            'sigma': (11, 15),
            'beta': (15, 30)
        }
        
        band_powers = {}
        total_power = np.trapz(psd, freqs)
        
        for band_name, (f_min, f_max) in frequency_bands.items():
            band_mask = (freqs >= f_min) & (freqs <= f_max)
            if np.any(band_mask):
                band_power = np.trapz(psd[band_mask], freqs[band_mask])
                band_powers[band_name] = band_power / total_power * 100
            else:
                band_powers[band_name] = 0
        
        # Sleep cycle regularity (coefficient of variation)
        if len(sleep_cycles) > 1:
            cycle_durations = [cycle['duration'] for cycle in sleep_cycles]
            cycle_regularity = 1.0 / (1.0 + np.std(cycle_durations) / np.mean(cycle_durations))
        else:
            cycle_regularity = 0
        
        # REM-NREM alternation analysis
        stage_transitions = np.diff(sleep_stage_trace)
        rem_entries = np.sum(stage_transitions < -1.5)  # Transitions into REM
        nrem_entries = np.sum(stage_transitions > 1.5)   # Transitions into deep NREM
        
        # Homeostatic sleep drive validation
        sleep_drive_decay = (homeostatic_drive_trace[0] - homeostatic_drive_trace[-1]) / homeostatic_drive_trace[0]
        
        # Theoretical predictions
        theoretical_predictions = {
            'expected_sleep_cycles': (4, 6),
            'expected_rem_percentage': (18, 25),
            'expected_deep_sleep_percentage': (10, 20),
            'expected_sleep_efficiency': (85, 95),
            'cycle_regularity_min': 0.6,
            'delta_power_dominance_min': 25,  # % of total power
            'rem_entries_min': 3,
            'sleep_drive_decay_min': 0.4  # Should decrease significantly
        }
        
        # Validation
        num_cycles = len(sleep_cycles)
        delta_power = band_powers.get('delta', 0)
        
        validation_success = (
            theoretical_predictions['expected_sleep_cycles'][0] <= num_cycles <= 
            theoretical_predictions['expected_sleep_cycles'][1] and
            theoretical_predictions['expected_rem_percentage'][0] <= rem_percentage <= 
            theoretical_predictions['expected_rem_percentage'][1] and
            theoretical_predictions['expected_deep_sleep_percentage'][0] <= deep_sleep_percentage <= 
            theoretical_predictions['expected_deep_sleep_percentage'][1] and
            sleep_efficiency >= theoretical_predictions['expected_sleep_efficiency'][0] and
            cycle_regularity >= theoretical_predictions['cycle_regularity_min'] and
            delta_power >= theoretical_predictions['delta_power_dominance_min'] and
            rem_entries >= theoretical_predictions['rem_entries_min'] and
            sleep_drive_decay >= theoretical_predictions['sleep_drive_decay_min']
        )
        
        results = {
            'experiment': 'Sleep Architecture Validation',
            'validation_success': validation_success,
            'sleep_traces': {
                'time_hours': t / 3600,
                'sleep_stage': sleep_stage_trace,
                'rem_pressure': rem_pressure_trace,
                'homeostatic_drive': homeostatic_drive_trace,
                'eeg_signal': eeg_signal
            },
            'frequency_amplitudes': {
                'delta': delta_amplitude_trace,
                'theta': theta_amplitude_trace,
                'alpha': alpha_amplitude_trace,
                'sigma': sigma_amplitude_trace
            },
            'sleep_architecture': {
                'sleep_cycles': sleep_cycles,
                'total_sleep_time': total_sleep_time,
                'wake_time': wake_time,
                'n1_time': n1_time,
                'n2_time': n2_time,
                'n3_time': n3_time,
                'rem_time': rem_time,
                'sleep_efficiency': sleep_efficiency,
                'rem_percentage': rem_percentage,
                'deep_sleep_percentage': deep_sleep_percentage
            },
            'eeg_analysis': {
                'band_powers': band_powers,
                'frequencies': freqs,
                'power_spectral_density': psd
            },
            'sleep_dynamics': {
                'cycle_regularity': cycle_regularity,
                'rem_entries': rem_entries,
                'nrem_entries': nrem_entries,
                'sleep_drive_decay': sleep_drive_decay,
                'num_cycles': num_cycles
            },
            'theoretical_predictions': theoretical_predictions
        }
        
        # Visualization
        self._plot_sleep_architecture_analysis(results)
        
        return results
    
    def experiment_3_consciousness_state_transitions(self) -> Dict[str, Any]:
        """
        Experiment 3: Consciousness State Transitions
        
        Validates oscillatory mechanisms of consciousness:
        - Wake-sleep transitions
        - Consciousness levels
        - Attention and awareness oscillations
        - Dream state generation
        """
        print("🧠 Experiment 3: Consciousness State Transitions")
        
        # Simulation parameters
        duration = 12 * 3600  # 12 hours (evening to morning)
        fs = 0.1  # 0.1 Hz sampling (10 second intervals)
        t = np.linspace(0, duration, int(duration * fs))
        
        # Consciousness state model
        def consciousness_system(state, t):
            """
            Multi-level consciousness model:
            - Arousal/vigilance levels
            - Attention networks
            - Awareness integration
            - Dream content generation
            """
            (arousal_level, attention_focus, awareness_integration, 
             default_mode_activity, dream_content, adenosine_level) = state
            
            # Time of day effects
            hours_elapsed = t / 3600
            circadian_sleepiness = 0.5 + 0.4 * np.sin(2 * np.pi * (hours_elapsed + 6) / 24)
            
            # Adenosine accumulation (sleep pressure)
            if arousal_level > 0.5:  # Awake
                adenosine_buildup_rate = 0.1 / 3600  # Build up when awake
            else:  # Asleep
                adenosine_buildup_rate = -0.2 / 3600  # Clear during sleep
            
            adenosine_level_dot = adenosine_buildup_rate
            
            # Arousal system (affected by circadian rhythm and sleep pressure)
            wake_drive = 1.0 - circadian_sleepiness - adenosine_level
            sleep_drive = circadian_sleepiness + adenosine_level
            
            target_arousal = 1.0 if wake_drive > sleep_drive else 0.2
            arousal_level_dot = 0.5 * (target_arousal - arousal_level)
            
            # Attention networks (active when aroused)
            if arousal_level > 0.7:  # Alert wake
                attention_target = 0.8 + 0.2 * np.sin(0.1 * 2 * np.pi * t)  # Oscillating attention
            elif arousal_level > 0.5:  # Drowsy
                attention_target = 0.4
            else:  # Sleep states
                attention_target = 0.1
            
            attention_focus_dot = 1.0 * (attention_target - attention_focus)
            
            # Awareness integration (global workspace)
            # High during wake, fragmented during sleep
            if arousal_level > 0.6:
                integration_target = arousal_level * attention_focus
            else:  # Sleep - fragmented consciousness
                integration_target = 0.1 + 0.2 * np.random.random()  # Random fragments
            
            awareness_integration_dot = 0.8 * (integration_target - awareness_integration)
            
            # Default Mode Network (DMN) - active during rest/dreams
            if arousal_level > 0.7:  # Focused wake state
                dmn_target = 0.3  # Suppressed during focused attention
            elif arousal_level > 0.4:  # Relaxed/drowsy
                dmn_target = 0.7  # Active during rest
            else:  # Sleep/dreams
                dmn_target = 0.8 + 0.2 * np.sin(0.05 * 2 * np.pi * t)  # High during dreams
            
            default_mode_activity_dot = 0.6 * (dmn_target - default_mode_activity)
            
            # Dream content generation (high DMN + low awareness integration)
            if arousal_level < 0.5 and default_mode_activity > 0.6:
                # REM-like state - vivid dreams
                dream_intensity = default_mode_activity * (1 - awareness_integration)
                dream_content_target = dream_intensity
            else:
                dream_content_target = 0.1  # Minimal dream activity
            
            dream_content_dot = 0.4 * (dream_content_target - dream_content)
            
            return [arousal_level_dot, attention_focus_dot, awareness_integration_dot,
                   default_mode_activity_dot, dream_content_dot, adenosine_level_dot]
        
        # Initial conditions (evening - starting to get sleepy)
        initial_state = [
            0.7,  # Arousal level (somewhat alert)
            0.6,  # Attention focus
            0.5,  # Awareness integration
            0.4,  # Default mode activity
            0.1,  # Dream content
            0.3   # Adenosine level (some sleep pressure)
        ]
        
        # Solve consciousness system
        solution = odeint(consciousness_system, initial_state, t)
        arousal_trace = solution[:, 0]
        attention_trace = solution[:, 1]
        awareness_trace = solution[:, 2]
        dmn_trace = solution[:, 3]
        dream_trace = solution[:, 4]
        adenosine_trace = solution[:, 5]
        
        # Derive consciousness states
        consciousness_level = arousal_trace * awareness_trace  # Composite measure
        
        # State classification
        consciousness_states = np.zeros_like(consciousness_level)
        for i, (arousal, awareness) in enumerate(zip(arousal_trace, awareness_trace)):
            if arousal > 0.7 and awareness > 0.6:
                consciousness_states[i] = 3  # Alert consciousness
            elif arousal > 0.5 and awareness > 0.4:
                consciousness_states[i] = 2  # Relaxed consciousness
            elif arousal > 0.3:
                consciousness_states[i] = 1  # Drowsy/hypnagogic
            else:
                consciousness_states[i] = 0  # Sleep/unconscious
        
        # State transition analysis
        state_transitions = np.diff(consciousness_states)
        wake_to_sleep_transitions = np.sum(state_transitions < -1)
        sleep_to_wake_transitions = np.sum(state_transitions > 1)
        
        # Consciousness oscillation analysis
        consciousness_signals = {
            'arousal': arousal_trace,
            'attention': attention_trace,
            'awareness': awareness_trace,
            'default_mode': dmn_trace,
            'consciousness_level': consciousness_level
        }
        
        # Cross-network coupling analysis
        # Attention-DMN anticorrelation (typical finding in neuroscience)
        attention_dmn_coupling = np.corrcoef(attention_trace, dmn_trace)[0, 1]
        
        # Arousal-awareness coupling (consciousness coherence)
        arousal_awareness_coupling = np.corrcoef(arousal_trace, awareness_trace)[0, 1]
        
        # Dream-DMN coupling (dreams emerge from DMN activity)
        dream_dmn_coupling = np.corrcoef(dream_trace, dmn_trace)[0, 1]
        
        # Attention variability (measure of sustained attention)
        attention_variability = np.std(attention_trace[consciousness_level > 0.5])
        
        # Sleep onset dynamics
        sleep_onset_indices = np.where(consciousness_level < 0.3)[0]
        if len(sleep_onset_indices) > 0:
            sleep_onset_time = t[sleep_onset_indices[0]] / 3600  # Hours from start
            
            # Sleep onset transition smoothness
            transition_window = slice(max(0, sleep_onset_indices[0] - 50), 
                                     min(len(consciousness_level), sleep_onset_indices[0] + 50))
            transition_smoothness = 1.0 / (1.0 + np.std(consciousness_level[transition_window]))
        else:
            sleep_onset_time = None
            transition_smoothness = 0
        
        # Dream periods identification
        dream_periods = []
        in_dream = False
        dream_start = None
        
        for i, dream_level in enumerate(dream_trace):
            if dream_level > 0.5 and not in_dream:  # Dream start
                in_dream = True
                dream_start = t[i] / 3600
            elif dream_level <= 0.5 and in_dream:  # Dream end
                in_dream = False
                if dream_start is not None:
                    dream_periods.append({
                        'start': dream_start,
                        'end': t[i] / 3600,
                        'duration': (t[i] / 3600) - dream_start
                    })
        
        # Consciousness integration metrics
        # Global workspace integration (awareness during different arousal states)
        high_arousal_awareness = np.mean(awareness_trace[arousal_trace > 0.7])
        low_arousal_awareness = np.mean(awareness_trace[arousal_trace < 0.3])
        consciousness_integration_ratio = high_arousal_awareness / (low_arousal_awareness + 0.1)
        
        # Theoretical predictions
        theoretical_predictions = {
            'attention_dmn_anticorrelation_max': -0.3,    # Negative correlation expected
            'arousal_awareness_coupling_min': 0.6,        # Should be positively correlated
            'dream_dmn_coupling_min': 0.5,                # Dreams linked to DMN
            'consciousness_integration_ratio_min': 3.0,    # Much higher when awake
            'wake_sleep_transitions_min': 1,              # At least one sleep episode
            'transition_smoothness_min': 0.7,             # Smooth transitions
            'dream_periods_min': 1,                       # At least one dream period
            'attention_variability_max': 0.2               # Stable attention when awake
        }
        
        # Validation
        num_dream_periods = len(dream_periods)
        
        validation_success = (
            attention_dmn_coupling <= theoretical_predictions['attention_dmn_anticorrelation_max'] and
            arousal_awareness_coupling >= theoretical_predictions['arousal_awareness_coupling_min'] and
            dream_dmn_coupling >= theoretical_predictions['dream_dmn_coupling_min'] and
            consciousness_integration_ratio >= theoretical_predictions['consciousness_integration_ratio_min'] and
            wake_to_sleep_transitions >= theoretical_predictions['wake_sleep_transitions_min'] and
            transition_smoothness >= theoretical_predictions['transition_smoothness_min'] and
            num_dream_periods >= theoretical_predictions['dream_periods_min'] and
            attention_variability <= theoretical_predictions['attention_variability_max']
        )
        
        results = {
            'experiment': 'Consciousness State Transitions',
            'validation_success': validation_success,
            'consciousness_traces': {
                'time_hours': t / 3600,
                'arousal_level': arousal_trace,
                'attention_focus': attention_trace,
                'awareness_integration': awareness_trace,
                'default_mode_activity': dmn_trace,
                'dream_content': dream_trace,
                'adenosine_level': adenosine_trace,
                'consciousness_level': consciousness_level,
                'consciousness_states': consciousness_states
            },
            'state_dynamics': {
                'wake_to_sleep_transitions': wake_to_sleep_transitions,
                'sleep_to_wake_transitions': sleep_to_wake_transitions,
                'sleep_onset_time': sleep_onset_time,
                'transition_smoothness': transition_smoothness
            },
            'network_coupling': {
                'attention_dmn_coupling': attention_dmn_coupling,
                'arousal_awareness_coupling': arousal_awareness_coupling,
                'dream_dmn_coupling': dream_dmn_coupling
            },
            'consciousness_metrics': {
                'high_arousal_awareness': high_arousal_awareness,
                'low_arousal_awareness': low_arousal_awareness,
                'consciousness_integration_ratio': consciousness_integration_ratio,
                'attention_variability': attention_variability
            },
            'dream_analysis': {
                'dream_periods': dream_periods,
                'num_dream_periods': num_dream_periods
            },
            'theoretical_predictions': theoretical_predictions
        }
        
        # Visualization
        self._plot_consciousness_analysis(results)
        
        return results
    
    def _plot_circadian_analysis(self, results: Dict[str, Any]):
        """Create circadian rhythm analysis visualizations"""
        fig, axes = plt.subplots(3, 3, figsize=(20, 16))
        
        traces = results['circadian_traces']
        coupling = results['coupling_analysis']
        periods = results['period_analysis']
        rhythms = results['rhythm_metrics']
        
        # Plot 1: Master and peripheral clocks
        axes[0, 0].plot(traces['time_hours'], traces['scn_oscillation'], 'red', 
                       label='SCN Master Clock', linewidth=2)
        axes[0, 0].plot(traces['time_hours'], traces['liver_oscillation'], 'blue', 
                       label='Liver Clock', linewidth=2)
        axes[0, 0].plot(traces['time_hours'], traces['muscle_oscillation'], 'green', 
                       label='Muscle Clock', linewidth=2)
        
        axes[0, 0].set_title('Circadian Oscillator Network')
        axes[0, 0].set_xlabel('Time (hours)')
        axes[0, 0].set_ylabel('Oscillation Amplitude')
        axes[0, 0].legend()
        axes[0, 0].grid(True, alpha=0.3)
        
        # Plot 2: Hormone rhythms
        ax1 = axes[0, 1]
        ax2 = ax1.twinx()
        
        line1 = ax1.plot(traces['time_hours'], traces['melatonin'], 'purple', 
                        linewidth=2, label='Melatonin')
        line2 = ax2.plot(traces['time_hours'], traces['cortisol'], 'orange', 
                        linewidth=2, label='Cortisol')
        
        ax1.set_xlabel('Time (hours)')
        ax1.set_ylabel('Melatonin (pg/mL)', color='purple')
        ax2.set_ylabel('Cortisol (μg/dL)', color='orange')
        ax1.tick_params(axis='y', labelcolor='purple')
        ax2.tick_params(axis='y', labelcolor='orange')
        
        lines = line1 + line2
        labels = [l.get_label() for l in lines]
        ax1.legend(lines, labels, loc='upper right')
        ax1.set_title('Circadian Hormone Rhythms')
        ax1.grid(True, alpha=0.3)
        
        # Plot 3: Temperature and light
        ax1 = axes[0, 2]
        ax2 = ax1.twinx()
        
        line1 = ax1.plot(traces['time_hours'], traces['core_temperature'], 'red', 
                        linewidth=2, label='Core Temperature')
        line2 = ax2.plot(traces['time_hours'], traces['light_exposure'] / 100, 'yellow', 
                        linewidth=2, label='Light Exposure (×100)')
        
        ax1.set_xlabel('Time (hours)')
        ax1.set_ylabel('Temperature (°C)', color='red')
        ax2.set_ylabel('Light Exposure (Lux×100)', color='gold')
        ax1.tick_params(axis='y', labelcolor='red')
        ax2.tick_params(axis='y', labelcolor='gold')
        
        lines = line1 + line2
        labels = [l.get_label() for l in lines]
        ax1.legend(lines, labels, loc='upper right')
        ax1.set_title('Temperature Rhythm & Light Exposure')
        ax1.grid(True, alpha=0.3)
        
        # Plot 4: Period analysis
        period_names = ['SCN Period', 'Melatonin Period', 'Cortisol Period']
        period_values = [periods['scn_period_hours'], periods['melatonin_period_hours'], 
                        periods['cortisol_period_hours']]
        
        bars = axes[1, 0].bar(period_names, period_values, 
                             color=['red', 'purple', 'orange'], alpha=0.7)
        axes[1, 0].axhline(y=24, color='black', linestyle='--', 
                          alpha=0.8, label='24h Reference')
        axes[1, 0].set_title('Circadian Periods')
        axes[1, 0].set_ylabel('Period (hours)')
        axes[1, 0].legend()
        axes[1, 0].tick_params(axis='x', rotation=45)
        
        for bar, value in zip(bars, period_values):
            height = bar.get_height()
            axes[1, 0].text(bar.get_x() + bar.get_width()/2., height + 0.5,
                           f'{value:.1f}h', ha='center', va='bottom')
        
        # Plot 5: Coupling relationships
        coupling_names = ['SCN-Liver', 'SCN-Muscle', 'Temp-SCN', 'Light-Melatonin']
        coupling_values = [coupling['scn_liver_coupling'], coupling['scn_muscle_coupling'],
                          coupling['temp_scn_coupling'], coupling['light_melatonin_coupling']]
        
        colors = ['blue', 'green', 'red', 'purple']
        bars = axes[1, 1].bar(coupling_names, coupling_values, color=colors, alpha=0.7)
        axes[1, 1].set_title('Circadian Network Coupling')
        axes[1, 1].set_ylabel('Coupling Strength')
        axes[1, 1].set_ylim(-1, 1)
        axes[1, 1].axhline(y=0, color='black', linestyle='--', alpha=0.5)
        axes[1, 1].tick_params(axis='x', rotation=45)
        
        for bar, value in zip(bars, coupling_values):
            height = bar.get_height()
            axes[1, 1].text(bar.get_x() + bar.get_width()/2., 
                           height + 0.05 if height >= 0 else height - 0.1,
                           f'{value:.3f}', ha='center', va='bottom' if height >= 0 else 'top')
        
        # Plot 6: Hormone peak timing
        if rhythms['melatonin_peak_times'] and rhythms['cortisol_peak_times']:
            mel_times = np.array(rhythms['melatonin_peak_times']) % 24
            cort_times = np.array(rhythms['cortisol_peak_times']) % 24
            
            axes[1, 2].scatter(mel_times, [1]*len(mel_times), 
                              color='purple', s=100, alpha=0.7, label='Melatonin Peaks')
            axes[1, 2].scatter(cort_times, [2]*len(cort_times), 
                              color='orange', s=100, alpha=0.7, label='Cortisol Peaks')
            
            axes[1, 2].set_title('Hormone Peak Timing')
            axes[1, 2].set_xlabel('Time of Day (hours)')
            axes[1, 2].set_yticks([1, 2])
            axes[1, 2].set_yticklabels(['Melatonin', 'Cortisol'])
            axes[1, 2].set_xlim(0, 24)
            axes[1, 2].grid(True, alpha=0.3)
            axes[1, 2].legend()
        
        # Plot 7: Daily rhythm profiles (average day)
        day_hours = np.linspace(0, 24, 25)
        
        # Average melatonin and cortisol over 24h
        mel_daily = []
        cort_daily = []
        temp_daily = []
        
        for hour in day_hours:
            hour_indices = np.where(np.abs(traces['time_hours'] % 24 - hour) < 0.5)[0]
            if len(hour_indices) > 0:
                mel_daily.append(np.mean(traces['melatonin'][hour_indices]))
                cort_daily.append(np.mean(traces['cortisol'][hour_indices]))
                temp_daily.append(np.mean(traces['core_temperature'][hour_indices]))
            else:
                mel_daily.append(0)
                cort_daily.append(0)
                temp_daily.append(36.8)
        
        ax1 = axes[2, 0]
        ax2 = ax1.twinx()
        ax3 = ax1.twinx()
        ax3.spines['right'].set_position(('outward', 60))
        
        line1 = ax1.plot(day_hours, mel_daily, 'purple', linewidth=2, label='Melatonin')
        line2 = ax2.plot(day_hours, cort_daily, 'orange', linewidth=2, label='Cortisol')  
        line3 = ax3.plot(day_hours, temp_daily, 'red', linewidth=2, label='Temperature')
        
        ax1.set_xlabel('Hour of Day')
        ax1.set_ylabel('Melatonin (pg/mL)', color='purple')
        ax2.set_ylabel('Cortisol (μg/dL)', color='orange')
        ax3.set_ylabel('Temperature (°C)', color='red')
        
        ax1.tick_params(axis='y', labelcolor='purple')
        ax2.tick_params(axis='y', labelcolor='orange')
        ax3.tick_params(axis='y', labelcolor='red')
        
        ax1.set_title('Average Daily Profiles')
        ax1.grid(True, alpha=0.3)
        
        # Plot 8: Entrainment quality
        metrics_names = ['Entrainment Quality', 'Mel-Cort Phase Diff']
        metrics_values = [rhythms['entrainment_quality'], 
                         rhythms['melatonin_cortisol_phase_diff']]
        
        bars = axes[2, 1].bar(metrics_names, metrics_values, 
                             color=['green', 'blue'], alpha=0.7)
        axes[2, 1].set_title('Circadian Rhythm Metrics')
        axes[2, 1].set_ylabel('Value')
        axes[2, 1].tick_params(axis='x', rotation=45)
        
        for bar, value in zip(bars, metrics_values):
            height = bar.get_height()
            axes[2, 1].text(bar.get_x() + bar.get_width()/2., height + height*0.02,
                           f'{value:.2f}', ha='center', va='bottom')
        
        # Plot 9: Validation summary
        predictions = results['theoretical_predictions']
        
        validation_text = (
            f"🕐 CIRCADIAN VALIDATION\n\n"
            f"✓ Status: {'PASS' if results['validation_success'] else 'FAIL'}\n\n"
            f"SCN Period: {periods['scn_period_hours']:.1f}h\n"
            f"Expected: {predictions['expected_period_range']}\n\n"
            f"SCN-Liver Coupling: {coupling['scn_liver_coupling']:.3f}\n"
            f"Required: ≥{predictions['scn_peripheral_coupling_min']}\n\n"
            f"Mel-Cort Phase Diff: {rhythms['melatonin_cortisol_phase_diff']:.1f}h\n"
            f"Expected: {predictions['melatonin_cortisol_phase_diff_range']}\n\n"
            f"Entrainment Quality: {rhythms['entrainment_quality']:.3f}\n"
            f"Required: ≥{predictions['entrainment_quality_min']}"
        )
        
        axes[2, 2].text(0.05, 0.95, validation_text, transform=axes[2, 2].transAxes,
                       verticalalignment='top', fontsize=10,
                       bbox=dict(boxstyle='round', 
                               facecolor='lightgreen' if results['validation_success'] else 'lightcoral', 
                               alpha=0.8))
        axes[2, 2].set_xlim(0, 1)
        axes[2, 2].set_ylim(0, 1)
        axes[2, 2].axis('off')
        axes[2, 2].set_title('Validation Results')
        
        plt.tight_layout()
        plt.savefig(f"{self.results_dir}/circadian_rhythm_analysis.png", 
                   dpi=300, bbox_inches='tight')
        plt.close()
    
    def _plot_sleep_architecture_analysis(self, results: Dict[str, Any]):
        """Create sleep architecture analysis visualizations"""
        fig, axes = plt.subplots(3, 3, figsize=(20, 16))
        
        traces = results['sleep_traces']
        freqs = results['frequency_amplitudes']
        architecture = results['sleep_architecture']
        eeg = results['eeg_analysis']
        dynamics = results['sleep_dynamics']
        
        # Plot 1: Sleep stage hypnogram
        axes[0, 0].plot(traces['time_hours'], traces['sleep_stage'], 'black', linewidth=2)
        axes[0, 0].fill_between(traces['time_hours'], traces['sleep_stage'], 
                               alpha=0.6, color='lightblue')
        axes[0, 0].set_title('Sleep Stage Hypnogram')
        axes[0, 0].set_xlabel('Time (hours)')
        axes[0, 0].set_ylabel('Sleep Stage')
        axes[0, 0].set_yticks([-1, 0, 1, 2, 3])
        axes[0, 0].set_yticklabels(['REM', 'Wake', 'N1', 'N2', 'N3'])
        axes[0, 0].grid(True, alpha=0.3)
        
        # Plot 2: Sleep drives
        ax1 = axes[0, 1]
        ax2 = ax1.twinx()
        
        line1 = ax1.plot(traces['time_hours'], traces['rem_pressure'], 'red', 
                        linewidth=2, label='REM Pressure')
        line2 = ax2.plot(traces['time_hours'], traces['homeostatic_drive'], 'blue', 
                        linewidth=2, label='Homeostatic Drive')
        
        ax1.set_xlabel('Time (hours)')
        ax1.set_ylabel('REM Pressure', color='red')
        ax2.set_ylabel('Homeostatic Drive', color='blue')
        ax1.tick_params(axis='y', labelcolor='red')
        ax2.tick_params(axis='y', labelcolor='blue')
        
        lines = line1 + line2
        labels = [l.get_label() for l in lines]
        ax1.legend(lines, labels, loc='upper right')
        ax1.set_title('Sleep Drive Dynamics')
        ax1.grid(True, alpha=0.3)
        
        # Plot 3: EEG frequency amplitudes
        axes[0, 2].plot(traces['time_hours'], freqs['delta'], 'purple', 
                       label='Delta', linewidth=2)
        axes[0, 2].plot(traces['time_hours'], freqs['theta'], 'green', 
                       label='Theta', linewidth=2)
        axes[0, 2].plot(traces['time_hours'], freqs['alpha'], 'blue', 
                       label='Alpha', linewidth=2)
        axes[0, 2].plot(traces['time_hours'], freqs['sigma'], 'red', 
                       label='Sigma/Spindles', linewidth=2)
        
        axes[0, 2].set_title('EEG Frequency Band Amplitudes')
        axes[0, 2].set_xlabel('Time (hours)')
        axes[0, 2].set_ylabel('Amplitude (μV)')
        axes[0, 2].legend()
        axes[0, 2].grid(True, alpha=0.3)
        
        # Plot 4: Sleep architecture summary
        stage_names = ['Wake', 'N1', 'N2', 'N3', 'REM']
        stage_durations = [architecture['wake_time'], architecture['n1_time'], 
                          architecture['n2_time'], architecture['n3_time'], 
                          architecture['rem_time']]
        
        colors = ['yellow', 'lightgreen', 'green', 'darkgreen', 'red']
        bars = axes[1, 0].bar(stage_names, stage_durations, color=colors, alpha=0.7)
        axes[1, 0].set_title('Sleep Stage Durations')
        axes[1, 0].set_ylabel('Duration (minutes)')
        
        for bar, duration in zip(bars, stage_durations):
            height = bar.get_height()
            axes[1, 0].text(bar.get_x() + bar.get_width()/2., height + 5,
                           f'{duration:.0f}min', ha='center', va='bottom')
        
        # Plot 5: EEG power spectrum
        axes[1, 1].semilogy(eeg['frequencies'], eeg['power_spectral_density'], 
                           'black', linewidth=2)
        
        # Highlight frequency bands
        band_colors = {'delta': 'purple', 'theta': 'green', 'alpha': 'blue', 
                      'sigma': 'red', 'beta': 'orange'}
        
        frequency_bands = {
            'delta': (0.5, 4),
            'theta': (4, 8),
            'alpha': (8, 12), 
            'sigma': (11, 15),
            'beta': (15, 30)
        }
        
        for band_name, (f_min, f_max) in frequency_bands.items():
            if f_max <= max(eeg['frequencies']):
                band_mask = ((eeg['frequencies'] >= f_min) & 
                           (eeg['frequencies'] <= f_max))
                axes[1, 1].fill_between(eeg['frequencies'][band_mask],
                                       eeg['power_spectral_density'][band_mask],
                                       alpha=0.3, color=band_colors.get(band_name, 'gray'),
                                       label=band_name.title())
        
        axes[1, 1].set_title('Sleep EEG Power Spectrum')
        axes[1, 1].set_xlabel('Frequency (Hz)')
        axes[1, 1].set_ylabel('Power Spectral Density')
        axes[1, 1].legend()
        axes[1, 1].set_xlim(0, 30)
        
        # Plot 6: Sleep cycles
        if architecture['sleep_cycles']:
            cycle_starts = [cycle['start_time'] for cycle in architecture['sleep_cycles']]
            cycle_durations = [cycle['duration'] for cycle in architecture['sleep_cycles']]
            
            bars = axes[1, 2].bar(range(len(cycle_durations)), cycle_durations, 
                                 color='lightblue', alpha=0.7)
            axes[1, 2].set_title(f'Sleep Cycles (n={len(cycle_durations)})')
            axes[1, 2].set_xlabel('Cycle Number')
            axes[1, 2].set_ylabel('Duration (minutes)')
            axes[1, 2].axhline(y=90, color='red', linestyle='--', 
                              alpha=0.8, label='Typical 90min')
            axes[1, 2].legend()
            
            for i, (bar, duration) in enumerate(zip(bars, cycle_durations)):
                height = bar.get_height()
                axes[1, 2].text(bar.get_x() + bar.get_width()/2., height + 2,
                               f'{duration:.0f}', ha='center', va='bottom')
        
        # Plot 7: Sleep efficiency and percentages
        metrics_names = ['Sleep Efficiency (%)', 'REM (%)', 'Deep Sleep (%)', 'Cycle Regularity']
        metrics_values = [architecture['sleep_efficiency'], architecture['rem_percentage'],
                         architecture['deep_sleep_percentage'], dynamics['cycle_regularity']]
        
        bars = axes[2, 0].bar(metrics_names, metrics_values, 
                             color=['blue', 'red', 'darkgreen', 'purple'], alpha=0.7)
        axes[2, 0].set_title('Sleep Quality Metrics')
        axes[2, 0].set_ylabel('Value (%/Ratio)')
        axes[2, 0].tick_params(axis='x', rotation=45)
        
        for bar, value in zip(bars, metrics_values):
            height = bar.get_height()
            axes[2, 0].text(bar.get_x() + bar.get_width()/2., height + height*0.02,
                           f'{value:.1f}', ha='center', va='bottom')
        
        # Plot 8: EEG band powers
        band_names = list(eeg['band_powers'].keys())
        band_values = list(eeg['band_powers'].values())
        colors = [band_colors.get(name, 'gray') for name in band_names]
        
        bars = axes[2, 1].bar(band_names, band_values, color=colors, alpha=0.7)
        axes[2, 1].set_title('EEG Frequency Band Powers')
        axes[2, 1].set_ylabel('Power (%)')
        
        for bar, value in zip(bars, band_values):
            height = bar.get_height()
            axes[2, 1].text(bar.get_x() + bar.get_width()/2., height + 1,
                           f'{value:.1f}%', ha='center', va='bottom')
        
        # Plot 9: Validation summary
        predictions = results['theoretical_predictions']
        
        validation_text = (
            f"💤 SLEEP ARCHITECTURE VALIDATION\n\n"
            f"✓ Status: {'PASS' if results['validation_success'] else 'FAIL'}\n\n"
            f"Sleep Cycles: {dynamics['num_cycles']}\n"
            f"Expected: {predictions['expected_sleep_cycles']}\n\n"
            f"REM %: {architecture['rem_percentage']:.1f}%\n"
            f"Expected: {predictions['expected_rem_percentage']}\n\n"
            f"Sleep Efficiency: {architecture['sleep_efficiency']:.1f}%\n"
            f"Required: ≥{predictions['expected_sleep_efficiency'][0]}%\n\n"
            f"Delta Power: {eeg['band_powers']['delta']:.1f}%\n"
            f"Required: ≥{predictions['delta_power_dominance_min']}%"
        )
        
        axes[2, 2].text(0.05, 0.95, validation_text, transform=axes[2, 2].transAxes,
                       verticalalignment='top', fontsize=10,
                       bbox=dict(boxstyle='round', 
                               facecolor='lightgreen' if results['validation_success'] else 'lightcoral', 
                               alpha=0.8))
        axes[2, 2].set_xlim(0, 1)
        axes[2, 2].set_ylim(0, 1)
        axes[2, 2].axis('off')
        axes[2, 2].set_title('Validation Results')
        
        plt.tight_layout()
        plt.savefig(f"{self.results_dir}/sleep_architecture_analysis.png", 
                   dpi=300, bbox_inches='tight')
        plt.close()
    
    def _plot_consciousness_analysis(self, results: Dict[str, Any]):
        """Create consciousness state analysis visualizations"""
        fig, axes = plt.subplots(3, 3, figsize=(20, 16))
        
        traces = results['consciousness_traces']
        coupling = results['network_coupling']
        metrics = results['consciousness_metrics']
        dreams = results['dream_analysis']
        dynamics = results['state_dynamics']
        
        # Plot 1: Consciousness components
        axes[0, 0].plot(traces['time_hours'], traces['arousal_level'], 'red', 
                       label='Arousal', linewidth=2)
        axes[0, 0].plot(traces['time_hours'], traces['attention_focus'], 'blue', 
                       label='Attention', linewidth=2)
        axes[0, 0].plot(traces['time_hours'], traces['awareness_integration'], 'green', 
                       label='Awareness', linewidth=2)
        axes[0, 0].plot(traces['time_hours'], traces['consciousness_level'], 'black', 
                       label='Consciousness Level', linewidth=3, alpha=0.8)
        
        axes[0, 0].set_title('Consciousness System Components')
        axes[0, 0].set_xlabel('Time (hours)')
        axes[0, 0].set_ylabel('Activity Level')
        axes[0, 0].legend()
        axes[0, 0].grid(True, alpha=0.3)
        
        # Plot 2: Network activity patterns
        ax1 = axes[0, 1]
        ax2 = ax1.twinx()
        
        line1 = ax1.plot(traces['time_hours'], traces['default_mode_activity'], 'purple', 
                        linewidth=2, label='Default Mode Network')
        line2 = ax2.plot(traces['time_hours'], traces['dream_content'], 'orange', 
                        linewidth=2, label='Dream Content')
        
        ax1.set_xlabel('Time (hours)')
        ax1.set_ylabel('DMN Activity', color='purple')
        ax2.set_ylabel('Dream Content', color='orange')
        ax1.tick_params(axis='y', labelcolor='purple')
        ax2.tick_params(axis='y', labelcolor='orange')
        
        lines = line1 + line2
        labels = [l.get_label() for l in lines]
        ax1.legend(lines, labels, loc='upper right')
        ax1.set_title('Network Activity & Dreams')
        ax1.grid(True, alpha=0.3)
        
        # Plot 3: Consciousness states
        state_colors = ['black', 'red', 'orange', 'green']  # Sleep, drowsy, relaxed, alert
        state_names = ['Sleep/Unconscious', 'Drowsy/Hypnagogic', 'Relaxed Conscious', 'Alert Conscious']
        
        unique_states = np.unique(traces['consciousness_states'])
        for state in unique_states:
            state_mask = traces['consciousness_states'] == state
            if np.any(state_mask):
                color_idx = int(state) if state < len(state_colors) else 0
                axes[0, 2].scatter(traces['time_hours'][state_mask], 
                                  traces['consciousness_states'][state_mask],
                                  c=state_colors[color_idx], s=10, alpha=0.6,
                                  label=state_names[color_idx] if color_idx < len(state_names) else 'Unknown')
        
        axes[0, 2].set_title('Consciousness State Timeline')
        axes[0, 2].set_xlabel('Time (hours)')
        axes[0, 2].set_ylabel('Consciousness State')
        axes[0, 2].set_yticks([0, 1, 2, 3])
        axes[0, 2].set_yticklabels(state_names)
        axes[0, 2].legend(bbox_to_anchor=(1.05, 1), loc='upper left')
        axes[0, 2].grid(True, alpha=0.3)
        
        # Plot 4: Network coupling relationships
        coupling_names = ['Attention-DMN', 'Arousal-Awareness', 'Dream-DMN']
        coupling_values = [coupling['attention_dmn_coupling'], 
                          coupling['arousal_awareness_coupling'],
                          coupling['dream_dmn_coupling']]
        
        colors = ['red', 'green', 'orange']
        bars = axes[1, 0].bar(coupling_names, coupling_values, color=colors, alpha=0.7)
        axes[1, 0].set_title('Network Coupling Analysis')
        axes[1, 0].set_ylabel('Coupling Strength')
        axes[1, 0].set_ylim(-1, 1)
        axes[1, 0].axhline(y=0, color='black', linestyle='--', alpha=0.5)
        axes[1, 0].tick_params(axis='x', rotation=45)
        
        for bar, value in zip(bars, coupling_values):
            height = bar.get_height()
            axes[1, 0].text(bar.get_x() + bar.get_width()/2., 
                           height + 0.05 if height >= 0 else height - 0.1,
                           f'{value:.3f}', ha='center', va='bottom' if height >= 0 else 'top')
        
        # Plot 5: Adenosine accumulation
        axes[1, 1].plot(traces['time_hours'], traces['adenosine_level'], 
                       'brown', linewidth=2)
        axes[1, 1].fill_between(traces['time_hours'], traces['adenosine_level'], 
                               alpha=0.3, color='brown')
        axes[1, 1].set_title('Sleep Pressure (Adenosine)')
        axes[1, 1].set_xlabel('Time (hours)')
        axes[1, 1].set_ylabel('Adenosine Level')
        axes[1, 1].grid(True, alpha=0.3)
        
        # Plot 6: Dream periods
        if dreams['dream_periods']:
            dream_starts = [period['start'] for period in dreams['dream_periods']]
            dream_durations = [period['duration'] for period in dreams['dream_periods']]
            
            bars = axes[1, 2].bar(range(len(dream_durations)), dream_durations, 
                                 color='orange', alpha=0.7)
            axes[1, 2].set_title(f'Dream Periods (n={len(dream_durations)})')
            axes[1, 2].set_xlabel('Dream Episode')
            axes[1, 2].set_ylabel('Duration (hours)')
            
            for i, (bar, duration) in enumerate(zip(bars, dream_durations)):
                height = bar.get_height()
                axes[1, 2].text(bar.get_x() + bar.get_width()/2., height + 0.02,
                               f'{duration:.2f}h', ha='center', va='bottom')
        else:
            axes[1, 2].text(0.5, 0.5, 'No Dream Periods Detected', 
                           transform=axes[1, 2].transAxes, ha='center', va='center')
            axes[1, 2].set_title('Dream Analysis')
        
        # Plot 7: Consciousness integration
        integration_names = ['High Arousal\nAwareness', 'Low Arousal\nAwareness', 'Integration\nRatio']
        integration_values = [metrics['high_arousal_awareness'], 
                             metrics['low_arousal_awareness'],
                             metrics['consciousness_integration_ratio']]
        
        bars = axes[2, 0].bar(integration_names, integration_values, 
                             color=['green', 'red', 'blue'], alpha=0.7)
        axes[2, 0].set_title('Consciousness Integration Metrics')
        axes[2, 0].set_ylabel('Value')
        
        for bar, value in zip(bars, integration_values):
            height = bar.get_height()
            axes[2, 0].text(bar.get_x() + bar.get_width()/2., height + height*0.02,
                           f'{value:.2f}', ha='center', va='bottom')
        
        # Plot 8: State transition dynamics
        transition_names = ['Wake→Sleep\nTransitions', 'Sleep→Wake\nTransitions', 'Transition\nSmoothness']
        transition_values = [dynamics['wake_to_sleep_transitions'], 
                            dynamics['sleep_to_wake_transitions'],
                            dynamics['transition_smoothness']]
        
        bars = axes[2, 1].bar(transition_names, transition_values, 
                             color=['blue', 'yellow', 'green'], alpha=0.7)
        axes[2, 1].set_title('State Transition Dynamics')
        axes[2, 1].set_ylabel('Value')
        axes[2, 1].tick_params(axis='x', rotation=45)
        
        for bar, value in zip(bars, transition_values):
            height = bar.get_height()
            axes[2, 1].text(bar.get_x() + bar.get_width()/2., height + height*0.02,
                           f'{value:.2f}', ha='center', va='bottom')
        
        # Plot 9: Validation summary
        predictions = results['theoretical_predictions']
        
        validation_text = (
            f"🧠 CONSCIOUSNESS VALIDATION\n\n"
            f"✓ Status: {'PASS' if results['validation_success'] else 'FAIL'}\n\n"
            f"Attention-DMN: {coupling['attention_dmn_coupling']:.3f}\n"
            f"Expected: ≤{predictions['attention_dmn_anticorrelation_max']}\n\n"
            f"Integration Ratio: {metrics['consciousness_integration_ratio']:.2f}\n"
            f"Required: ≥{predictions['consciousness_integration_ratio_min']}\n\n"
            f"Dream Periods: {dreams['num_dream_periods']}\n"
            f"Required: ≥{predictions['dream_periods_min']}\n\n"
            f"Attention Variability: {metrics['attention_variability']:.3f}\n"
            f"Max Allowed: {predictions['attention_variability_max']}"
        )
        
        axes[2, 2].text(0.05, 0.95, validation_text, transform=axes[2, 2].transAxes,
                       verticalalignment='top', fontsize=10,
                       bbox=dict(boxstyle='round', 
                               facecolor='lightgreen' if results['validation_success'] else 'lightcoral', 
                               alpha=0.8))
        axes[2, 2].set_xlim(0, 1)
        axes[2, 2].set_ylim(0, 1)
        axes[2, 2].axis('off')
        axes[2, 2].set_title('Validation Results')
        
        plt.tight_layout()
        plt.savefig(f"{self.results_dir}/consciousness_transitions_analysis.png", 
                   dpi=300, bbox_inches='tight')
        plt.close()
    
    def run_all_experiments(self) -> Dict[str, Any]:
        """Run all sleep and circadian oscillatory validation experiments"""
        print("💤 Running Sleep and Circadian System Oscillatory Validation Suite")
        print("=" * 70)
        
        all_results = {}
        
        # Run experiments
        all_results['experiment_1'] = self.experiment_1_circadian_rhythm_oscillatory_coupling()
        all_results['experiment_2'] = self.experiment_2_sleep_architecture_validation()
        all_results['experiment_3'] = self.experiment_3_consciousness_state_transitions()
        
        # Compile validation summary
        validations = [result['validation_success'] for result in all_results.values()]
        overall_success = all(validations)
        
        summary = {
            'domain': 'Sleep and Circadian System Oscillations',
            'total_experiments': len(all_results),
            'successful_validations': sum(validations),
            'overall_validation_success': overall_success,
            'timestamp': datetime.now().isoformat(),
            'detailed_results': all_results
        }
        
        # Save comprehensive results
        results_file = f"{self.results_dir}/sleep_validation_summary.json"
        import json
        with open(results_file, 'w') as f:
            json.dump({k: v for k, v in summary.items() 
                      if k != 'detailed_results'}, f, indent=2)
        
        print(f"\n💤 Sleep & Circadian Validation Complete:")
        print(f"   ✓ Successful: {sum(validations)}/{len(validations)} experiments")
        print(f"   ✓ Overall Status: {'PASS' if overall_success else 'FAIL'}")
        print(f"   ✓ Results saved to: {self.results_dir}/")
        
        self.validation_results = summary
        return summary

def main():
    """Run sleep and circadian oscillatory validation as standalone"""
    validator = SleepOscillatoryValidator()
    return validator.run_all_experiments()

if __name__ == "__main__":
    results = main()
    print(f"Sleep validation completed: {results['overall_validation_success']}")
