"""
Metabolic System Oscillatory Dynamics Validator

This module validates the theoretical predictions about metabolic oscillations,
glycolytic cycles, ATP production rhythms, and cellular energy dynamics within 
the unified biological oscillations framework.

Key Validations:
1. Glycolytic Oscillation Dynamics
2. ATP Production Cycle Validation
3. Metabolic Network Coupling
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

class MetabolicOscillatoryValidator:
    """Validates oscillatory dynamics in metabolic systems"""
    
    def __init__(self, results_dir: str = "results/metabolic"):
        self.results_dir = results_dir
        os.makedirs(results_dir, exist_ok=True)
        
        # Glycolytic pathway parameters
        self.glycolytic_params = {
            'glucose_concentration': 5.0,      # mM
            'atp_adp_ratio': 3.0,             # ATP:ADP ratio
            'phosphofructokinase_activity': 1.0,  # Relative activity
            'pyruvate_kinase_activity': 1.0,      # Relative activity
            'oscillation_frequency': 0.02,        # Hz (50 second period)
        }
        
        # ATP synthesis parameters  
        self.atp_params = {
            'oxidative_phosphorylation_rate': 100,  # μmol/min/mg protein
            'substrate_level_phosphorylation': 20,   # μmol/min/mg protein
            'atp_hydrolysis_rate': 80,              # μmol/min/mg protein
            'mitochondrial_capacity': 1.0,          # Relative capacity
        }
        
        # Metabolic coupling parameters
        self.coupling_params = {
            'glycolysis_oxidation_coupling': 0.8,   # Coupling strength
            'atp_feedback_strength': 0.6,           # ATP feedback inhibition
            'calcium_coupling': 0.4,                # Ca²⁺ oscillation coupling
            'circadian_coupling': 0.3,              # Daily rhythm coupling
        }
        
        # Metabolic oscillation frequencies
        self.metabolic_frequencies = {
            'glycolytic_oscillation': 0.02,      # Hz - glycolytic cycles
            'calcium_oscillation': 0.1,          # Hz - intracellular Ca²⁺
            'mitochondrial_oscillation': 0.05,   # Hz - respiratory chain
            'circadian_metabolic': 1.16e-5,      # Hz - 24 hour cycle
        }
        
        self.validation_results = {}
        
    def experiment_1_glycolytic_oscillation_dynamics(self) -> Dict[str, Any]:
        """
        Experiment 1: Glycolytic Oscillation Dynamics
        
        Validates the classic glycolytic oscillations:
        - Phosphofructokinase feedback loops
        - ATP/ADP ratio oscillations
        - NADH/NAD+ redox oscillations
        - Pyruvate production cycles
        """
        print("🍯 Experiment 1: Glycolytic Oscillation Dynamics")
        
        # Simulation parameters
        duration = 1000  # seconds (16.7 minutes)
        fs = 2.0  # 2 Hz sampling
        t = np.linspace(0, duration, int(duration * fs))
        
        # Glycolytic pathway oscillator model
        def glycolytic_oscillator(state, t):
            """
            Simplified glycolytic oscillator based on Sel'kov model:
            - Glucose-6-phosphate
            - Fructose-6-phosphate  
            - Fructose-1,6-bisphosphate
            - ATP/ADP levels
            - NADH levels
            """
            glucose_6p, fructose_6p, fructose_16bp, atp, nadh = state
            
            # Parameters
            glucose_input = 0.1  # External glucose influx
            k1 = 0.1  # Hexokinase activity
            k2 = 1.0  # Phosphofructokinase activity (key regulatory step)
            k3 = 0.8  # Aldolase activity
            k4 = 0.5  # ATP regeneration rate
            k5 = 0.3  # NADH oxidation rate
            
            # ATP inhibition of phosphofructokinase (negative feedback)
            atp_inhibition = 1.0 / (1.0 + (atp / 2.0)**2)
            
            # ADP activation of phosphofructokinase (positive feedback)  
            adp = 5.0 - atp  # Total adenine nucleotide pool
            adp_activation = 1.0 + (adp / 1.0)**2
            
            # Phosphofructokinase regulation (central oscillator)
            pfk_activity = k2 * atp_inhibition * adp_activation
            
            # Glycolytic flux equations
            glucose_6p_dot = glucose_input + k1 * self.glycolytic_params['glucose_concentration'] - k1 * glucose_6p
            
            fructose_6p_dot = k1 * glucose_6p - pfk_activity * fructose_6p
            
            fructose_16bp_dot = pfk_activity * fructose_6p - k3 * fructose_16bp
            
            # ATP dynamics (consumption and regeneration)
            atp_consumption = pfk_activity * fructose_6p + k1 * glucose_6p
            atp_regeneration = k4 * fructose_16bp + k5 * nadh
            atp_dot = atp_regeneration - atp_consumption
            
            # NADH dynamics (production and oxidation)
            nadh_production = k3 * fructose_16bp  # From glycolysis
            nadh_oxidation = k5 * nadh  # Mitochondrial oxidation
            nadh_dot = nadh_production - nadh_oxidation
            
            return [glucose_6p_dot, fructose_6p_dot, fructose_16bp_dot, atp_dot, nadh_dot]
        
        # Initial conditions
        initial_state = [1.0, 0.5, 0.3, 3.0, 0.2]  # Physiological levels
        
        # Solve glycolytic oscillator
        solution = odeint(glycolytic_oscillator, initial_state, t)
        glucose_6p_trace = solution[:, 0]
        fructose_6p_trace = solution[:, 1] 
        fructose_16bp_trace = solution[:, 2]
        atp_trace = solution[:, 3]
        nadh_trace = solution[:, 4]
        
        # Calculate derived metabolic variables
        adp_trace = 5.0 - atp_trace  # Total adenine nucleotide conservation
        atp_adp_ratio = atp_trace / (adp_trace + 1e-6)
        
        # Glycolytic flux (glucose consumption rate)
        glycolytic_flux = np.gradient(fructose_16bp_trace, t[1] - t[0])
        
        # Energy charge (Atkinson's energy charge)
        amp_trace = np.maximum(0, 2.0 - atp_trace - adp_trace)  # Simplified
        energy_charge = (atp_trace + 0.5 * adp_trace) / (atp_trace + adp_trace + amp_trace + 1e-6)
        
        # Oscillation analysis
        metabolic_signals = {
            'glucose_6p': glucose_6p_trace,
            'fructose_6p': fructose_6p_trace,
            'fructose_16bp': fructose_16bp_trace,
            'atp': atp_trace,
            'nadh': nadh_trace,
            'glycolytic_flux': glycolytic_flux
        }
        
        # Frequency domain analysis
        oscillation_metrics = {}
        
        for signal_name, signal_data in metabolic_signals.items():
            freqs, psd = signal.welch(signal_data, fs=fs, nperseg=256)
            
            # Find peak frequency
            peak_idx = np.argmax(psd[1:]) + 1  # Skip DC component
            peak_frequency = freqs[peak_idx]
            
            # Calculate oscillation strength (ratio of peak to mean power)
            mean_power = np.mean(psd)
            peak_power = psd[peak_idx]
            oscillation_strength = peak_power / mean_power
            
            oscillation_metrics[signal_name] = {
                'peak_frequency': peak_frequency,
                'oscillation_strength': oscillation_strength,
                'frequencies': freqs,
                'power_spectral_density': psd
            }
        
        # Phase relationships between metabolites
        from scipy.signal import hilbert
        
        # ATP-ADP phase relationship
        atp_analytic = hilbert(atp_trace - np.mean(atp_trace))
        adp_analytic = hilbert(adp_trace - np.mean(adp_trace))
        
        atp_phase = np.angle(atp_analytic)
        adp_phase = np.angle(adp_analytic)
        
        atp_adp_phase_diff = np.angle(np.exp(1j * (atp_phase - adp_phase)))
        atp_adp_phase_coupling = np.abs(np.mean(np.exp(1j * atp_adp_phase_diff)))
        
        # Glycolytic flux-ATP phase relationship
        flux_analytic = hilbert(glycolytic_flux - np.mean(glycolytic_flux))
        flux_phase = np.angle(flux_analytic)
        
        flux_atp_phase_diff = np.angle(np.exp(1j * (flux_phase - atp_phase)))
        flux_atp_phase_coupling = np.abs(np.mean(np.exp(1j * flux_atp_phase_diff)))
        
        # Metabolic efficiency metrics
        # ATP yield per glucose (theoretical max is ~38 mol ATP/mol glucose)
        glucose_consumption = np.trapz(np.maximum(0, -np.gradient(glucose_6p_trace)), t)
        atp_production = np.trapz(np.maximum(0, np.gradient(atp_trace)), t) 
        atp_yield = atp_production / (glucose_consumption + 1e-6)
        
        # Oscillation stability (coefficient of variation)
        atp_cv = np.std(atp_trace) / np.mean(atp_trace)
        flux_cv = np.std(glycolytic_flux) / (np.mean(np.abs(glycolytic_flux)) + 1e-6)
        
        # Cross-correlation analysis
        correlation_matrix = np.zeros((len(metabolic_signals), len(metabolic_signals)))
        signal_names = list(metabolic_signals.keys())
        
        for i, sig1_name in enumerate(signal_names):
            for j, sig2_name in enumerate(signal_names):
                sig1 = metabolic_signals[sig1_name]
                sig2 = metabolic_signals[sig2_name]
                correlation_matrix[i, j] = np.corrcoef(sig1, sig2)[0, 1]
        
        # Theoretical predictions for glycolytic oscillations
        theoretical_predictions = {
            'expected_oscillation_frequency': (0.01, 0.05),  # Hz
            'atp_adp_phase_coupling_min': 0.8,  # Strong antiphase coupling expected
            'flux_atp_phase_coupling_min': 0.6, # Moderate coupling expected
            'oscillation_strength_min': 2.0,    # Peak/mean power ratio
            'energy_charge_range': (0.7, 0.95), # Typical cellular energy charge
            'atp_cv_max': 0.3,                  # Maximum coefficient of variation
        }
        
        # Validation
        glycolytic_freq = oscillation_metrics['atp']['peak_frequency']
        energy_charge_mean = np.mean(energy_charge)
        
        validation_success = (
            theoretical_predictions['expected_oscillation_frequency'][0] <= glycolytic_freq <= 
            theoretical_predictions['expected_oscillation_frequency'][1] and
            atp_adp_phase_coupling >= theoretical_predictions['atp_adp_phase_coupling_min'] and
            flux_atp_phase_coupling >= theoretical_predictions['flux_atp_phase_coupling_min'] and
            oscillation_metrics['atp']['oscillation_strength'] >= theoretical_predictions['oscillation_strength_min'] and
            theoretical_predictions['energy_charge_range'][0] <= energy_charge_mean <= 
            theoretical_predictions['energy_charge_range'][1] and
            atp_cv <= theoretical_predictions['atp_cv_max']
        )
        
        results = {
            'experiment': 'Glycolytic Oscillation Dynamics',
            'validation_success': validation_success,
            'metabolite_traces': {
                'time': t,
                'glucose_6p': glucose_6p_trace,
                'fructose_6p': fructose_6p_trace,
                'fructose_16bp': fructose_16bp_trace,
                'atp': atp_trace,
                'nadh': nadh_trace,
                'adp': adp_trace
            },
            'derived_metrics': {
                'atp_adp_ratio': atp_adp_ratio,
                'glycolytic_flux': glycolytic_flux,
                'energy_charge': energy_charge,
                'atp_yield': atp_yield
            },
            'oscillation_analysis': {
                'oscillation_metrics': oscillation_metrics,
                'atp_adp_phase_coupling': atp_adp_phase_coupling,
                'flux_atp_phase_coupling': flux_atp_phase_coupling,
                'correlation_matrix': correlation_matrix,
                'signal_names': signal_names
            },
            'stability_metrics': {
                'atp_cv': atp_cv,
                'flux_cv': flux_cv,
                'energy_charge_mean': energy_charge_mean
            },
            'theoretical_predictions': theoretical_predictions
        }
        
        # Visualization
        self._plot_glycolytic_analysis(results)
        
        return results
    
    def experiment_2_atp_production_cycle_validation(self) -> Dict[str, Any]:
        """
        Experiment 2: ATP Production Cycle Validation
        
        Validates ATP synthesis and hydrolysis oscillations:
        - Oxidative phosphorylation cycles
        - Substrate-level phosphorylation
        - ATP hydrolysis patterns
        - Mitochondrial respiratory oscillations
        """
        print("⚡ Experiment 2: ATP Production Cycle Validation")
        
        # Simulation parameters
        duration = 800  # seconds
        fs = 5.0  # 5 Hz sampling  
        t = np.linspace(0, duration, int(duration * fs))
        
        # ATP production system model
        def atp_production_system(state, t):
            """
            Multi-compartment ATP production model:
            - Mitochondrial ATP synthesis
            - Cytosolic ATP hydrolysis
            - Phosphocreatine shuttle
            - ADP/ATP transport
            """
            (mito_atp, cyto_atp, phosphocreatine, mito_adp, 
             cyto_adp, nadh, oxygen_consumption) = state
            
            # Mitochondrial respiration parameters
            km_adp = 0.05  # mM - ADP affinity
            km_pi = 1.0   # mM - phosphate affinity  
            km_o2 = 0.01  # mM - oxygen affinity
            
            # Oscillatory components
            calcium_oscillation = 1.0 + 0.3 * np.sin(self.metabolic_frequencies['calcium_oscillation'] * 2 * np.pi * t)
            respiratory_oscillation = 1.0 + 0.2 * np.sin(self.metabolic_frequencies['mitochondrial_oscillation'] * 2 * np.pi * t)
            
            # Mitochondrial ATP synthesis (oxidative phosphorylation)
            # Respiratory control - ADP stimulation
            adp_stimulation = mito_adp / (km_adp + mito_adp)
            oxygen_availability = 0.2 / (km_o2 + 0.2)  # Assume 0.2 mM O2
            
            atp_synthesis_rate = (100 * adp_stimulation * oxygen_availability * 
                                respiratory_oscillation * calcium_oscillation)
            
            # ATP synthase reaction: ADP + Pi → ATP
            mito_atp_dot = atp_synthesis_rate - 10 * mito_atp  # ATP export to cytosol
            mito_adp_dot = -atp_synthesis_rate + 10 * mito_atp  # ADP import from cytosol
            
            # Cytosolic ATP dynamics
            atp_import = 10 * mito_atp  # From mitochondria
            atp_hydrolysis = 80 * cyto_atp * calcium_oscillation  # Energy demand
            
            cyto_atp_dot = atp_import - atp_hydrolysis
            cyto_adp_dot = atp_hydrolysis - 10 * cyto_adp  # ADP export to mitochondria
            
            # Phosphocreatine shuttle (energy buffer)
            creatine_kinase_activity = 50
            pc_synthesis = creatine_kinase_activity * cyto_atp * 0.1  # ATP + Creatine → PCr
            pc_hydrolysis = creatine_kinase_activity * phosphocreatine * 0.05  # PCr + ADP → ATP
            
            phosphocreatine_dot = pc_synthesis - pc_hydrolysis
            
            # Update ATP/ADP with phosphocreatine shuttle
            cyto_atp_dot += pc_hydrolysis - pc_synthesis
            cyto_adp_dot += pc_synthesis - pc_hydrolysis
            
            # NADH dynamics (substrate for respiration)
            nadh_production = 30 + 10 * np.sin(0.05 * 2 * np.pi * t)  # From glycolysis/TCA
            nadh_oxidation = atp_synthesis_rate / 3  # 3 NADH per ATP (simplified)
            
            nadh_dot = nadh_production - nadh_oxidation
            
            # Oxygen consumption (coupled to ATP synthesis)
            oxygen_consumption_dot = 0.1 * (atp_synthesis_rate / 6 - oxygen_consumption)  # 6 ATP per O2
            
            return [mito_atp_dot, cyto_atp_dot, phosphocreatine_dot, 
                   mito_adp_dot, cyto_adp_dot, nadh_dot, oxygen_consumption_dot]
        
        # Initial conditions
        initial_state = [
            2.0,  # Mitochondrial ATP (mM)
            5.0,  # Cytosolic ATP (mM)
            25.0, # Phosphocreatine (mM)
            0.5,  # Mitochondrial ADP (mM)
            0.8,  # Cytosolic ADP (mM)
            0.3,  # NADH (mM)
            0.05  # Oxygen consumption (mM/min)
        ]
        
        # Solve ATP production system
        solution = odeint(atp_production_system, initial_state, t)
        mito_atp_trace = solution[:, 0]
        cyto_atp_trace = solution[:, 1]
        phosphocreatine_trace = solution[:, 2]
        mito_adp_trace = solution[:, 3]
        cyto_adp_trace = solution[:, 4]
        nadh_trace = solution[:, 5]
        oxygen_consumption_trace = solution[:, 6]
        
        # Calculate total cellular ATP and energy metrics
        total_atp = mito_atp_trace + cyto_atp_trace
        total_adp = mito_adp_trace + cyto_adp_trace
        
        # Energy charge calculation
        total_amp = np.maximum(0, 10.0 - total_atp - total_adp)  # Conservation
        energy_charge = (total_atp + 0.5 * total_adp) / (total_atp + total_adp + total_amp + 1e-6)
        
        # ATP turnover rate
        atp_synthesis_rate = np.gradient(total_atp, t[1] - t[0])
        atp_hydrolysis_rate = -atp_synthesis_rate  # Conservation
        
        # Phosphocreatine/ATP ratio (energy buffer capacity)
        pcr_atp_ratio = phosphocreatine_trace / (total_atp + 1e-6)
        
        # Respiratory control ratio (state 3/state 4 respiration)
        o2_consumption_max = np.max(oxygen_consumption_trace)
        o2_consumption_min = np.min(oxygen_consumption_trace)
        respiratory_control_ratio = o2_consumption_max / (o2_consumption_min + 1e-6)
        
        # P/O ratio estimation (ATP synthesized per oxygen consumed)
        total_atp_produced = np.trapz(np.maximum(0, atp_synthesis_rate), t)
        total_o2_consumed = np.trapz(oxygen_consumption_trace, t)
        po_ratio = total_atp_produced / (total_o2_consumed + 1e-6)
        
        # Oscillation analysis of ATP production
        atp_signals = {
            'total_atp': total_atp,
            'mitochondrial_atp': mito_atp_trace,
            'cytosolic_atp': cyto_atp_trace,
            'phosphocreatine': phosphocreatine_trace,
            'nadh': nadh_trace,
            'oxygen_consumption': oxygen_consumption_trace
        }
        
        # Frequency domain analysis
        atp_oscillation_metrics = {}
        
        for signal_name, signal_data in atp_signals.items():
            freqs, psd = signal.welch(signal_data, fs=fs, nperseg=512)
            
            # Extract power in different frequency bands
            calcium_band = (0.08, 0.12)  # Ca²⁺ oscillation band
            respiratory_band = (0.04, 0.06)  # Mitochondrial oscillation band
            
            calcium_mask = (freqs >= calcium_band[0]) & (freqs <= calcium_band[1])
            respiratory_mask = (freqs >= respiratory_band[0]) & (freqs <= respiratory_band[1])
            
            total_power = np.trapz(psd, freqs)
            calcium_power = np.trapz(psd[calcium_mask], freqs[calcium_mask]) if np.any(calcium_mask) else 0
            respiratory_power = np.trapz(psd[respiratory_mask], freqs[respiratory_mask]) if np.any(respiratory_mask) else 0
            
            atp_oscillation_metrics[signal_name] = {
                'calcium_band_power': calcium_power / total_power * 100,
                'respiratory_band_power': respiratory_power / total_power * 100,
                'frequencies': freqs,
                'power_spectral_density': psd
            }
        
        # Cross-compartment coupling analysis
        # Mitochondrial-cytosolic ATP coupling
        mito_cyto_atp_coupling = np.corrcoef(mito_atp_trace, cyto_atp_trace)[0, 1]
        
        # ATP-phosphocreatine coupling (energy buffering)
        atp_pcr_coupling = np.corrcoef(total_atp, phosphocreatine_trace)[0, 1]
        
        # NADH-ATP coupling (respiratory coupling)
        nadh_atp_coupling = np.corrcoef(nadh_trace, total_atp)[0, 1]
        
        # ATP-oxygen coupling (oxidative phosphorylation efficiency)
        atp_oxygen_coupling = np.corrcoef(total_atp, oxygen_consumption_trace)[0, 1]
        
        # Energy system stability
        energy_charge_cv = np.std(energy_charge) / np.mean(energy_charge)
        atp_stability = 1.0 / (1.0 + np.std(total_atp) / np.mean(total_atp))
        
        # Theoretical predictions
        theoretical_predictions = {
            'energy_charge_range': (0.8, 0.95),
            'respiratory_control_ratio_min': 3.0,
            'po_ratio_range': (2.0, 3.0),  # ATP per O2
            'mito_cyto_coupling_min': 0.7,
            'atp_pcr_coupling_range': (-0.8, -0.3),  # Inverse buffering relationship
            'nadh_atp_coupling_min': 0.5,
            'calcium_oscillation_power_min': 5.0,  # % of total power
            'energy_charge_cv_max': 0.1
        }
        
        # Validation
        energy_charge_mean = np.mean(energy_charge)
        calcium_power = atp_oscillation_metrics['total_atp']['calcium_band_power']
        
        validation_success = (
            theoretical_predictions['energy_charge_range'][0] <= energy_charge_mean <= 
            theoretical_predictions['energy_charge_range'][1] and
            respiratory_control_ratio >= theoretical_predictions['respiratory_control_ratio_min'] and
            theoretical_predictions['po_ratio_range'][0] <= po_ratio <= 
            theoretical_predictions['po_ratio_range'][1] and
            mito_cyto_atp_coupling >= theoretical_predictions['mito_cyto_coupling_min'] and
            theoretical_predictions['atp_pcr_coupling_range'][0] <= atp_pcr_coupling <= 
            theoretical_predictions['atp_pcr_coupling_range'][1] and
            nadh_atp_coupling >= theoretical_predictions['nadh_atp_coupling_min'] and
            calcium_power >= theoretical_predictions['calcium_oscillation_power_min'] and
            energy_charge_cv <= theoretical_predictions['energy_charge_cv_max']
        )
        
        results = {
            'experiment': 'ATP Production Cycle Validation',
            'validation_success': validation_success,
            'atp_traces': {
                'time': t,
                'mitochondrial_atp': mito_atp_trace,
                'cytosolic_atp': cyto_atp_trace,
                'total_atp': total_atp,
                'phosphocreatine': phosphocreatine_trace,
                'nadh': nadh_trace,
                'oxygen_consumption': oxygen_consumption_trace
            },
            'energy_metrics': {
                'energy_charge': energy_charge,
                'atp_synthesis_rate': atp_synthesis_rate,
                'pcr_atp_ratio': pcr_atp_ratio,
                'respiratory_control_ratio': respiratory_control_ratio,
                'po_ratio': po_ratio
            },
            'oscillation_analysis': atp_oscillation_metrics,
            'coupling_analysis': {
                'mito_cyto_atp_coupling': mito_cyto_atp_coupling,
                'atp_pcr_coupling': atp_pcr_coupling,
                'nadh_atp_coupling': nadh_atp_coupling,
                'atp_oxygen_coupling': atp_oxygen_coupling
            },
            'stability_metrics': {
                'energy_charge_cv': energy_charge_cv,
                'atp_stability': atp_stability,
                'energy_charge_mean': energy_charge_mean
            },
            'theoretical_predictions': theoretical_predictions
        }
        
        # Visualization
        self._plot_atp_production_analysis(results)
        
        return results
    
    def experiment_3_metabolic_network_coupling(self) -> Dict[str, Any]:
        """
        Experiment 3: Metabolic Network Coupling
        
        Validates system-level metabolic oscillations:
        - Glycolysis-TCA cycle coupling
        - Pentose phosphate pathway oscillations
        - Fatty acid oxidation rhythms  
        - Circadian metabolic coupling
        """
        print("🔄 Experiment 3: Metabolic Network Coupling")
        
        # Simulation parameters
        duration = 1800  # 30 minutes
        fs = 1.0  # 1 Hz sampling
        t = np.linspace(0, duration, int(duration * fs))
        
        # Integrated metabolic network model
        def metabolic_network_system(state, t):
            """
            Multi-pathway metabolic network:
            - Glycolysis
            - TCA cycle
            - Pentose phosphate pathway
            - Fatty acid oxidation
            - Circadian regulation
            """
            (glucose, g6p, pyruvate, acetyl_coa, citrate, nadh, 
             nadph, fatty_acids, circadian_clock) = state
            
            # Circadian clock (24-hour rhythm)
            circadian_freq = self.metabolic_frequencies['circadian_metabolic']
            circadian_clock_dot = 2 * np.pi * circadian_freq
            
            # Circadian modulation of metabolism
            circadian_amplitude = np.sin(circadian_clock)
            metabolic_activity = 1.0 + 0.4 * circadian_amplitude
            
            # Energy state feedback
            atp_level = 3.0 + 1.5 * np.sin(0.05 * 2 * np.pi * t)  # Oscillating ATP
            energy_state = atp_level / 3.0  # Normalized energy state
            
            # Glycolytic pathway
            glucose_uptake = 0.1 * metabolic_activity
            hexokinase_activity = 0.8 * (1.0 + 0.3 / (1.0 + energy_state**2))  # ATP inhibition
            
            glucose_dot = glucose_uptake - hexokinase_activity * glucose
            g6p_dot = hexokinase_activity * glucose - 0.5 * g6p * (1.0 + 0.3 * energy_state)
            
            # Glycolytic flux to pyruvate
            glycolytic_flux = 0.5 * g6p * metabolic_activity
            pyruvate_dot = glycolytic_flux - 0.8 * pyruvate
            
            # TCA cycle entry
            pdh_activity = 0.4 * (1.0 + 0.5 * circadian_amplitude)  # Pyruvate dehydrogenase
            acetyl_coa_production = pdh_activity * pyruvate + 0.2 * fatty_acids  # From FA oxidation
            
            acetyl_coa_dot = acetyl_coa_production - 0.6 * acetyl_coa
            
            # TCA cycle
            citrate_synthase_activity = 0.6 * metabolic_activity
            citrate_dot = citrate_synthase_activity * acetyl_coa - 0.4 * citrate
            
            # NADH production (from glycolysis + TCA cycle)
            nadh_production = 0.3 * pyruvate + 0.8 * citrate
            nadh_oxidation = 1.2 * nadh * energy_state  # Respiratory chain
            nadh_dot = nadh_production - nadh_oxidation
            
            # Pentose phosphate pathway (PPP)
            ppp_flux = 0.2 * g6p * (1.0 + 0.5 / (1.0 + energy_state))  # NADPH demand
            
            # NADPH production and consumption
            nadph_production = ppp_flux + 0.1 * citrate  # PPP + malic enzyme
            nadph_consumption = 0.3 * nadph * (1.0 + 0.5 * circadian_amplitude)  # Biosynthesis
            nadph_dot = nadph_production - nadph_consumption
            
            # Fatty acid oxidation
            fa_oxidation_activity = 0.3 * (1.0 - energy_state) * metabolic_activity  # High when ATP low
            fatty_acids_dot = 0.05 - fa_oxidation_activity * fatty_acids
            
            return [glucose_dot, g6p_dot, pyruvate_dot, acetyl_coa_dot, citrate_dot,
                   nadh_dot, nadph_dot, fatty_acids_dot, circadian_clock_dot]
        
        # Initial conditions
        initial_state = [
            5.0,  # Glucose (mM)
            1.0,  # Glucose-6-phosphate (mM)
            0.5,  # Pyruvate (mM)
            0.3,  # Acetyl-CoA (mM)
            0.8,  # Citrate (mM)
            0.4,  # NADH (mM)
            0.2,  # NADPH (mM)
            2.0,  # Fatty acids (mM)
            0.0   # Circadian clock phase
        ]
        
        # Solve metabolic network
        solution = odeint(metabolic_network_system, initial_state, t)
        glucose_trace = solution[:, 0]
        g6p_trace = solution[:, 1]
        pyruvate_trace = solution[:, 2]
        acetyl_coa_trace = solution[:, 3]
        citrate_trace = solution[:, 4]
        nadh_trace = solution[:, 5]
        nadph_trace = solution[:, 6]
        fatty_acids_trace = solution[:, 7]
        circadian_clock_trace = solution[:, 8]
        
        # Calculate metabolic fluxes
        glycolytic_flux = np.gradient(pyruvate_trace, t[1] - t[0])
        tca_flux = np.gradient(citrate_trace, t[1] - t[0])
        fa_oxidation_flux = -np.gradient(fatty_acids_trace, t[1] - t[0])
        
        # Metabolic ratios
        nadh_nadph_ratio = nadh_trace / (nadph_trace + 1e-6)
        citrate_pyruvate_ratio = citrate_trace / (pyruvate_trace + 1e-6)
        
        # Circadian metabolic modulation
        circadian_amplitude = np.sin(circadian_clock_trace)
        
        # Multi-pathway coupling analysis
        metabolic_pathways = {
            'glycolysis': pyruvate_trace,
            'tca_cycle': citrate_trace,
            'ppp': nadph_trace,
            'fa_oxidation': fa_oxidation_flux,
            'circadian': circadian_amplitude
        }
        
        # Cross-pathway correlation matrix
        pathway_coupling_matrix = np.zeros((len(metabolic_pathways), len(metabolic_pathways)))
        pathway_names = list(metabolic_pathways.keys())
        
        for i, path1_name in enumerate(pathway_names):
            for j, path2_name in enumerate(pathway_names):
                path1 = metabolic_pathways[path1_name]
                path2 = metabolic_pathways[path2_name]
                pathway_coupling_matrix[i, j] = np.corrcoef(path1, path2)[0, 1]
        
        # Key metabolic coupling relationships
        glycolysis_tca_coupling = np.corrcoef(pyruvate_trace, citrate_trace)[0, 1]
        nadh_nadph_coupling = np.corrcoef(nadh_trace, nadph_trace)[0, 1]
        circadian_metabolic_coupling = np.corrcoef(circadian_amplitude, pyruvate_trace)[0, 1]
        
        # Metabolic flexibility (ability to switch between fuel sources)
        glucose_dependency = np.mean(pyruvate_trace) / (np.mean(pyruvate_trace) + np.mean(fa_oxidation_flux) + 1e-6)
        fa_dependency = np.mean(fa_oxidation_flux) / (np.mean(pyruvate_trace) + np.mean(fa_oxidation_flux) + 1e-6)
        metabolic_flexibility = 1.0 - abs(glucose_dependency - fa_dependency)  # Balanced = flexible
        
        # Redox balance
        nadh_production_rate = np.mean(np.maximum(0, np.gradient(nadh_trace)))
        nadph_production_rate = np.mean(np.maximum(0, np.gradient(nadph_trace)))
        redox_balance = min(nadh_production_rate, nadph_production_rate) / max(nadh_production_rate, nadph_production_rate)
        
        # Oscillation synchrony across pathways
        from scipy.signal import hilbert
        
        # Calculate phase synchrony between major pathways
        glycolysis_analytic = hilbert(pyruvate_trace - np.mean(pyruvate_trace))
        tca_analytic = hilbert(citrate_trace - np.mean(citrate_trace))
        circadian_analytic = hilbert(circadian_amplitude)
        
        glycolysis_phase = np.angle(glycolysis_analytic)
        tca_phase = np.angle(tca_analytic)
        circadian_phase = np.angle(circadian_analytic)
        
        # Phase coupling strength
        glycolysis_tca_phase_coupling = np.abs(np.mean(np.exp(1j * (glycolysis_phase - tca_phase))))
        circadian_metabolic_phase_coupling = np.abs(np.mean(np.exp(1j * (circadian_phase - glycolysis_phase))))
        
        # Network-level oscillation coherence
        all_phases = [glycolysis_phase, tca_phase, circadian_phase]
        phase_coherence_scores = []
        
        for i in range(len(all_phases)):
            for j in range(i+1, len(all_phases)):
                phase_coupling = np.abs(np.mean(np.exp(1j * (all_phases[i] - all_phases[j]))))
                phase_coherence_scores.append(phase_coupling)
        
        network_phase_coherence = np.mean(phase_coherence_scores)
        
        # Metabolic efficiency metrics
        total_substrate_consumption = np.trapz(glucose_trace, t) + np.trapz(fatty_acids_trace, t)
        total_nadh_production = np.trapz(np.maximum(0, np.gradient(nadh_trace)), t)
        metabolic_efficiency = total_nadh_production / (total_substrate_consumption + 1e-6)
        
        # Theoretical predictions
        theoretical_predictions = {
            'glycolysis_tca_coupling_min': 0.6,
            'circadian_metabolic_coupling_min': 0.4,
            'metabolic_flexibility_min': 0.3,
            'redox_balance_min': 0.7,
            'network_phase_coherence_min': 0.5,
            'nadh_nadph_ratio_range': (1.5, 4.0),
            'metabolic_efficiency_min': 0.1
        }
        
        # Validation
        nadh_nadph_ratio_mean = np.mean(nadh_nadph_ratio)
        
        validation_success = (
            glycolysis_tca_coupling >= theoretical_predictions['glycolysis_tca_coupling_min'] and
            abs(circadian_metabolic_coupling) >= theoretical_predictions['circadian_metabolic_coupling_min'] and
            metabolic_flexibility >= theoretical_predictions['metabolic_flexibility_min'] and
            redox_balance >= theoretical_predictions['redox_balance_min'] and
            network_phase_coherence >= theoretical_predictions['network_phase_coherence_min'] and
            theoretical_predictions['nadh_nadph_ratio_range'][0] <= nadh_nadph_ratio_mean <= 
            theoretical_predictions['nadh_nadph_ratio_range'][1] and
            metabolic_efficiency >= theoretical_predictions['metabolic_efficiency_min']
        )
        
        results = {
            'experiment': 'Metabolic Network Coupling',
            'validation_success': validation_success,
            'metabolic_traces': {
                'time': t,
                'glucose': glucose_trace,
                'pyruvate': pyruvate_trace,
                'citrate': citrate_trace,
                'nadh': nadh_trace,
                'nadph': nadph_trace,
                'fatty_acids': fatty_acids_trace,
                'circadian_amplitude': circadian_amplitude
            },
            'metabolic_fluxes': {
                'glycolytic_flux': glycolytic_flux,
                'tca_flux': tca_flux,
                'fa_oxidation_flux': fa_oxidation_flux
            },
            'metabolic_ratios': {
                'nadh_nadph_ratio': nadh_nadph_ratio,
                'citrate_pyruvate_ratio': citrate_pyruvate_ratio
            },
            'coupling_analysis': {
                'pathway_coupling_matrix': pathway_coupling_matrix,
                'pathway_names': pathway_names,
                'glycolysis_tca_coupling': glycolysis_tca_coupling,
                'nadh_nadph_coupling': nadh_nadph_coupling,
                'circadian_metabolic_coupling': circadian_metabolic_coupling,
                'glycolysis_tca_phase_coupling': glycolysis_tca_phase_coupling,
                'circadian_metabolic_phase_coupling': circadian_metabolic_phase_coupling,
                'network_phase_coherence': network_phase_coherence
            },
            'system_metrics': {
                'metabolic_flexibility': metabolic_flexibility,
                'glucose_dependency': glucose_dependency,
                'fa_dependency': fa_dependency,
                'redox_balance': redox_balance,
                'metabolic_efficiency': metabolic_efficiency,
                'nadh_nadph_ratio_mean': nadh_nadph_ratio_mean
            },
            'theoretical_predictions': theoretical_predictions
        }
        
        # Visualization
        self._plot_metabolic_network_analysis(results)
        
        return results
    
    def _plot_glycolytic_analysis(self, results: Dict[str, Any]):
        """Create glycolytic oscillation analysis visualizations"""
        fig, axes = plt.subplots(3, 3, figsize=(20, 16))
        
        traces = results['metabolite_traces']
        derived = results['derived_metrics']
        oscillation = results['oscillation_analysis']
        
        # Plot 1: Glycolytic metabolites
        axes[0, 0].plot(traces['time'], traces['glucose_6p'], 'blue', 
                       label='Glucose-6-P', linewidth=2)
        axes[0, 0].plot(traces['time'], traces['fructose_6p'], 'green', 
                       label='Fructose-6-P', linewidth=2)
        axes[0, 0].plot(traces['time'], traces['fructose_16bp'], 'red', 
                       label='Fructose-1,6-BP', linewidth=2)
        
        axes[0, 0].set_title('Glycolytic Intermediates')
        axes[0, 0].set_xlabel('Time (s)')
        axes[0, 0].set_ylabel('Concentration (mM)')
        axes[0, 0].legend()
        axes[0, 0].grid(True, alpha=0.3)
        
        # Plot 2: ATP/ADP dynamics
        ax1 = axes[0, 1]
        ax2 = ax1.twinx()
        
        line1 = ax1.plot(traces['time'], traces['atp'], 'red', 
                        linewidth=2, label='ATP')
        line2 = ax1.plot(traces['time'], traces['adp'], 'blue', 
                        linewidth=2, label='ADP')
        line3 = ax2.plot(traces['time'], derived['atp_adp_ratio'], 'green', 
                        linewidth=2, label='ATP/ADP Ratio')
        
        ax1.set_xlabel('Time (s)')
        ax1.set_ylabel('Concentration (mM)', color='black')
        ax2.set_ylabel('ATP/ADP Ratio', color='green')
        ax2.tick_params(axis='y', labelcolor='green')
        
        lines = line1 + line2 + line3
        labels = [l.get_label() for l in lines]
        ax1.legend(lines, labels, loc='upper right')
        ax1.set_title('ATP/ADP Dynamics')
        ax1.grid(True, alpha=0.3)
        
        # Plot 3: NADH and energy charge
        ax1 = axes[0, 2]
        ax2 = ax1.twinx()
        
        line1 = ax1.plot(traces['time'], traces['nadh'], 'purple', 
                        linewidth=2, label='NADH')
        line2 = ax2.plot(traces['time'], derived['energy_charge'], 'orange', 
                        linewidth=2, label='Energy Charge')
        
        ax1.set_xlabel('Time (s)')
        ax1.set_ylabel('NADH (mM)', color='purple')
        ax2.set_ylabel('Energy Charge', color='orange')
        ax1.tick_params(axis='y', labelcolor='purple')
        ax2.tick_params(axis='y', labelcolor='orange')
        
        lines = line1 + line2
        labels = [l.get_label() for l in lines]
        ax1.legend(lines, labels, loc='upper right')
        ax1.set_title('NADH and Energy Charge')
        ax1.grid(True, alpha=0.3)
        
        # Plot 4: Correlation matrix heatmap
        im = axes[1, 0].imshow(oscillation['correlation_matrix'], cmap='RdBu_r', 
                              aspect='auto', vmin=-1, vmax=1)
        axes[1, 0].set_xticks(range(len(oscillation['signal_names'])))
        axes[1, 0].set_yticks(range(len(oscillation['signal_names'])))
        axes[1, 0].set_xticklabels([name.replace('_', '\n') for name in oscillation['signal_names']], 
                                  rotation=45)
        axes[1, 0].set_yticklabels([name.replace('_', '\n') for name in oscillation['signal_names']])
        axes[1, 0].set_title('Metabolite Cross-Correlations')
        plt.colorbar(im, ax=axes[1, 0])
        
        # Plot 5: Power spectra
        atp_metrics = oscillation['oscillation_metrics']['atp']
        axes[1, 1].semilogy(atp_metrics['frequencies'], atp_metrics['power_spectral_density'], 
                           'red', linewidth=2, label='ATP')
        
        flux_metrics = oscillation['oscillation_metrics']['glycolytic_flux']
        axes[1, 1].semilogy(flux_metrics['frequencies'], flux_metrics['power_spectral_density'], 
                           'blue', linewidth=2, label='Glycolytic Flux')
        
        axes[1, 1].set_title('Power Spectral Density')
        axes[1, 1].set_xlabel('Frequency (Hz)')
        axes[1, 1].set_ylabel('PSD')
        axes[1, 1].legend()
        axes[1, 1].grid(True, alpha=0.3)
        axes[1, 1].set_xlim(0, 0.1)
        
        # Plot 6: Oscillation metrics
        signal_names = ['ATP', 'Flux', 'NADH', 'G6P']
        oscillation_strengths = []
        peak_frequencies = []
        
        for sig_name in signal_names:
            key = sig_name.lower().replace(' ', '_')
            if key == 'g6p':
                key = 'glucose_6p'
            elif key == 'flux':
                key = 'glycolytic_flux'
            
            if key in oscillation['oscillation_metrics']:
                metrics = oscillation['oscillation_metrics'][key]
                oscillation_strengths.append(metrics['oscillation_strength'])
                peak_frequencies.append(metrics['peak_frequency'])
            else:
                oscillation_strengths.append(0)
                peak_frequencies.append(0)
        
        x = np.arange(len(signal_names))
        width = 0.35
        
        bars1 = axes[1, 2].bar(x - width/2, oscillation_strengths, width, 
                              label='Oscillation Strength', color='lightblue', alpha=0.7)
        
        ax2 = axes[1, 2].twinx()
        bars2 = ax2.bar(x + width/2, np.array(peak_frequencies)*1000, width, 
                       label='Peak Freq (mHz)', color='lightcoral', alpha=0.7)
        
        axes[1, 2].set_xlabel('Signal')
        axes[1, 2].set_ylabel('Oscillation Strength', color='blue')
        ax2.set_ylabel('Peak Frequency (mHz)', color='red')
        axes[1, 2].set_xticks(x)
        axes[1, 2].set_xticklabels(signal_names)
        axes[1, 2].tick_params(axis='y', labelcolor='blue')
        ax2.tick_params(axis='y', labelcolor='red')
        
        # Combined legend
        lines1, labels1 = axes[1, 2].get_legend_handles_labels()
        lines2, labels2 = ax2.get_legend_handles_labels()
        axes[1, 2].legend(lines1 + lines2, labels1 + labels2, loc='upper right')
        axes[1, 2].set_title('Oscillation Characteristics')
        
        # Plot 7: Glycolytic flux
        axes[2, 0].plot(traces['time'], derived['glycolytic_flux'], 
                       'green', linewidth=2)
        axes[2, 0].fill_between(traces['time'], derived['glycolytic_flux'], 
                               alpha=0.3, color='green')
        axes[2, 0].set_title('Glycolytic Flux')
        axes[2, 0].set_xlabel('Time (s)')
        axes[2, 0].set_ylabel('Flux (mM/s)')
        axes[2, 0].grid(True, alpha=0.3)
        
        # Plot 8: Phase relationships
        coupling_names = ['ATP-ADP\nPhase Coupling', 'Flux-ATP\nPhase Coupling']
        coupling_values = [oscillation['atp_adp_phase_coupling'], 
                          oscillation['flux_atp_phase_coupling']]
        
        bars = axes[2, 1].bar(coupling_names, coupling_values, 
                             color=['red', 'green'], alpha=0.7)
        axes[2, 1].set_title('Phase Coupling Analysis')
        axes[2, 1].set_ylabel('Coupling Strength')
        axes[2, 1].set_ylim(0, 1)
        
        for bar, value in zip(bars, coupling_values):
            height = bar.get_height()
            axes[2, 1].text(bar.get_x() + bar.get_width()/2., height + 0.02,
                           f'{value:.3f}', ha='center', va='bottom')
        
        # Plot 9: Validation summary
        predictions = results['theoretical_predictions']
        stability = results['stability_metrics']
        
        validation_text = (
            f"🍯 GLYCOLYTIC VALIDATION\n\n"
            f"✓ Status: {'PASS' if results['validation_success'] else 'FAIL'}\n\n"
            f"Oscillation Freq: {oscillation['oscillation_metrics']['atp']['peak_frequency']:.3f} Hz\n"
            f"Expected: {predictions['expected_oscillation_frequency']}\n\n"
            f"Energy Charge: {stability['energy_charge_mean']:.3f}\n"
            f"Expected: {predictions['energy_charge_range']}\n\n"
            f"ATP-ADP Coupling: {oscillation['atp_adp_phase_coupling']:.3f}\n"
            f"Required: ≥{predictions['atp_adp_phase_coupling_min']}\n\n"
            f"ATP Variability: {stability['atp_cv']:.3f}\n"
            f"Max Allowed: {predictions['atp_cv_max']}"
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
        plt.savefig(f"{self.results_dir}/glycolytic_oscillation_analysis.png", 
                   dpi=300, bbox_inches='tight')
        plt.close()
    
    def _plot_atp_production_analysis(self, results: Dict[str, Any]):
        """Create ATP production cycle analysis visualizations"""
        fig, axes = plt.subplots(3, 3, figsize=(20, 16))
        
        traces = results['atp_traces']
        energy = results['energy_metrics']
        coupling = results['coupling_analysis']
        oscillation = results['oscillation_analysis']
        stability = results['stability_metrics']
        
        # Plot 1: ATP compartments
        axes[0, 0].plot(traces['time'], traces['mitochondrial_atp'], 'red', 
                       label='Mitochondrial ATP', linewidth=2)
        axes[0, 0].plot(traces['time'], traces['cytosolic_atp'], 'blue', 
                       label='Cytosolic ATP', linewidth=2)
        axes[0, 0].plot(traces['time'], traces['total_atp'], 'black', 
                       label='Total ATP', linewidth=2)
        
        axes[0, 0].set_title('ATP Compartments')
        axes[0, 0].set_xlabel('Time (s)')
        axes[0, 0].set_ylabel('ATP Concentration (mM)')
        axes[0, 0].legend()
        axes[0, 0].grid(True, alpha=0.3)
        
        # Plot 2: Energy systems
        ax1 = axes[0, 1]
        ax2 = ax1.twinx()
        
        line1 = ax1.plot(traces['time'], traces['phosphocreatine'], 'green', 
                        linewidth=2, label='Phosphocreatine')
        line2 = ax2.plot(traces['time'], energy['energy_charge'], 'purple', 
                        linewidth=2, label='Energy Charge')
        
        ax1.set_xlabel('Time (s)')
        ax1.set_ylabel('Phosphocreatine (mM)', color='green')
        ax2.set_ylabel('Energy Charge', color='purple')
        ax1.tick_params(axis='y', labelcolor='green')
        ax2.tick_params(axis='y', labelcolor='purple')
        
        lines = line1 + line2
        labels = [l.get_label() for l in lines]
        ax1.legend(lines, labels, loc='upper right')
        ax1.set_title('Energy Buffer Systems')
        ax1.grid(True, alpha=0.3)
        
        # Plot 3: Respiratory components
        ax1 = axes[0, 2]
        ax2 = ax1.twinx()
        
        line1 = ax1.plot(traces['time'], traces['nadh'], 'orange', 
                        linewidth=2, label='NADH')
        line2 = ax2.plot(traces['time'], traces['oxygen_consumption'], 'blue', 
                        linewidth=2, label='O₂ Consumption')
        
        ax1.set_xlabel('Time (s)')
        ax1.set_ylabel('NADH (mM)', color='orange')
        ax2.set_ylabel('O₂ Consumption (mM/min)', color='blue')
        ax1.tick_params(axis='y', labelcolor='orange')
        ax2.tick_params(axis='y', labelcolor='blue')
        
        lines = line1 + line2
        labels = [l.get_label() for l in lines]
        ax1.legend(lines, labels, loc='upper right')
        ax1.set_title('Respiratory Chain Components')
        ax1.grid(True, alpha=0.3)
        
        # Plot 4: ATP synthesis rate
        axes[1, 0].plot(traces['time'], energy['atp_synthesis_rate'], 
                       'red', linewidth=2)
        axes[1, 0].fill_between(traces['time'], energy['atp_synthesis_rate'], 
                               alpha=0.3, color='red')
        axes[1, 0].set_title('ATP Synthesis Rate')
        axes[1, 0].set_xlabel('Time (s)')
        axes[1, 0].set_ylabel('Synthesis Rate (mM/s)')
        axes[1, 0].grid(True, alpha=0.3)
        
        # Plot 5: ATP power spectra
        total_atp_metrics = oscillation['total_atp']
        o2_metrics = oscillation['oxygen_consumption']
        
        axes[1, 1].semilogy(total_atp_metrics['frequencies'], 
                           total_atp_metrics['power_spectral_density'], 
                           'red', linewidth=2, label='Total ATP')
        axes[1, 1].semilogy(o2_metrics['frequencies'], 
                           o2_metrics['power_spectral_density'], 
                           'blue', linewidth=2, label='O₂ Consumption')
        
        # Highlight calcium oscillation band
        calcium_band = (0.08, 0.12)
        axes[1, 1].axvspan(calcium_band[0], calcium_band[1], alpha=0.2, 
                          color='green', label='Ca²⁺ Band')
        
        axes[1, 1].set_title('ATP Production Power Spectra')
        axes[1, 1].set_xlabel('Frequency (Hz)')
        axes[1, 1].set_ylabel('PSD')
        axes[1, 1].legend()
        axes[1, 1].grid(True, alpha=0.3)
        axes[1, 1].set_xlim(0, 0.2)
        
        # Plot 6: Coupling relationships
        coupling_names = ['Mito-Cyto\nATP', 'ATP-PCr', 'NADH-ATP', 'ATP-O₂']
        coupling_values = [coupling['mito_cyto_atp_coupling'], 
                          coupling['atp_pcr_coupling'],
                          coupling['nadh_atp_coupling'], 
                          coupling['atp_oxygen_coupling']]
        
        colors = ['red', 'green', 'orange', 'blue']
        bars = axes[1, 2].bar(coupling_names, coupling_values, color=colors, alpha=0.7)
        axes[1, 2].set_title('ATP System Coupling')
        axes[1, 2].set_ylabel('Coupling Strength')
        axes[1, 2].set_ylim(-1, 1)
        axes[1, 2].axhline(y=0, color='black', linestyle='--', alpha=0.5)
        
        for bar, value in zip(bars, coupling_values):
            height = bar.get_height()
            axes[1, 2].text(bar.get_x() + bar.get_width()/2., 
                           height + 0.05 if height >= 0 else height - 0.1,
                           f'{value:.3f}', ha='center', va='bottom' if height >= 0 else 'top')
        
        # Plot 7: Energy metrics
        metric_names = ['P/O Ratio', 'RCR', 'Energy Charge', 'ATP Stability']
        metric_values = [energy['po_ratio'], energy['respiratory_control_ratio'], 
                        stability['energy_charge_mean'], stability['atp_stability']]
        
        bars = axes[2, 0].bar(metric_names, metric_values, 
                             color=['gold', 'lightblue', 'lightgreen', 'lightcoral'], alpha=0.7)
        axes[2, 0].set_title('Energy Production Metrics')
        axes[2, 0].set_ylabel('Metric Value')
        axes[2, 0].tick_params(axis='x', rotation=45)
        
        for bar, value in zip(bars, metric_values):
            height = bar.get_height()
            axes[2, 0].text(bar.get_x() + bar.get_width()/2., height + height*0.02,
                           f'{value:.2f}', ha='center', va='bottom')
        
        # Plot 8: PCr/ATP ratio over time
        axes[2, 1].plot(traces['time'], energy['pcr_atp_ratio'], 
                       'green', linewidth=2)
        axes[2, 1].set_title('Phosphocreatine/ATP Ratio')
        axes[2, 1].set_xlabel('Time (s)')
        axes[2, 1].set_ylabel('PCr/ATP Ratio')
        axes[2, 1].grid(True, alpha=0.3)
        
        # Plot 9: Validation summary
        predictions = results['theoretical_predictions']
        
        validation_text = (
            f"⚡ ATP PRODUCTION VALIDATION\n\n"
            f"✓ Status: {'PASS' if results['validation_success'] else 'FAIL'}\n\n"
            f"Energy Charge: {stability['energy_charge_mean']:.3f}\n"
            f"Expected: {predictions['energy_charge_range']}\n\n"
            f"P/O Ratio: {energy['po_ratio']:.2f}\n"
            f"Expected: {predictions['po_ratio_range']}\n\n"
            f"RCR: {energy['respiratory_control_ratio']:.2f}\n"
            f"Required: ≥{predictions['respiratory_control_ratio_min']}\n\n"
            f"Ca²⁺ Oscillation: {oscillation['total_atp']['calcium_band_power']:.1f}%\n"
            f"Required: ≥{predictions['calcium_oscillation_power_min']}%"
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
        plt.savefig(f"{self.results_dir}/atp_production_analysis.png", 
                   dpi=300, bbox_inches='tight')
        plt.close()
    
    def _plot_metabolic_network_analysis(self, results: Dict[str, Any]):
        """Create metabolic network coupling analysis visualizations"""
        fig, axes = plt.subplots(3, 3, figsize=(20, 16))
        
        traces = results['metabolic_traces']
        fluxes = results['metabolic_fluxes']
        ratios = results['metabolic_ratios']
        coupling = results['coupling_analysis']
        system = results['system_metrics']
        
        # Plot 1: Major metabolic pathways
        axes[0, 0].plot(traces['time'], traces['pyruvate'], 'red', 
                       label='Pyruvate (Glycolysis)', linewidth=2)
        axes[0, 0].plot(traces['time'], traces['citrate'], 'blue', 
                       label='Citrate (TCA)', linewidth=2)
        axes[0, 0].plot(traces['time'], traces['fatty_acids'], 'green', 
                       label='Fatty Acids', linewidth=2)
        
        axes[0, 0].set_title('Major Metabolic Pathways')
        axes[0, 0].set_xlabel('Time (s)')
        axes[0, 0].set_ylabel('Concentration (mM)')
        axes[0, 0].legend()
        axes[0, 0].grid(True, alpha=0.3)
        
        # Plot 2: Redox cofactors
        ax1 = axes[0, 1]
        ax2 = ax1.twinx()
        
        line1 = ax1.plot(traces['time'], traces['nadh'], 'purple', 
                        linewidth=2, label='NADH')
        line2 = ax1.plot(traces['time'], traces['nadph'], 'orange', 
                        linewidth=2, label='NADPH')
        line3 = ax2.plot(traces['time'], ratios['nadh_nadph_ratio'], 'black', 
                        linewidth=2, label='NADH/NADPH Ratio')
        
        ax1.set_xlabel('Time (s)')
        ax1.set_ylabel('Concentration (mM)', color='black')
        ax2.set_ylabel('NADH/NADPH Ratio', color='black')
        
        lines = line1 + line2 + line3
        labels = [l.get_label() for l in lines]
        ax1.legend(lines, labels, loc='upper right')
        ax1.set_title('Redox Cofactor Balance')
        ax1.grid(True, alpha=0.3)
        
        # Plot 3: Circadian metabolic modulation
        ax1 = axes[0, 2]
        ax2 = ax1.twinx()
        
        line1 = ax1.plot(traces['time'], traces['pyruvate'], 'red', 
                        linewidth=2, label='Pyruvate')
        line2 = ax2.plot(traces['time'], traces['circadian_amplitude'], 'cyan', 
                        linewidth=2, label='Circadian Amplitude')
        
        ax1.set_xlabel('Time (s)')
        ax1.set_ylabel('Pyruvate (mM)', color='red')
        ax2.set_ylabel('Circadian Amplitude', color='cyan')
        ax1.tick_params(axis='y', labelcolor='red')
        ax2.tick_params(axis='y', labelcolor='cyan')
        
        lines = line1 + line2
        labels = [l.get_label() for l in lines]
        ax1.legend(lines, labels, loc='upper right')
        ax1.set_title('Circadian Metabolic Modulation')
        ax1.grid(True, alpha=0.3)
        
        # Plot 4: Pathway coupling matrix
        im = axes[1, 0].imshow(coupling['pathway_coupling_matrix'], cmap='RdBu_r', 
                              aspect='auto', vmin=-1, vmax=1)
        axes[1, 0].set_xticks(range(len(coupling['pathway_names'])))
        axes[1, 0].set_yticks(range(len(coupling['pathway_names'])))
        axes[1, 0].set_xticklabels([name.replace('_', '\n') for name in coupling['pathway_names']], 
                                  rotation=45)
        axes[1, 0].set_yticklabels([name.replace('_', '\n') for name in coupling['pathway_names']])
        axes[1, 0].set_title('Metabolic Pathway Coupling')
        plt.colorbar(im, ax=axes[1, 0])
        
        # Plot 5: Metabolic fluxes
        axes[1, 1].plot(traces['time'], fluxes['glycolytic_flux'], 'red', 
                       label='Glycolytic Flux', linewidth=2)
        axes[1, 1].plot(traces['time'], fluxes['tca_flux'], 'blue', 
                       label='TCA Flux', linewidth=2)
        axes[1, 1].plot(traces['time'], fluxes['fa_oxidation_flux'], 'green', 
                       label='FA Oxidation Flux', linewidth=2)
        
        axes[1, 1].set_title('Metabolic Fluxes')
        axes[1, 1].set_xlabel('Time (s)')
        axes[1, 1].set_ylabel('Flux (mM/s)')
        axes[1, 1].legend()
        axes[1, 1].grid(True, alpha=0.3)
        
        # Plot 6: Key coupling relationships
        coupling_names = ['Glycolysis-TCA', 'NADH-NADPH', 'Circadian-Metabolic']
        coupling_values = [coupling['glycolysis_tca_coupling'], 
                          coupling['nadh_nadph_coupling'],
                          coupling['circadian_metabolic_coupling']]
        
        bars = axes[1, 2].bar(coupling_names, coupling_values, 
                             color=['red', 'purple', 'cyan'], alpha=0.7)
        axes[1, 2].set_title('Key Metabolic Coupling')
        axes[1, 2].set_ylabel('Coupling Strength')
        axes[1, 2].set_ylim(-1, 1)
        axes[1, 2].axhline(y=0, color='black', linestyle='--', alpha=0.5)
        axes[1, 2].tick_params(axis='x', rotation=45)
        
        for bar, value in zip(bars, coupling_values):
            height = bar.get_height()
            axes[1, 2].text(bar.get_x() + bar.get_width()/2., 
                           height + 0.05 if height >= 0 else height - 0.1,
                           f'{value:.3f}', ha='center', va='bottom' if height >= 0 else 'top')
        
        # Plot 7: Metabolic flexibility
        fuel_names = ['Glucose Dependency', 'FA Dependency', 'Metabolic Flexibility']
        fuel_values = [system['glucose_dependency'], system['fa_dependency'], 
                      system['metabolic_flexibility']]
        
        bars = axes[2, 0].bar(fuel_names, fuel_values, 
                             color=['lightcoral', 'lightgreen', 'gold'], alpha=0.7)
        axes[2, 0].set_title('Metabolic Flexibility')
        axes[2, 0].set_ylabel('Dependency/Flexibility')
        axes[2, 0].set_ylim(0, 1)
        axes[2, 0].tick_params(axis='x', rotation=45)
        
        for bar, value in zip(bars, fuel_values):
            height = bar.get_height()
            axes[2, 0].text(bar.get_x() + bar.get_width()/2., height + 0.02,
                           f'{value:.3f}', ha='center', va='bottom')
        
        # Plot 8: System-level metrics
        system_names = ['Redox Balance', 'Network Coherence', 'Metabolic Efficiency']
        system_values = [system['redox_balance'], coupling['network_phase_coherence'], 
                        system['metabolic_efficiency']]
        
        bars = axes[2, 1].bar(system_names, system_values, 
                             color=['lightblue', 'lightpink', 'lightyellow'], alpha=0.7)
        axes[2, 1].set_title('System-Level Metrics')
        axes[2, 1].set_ylabel('Metric Value')
        axes[2, 1].tick_params(axis='x', rotation=45)
        
        for bar, value in zip(bars, system_values):
            height = bar.get_height()
            axes[2, 1].text(bar.get_x() + bar.get_width()/2., height + height*0.02,
                           f'{value:.3f}', ha='center', va='bottom')
        
        # Plot 9: Validation summary
        predictions = results['theoretical_predictions']
        
        validation_text = (
            f"🔄 METABOLIC NETWORK VALIDATION\n\n"
            f"✓ Status: {'PASS' if results['validation_success'] else 'FAIL'}\n\n"
            f"Glycolysis-TCA: {coupling['glycolysis_tca_coupling']:.3f}\n"
            f"Required: ≥{predictions['glycolysis_tca_coupling_min']}\n\n"
            f"Metabolic Flexibility: {system['metabolic_flexibility']:.3f}\n"
            f"Required: ≥{predictions['metabolic_flexibility_min']}\n\n"
            f"Network Coherence: {coupling['network_phase_coherence']:.3f}\n"
            f"Required: ≥{predictions['network_phase_coherence_min']}\n\n"
            f"NADH/NADPH Ratio: {system['nadh_nadph_ratio_mean']:.2f}\n"
            f"Expected: {predictions['nadh_nadph_ratio_range']}"
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
        plt.savefig(f"{self.results_dir}/metabolic_network_analysis.png", 
                   dpi=300, bbox_inches='tight')
        plt.close()
    
    def run_all_experiments(self) -> Dict[str, Any]:
        """Run all metabolic oscillatory validation experiments"""
        print("🍯 Running Metabolic System Oscillatory Validation Suite")
        print("=" * 60)
        
        all_results = {}
        
        # Run experiments
        all_results['experiment_1'] = self.experiment_1_glycolytic_oscillation_dynamics()
        all_results['experiment_2'] = self.experiment_2_atp_production_cycle_validation()
        all_results['experiment_3'] = self.experiment_3_metabolic_network_coupling()
        
        # Compile validation summary
        validations = [result['validation_success'] for result in all_results.values()]
        overall_success = all(validations)
        
        summary = {
            'domain': 'Metabolic System Oscillations',
            'total_experiments': len(all_results),
            'successful_validations': sum(validations),
            'overall_validation_success': overall_success,
            'timestamp': datetime.now().isoformat(),
            'detailed_results': all_results
        }
        
        # Save comprehensive results
        results_file = f"{self.results_dir}/metabolic_validation_summary.json"
        import json
        with open(results_file, 'w') as f:
            json.dump({k: v for k, v in summary.items() 
                      if k != 'detailed_results'}, f, indent=2)
        
        print(f"\n🍯 Metabolic Validation Complete:")
        print(f"   ✓ Successful: {sum(validations)}/{len(validations)} experiments")
        print(f"   ✓ Overall Status: {'PASS' if overall_success else 'FAIL'}")
        print(f"   ✓ Results saved to: {self.results_dir}/")
        
        self.validation_results = summary
        return summary

def main():
    """Run metabolic oscillatory validation as standalone"""
    validator = MetabolicOscillatoryValidator()
    return validator.run_all_experiments()

if __name__ == "__main__":
    results = main()
    print(f"Metabolic validation completed: {results['overall_validation_success']}")
