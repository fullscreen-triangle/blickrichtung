"""
Neural System Oscillatory Dynamics Validator

This module validates the theoretical predictions about neural oscillations,
brain waves, cognitive processing, and neuromuscular control within the unified
biological oscillations framework.

Key Validations:
1. Brain Wave Oscillatory Coupling
2. Cognitive Processing Oscillations
3. Neuromuscular Control Integration
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

class NeuralOscillatoryValidator:
    """Validates oscillatory dynamics in neural systems"""
    
    def __init__(self, results_dir: str = "results/neural"):
        self.results_dir = results_dir
        os.makedirs(results_dir, exist_ok=True)
        
        # Neural oscillation parameters
        self.brain_wave_bands = {
            'delta': (0.5, 4.0),      # Deep sleep
            'theta': (4.0, 8.0),      # REM, meditation
            'alpha': (8.0, 13.0),     # Relaxed awareness
            'beta': (13.0, 30.0),     # Active thinking
            'gamma': (30.0, 100.0),   # Cognitive binding
            'high_gamma': (100.0, 200.0)  # Ultra-fast processing
        }
        
        # Neuron parameters
        self.neuron_params = {
            'c_m': 1.0,          # membrane capacitance (μF/cm²)
            'g_na': 120.0,       # sodium conductance (mS/cm²)
            'g_k': 36.0,         # potassium conductance (mS/cm²)
            'g_l': 0.3,          # leak conductance (mS/cm²)
            'e_na': 50.0,        # sodium reversal potential (mV)
            'e_k': -77.0,        # potassium reversal potential (mV)
            'e_l': -54.387       # leak reversal potential (mV)
        }
        
        # Cognitive processing parameters
        self.cognitive_params = {
            'attention_freq': 10.0,    # Hz - alpha rhythm
            'working_memory_freq': 25.0,  # Hz - beta rhythm
            'binding_freq': 40.0,      # Hz - gamma rhythm
            'consciousness_freq': 80.0  # Hz - high gamma
        }
        
        # Neuromuscular parameters
        self.motor_params = {
            'motor_unit_freq': 15.0,   # Hz - motor unit firing
            'tremor_freq': 8.0,        # Hz - physiological tremor
            'reflex_delay': 0.03,      # s - spinal reflex delay
            'cortical_delay': 0.15     # s - cortical motor delay
        }
        
        self.validation_results = {}
        
    def experiment_1_brain_wave_oscillatory_coupling(self) -> Dict[str, Any]:
        """
        Experiment 1: Brain Wave Oscillatory Coupling
        
        Validates coupling between different brain wave frequencies:
        - Delta-theta coupling in sleep
        - Alpha-beta coupling in cognition
        - Gamma coupling for binding
        - Cross-frequency phase-amplitude coupling
        """
        print("🧠 Experiment 1: Brain Wave Oscillatory Coupling")
        
        # Simulation parameters
        duration = 120  # 2 minutes
        fs = 500.0  # 500 Hz sampling
        t = np.linspace(0, duration, int(duration * fs))
        
        # Generate brain wave components with realistic coupling
        brain_signal = np.zeros_like(t)
        
        # 1. Delta waves (deep sleep base rhythm)
        delta_phase = 2 * np.pi * 2.0 * t
        delta_amplitude = 50  # μV
        delta_wave = delta_amplitude * np.sin(delta_phase)
        
        # 2. Theta waves (REM, memory consolidation)
        theta_phase = 2 * np.pi * 6.0 * t
        # Phase-amplitude coupling: theta amplitude modulated by delta phase
        theta_amplitude = 30 * (1 + 0.3 * np.cos(delta_phase))
        theta_wave = theta_amplitude * np.sin(theta_phase)
        
        # 3. Alpha waves (relaxed awareness)
        alpha_phase = 2 * np.pi * 10.0 * t
        # Alpha suppression during active cognition
        cognitive_load = 0.5 * (1 + np.sin(0.05 * 2 * np.pi * t))  # Slow modulation
        alpha_amplitude = 40 * (1 - 0.7 * cognitive_load)
        alpha_wave = alpha_amplitude * np.sin(alpha_phase)
        
        # 4. Beta waves (active thinking)
        beta_phase = 2 * np.pi * 20.0 * t
        # Beta increases with cognitive load
        beta_amplitude = 25 * (1 + 0.8 * cognitive_load)
        beta_wave = beta_amplitude * np.sin(beta_phase)
        
        # 5. Gamma waves (cognitive binding)
        gamma_phase = 2 * np.pi * 40.0 * t
        # Gamma phase-locked to theta rhythm (theta-gamma coupling)
        gamma_amplitude = 15 * (1 + 0.5 * np.cos(theta_phase))
        gamma_wave = gamma_amplitude * np.sin(gamma_phase)
        
        # 6. High gamma (consciousness, integration)
        high_gamma_phase = 2 * np.pi * 80.0 * t
        # High gamma modulated by alpha rhythm
        high_gamma_amplitude = 8 * (1 + 0.4 * np.cos(alpha_phase))
        high_gamma_wave = high_gamma_amplitude * np.sin(high_gamma_phase)
        
        # Combined EEG signal
        eeg_signal = (delta_wave + theta_wave + alpha_wave + 
                     beta_wave + gamma_wave + high_gamma_wave)
        
        # Add realistic noise
        noise_amplitude = 5  # μV
        eeg_signal += noise_amplitude * np.random.randn(len(t))
        
        # Frequency domain analysis
        freqs, psd = signal.welch(eeg_signal, fs=fs, nperseg=2048)
        
        # Extract power in each brain wave band
        band_powers = {}
        total_power = np.trapz(psd, freqs)
        
        for band_name, (f_min, f_max) in self.brain_wave_bands.items():
            band_mask = (freqs >= f_min) & (freqs <= f_max)
            if np.any(band_mask):
                band_power = np.trapz(psd[band_mask], freqs[band_mask])
                band_powers[band_name] = band_power / total_power * 100
            else:
                band_powers[band_name] = 0
        
        # Cross-frequency coupling analysis
        coupling_analysis = {}
        
        # Phase-amplitude coupling (PAC)
        def calculate_pac(low_freq_signal, high_freq_signal, n_bins=20):
            """Calculate phase-amplitude coupling"""
            from scipy.signal import hilbert
            
            # Get phase of low frequency
            low_analytic = hilbert(low_freq_signal)
            low_phase = np.angle(low_analytic)
            
            # Get amplitude of high frequency
            high_analytic = hilbert(high_freq_signal)
            high_amplitude = np.abs(high_analytic)
            
            # Bin phases and calculate mean amplitudes
            phase_bins = np.linspace(-np.pi, np.pi, n_bins + 1)
            mean_amplitudes = []
            
            for i in range(n_bins):
                phase_mask = ((low_phase >= phase_bins[i]) & 
                             (low_phase < phase_bins[i + 1]))
                if np.any(phase_mask):
                    mean_amplitudes.append(np.mean(high_amplitude[phase_mask]))
                else:
                    mean_amplitudes.append(0)
            
            # Calculate modulation index
            mean_amplitudes = np.array(mean_amplitudes)
            if np.sum(mean_amplitudes) > 0:
                p_amp = mean_amplitudes / np.sum(mean_amplitudes)
                # Kullback-Leibler divergence from uniform distribution
                uniform = np.ones(n_bins) / n_bins
                kl_div = np.sum(p_amp * np.log(p_amp / uniform + 1e-10))
                modulation_index = kl_div / np.log(n_bins)
            else:
                modulation_index = 0
                
            return modulation_index, mean_amplitudes
        
        # Extract individual frequency components
        frequency_components = {}
        for band_name, (f_min, f_max) in self.brain_wave_bands.items():
            if f_max <= fs/2:  # Nyquist limit
                nyquist = fs / 2
                low = f_min / nyquist
                high = min(f_max / nyquist, 0.99)
                if low < high:
                    b, a = signal.butter(4, [low, high], btype='band')
                    frequency_components[band_name] = signal.filtfilt(b, a, eeg_signal)
        
        # Calculate key coupling relationships
        # Theta-gamma coupling (memory formation)
        if 'theta' in frequency_components and 'gamma' in frequency_components:
            theta_gamma_pac, _ = calculate_pac(frequency_components['theta'], 
                                             frequency_components['gamma'])
            coupling_analysis['theta_gamma_pac'] = theta_gamma_pac
        
        # Alpha-beta coupling (cognitive control)
        if 'alpha' in frequency_components and 'beta' in frequency_components:
            alpha_beta_coupling = np.corrcoef(frequency_components['alpha'], 
                                            frequency_components['beta'])[0, 1]
            coupling_analysis['alpha_beta_coupling'] = alpha_beta_coupling
        
        # Delta-theta coupling (sleep states)
        if 'delta' in frequency_components and 'theta' in frequency_components:
            delta_theta_coupling = np.corrcoef(frequency_components['delta'], 
                                             frequency_components['theta'])[0, 1]
            coupling_analysis['delta_theta_coupling'] = delta_theta_coupling
        
        # Gamma coherence (binding)
        if 'gamma' in frequency_components and 'high_gamma' in frequency_components:
            gamma_coherence = np.corrcoef(frequency_components['gamma'],
                                        frequency_components['high_gamma'])[0, 1]
            coupling_analysis['gamma_coherence'] = gamma_coherence
        
        # Theoretical predictions for brain wave coupling
        theoretical_predictions = {
            'expected_alpha_dominance': (20, 40),  # % of total power
            'theta_gamma_pac_threshold': 0.1,
            'alpha_beta_anticorrelation': (-0.7, -0.2),
            'gamma_coherence_threshold': 0.3
        }
        
        # Validation checks
        alpha_dominance = band_powers.get('alpha', 0)
        theta_gamma_pac = coupling_analysis.get('theta_gamma_pac', 0)
        alpha_beta_coupling = coupling_analysis.get('alpha_beta_coupling', 0)
        gamma_coherence = coupling_analysis.get('gamma_coherence', 0)
        
        validation_success = (
            theoretical_predictions['expected_alpha_dominance'][0] <= alpha_dominance <= 
            theoretical_predictions['expected_alpha_dominance'][1] and
            theta_gamma_pac >= theoretical_predictions['theta_gamma_pac_threshold'] and
            theoretical_predictions['alpha_beta_anticorrelation'][0] <= alpha_beta_coupling <= 
            theoretical_predictions['alpha_beta_anticorrelation'][1] and
            gamma_coherence >= theoretical_predictions['gamma_coherence_threshold']
        )
        
        results = {
            'experiment': 'Brain Wave Oscillatory Coupling',
            'validation_success': validation_success,
            'band_powers': band_powers,
            'coupling_analysis': coupling_analysis,
            'signal_data': {
                'time': t,
                'eeg_signal': eeg_signal,
                'frequency_components': frequency_components
            },
            'frequency_analysis': {
                'frequencies': freqs,
                'power_spectral_density': psd
            },
            'theoretical_predictions': theoretical_predictions
        }
        
        # Visualization
        self._plot_brain_wave_analysis(results)
        
        return results
    
    def experiment_2_cognitive_processing_oscillations(self) -> Dict[str, Any]:
        """
        Experiment 2: Cognitive Processing Oscillations
        
        Validates oscillatory dynamics in cognitive processes:
        - Attention networks (alpha suppression)
        - Working memory (theta-gamma coupling)
        - Executive control (beta synchronization)
        - Consciousness binding (high gamma)
        """
        print("🎯 Experiment 2: Cognitive Processing Oscillations")
        
        # Simulation parameters
        duration = 180  # 3 minutes
        fs = 250.0  # 250 Hz sampling
        t = np.linspace(0, duration, int(duration * fs))
        
        # Cognitive task simulation
        def cognitive_task_model(state, t):
            """
            Multi-scale cognitive processing model:
            - Attention networks
            - Working memory
            - Executive control
            - Consciousness integration
            """
            attention_state, wm_state, executive_state, consciousness_state = state
            
            # Task demands (varying cognitive load)
            task_difficulty = 0.5 * (1 + np.sin(0.02 * 2 * np.pi * t))  # Slow variation
            attention_demand = task_difficulty + 0.3 * np.sin(0.1 * 2 * np.pi * t)
            
            # Attention network dynamics (alpha suppression)
            attention_baseline = 0.8
            attention_suppression = 0.4 * attention_demand
            attention_dot = -2 * (attention_state - (attention_baseline - attention_suppression))
            
            # Working memory dynamics (theta oscillations)
            wm_capacity = 7  # Miller's magic number
            wm_load = task_difficulty * wm_capacity
            theta_drive = 0.3 * np.sin(self.cognitive_params['working_memory_freq'] * 2 * np.pi * t)
            wm_dot = 0.5 * (wm_load - wm_state) + theta_drive
            
            # Executive control (beta synchronization)
            executive_demand = attention_demand * task_difficulty
            beta_oscillation = 0.2 * np.sin(self.cognitive_params['attention_freq'] * 2 * np.pi * t)
            executive_dot = 0.8 * (executive_demand - executive_state) + beta_oscillation
            
            # Consciousness integration (gamma binding)
            consciousness_input = (attention_state + wm_state + executive_state) / 3
            gamma_binding = 0.15 * np.sin(self.cognitive_params['binding_freq'] * 2 * np.pi * t)
            consciousness_dot = 1.2 * (consciousness_input - consciousness_state) + gamma_binding
            
            return [attention_dot, wm_dot, executive_dot, consciousness_dot]
        
        # Initial conditions
        initial_state = [0.8, 3.5, 0.5, 0.6]  # Baseline cognitive state
        
        # Solve cognitive dynamics
        solution = odeint(cognitive_task_model, initial_state, t)
        attention_trace = solution[:, 0]
        wm_trace = solution[:, 1]
        executive_trace = solution[:, 2]
        consciousness_trace = solution[:, 3]
        
        # Generate synthetic neural signals for each cognitive process
        # Attention: Alpha suppression with task modulation
        alpha_base = 40 * np.sin(self.cognitive_params['attention_freq'] * 2 * np.pi * t)
        attention_signal = alpha_base * attention_trace + 5 * np.random.randn(len(t))
        
        # Working memory: Theta-gamma coupling
        theta_carrier = 30 * np.sin(6.0 * 2 * np.pi * t)
        gamma_modulation = 15 * np.sin(self.cognitive_params['binding_freq'] * 2 * np.pi * t)
        wm_signal = theta_carrier * (1 + 0.4 * gamma_modulation / 15) * (wm_trace / 7) + 3 * np.random.randn(len(t))
        
        # Executive control: Beta synchronization
        beta_base = 25 * np.sin(self.cognitive_params['working_memory_freq'] * 2 * np.pi * t)
        executive_signal = beta_base * executive_trace + 4 * np.random.randn(len(t))
        
        # Consciousness: High gamma binding
        high_gamma_base = 12 * np.sin(self.cognitive_params['consciousness_freq'] * 2 * np.pi * t)
        consciousness_signal = high_gamma_base * consciousness_trace + 2 * np.random.randn(len(t))
        
        # Combined cognitive EEG signal
        cognitive_eeg = attention_signal + wm_signal + executive_signal + consciousness_signal
        
        # Cognitive performance metrics
        # Reaction time model (inversely related to processing efficiency)
        processing_efficiency = (attention_trace + executive_trace) / 2
        reaction_time = 300 + 200 * (1 - processing_efficiency)  # ms
        
        # Accuracy model (related to working memory and consciousness)
        cognitive_resources = (wm_trace / 7 + consciousness_trace) / 2
        accuracy = 0.5 + 0.45 * cognitive_resources  # 50-95% range
        
        # Oscillatory coupling analysis
        # Cross-frequency coupling between cognitive processes
        cognitive_signals = {
            'attention': attention_signal,
            'working_memory': wm_signal,
            'executive': executive_signal,
            'consciousness': consciousness_signal
        }
        
        # Calculate coupling matrix
        coupling_matrix = np.zeros((len(cognitive_signals), len(cognitive_signals)))
        signal_names = list(cognitive_signals.keys())
        
        for i, sig1_name in enumerate(signal_names):
            for j, sig2_name in enumerate(signal_names):
                sig1 = cognitive_signals[sig1_name]
                sig2 = cognitive_signals[sig2_name]
                
                # Calculate phase coupling
                from scipy.signal import hilbert
                analytic1 = hilbert(sig1 - np.mean(sig1))
                analytic2 = hilbert(sig2 - np.mean(sig2))
                
                phase1 = np.angle(analytic1)
                phase2 = np.angle(analytic2)
                
                phase_diff = phase1 - phase2
                coupling_strength = np.abs(np.mean(np.exp(1j * phase_diff)))
                coupling_matrix[i, j] = coupling_strength
        
        # Attention-executive coupling (cognitive control)
        attention_executive_coupling = coupling_matrix[0, 2]
        
        # Working memory-consciousness coupling (awareness)
        wm_consciousness_coupling = coupling_matrix[1, 3]
        
        # Overall cognitive coherence
        cognitive_coherence = np.mean(coupling_matrix[np.triu_indices(len(signal_names), k=1)])
        
        # Performance correlations with neural oscillations
        rt_neural_correlation = np.corrcoef(reaction_time, np.abs(attention_signal))[0, 1]
        accuracy_neural_correlation = np.corrcoef(accuracy, np.abs(consciousness_signal))[0, 1]
        
        # Theoretical predictions
        theoretical_predictions = {
            'attention_executive_coupling_min': 0.4,
            'wm_consciousness_coupling_min': 0.35,
            'cognitive_coherence_min': 0.3,
            'rt_neural_correlation_range': (-0.8, -0.2),  # Negative: better neural = faster RT
            'accuracy_neural_correlation_min': 0.3
        }
        
        # Validation
        validation_success = (
            attention_executive_coupling >= theoretical_predictions['attention_executive_coupling_min'] and
            wm_consciousness_coupling >= theoretical_predictions['wm_consciousness_coupling_min'] and
            cognitive_coherence >= theoretical_predictions['cognitive_coherence_min'] and
            theoretical_predictions['rt_neural_correlation_range'][0] <= rt_neural_correlation <= 
            theoretical_predictions['rt_neural_correlation_range'][1] and
            accuracy_neural_correlation >= theoretical_predictions['accuracy_neural_correlation_min']
        )
        
        results = {
            'experiment': 'Cognitive Processing Oscillations',
            'validation_success': validation_success,
            'cognitive_traces': {
                'time': t,
                'attention_state': attention_trace,
                'working_memory_state': wm_trace,
                'executive_state': executive_trace,
                'consciousness_state': consciousness_trace
            },
            'neural_signals': cognitive_signals,
            'performance_metrics': {
                'reaction_time': reaction_time,
                'accuracy': accuracy,
                'processing_efficiency': processing_efficiency,
                'cognitive_resources': cognitive_resources
            },
            'coupling_analysis': {
                'coupling_matrix': coupling_matrix,
                'signal_names': signal_names,
                'attention_executive_coupling': attention_executive_coupling,
                'wm_consciousness_coupling': wm_consciousness_coupling,
                'cognitive_coherence': cognitive_coherence
            },
            'performance_correlations': {
                'rt_neural_correlation': rt_neural_correlation,
                'accuracy_neural_correlation': accuracy_neural_correlation
            },
            'theoretical_predictions': theoretical_predictions
        }
        
        # Visualization
        self._plot_cognitive_analysis(results)
        
        return results
    
    def experiment_3_neuromuscular_control_integration(self) -> Dict[str, Any]:
        """
        Experiment 3: Neuromuscular Control Integration
        
        Validates oscillatory coupling in motor control:
        - Motor cortex oscillations
        - Spinal motor neuron pools
        - Muscle fiber recruitment
        - Sensorimotor feedback loops
        """
        print("💪 Experiment 3: Neuromuscular Control Integration")
        
        # Simulation parameters
        duration = 60  # 1 minute
        fs = 1000.0  # 1 kHz sampling
        t = np.linspace(0, duration, int(duration * fs))
        
        # Motor control system model
        def neuromuscular_system(state, t):
            """
            Integrated neuromuscular control system:
            - Motor cortex command
            - Spinal motor neurons
            - Muscle contraction
            - Sensory feedback
            """
            (cortical_activity, spinal_activity, muscle_activation, 
             sensory_feedback, joint_angle) = state
            
            # Motor cortex oscillations (beta/gamma)
            motor_command = 0.5 + 0.3 * np.sin(0.1 * 2 * np.pi * t)  # Varying motor intention
            cortical_beta = 0.2 * np.sin(self.motor_params['motor_unit_freq'] * 2 * np.pi * t)
            cortical_gamma = 0.1 * np.sin(40 * 2 * np.pi * t)
            
            cortical_dot = 2 * (motor_command - cortical_activity) + cortical_beta + cortical_gamma
            
            # Spinal motor neuron pool
            # Delayed cortical input + local oscillations
            cortical_input_delayed = cortical_activity  # Simplified delay
            spinal_oscillation = 0.15 * np.sin(self.motor_params['motor_unit_freq'] * 2 * np.pi * t)
            
            spinal_dot = 3 * (cortical_input_delayed - spinal_activity) + spinal_oscillation
            
            # Muscle activation dynamics
            motor_unit_recruitment = spinal_activity
            muscle_dynamics_freq = 50  # Hz - muscle fiber dynamics
            muscle_oscillation = 0.1 * np.sin(muscle_dynamics_freq * 2 * np.pi * t)
            
            muscle_dot = 5 * (motor_unit_recruitment - muscle_activation) + muscle_oscillation
            
            # Joint movement (biomechanics)
            muscle_torque = muscle_activation * 10  # Nm
            joint_inertia = 0.1  # kg⋅m²
            joint_damping = 2.0  # Nm⋅s/rad
            
            joint_velocity = np.gradient(joint_angle) if hasattr(joint_angle, '__len__') else 0
            joint_acceleration = (muscle_torque - joint_damping * joint_velocity) / joint_inertia
            joint_dot = joint_velocity + 0.01 * joint_acceleration  # Simplified integration
            
            # Sensory feedback (proprioception)
            position_error = joint_angle - np.sin(0.2 * 2 * np.pi * t)  # Target tracking
            velocity_feedback = joint_velocity
            sensory_delay = self.motor_params['reflex_delay']
            
            sensory_dot = 8 * (position_error + 0.3 * velocity_feedback - sensory_feedback)
            
            return [cortical_dot, spinal_dot, muscle_dot, sensory_dot, joint_dot]
        
        # Initial conditions
        initial_state = [0.5, 0.3, 0.2, 0.0, 0.0]
        
        # Solve neuromuscular system
        solution = odeint(neuromuscular_system, initial_state, t)
        cortical_trace = solution[:, 0]
        spinal_trace = solution[:, 1]
        muscle_trace = solution[:, 2]
        sensory_trace = solution[:, 3]
        joint_trace = solution[:, 4]
        
        # Generate synthetic EMG and neural signals
        # Motor cortex signal (beta/gamma oscillations)
        cortical_beta = 30 * np.sin(20 * 2 * np.pi * t) * cortical_trace
        cortical_gamma = 15 * np.sin(40 * 2 * np.pi * t) * cortical_trace
        motor_cortex_signal = cortical_beta + cortical_gamma + 5 * np.random.randn(len(t))
        
        # Spinal motor neuron signal
        motor_neuron_firing = self.motor_params['motor_unit_freq']
        spinal_signal = 25 * np.sin(motor_neuron_firing * 2 * np.pi * t) * spinal_trace
        spinal_signal += 3 * np.random.randn(len(t))
        
        # EMG signal (muscle electrical activity)
        emg_signal = muscle_trace * 50 * (1 + 0.5 * np.random.randn(len(t)))
        emg_signal = np.abs(emg_signal)  # Rectified EMG
        
        # Physiological tremor (8-12 Hz)
        tremor_component = 5 * np.sin(self.motor_params['tremor_freq'] * 2 * np.pi * t)
        emg_signal += tremor_component * (1 + 0.1 * np.random.randn(len(t)))
        
        # Motor performance metrics
        # Movement smoothness (jerk)
        joint_velocity = np.gradient(joint_trace, t[1] - t[0])
        joint_acceleration = np.gradient(joint_velocity, t[1] - t[0])
        joint_jerk = np.gradient(joint_acceleration, t[1] - t[0])
        movement_smoothness = 1.0 / (1.0 + np.std(joint_jerk))  # Higher = smoother
        
        # Motor unit synchronization
        def calculate_synchronization_index(signal, freq_range):
            """Calculate motor unit synchronization in frequency band"""
            freqs, psd = signal.welch(signal, fs=fs, nperseg=1024)
            freq_mask = (freqs >= freq_range[0]) & (freqs <= freq_range[1])
            if np.any(freq_mask):
                band_power = np.trapz(psd[freq_mask], freqs[freq_mask])
                total_power = np.trapz(psd, freqs)
                return band_power / total_power
            return 0
        
        # Motor unit synchronization at 15-30 Hz
        motor_sync_index = calculate_synchronization_index(emg_signal, (15, 30))
        
        # Tremor analysis
        tremor_power = calculate_synchronization_index(joint_trace, (6, 12))
        
        # Sensorimotor coupling analysis
        # Cortical-spinal coupling
        cortical_spinal_coupling = np.corrcoef(cortical_trace, spinal_trace)[0, 1]
        
        # Spinal-muscle coupling
        spinal_muscle_coupling = np.corrcoef(spinal_trace, muscle_trace)[0, 1]
        
        # Sensory-motor coupling (feedback control)
        sensory_motor_coupling = np.corrcoef(sensory_trace, muscle_trace)[0, 1]
        
        # Phase coupling in motor control loop
        from scipy.signal import hilbert
        
        # Cortical-muscle phase coupling
        cortical_analytic = hilbert(cortical_trace - np.mean(cortical_trace))
        muscle_analytic = hilbert(muscle_trace - np.mean(muscle_trace))
        
        cortical_phase = np.angle(cortical_analytic)
        muscle_phase = np.angle(muscle_analytic)
        
        phase_coupling_strength = np.abs(np.mean(np.exp(1j * (cortical_phase - muscle_phase))))
        
        # Motor learning index (improvement in performance over time)
        window_size = int(10 * fs)  # 10 second windows
        performance_windows = []
        
        for i in range(0, len(joint_trace) - window_size, window_size):
            window_jerk = joint_jerk[i:i+window_size]
            window_performance = 1.0 / (1.0 + np.std(window_jerk))
            performance_windows.append(window_performance)
        
        if len(performance_windows) > 1:
            motor_learning_slope = np.polyfit(range(len(performance_windows)), 
                                            performance_windows, 1)[0]
        else:
            motor_learning_slope = 0
        
        # Theoretical predictions
        theoretical_predictions = {
            'cortical_spinal_coupling_min': 0.7,
            'spinal_muscle_coupling_min': 0.8,
            'phase_coupling_min': 0.6,
            'motor_sync_index_range': (0.1, 0.4),
            'tremor_power_max': 0.2,
            'movement_smoothness_min': 0.3
        }
        
        # Validation
        validation_success = (
            cortical_spinal_coupling >= theoretical_predictions['cortical_spinal_coupling_min'] and
            spinal_muscle_coupling >= theoretical_predictions['spinal_muscle_coupling_min'] and
            phase_coupling_strength >= theoretical_predictions['phase_coupling_min'] and
            theoretical_predictions['motor_sync_index_range'][0] <= motor_sync_index <= 
            theoretical_predictions['motor_sync_index_range'][1] and
            tremor_power <= theoretical_predictions['tremor_power_max'] and
            movement_smoothness >= theoretical_predictions['movement_smoothness_min']
        )
        
        results = {
            'experiment': 'Neuromuscular Control Integration',
            'validation_success': validation_success,
            'motor_traces': {
                'time': t,
                'cortical_activity': cortical_trace,
                'spinal_activity': spinal_trace,
                'muscle_activation': muscle_trace,
                'joint_angle': joint_trace,
                'sensory_feedback': sensory_trace
            },
            'neural_signals': {
                'motor_cortex': motor_cortex_signal,
                'spinal_neurons': spinal_signal,
                'emg': emg_signal
            },
            'motor_metrics': {
                'movement_smoothness': movement_smoothness,
                'motor_sync_index': motor_sync_index,
                'tremor_power': tremor_power,
                'motor_learning_slope': motor_learning_slope
            },
            'coupling_analysis': {
                'cortical_spinal_coupling': cortical_spinal_coupling,
                'spinal_muscle_coupling': spinal_muscle_coupling,
                'sensory_motor_coupling': sensory_motor_coupling,
                'phase_coupling_strength': phase_coupling_strength
            },
            'kinematics': {
                'joint_velocity': joint_velocity,
                'joint_acceleration': joint_acceleration,
                'joint_jerk': joint_jerk
            },
            'theoretical_predictions': theoretical_predictions
        }
        
        # Visualization
        self._plot_neuromuscular_analysis(results)
        
        return results
    
    def _plot_brain_wave_analysis(self, results: Dict[str, Any]):
        """Create comprehensive brain wave analysis visualizations"""
        fig, axes = plt.subplots(3, 3, figsize=(20, 16))
        
        signal_data = results['signal_data']
        freq_data = results['frequency_analysis']
        bands = results['band_powers']
        coupling = results['coupling_analysis']
        
        # Plot 1: EEG time series
        time_window = slice(0, int(10 * 500))  # First 10 seconds
        axes[0, 0].plot(signal_data['time'][time_window], 
                       signal_data['eeg_signal'][time_window], 'k-', linewidth=1)
        axes[0, 0].set_title('EEG Signal (10 seconds)')
        axes[0, 0].set_xlabel('Time (s)')
        axes[0, 0].set_ylabel('Amplitude (μV)')
        axes[0, 0].grid(True, alpha=0.3)
        
        # Plot 2: Power spectral density with band highlights
        axes[0, 1].semilogy(freq_data['frequencies'], freq_data['power_spectral_density'], 'b-')
        
        # Highlight brain wave bands
        colors = plt.cm.tab10(np.linspace(0, 1, len(self.brain_wave_bands)))
        for (band_name, (f_min, f_max)), color in zip(self.brain_wave_bands.items(), colors):
            if f_max <= max(freq_data['frequencies']):
                band_mask = (freq_data['frequencies'] >= f_min) & (freq_data['frequencies'] <= f_max)
                axes[0, 1].fill_between(freq_data['frequencies'][band_mask],
                                       freq_data['power_spectral_density'][band_mask],
                                       alpha=0.3, color=color, label=band_name)
        
        axes[0, 1].set_title('Power Spectral Density')
        axes[0, 1].set_xlabel('Frequency (Hz)')
        axes[0, 1].set_ylabel('PSD (μV²/Hz)')
        axes[0, 1].legend(bbox_to_anchor=(1.05, 1), loc='upper left')
        axes[0, 1].set_xlim(0, 100)
        
        # Plot 3: Band power distribution
        band_names = list(bands.keys())
        band_values = list(bands.values())
        colors = plt.cm.viridis(np.linspace(0, 1, len(band_names)))
        
        bars = axes[0, 2].bar(band_names, band_values, color=colors)
        axes[0, 2].set_title('Brain Wave Band Powers')
        axes[0, 2].set_ylabel('Power (%)')
        axes[0, 2].tick_params(axis='x', rotation=45)
        
        for bar, value in zip(bars, band_values):
            height = bar.get_height()
            axes[0, 2].text(bar.get_x() + bar.get_width()/2., height + 0.5,
                           f'{value:.1f}%', ha='center', va='bottom')
        
        # Plot 4: Individual frequency components
        components = signal_data['frequency_components']
        component_names = ['delta', 'theta', 'alpha', 'beta']
        for i, comp_name in enumerate(component_names[:4]):
            if comp_name in components:
                time_slice = slice(0, int(5 * 500))  # 5 seconds
                axes[1, 0].plot(signal_data['time'][time_slice], 
                               components[comp_name][time_slice] + i*50, 
                               label=comp_name, linewidth=1.5)
        
        axes[1, 0].set_title('Frequency Components (5 seconds)')
        axes[1, 0].set_xlabel('Time (s)')
        axes[1, 0].set_ylabel('Amplitude (μV)')
        axes[1, 0].legend()
        axes[1, 0].grid(True, alpha=0.3)
        
        # Plot 5: Cross-frequency coupling
        coupling_names = list(coupling.keys())
        coupling_values = list(coupling.values())
        
        if coupling_values:
            bars = axes[1, 1].bar(coupling_names, coupling_values, color='lightcoral')
            axes[1, 1].set_title('Cross-Frequency Coupling')
            axes[1, 1].set_ylabel('Coupling Strength')
            axes[1, 1].tick_params(axis='x', rotation=45)
            
            for bar, value in zip(bars, coupling_values):
                height = bar.get_height()
                axes[1, 1].text(bar.get_x() + bar.get_width()/2., height + 0.01,
                               f'{value:.3f}', ha='center', va='bottom')
        
        # Plot 6: Gamma component detail
        if 'gamma' in components:
            gamma_slice = slice(0, int(2 * 500))  # 2 seconds for detail
            axes[1, 2].plot(signal_data['time'][gamma_slice], 
                           components['gamma'][gamma_slice], 'red', linewidth=2)
            axes[1, 2].set_title('Gamma Oscillations (2 seconds)')
            axes[1, 2].set_xlabel('Time (s)')
            axes[1, 2].set_ylabel('Amplitude (μV)')
            axes[1, 2].grid(True, alpha=0.3)
        
        # Plot 7: Alpha-beta interaction
        if 'alpha' in components and 'beta' in components:
            alpha_envelope = np.abs(signal.hilbert(components['alpha']))
            beta_envelope = np.abs(signal.hilbert(components['beta']))
            
            interaction_slice = slice(0, int(10 * 500))
            axes[2, 0].plot(signal_data['time'][interaction_slice], 
                           alpha_envelope[interaction_slice], 'blue', 
                           label='Alpha envelope', linewidth=2)
            axes[2, 0].plot(signal_data['time'][interaction_slice], 
                           beta_envelope[interaction_slice], 'orange', 
                           label='Beta envelope', linewidth=2)
            axes[2, 0].set_title('Alpha-Beta Interaction')
            axes[2, 0].set_xlabel('Time (s)')
            axes[2, 0].set_ylabel('Envelope Amplitude')
            axes[2, 0].legend()
            axes[2, 0].grid(True, alpha=0.3)
        
        # Plot 8: Theta-gamma coupling visualization
        if 'theta_gamma_pac' in coupling:
            # Create phase-amplitude plot
            from scipy.signal import hilbert
            if 'theta' in components and 'gamma' in components:
                theta_phase = np.angle(hilbert(components['theta']))
                gamma_amplitude = np.abs(hilbert(components['gamma']))
                
                # Bin by phase
                phase_bins = np.linspace(-np.pi, np.pi, 20)
                binned_amplitudes = []
                
                for i in range(len(phase_bins)-1):
                    mask = (theta_phase >= phase_bins[i]) & (theta_phase < phase_bins[i+1])
                    if np.any(mask):
                        binned_amplitudes.append(np.mean(gamma_amplitude[mask]))
                    else:
                        binned_amplitudes.append(0)
                
                axes[2, 1].bar(phase_bins[:-1], binned_amplitudes, 
                              width=np.diff(phase_bins)[0]*0.8, alpha=0.7)
                axes[2, 1].set_title(f'Theta-Gamma PAC (MI={coupling["theta_gamma_pac"]:.3f})')
                axes[2, 1].set_xlabel('Theta Phase (radians)')
                axes[2, 1].set_ylabel('Mean Gamma Amplitude')
        
        # Plot 9: Validation summary
        predictions = results['theoretical_predictions']
        validation_text = (
            f"🧠 BRAIN WAVE VALIDATION\n\n"
            f"✓ Status: {'PASS' if results['validation_success'] else 'FAIL'}\n\n"
            f"Alpha Dominance: {bands.get('alpha', 0):.1f}%\n"
            f"Expected: {predictions['expected_alpha_dominance']}\n\n"
            f"Theta-Gamma PAC: {coupling.get('theta_gamma_pac', 0):.3f}\n"
            f"Threshold: ≥{predictions['theta_gamma_pac_threshold']}\n\n"
            f"Alpha-Beta Coupling: {coupling.get('alpha_beta_coupling', 0):.3f}\n"
            f"Expected: {predictions['alpha_beta_anticorrelation']}"
        )
        
        axes[2, 2].text(0.05, 0.95, validation_text, transform=axes[2, 2].transAxes,
                       verticalalignment='top', fontsize=10,
                       bbox=dict(boxstyle='round', 
                               facecolor='lightgreen' if results['validation_success'] else 'lightcoral', 
                               alpha=0.8))
        axes[2, 2].set_xlim(0, 1)
        axes[2, 2].set_ylim(0, 1)
        axes[2, 2].axis('off')
        axes[2, 2].set_title('Validation Summary')
        
        plt.tight_layout()
        plt.savefig(f"{self.results_dir}/brain_wave_oscillatory_analysis.png", 
                   dpi=300, bbox_inches='tight')
        plt.close()
    
    def _plot_cognitive_analysis(self, results: Dict[str, Any]):
        """Create cognitive processing analysis visualizations"""
        fig, axes = plt.subplots(3, 3, figsize=(20, 16))
        
        traces = results['cognitive_traces']
        signals = results['neural_signals']
        performance = results['performance_metrics']
        coupling = results['coupling_analysis']
        correlations = results['performance_correlations']
        
        # Plot 1: Cognitive state traces
        axes[0, 0].plot(traces['time'], traces['attention_state'], 'blue', 
                       label='Attention', linewidth=2)
        axes[0, 0].plot(traces['time'], traces['working_memory_state'], 'green', 
                       label='Working Memory', linewidth=2)
        axes[0, 0].plot(traces['time'], traces['executive_state'], 'red', 
                       label='Executive', linewidth=2)
        axes[0, 0].plot(traces['time'], traces['consciousness_state'], 'purple', 
                       label='Consciousness', linewidth=2)
        
        axes[0, 0].set_title('Cognitive State Dynamics')
        axes[0, 0].set_xlabel('Time (s)')
        axes[0, 0].set_ylabel('State Level')
        axes[0, 0].legend()
        axes[0, 0].grid(True, alpha=0.3)
        
        # Plot 2: Neural signal oscillations
        time_window = slice(0, int(10 * 250))  # 10 seconds
        offset = 0
        colors = ['blue', 'green', 'red', 'purple']
        
        for i, (sig_name, sig_data) in enumerate(signals.items()):
            axes[0, 1].plot(traces['time'][time_window], 
                           sig_data[time_window] + offset, 
                           color=colors[i], label=sig_name.replace('_', ' ').title(), 
                           linewidth=1.5)
            offset += 60
        
        axes[0, 1].set_title('Neural Oscillations (10 seconds)')
        axes[0, 1].set_xlabel('Time (s)')
        axes[0, 1].set_ylabel('Neural Activity (offset)')
        axes[0, 1].legend()
        axes[0, 1].grid(True, alpha=0.3)
        
        # Plot 3: Performance metrics over time
        time_reduced = traces['time'][::100]  # Downsample for plotting
        rt_reduced = performance['reaction_time'][::100]
        acc_reduced = performance['accuracy'][::100]
        
        ax_rt = axes[0, 2]
        ax_acc = ax_rt.twinx()
        
        line1 = ax_rt.plot(time_reduced, rt_reduced, 'red', 
                          linewidth=2, label='Reaction Time')
        line2 = ax_acc.plot(time_reduced, acc_reduced, 'blue', 
                           linewidth=2, label='Accuracy')
        
        ax_rt.set_xlabel('Time (s)')
        ax_rt.set_ylabel('Reaction Time (ms)', color='red')
        ax_acc.set_ylabel('Accuracy', color='blue')
        ax_rt.tick_params(axis='y', labelcolor='red')
        ax_acc.tick_params(axis='y', labelcolor='blue')
        
        # Combined legend
        lines = line1 + line2
        labels = [l.get_label() for l in lines]
        ax_rt.legend(lines, labels, loc='upper right')
        ax_rt.set_title('Cognitive Performance Over Time')
        ax_rt.grid(True, alpha=0.3)
        
        # Plot 4: Coupling matrix heatmap
        im = axes[1, 0].imshow(coupling['coupling_matrix'], cmap='RdBu_r', 
                              aspect='auto', vmin=0, vmax=1)
        axes[1, 0].set_xticks(range(len(coupling['signal_names'])))
        axes[1, 0].set_yticks(range(len(coupling['signal_names'])))
        axes[1, 0].set_xticklabels([name.replace('_', '\n') for name in coupling['signal_names']], 
                                  rotation=45)
        axes[1, 0].set_yticklabels([name.replace('_', '\n') for name in coupling['signal_names']])
        axes[1, 0].set_title('Cognitive Network Coupling')
        plt.colorbar(im, ax=axes[1, 0])
        
        # Plot 5: Key coupling relationships
        coupling_names = ['Attention-Executive', 'WM-Consciousness', 'Overall Coherence']
        coupling_values = [coupling['attention_executive_coupling'], 
                          coupling['wm_consciousness_coupling'],
                          coupling['cognitive_coherence']]
        
        bars = axes[1, 1].bar(coupling_names, coupling_values, 
                             color=['skyblue', 'lightgreen', 'gold'])
        axes[1, 1].set_title('Key Coupling Relationships')
        axes[1, 1].set_ylabel('Coupling Strength')
        axes[1, 1].tick_params(axis='x', rotation=45)
        
        for bar, value in zip(bars, coupling_values):
            height = bar.get_height()
            axes[1, 1].text(bar.get_x() + bar.get_width()/2., height + 0.02,
                           f'{value:.3f}', ha='center', va='bottom')
        
        # Plot 6: Performance-neural correlations
        # Reaction time vs attention neural activity
        axes[1, 2].scatter(np.abs(signals['attention'][::50]), 
                          performance['reaction_time'][::50], 
                          alpha=0.6, s=20, color='red')
        
        # Trend line
        x_data = np.abs(signals['attention'][::50])
        y_data = performance['reaction_time'][::50]
        z = np.polyfit(x_data, y_data, 1)
        p = np.poly1d(z)
        axes[1, 2].plot(x_data, p(x_data), "r--", alpha=0.8, linewidth=2)
        
        axes[1, 2].set_title(f'RT-Neural Correlation (r={correlations["rt_neural_correlation"]:.3f})')
        axes[1, 2].set_xlabel('Attention Neural Activity')
        axes[1, 2].set_ylabel('Reaction Time (ms)')
        axes[1, 2].grid(True, alpha=0.3)
        
        # Plot 7: Processing efficiency over time
        axes[2, 0].plot(traces['time'], performance['processing_efficiency'], 
                       'orange', linewidth=2)
        axes[2, 0].fill_between(traces['time'], performance['processing_efficiency'], 
                               alpha=0.3, color='orange')
        axes[2, 0].set_title('Processing Efficiency')
        axes[2, 0].set_xlabel('Time (s)')
        axes[2, 0].set_ylabel('Efficiency')
        axes[2, 0].grid(True, alpha=0.3)
        
        # Plot 8: Cognitive resources utilization
        axes[2, 1].plot(traces['time'], performance['cognitive_resources'], 
                       'brown', linewidth=2)
        axes[2, 1].fill_between(traces['time'], performance['cognitive_resources'], 
                               alpha=0.3, color='brown')
        axes[2, 1].set_title('Cognitive Resources')
        axes[2, 1].set_xlabel('Time (s)')
        axes[2, 1].set_ylabel('Resource Level')
        axes[2, 1].grid(True, alpha=0.3)
        
        # Plot 9: Validation summary
        predictions = results['theoretical_predictions']
        validation_text = (
            f"🎯 COGNITIVE VALIDATION\n\n"
            f"✓ Status: {'PASS' if results['validation_success'] else 'FAIL'}\n\n"
            f"Attention-Executive: {coupling['attention_executive_coupling']:.3f}\n"
            f"Required: ≥{predictions['attention_executive_coupling_min']}\n\n"
            f"WM-Consciousness: {coupling['wm_consciousness_coupling']:.3f}\n"
            f"Required: ≥{predictions['wm_consciousness_coupling_min']}\n\n"
            f"RT-Neural Correlation: {correlations['rt_neural_correlation']:.3f}\n"
            f"Expected: {predictions['rt_neural_correlation_range']}\n\n"
            f"Cognitive Coherence: {coupling['cognitive_coherence']:.3f}\n"
            f"Required: ≥{predictions['cognitive_coherence_min']}"
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
        plt.savefig(f"{self.results_dir}/cognitive_processing_analysis.png", 
                   dpi=300, bbox_inches='tight')
        plt.close()
    
    def _plot_neuromuscular_analysis(self, results: Dict[str, Any]):
        """Create neuromuscular control analysis visualizations"""
        fig, axes = plt.subplots(3, 3, figsize=(20, 16))
        
        traces = results['motor_traces']
        signals = results['neural_signals']
        metrics = results['motor_metrics']
        coupling = results['coupling_analysis']
        kinematics = results['kinematics']
        
        # Plot 1: Motor system state traces
        axes[0, 0].plot(traces['time'], traces['cortical_activity'], 'red', 
                       label='Cortical', linewidth=2)
        axes[0, 0].plot(traces['time'], traces['spinal_activity'], 'blue', 
                       label='Spinal', linewidth=2)
        axes[0, 0].plot(traces['time'], traces['muscle_activation'], 'green', 
                       label='Muscle', linewidth=2)
        axes[0, 0].plot(traces['time'], traces['sensory_feedback'], 'orange', 
                       label='Sensory', linewidth=2)
        
        axes[0, 0].set_title('Motor System State Variables')
        axes[0, 0].set_xlabel('Time (s)')
        axes[0, 0].set_ylabel('Activity Level')
        axes[0, 0].legend()
        axes[0, 0].grid(True, alpha=0.3)
        
        # Plot 2: Neural signals
        time_window = slice(0, int(5 * 1000))  # 5 seconds
        
        axes[0, 1].plot(traces['time'][time_window], 
                       signals['motor_cortex'][time_window], 'red', 
                       label='Motor Cortex', linewidth=1)
        axes[0, 1].plot(traces['time'][time_window], 
                       signals['spinal_neurons'][time_window] + 50, 'blue', 
                       label='Spinal Neurons', linewidth=1)
        
        axes[0, 1].set_title('Neural Oscillations (5 seconds)')
        axes[0, 1].set_xlabel('Time (s)')
        axes[0, 1].set_ylabel('Neural Activity')
        axes[0, 1].legend()
        axes[0, 1].grid(True, alpha=0.3)
        
        # Plot 3: EMG and joint movement
        ax_emg = axes[0, 2]
        ax_joint = ax_emg.twinx()
        
        time_slice = slice(0, int(10 * 1000))  # 10 seconds
        line1 = ax_emg.plot(traces['time'][time_slice], 
                           signals['emg'][time_slice], 'green', 
                           linewidth=1.5, label='EMG')
        line2 = ax_joint.plot(traces['time'][time_slice], 
                             traces['joint_angle'][time_slice], 'purple', 
                             linewidth=2, label='Joint Angle')
        
        ax_emg.set_xlabel('Time (s)')
        ax_emg.set_ylabel('EMG Amplitude', color='green')
        ax_joint.set_ylabel('Joint Angle (rad)', color='purple')
        ax_emg.tick_params(axis='y', labelcolor='green')
        ax_joint.tick_params(axis='y', labelcolor='purple')
        
        lines = line1 + line2
        labels = [l.get_label() for l in lines]
        ax_emg.legend(lines, labels, loc='upper right')
        ax_emg.set_title('EMG and Joint Movement')
        ax_emg.grid(True, alpha=0.3)
        
        # Plot 4: Motor coupling analysis
        coupling_names = ['Cortical-Spinal', 'Spinal-Muscle', 'Sensory-Motor', 'Phase Coupling']
        coupling_values = [coupling['cortical_spinal_coupling'], 
                          coupling['spinal_muscle_coupling'],
                          coupling['sensory_motor_coupling'], 
                          coupling['phase_coupling_strength']]
        
        bars = axes[1, 0].bar(coupling_names, coupling_values, 
                             color=['red', 'blue', 'orange', 'purple'])
        axes[1, 0].set_title('Motor System Coupling')
        axes[1, 0].set_ylabel('Coupling Strength')
        axes[1, 0].tick_params(axis='x', rotation=45)
        
        for bar, value in zip(bars, coupling_values):
            height = bar.get_height()
            axes[1, 0].text(bar.get_x() + bar.get_width()/2., height + 0.02,
                           f'{value:.3f}', ha='center', va='bottom')
        
        # Plot 5: Motor performance metrics
        metric_names = ['Smoothness', 'Sync Index', 'Tremor Power', 'Learning Slope']
        metric_values = [metrics['movement_smoothness'], 
                        metrics['motor_sync_index'],
                        metrics['tremor_power'], 
                        metrics['motor_learning_slope']]
        
        colors = ['lightgreen', 'skyblue', 'lightcoral', 'gold']
        bars = axes[1, 1].bar(metric_names, metric_values, color=colors)
        axes[1, 1].set_title('Motor Performance Metrics')
        axes[1, 1].set_ylabel('Metric Value')
        axes[1, 1].tick_params(axis='x', rotation=45)
        
        for bar, value in zip(bars, metric_values):
            height = bar.get_height()
            axes[1, 1].text(bar.get_x() + bar.get_width()/2., height + height*0.1,
                           f'{value:.3f}', ha='center', va='bottom')
        
        # Plot 6: Joint kinematics
        axes[1, 2].plot(traces['time'], kinematics['joint_velocity'], 
                       'blue', label='Velocity', linewidth=2)
        axes[1, 2].plot(traces['time'], kinematics['joint_acceleration'], 
                       'red', label='Acceleration', linewidth=2)
        axes[1, 2].plot(traces['time'], kinematics['joint_jerk']/10, 
                       'green', label='Jerk/10', linewidth=2)
        
        axes[1, 2].set_title('Joint Kinematics')
        axes[1, 2].set_xlabel('Time (s)')
        axes[1, 2].set_ylabel('Kinematic Variables')
        axes[1, 2].legend()
        axes[1, 2].grid(True, alpha=0.3)
        
        # Plot 7: EMG power spectrum
        freqs, emg_psd = signal.welch(signals['emg'], fs=1000, nperseg=1024)
        axes[2, 0].semilogy(freqs, emg_psd, 'green', linewidth=2)
        
        # Highlight motor unit synchronization band (15-30 Hz)
        sync_mask = (freqs >= 15) & (freqs <= 30)
        axes[2, 0].fill_between(freqs[sync_mask], emg_psd[sync_mask], 
                               alpha=0.3, color='red', label='Sync Band')
        
        # Highlight tremor band (6-12 Hz)
        tremor_mask = (freqs >= 6) & (freqs <= 12)
        axes[2, 0].fill_between(freqs[tremor_mask], emg_psd[tremor_mask], 
                               alpha=0.3, color='orange', label='Tremor Band')
        
        axes[2, 0].set_title('EMG Power Spectrum')
        axes[2, 0].set_xlabel('Frequency (Hz)')
        axes[2, 0].set_ylabel('PSD')
        axes[2, 0].legend()
        axes[2, 0].set_xlim(0, 100)
        
        # Plot 8: Cortical-muscle phase relationship
        from scipy.signal import hilbert
        
        # Calculate phases
        cortical_phase = np.angle(hilbert(traces['cortical_activity'] - np.mean(traces['cortical_activity'])))
        muscle_phase = np.angle(hilbert(traces['muscle_activation'] - np.mean(traces['muscle_activation'])))
        
        # Phase difference histogram
        phase_diff = np.angle(np.exp(1j * (cortical_phase - muscle_phase)))
        axes[2, 1].hist(phase_diff, bins=50, alpha=0.7, density=True, color='purple')
        axes[2, 1].axvline(np.mean(phase_diff), color='red', linestyle='--', 
                          linewidth=2, label=f'Mean: {np.mean(phase_diff):.3f}')
        axes[2, 1].set_title(f'Phase Coupling (Strength: {coupling["phase_coupling_strength"]:.3f})')
        axes[2, 1].set_xlabel('Phase Difference (radians)')
        axes[2, 1].set_ylabel('Probability Density')
        axes[2, 1].legend()
        
        # Plot 9: Validation summary
        predictions = results['theoretical_predictions']
        validation_text = (
            f"💪 NEUROMUSCULAR VALIDATION\n\n"
            f"✓ Status: {'PASS' if results['validation_success'] else 'FAIL'}\n\n"
            f"Cortical-Spinal: {coupling['cortical_spinal_coupling']:.3f}\n"
            f"Required: ≥{predictions['cortical_spinal_coupling_min']}\n\n"
            f"Phase Coupling: {coupling['phase_coupling_strength']:.3f}\n"
            f"Required: ≥{predictions['phase_coupling_min']}\n\n"
            f"Motor Sync: {metrics['motor_sync_index']:.3f}\n"
            f"Expected: {predictions['motor_sync_index_range']}\n\n"
            f"Movement Smoothness: {metrics['movement_smoothness']:.3f}\n"
            f"Required: ≥{predictions['movement_smoothness_min']}"
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
        plt.savefig(f"{self.results_dir}/neuromuscular_control_analysis.png", 
                   dpi=300, bbox_inches='tight')
        plt.close()
    
    def run_all_experiments(self) -> Dict[str, Any]:
        """Run all neural oscillatory validation experiments"""
        print("🧠 Running Neural System Oscillatory Validation Suite")
        print("=" * 60)
        
        all_results = {}
        
        # Run experiments
        all_results['experiment_1'] = self.experiment_1_brain_wave_oscillatory_coupling()
        all_results['experiment_2'] = self.experiment_2_cognitive_processing_oscillations()
        all_results['experiment_3'] = self.experiment_3_neuromuscular_control_integration()
        
        # Compile validation summary
        validations = [result['validation_success'] for result in all_results.values()]
        overall_success = all(validations)
        
        summary = {
            'domain': 'Neural System Oscillations',
            'total_experiments': len(all_results),
            'successful_validations': sum(validations),
            'overall_validation_success': overall_success,
            'timestamp': datetime.now().isoformat(),
            'detailed_results': all_results
        }
        
        # Save comprehensive results
        results_file = f"{self.results_dir}/neural_validation_summary.json"
        import json
        with open(results_file, 'w') as f:
            json.dump({k: v for k, v in summary.items() 
                      if k != 'detailed_results'}, f, indent=2)
        
        print(f"\n🧠 Neural Validation Complete:")
        print(f"   ✓ Successful: {sum(validations)}/{len(validations)} experiments")
        print(f"   ✓ Overall Status: {'PASS' if overall_success else 'FAIL'}")
        print(f"   ✓ Results saved to: {self.results_dir}/")
        
        self.validation_results = summary
        return summary

def main():
    """Run neural oscillatory validation as standalone"""
    validator = NeuralOscillatoryValidator()
    return validator.run_all_experiments()

if __name__ == "__main__":
    results = main()
    print(f"Neural validation completed: {results['overall_validation_success']}")
