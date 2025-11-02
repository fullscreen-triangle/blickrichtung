"""
Comprehensive Tissue Oscillatory Dynamics Validation

This module validates the oscillatory nature of tissue-level processes including:
1. Cell-Cell Communication Oscillatory Networks (Gap junction synchronization)
2. Tissue Integration and Multi-cellular Coordination Rhythms
3. Morphogenetic Oscillatory Patterns (Development and regeneration)
4. Mechanotransduction Oscillatory Responses (Force-induced rhythms)
5. Tissue-Scale Metabolic Oscillations (Coordinated energy production)

Based on the theoretical frameworks for tissue integration and multi-cellular oscillatory coupling
"""

import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
from scipy import signal
from scipy.integrate import solve_ivp
from scipy.spatial.distance import pdist, squareform
from scipy.sparse import csr_matrix
import networkx as nx
from pathlib import Path
import json
import h5py
from collections import defaultdict

class TissueOscillatoryValidator:
    """
    Comprehensive validation of oscillatory dynamics in tissue systems
    """
    
    def __init__(self, results_dir="tissue_validation_results"):
        self.results_dir = Path(results_dir)
        self.results_dir.mkdir(exist_ok=True)
        
        # Tissue-level parameters
        self.cell_density = 1e6  # cells/cm³
        self.tissue_conductivity = 0.1  # S/m (electrical conductivity)
        self.gap_junction_conductance = 1e-9  # S (single gap junction)
        self.tissue_diffusion_coefficient = 1e-6  # cm²/s
        
        # Oscillatory frequency ranges for tissue processes
        self.tissue_frequencies = {
            'cell_cycle_sync': (1e-5, 1e-4),      # Cell cycle synchronization
            'gap_junction': (1e-1, 1e2),          # Gap junction communication
            'mechanical_wave': (1e0, 1e3),        # Mechanical wave propagation
            'metabolic_wave': (1e-3, 1e0),        # Metabolic coordination
            'morphogenetic': (1e-6, 1e-3),        # Developmental patterns
            'calcium_wave': (1e-1, 1e1)           # Calcium signaling waves
        }
        
        # Tissue geometry parameters
        self.tissue_dimensions = (100, 100)  # 100x100 cell grid
        self.cell_spacing = 10e-6  # 10 micrometers between cell centers
        
        # Multi-cellular coordination parameters
        self.coordination_threshold = 0.5  # Synchronization threshold
        self.coupling_strength = 0.1  # Inter-cellular coupling
        
        self.results = {}
        print("🧪 Tissue Oscillatory Dynamics Validator Initialized")
    
    def validate_cell_cell_communication_networks(self):
        """
        EXPERIMENT 1: Validate Cell-Cell Communication Oscillatory Networks
        
        Tests synchronization of cellular oscillations through gap junction
        networks and intercellular signaling pathways.
        """
        print("🔬 EXPERIMENT 1: Cell-Cell Communication Oscillatory Networks")
        
        # Create tissue network with gap junction connectivity
        n_cells = 400  # 20x20 grid for computational efficiency
        grid_size = int(np.sqrt(n_cells))
        
        # Generate cell positions
        cell_positions = []
        for i in range(grid_size):
            for j in range(grid_size):
                x = i * self.cell_spacing + np.random.normal(0, self.cell_spacing * 0.1)
                y = j * self.cell_spacing + np.random.normal(0, self.cell_spacing * 0.1)
                cell_positions.append([x, y])
        
        cell_positions = np.array(cell_positions)
        
        # Create gap junction network (nearest neighbor connectivity)
        gap_junction_network = nx.Graph()
        gap_junction_network.add_nodes_from(range(n_cells))
        
        # Calculate distances between all cell pairs
        distances = squareform(pdist(cell_positions))
        
        # Connect cells within communication range
        communication_range = self.cell_spacing * 1.5  # 1.5x spacing
        
        for i in range(n_cells):
            for j in range(i+1, n_cells):
                if distances[i, j] < communication_range:
                    # Gap junction strength depends on distance
                    strength = self.gap_junction_conductance * np.exp(-distances[i, j] / self.cell_spacing)
                    gap_junction_network.add_edge(i, j, weight=strength, distance=distances[i, j])
        
        # Cellular oscillator dynamics
        def tissue_oscillator_dynamics(t, y):
            # y contains [calcium, voltage] for each cell
            n = n_cells
            calcium = y[:n]
            voltage = y[n:]
            
            dydt = np.zeros_like(y)
            
            for cell_id in range(n):
                # Intrinsic cellular oscillations
                Ca = calcium[cell_id]
                V = voltage[cell_id]
                
                # Calcium dynamics (simplified)
                # Intrinsic oscillation frequency varies between cells
                base_freq = 0.5 + 0.2 * np.sin(2 * np.pi * cell_id / n_cells)  # Spatial frequency variation
                
                dCa_dt = base_freq * np.sin(2 * np.pi * base_freq * t) - 0.1 * Ca
                
                # Voltage dynamics
                dV_dt = -V + 0.5 * Ca
                
                # Gap junction coupling
                neighbors = list(gap_junction_network.neighbors(cell_id))
                
                gap_junction_current = 0
                calcium_diffusion = 0
                
                for neighbor in neighbors:
                    edge_data = gap_junction_network[cell_id][neighbor]
                    conductance = edge_data['weight']
                    
                    # Electrical coupling (voltage)
                    gap_junction_current += conductance * (voltage[neighbor] - V)
                    
                    # Chemical coupling (calcium diffusion)
                    calcium_diffusion += conductance * 1e3 * (calcium[neighbor] - Ca)
                
                # Update derivatives with coupling
                dydt[cell_id] = dCa_dt + calcium_diffusion  # Calcium
                dydt[n + cell_id] = dV_dt + gap_junction_current * 1e6  # Voltage
            
            return dydt
        
        # Initial conditions
        np.random.seed(42)
        initial_calcium = 0.1 + 0.05 * np.random.randn(n_cells)
        initial_voltage = -70e-3 + 5e-3 * np.random.randn(n_cells)  # mV
        y0 = np.concatenate([initial_calcium, initial_voltage])
        
        # Simulate tissue dynamics
        simulation_time = 100.0  # seconds
        t = np.linspace(0, simulation_time, 2000)
        
        sol = solve_ivp(tissue_oscillator_dynamics, [0, simulation_time], y0,
                       t_eval=t, method='RK45', rtol=1e-6)
        
        calcium_history = sol.y[:n_cells]
        voltage_history = sol.y[n_cells:]
        
        # Analyze synchronization
        synchronization_analysis = {}
        
        # Calculate pairwise synchronization
        synchronization_matrix = np.zeros((n_cells, n_cells))
        
        for i in range(n_cells):
            for j in range(i+1, n_cells):
                # Phase synchronization using Hilbert transform
                ca_i = calcium_history[i]
                ca_j = calcium_history[j]
                
                analytic_i = signal.hilbert(ca_i)
                analytic_j = signal.hilbert(ca_j)
                
                phase_i = np.angle(analytic_i)
                phase_j = np.angle(analytic_j)
                
                phase_diff = phase_i - phase_j
                sync_measure = np.abs(np.mean(np.exp(1j * phase_diff)))
                
                synchronization_matrix[i, j] = sync_measure
                synchronization_matrix[j, i] = sync_measure
        
        # Overall tissue synchronization
        mean_synchronization = np.mean(synchronization_matrix[synchronization_matrix > 0])
        
        # Distance-dependent synchronization
        sync_vs_distance = []
        distance_bins = np.linspace(0, communication_range, 10)
        
        for k in range(len(distance_bins)-1):
            d_min, d_max = distance_bins[k], distance_bins[k+1]
            
            sync_values = []
            for i in range(n_cells):
                for j in range(i+1, n_cells):
                    if d_min <= distances[i, j] < d_max:
                        sync_values.append(synchronization_matrix[i, j])
            
            if sync_values:
                sync_vs_distance.append(np.mean(sync_values))
            else:
                sync_vs_distance.append(0)
        
        # Communication efficiency
        # Calculate how effectively signals propagate through tissue
        signal_propagation_speeds = []
        
        # Test signal propagation from random source cells
        for source_cell in np.random.choice(n_cells, 10, replace=False):
            # Find time delays to reach other cells
            source_signal = calcium_history[source_cell]
            
            for target_cell in range(n_cells):
                if target_cell != source_cell and distances[source_cell, target_cell] > 0:
                    target_signal = calcium_history[target_cell]
                    
                    # Cross-correlation to find delay
                    cross_corr = np.correlate(source_signal, target_signal, mode='full')
                    delay_idx = np.argmax(cross_corr) - len(target_signal) + 1
                    delay_time = delay_idx * (t[1] - t[0])
                    
                    if delay_time > 0:
                        propagation_speed = distances[source_cell, target_cell] / delay_time
                        signal_propagation_speeds.append(propagation_speed)
        
        mean_propagation_speed = np.mean(signal_propagation_speeds) if signal_propagation_speeds else 0
        
        # Network analysis
        network_analysis = {
            'n_nodes': gap_junction_network.number_of_nodes(),
            'n_edges': gap_junction_network.number_of_edges(),
            'average_degree': np.mean([d for n, d in gap_junction_network.degree()]),
            'clustering_coefficient': nx.average_clustering(gap_junction_network),
            'average_path_length': nx.average_shortest_path_length(gap_junction_network) if nx.is_connected(gap_junction_network) else float('inf'),
            'is_connected': nx.is_connected(gap_junction_network)
        }
        
        # Oscillation coherence across tissue
        tissue_oscillation_coherence = []
        for freq_range in self.tissue_frequencies.values():
            # Filter signals in frequency range
            freq_coherence_values = []
            
            for i in range(min(n_cells, 50)):  # Sample subset for efficiency
                ca_signal = calcium_history[i]
                
                # FFT analysis
                fft_data = np.fft.fft(ca_signal)
                freqs = np.fft.fftfreq(len(ca_signal), t[1] - t[0])
                power_spectrum = np.abs(fft_data)**2
                
                # Power in frequency range
                freq_mask = (freqs >= freq_range[0]) & (freqs <= freq_range[1])
                if np.any(freq_mask):
                    freq_power = np.sum(power_spectrum[freq_mask])
                    total_power = np.sum(power_spectrum)
                    coherence = freq_power / total_power if total_power > 0 else 0
                    freq_coherence_values.append(coherence)
            
            if freq_coherence_values:
                tissue_oscillation_coherence.append(np.mean(freq_coherence_values))
            else:
                tissue_oscillation_coherence.append(0)
        
        results = {
            'n_cells': n_cells,
            'cell_positions': cell_positions,
            'gap_junction_network': gap_junction_network,
            'simulation_time': simulation_time,
            'time': t,
            'calcium_history': calcium_history,
            'voltage_history': voltage_history,
            'synchronization_matrix': synchronization_matrix,
            'mean_synchronization': mean_synchronization,
            'sync_vs_distance': sync_vs_distance,
            'distance_bins': distance_bins,
            'signal_propagation_speeds': signal_propagation_speeds,
            'mean_propagation_speed': mean_propagation_speed,
            'network_analysis': network_analysis,
            'tissue_oscillation_coherence': tissue_oscillation_coherence,
            'frequency_ranges': list(self.tissue_frequencies.keys()),
            'communication_validated': mean_synchronization > self.coordination_threshold,
            'network_connected': network_analysis['is_connected']
        }
        
        print(f"   ✅ Cells simulated: {n_cells}")
        print(f"   ✅ Mean synchronization: {mean_synchronization:.3f}")
        print(f"   ✅ Network connectivity: {network_analysis['average_degree']:.1f} avg degree")
        print(f"   ✅ Signal propagation speed: {mean_propagation_speed:.2e} m/s")
        print(f"   ✅ Communication validation: {'✅ VALIDATED' if results['communication_validated'] else '❌ FAILED'}")
        
        return results
    
    def validate_morphogenetic_oscillatory_patterns(self):
        """
        EXPERIMENT 2: Validate Morphogenetic Oscillatory Patterns
        
        Tests oscillatory mechanisms in development, pattern formation,
        and tissue regeneration processes.
        """
        print("🔬 EXPERIMENT 2: Morphogenetic Oscillatory Patterns")
        
        # Reaction-diffusion system for pattern formation
        # Based on Turing patterns with oscillatory dynamics
        
        # Spatial grid
        nx, ny = 64, 64  # Grid size
        dx, dy = 1.0, 1.0  # Spatial resolution
        
        # Morphogen concentrations: [activator, inhibitor]
        def morphogenetic_dynamics(t, y):
            n = nx * ny
            activator = y[:n].reshape((nx, ny))
            inhibitor = y[n:].reshape((nx, ny))
            
            # Parameters for Turing system with oscillatory dynamics
            # Oscillatory component varies with time
            oscillation_freq = 0.1  # Hz
            oscillation_amplitude = 0.1
            
            # Time-varying parameters
            a = 0.1 + oscillation_amplitude * np.sin(2 * np.pi * oscillation_freq * t)
            b = 0.9 + oscillation_amplitude * np.cos(2 * np.pi * oscillation_freq * t)
            
            # Diffusion coefficients
            D_a = 1.0  # Activator diffusion
            D_i = 10.0  # Inhibitor diffusion (faster)
            
            # Reaction terms
            reaction_a = a - activator * inhibitor**2
            reaction_i = activator * inhibitor**2 - b * inhibitor
            
            # Diffusion (Laplacian)
            # Using finite differences with periodic boundary conditions
            laplacian_a = np.zeros_like(activator)
            laplacian_i = np.zeros_like(inhibitor)
            
            # Central differences for Laplacian
            laplacian_a[1:-1, 1:-1] = (
                activator[2:, 1:-1] + activator[:-2, 1:-1] +
                activator[1:-1, 2:] + activator[1:-1, :-2] -
                4 * activator[1:-1, 1:-1]
            ) / (dx**2)
            
            laplacian_i[1:-1, 1:-1] = (
                inhibitor[2:, 1:-1] + inhibitor[:-2, 1:-1] +
                inhibitor[1:-1, 2:] + inhibitor[1:-1, :-2] -
                4 * inhibitor[1:-1, 1:-1]
            ) / (dx**2)
            
            # Periodic boundary conditions
            laplacian_a[0, :] = laplacian_a[-2, :]
            laplacian_a[-1, :] = laplacian_a[1, :]
            laplacian_a[:, 0] = laplacian_a[:, -2]
            laplacian_a[:, -1] = laplacian_a[:, 1]
            
            laplacian_i[0, :] = laplacian_i[-2, :]
            laplacian_i[-1, :] = laplacian_i[1, :]
            laplacian_i[:, 0] = laplacian_i[:, -2]
            laplacian_i[:, -1] = laplacian_i[:, 1]
            
            # Rate equations
            dA_dt = reaction_a + D_a * laplacian_a
            dI_dt = reaction_i + D_i * laplacian_i
            
            # Flatten for ODE solver
            return np.concatenate([dA_dt.flatten(), dI_dt.flatten()])
        
        # Initial conditions (small random perturbations)
        np.random.seed(42)
        initial_activator = 1.0 + 0.01 * np.random.randn(nx, ny)
        initial_inhibitor = 1.0 + 0.01 * np.random.randn(nx, ny)
        y0 = np.concatenate([initial_activator.flatten(), initial_inhibitor.flatten()])
        
        # Simulation
        simulation_time = 100.0
        t_eval = np.linspace(0, simulation_time, 200)  # 200 time points
        
        sol = solve_ivp(morphogenetic_dynamics, [0, simulation_time], y0,
                       t_eval=t_eval, method='RK45', rtol=1e-6)
        
        # Extract morphogen evolution
        n_total = nx * ny
        activator_evolution = []
        inhibitor_evolution = []
        
        for i, t_point in enumerate(sol.t):
            activator = sol.y[:n_total, i].reshape((nx, ny))
            inhibitor = sol.y[n_total:, i].reshape((nx, ny))
            
            activator_evolution.append(activator.copy())
            inhibitor_evolution.append(inhibitor.copy())
        
        activator_evolution = np.array(activator_evolution)
        inhibitor_evolution = np.array(inhibitor_evolution)
        
        # Pattern analysis
        pattern_metrics = []
        
        for t_idx in range(len(sol.t)):
            activator_pattern = activator_evolution[t_idx]
            
            # Pattern wavelength analysis using FFT
            fft_2d = np.fft.fft2(activator_pattern)
            power_spectrum_2d = np.abs(fft_2d)**2
            
            # Find dominant spatial frequency
            freq_x = np.fft.fftfreq(nx, dx)
            freq_y = np.fft.fftfreq(ny, dy)
            
            # Radial average of power spectrum
            center_x, center_y = nx // 2, ny // 2
            y_grid, x_grid = np.ogrid[:ny, :nx]
            r = np.sqrt((x_grid - center_x)**2 + (y_grid - center_y)**2)
            
            # Radial profile
            r_max = int(np.max(r))
            radial_profile = np.zeros(r_max)
            
            for radius in range(r_max):
                mask = (r >= radius) & (r < radius + 1)
                if np.any(mask):
                    radial_profile[radius] = np.mean(power_spectrum_2d[mask])
            
            # Find dominant wavelength
            if len(radial_profile) > 1:
                dominant_freq_idx = np.argmax(radial_profile[1:]) + 1  # Exclude DC
                dominant_wavelength = nx / max(dominant_freq_idx, 1)
            else:
                dominant_wavelength = nx
            
            # Pattern contrast (measure of pattern formation)
            pattern_contrast = np.std(activator_pattern) / np.mean(activator_pattern)
            
            # Pattern correlation (spatial organization)
            # Autocorrelation at different lags
            correlation_length = 0
            for lag in range(1, min(10, nx//4)):
                shifted_pattern = np.roll(activator_pattern, lag, axis=0)
                correlation = np.corrcoef(activator_pattern.flatten(), shifted_pattern.flatten())[0, 1]
                if correlation > 0.5:
                    correlation_length = lag
                else:
                    break
            
            pattern_metrics.append({
                'time': sol.t[t_idx],
                'dominant_wavelength': dominant_wavelength,
                'pattern_contrast': pattern_contrast,
                'correlation_length': correlation_length,
                'mean_activator': np.mean(activator_pattern),
                'mean_inhibitor': np.mean(inhibitor_evolution[t_idx])
            })
        
        # Oscillatory pattern analysis
        # Track patterns at specific spatial locations
        spatial_oscillations = {}
        sample_locations = [(nx//4, ny//4), (nx//2, ny//2), (3*nx//4, 3*ny//4)]
        
        for loc_idx, (x, y) in enumerate(sample_locations):
            activator_timeseries = activator_evolution[:, x, y]
            inhibitor_timeseries = inhibitor_evolution[:, x, y]
            
            # FFT analysis of temporal oscillations
            fft_activator = np.fft.fft(activator_timeseries)
            fft_inhibitor = np.fft.fft(inhibitor_timeseries)
            
            temporal_freqs = np.fft.fftfreq(len(sol.t), sol.t[1] - sol.t[0])
            
            power_activator = np.abs(fft_activator)**2
            power_inhibitor = np.abs(fft_inhibitor)**2
            
            # Dominant temporal frequency
            positive_freqs = temporal_freqs[1:len(temporal_freqs)//2]
            positive_power_a = power_activator[1:len(power_activator)//2]
            positive_power_i = power_inhibitor[1:len(power_inhibitor)//2]
            
            if len(positive_power_a) > 0:
                dominant_freq_a = positive_freqs[np.argmax(positive_power_a)]
                dominant_freq_i = positive_freqs[np.argmax(positive_power_i)]
            else:
                dominant_freq_a = 0
                dominant_freq_i = 0
            
            spatial_oscillations[f'location_{loc_idx}'] = {
                'position': (x, y),
                'activator_timeseries': activator_timeseries,
                'inhibitor_timeseries': inhibitor_timeseries,
                'dominant_freq_activator': dominant_freq_a,
                'dominant_freq_inhibitor': dominant_freq_i,
                'oscillation_amplitude_a': np.std(activator_timeseries),
                'oscillation_amplitude_i': np.std(inhibitor_timeseries)
            }
        
        # Pattern formation success criteria
        final_pattern_contrast = pattern_metrics[-1]['pattern_contrast']
        pattern_formation_success = final_pattern_contrast > 0.1
        
        # Oscillatory pattern criteria
        mean_oscillation_freq = np.mean([
            spatial_oscillations[loc]['dominant_freq_activator'] 
            for loc in spatial_oscillations.keys()
        ])
        
        oscillatory_pattern_success = mean_oscillation_freq > 0.01  # > 0.01 Hz
        
        results = {
            'grid_size': (nx, ny),
            'simulation_time': simulation_time,
            'time': sol.t,
            'activator_evolution': activator_evolution,
            'inhibitor_evolution': inhibitor_evolution,
            'pattern_metrics': pattern_metrics,
            'spatial_oscillations': spatial_oscillations,
            'final_pattern_contrast': final_pattern_contrast,
            'pattern_formation_success': pattern_formation_success,
            'mean_oscillation_frequency': mean_oscillation_freq,
            'oscillatory_pattern_success': oscillatory_pattern_success,
            'morphogenetic_validated': pattern_formation_success and oscillatory_pattern_success,
            'sample_locations': sample_locations
        }
        
        print(f"   ✅ Grid size: {nx}×{ny}")
        print(f"   ✅ Pattern contrast: {final_pattern_contrast:.3f}")
        print(f"   ✅ Mean oscillation frequency: {mean_oscillation_freq:.4f} Hz")
        print(f"   ✅ Pattern formation: {'✅ SUCCESS' if pattern_formation_success else '❌ FAILED'}")
        print(f"   ✅ Morphogenetic validation: {'✅ VALIDATED' if results['morphogenetic_validated'] else '❌ FAILED'}")
        
        return results
    
    def validate_mechanotransduction_oscillations(self):
        """
        EXPERIMENT 3: Validate Mechanotransduction Oscillatory Responses
        
        Tests how mechanical forces induce oscillatory responses in tissues
        and how these oscillations coordinate tissue-level behaviors.
        """
        print("🔬 EXPERIMENT 3: Mechanotransduction Oscillatory Responses")
        
        # Tissue mechanical model with cells responding to mechanical forces
        n_cells = 200  # Linear array of cells for simplicity
        cell_spacing = 10e-6  # 10 micrometers
        cell_positions = np.arange(n_cells) * cell_spacing
        
        # Mechanical properties
        cell_stiffness = 1e3  # Pa (cell elastic modulus)
        tissue_damping = 10  # Pa⋅s (tissue viscosity)
        
        # External force application
        def external_force(t, position):
            """Time and position-dependent external force"""
            # Oscillatory force applied at one end
            force_frequency = 2.0  # Hz
            force_amplitude = 1e-6  # N
            
            # Force decreases with distance from application point
            force_decay_length = 50e-6  # 50 micrometers
            spatial_factor = np.exp(-position / force_decay_length)
            
            return force_amplitude * spatial_factor * np.sin(2 * np.pi * force_frequency * t)
        
        # Mechanotransduction dynamics
        def mechanotransduction_dynamics(t, y):
            # State: [displacement, velocity, intracellular_calcium] for each cell
            n = n_cells
            displacement = y[:n]
            velocity = y[n:2*n]
            calcium = y[2*n:]
            
            dydt = np.zeros_like(y)
            
            for i in range(n):
                pos = cell_positions[i]
                
                # Mechanical forces
                # Elastic force from neighboring cells
                elastic_force = 0
                if i > 0:  # Left neighbor
                    spring_extension = displacement[i] - displacement[i-1]
                    elastic_force -= cell_stiffness * spring_extension
                
                if i < n-1:  # Right neighbor
                    spring_extension = displacement[i+1] - displacement[i]
                    elastic_force += cell_stiffness * spring_extension
                
                # Damping force
                damping_force = -tissue_damping * velocity[i]
                
                # External force
                ext_force = external_force(t, pos)
                
                # Total force
                total_force = elastic_force + damping_force + ext_force
                
                # Cell mass (approximate)
                cell_mass = 1e-12  # kg (typical cell mass)
                
                # Newton's law
                acceleration = total_force / cell_mass
                
                # Mechanotransduction: force → calcium
                # Mechanical stress induces calcium release
                mechanical_stress = abs(total_force) / (cell_stiffness * cell_spacing)
                stress_threshold = 1e-3
                
                if mechanical_stress > stress_threshold:
                    calcium_influx = 0.1 * (mechanical_stress - stress_threshold)
                else:
                    calcium_influx = 0
                
                # Calcium dynamics
                calcium_decay = 0.1 * calcium[i]  # Calcium removal
                calcium_oscillation = 0.05 * np.sin(2 * np.pi * 0.5 * t)  # Intrinsic oscillation
                
                dCa_dt = calcium_influx - calcium_decay + calcium_oscillation
                
                # Update derivatives
                dydt[i] = velocity[i]  # dx/dt = v
                dydt[n + i] = acceleration  # dv/dt = a
                dydt[2*n + i] = dCa_dt  # dCa/dt
            
            return dydt
        
        # Initial conditions
        initial_displacement = np.zeros(n_cells)
        initial_velocity = np.zeros(n_cells)
        initial_calcium = 0.1 + 0.01 * np.random.randn(n_cells)
        
        y0 = np.concatenate([initial_displacement, initial_velocity, initial_calcium])
        
        # Simulation
        simulation_time = 10.0  # seconds
        t = np.linspace(0, simulation_time, 2000)
        
        sol = solve_ivp(mechanotransduction_dynamics, [0, simulation_time], y0,
                       t_eval=t, method='RK45', rtol=1e-6)
        
        # Extract results
        displacement_history = sol.y[:n_cells]
        velocity_history = sol.y[n_cells:2*n_cells]
        calcium_history = sol.y[2*n_cells:]
        
        # Analyze mechanical wave propagation
        wave_propagation_analysis = {}
        
        # Find wave propagation speed
        # Track displacement peaks across cells
        displacement_peaks = []
        
        for cell_idx in range(n_cells):
            displacement_signal = displacement_history[cell_idx]
            
            # Find peaks in displacement
            peaks, _ = signal.find_peaks(displacement_signal, height=np.max(displacement_signal) * 0.1)
            
            if len(peaks) > 0:
                # Time of first significant peak
                first_peak_time = t[peaks[0]]
                displacement_peaks.append((cell_idx, first_peak_time))
        
        # Calculate wave speed from peak arrival times
        if len(displacement_peaks) > 1:
            positions = [cell_positions[idx] for idx, _ in displacement_peaks]
            times = [time for _, time in displacement_peaks]
            
            if len(set(times)) > 1:  # Multiple distinct times
                # Linear fit: position = speed * time + offset
                wave_speed_fit = np.polyfit(times, positions, 1)
                wave_speed = wave_speed_fit[0] if len(wave_speed_fit) > 0 else 0
            else:
                wave_speed = 0
        else:
            wave_speed = 0
        
        # Mechanotransduction efficiency
        # Correlation between mechanical stress and calcium response
        mechanotransduction_correlations = []
        
        for cell_idx in range(n_cells):
            # Calculate mechanical stress time series
            if cell_idx > 0 and cell_idx < n_cells - 1:
                strain = np.gradient(displacement_history[cell_idx])  # Approximation of strain
                stress = cell_stiffness * strain
            else:
                stress = np.zeros_like(t)
            
            calcium_signal = calcium_history[cell_idx]
            
            # Cross-correlation
            if np.std(stress) > 0 and np.std(calcium_signal) > 0:
                correlation = np.corrcoef(stress, calcium_signal)[0, 1]
                mechanotransduction_correlations.append(abs(correlation))
            else:
                mechanotransduction_correlations.append(0)
        
        mean_mechanotransduction_efficiency = np.mean(mechanotransduction_correlations)
        
        # Oscillatory response analysis
        oscillatory_responses = {}
        
        for cell_idx in [0, n_cells//4, n_cells//2, 3*n_cells//4, n_cells-1]:
            displacement_signal = displacement_history[cell_idx]
            calcium_signal = calcium_history[cell_idx]
            
            # FFT analysis
            fft_disp = np.fft.fft(displacement_signal)
            fft_ca = np.fft.fft(calcium_signal)
            
            freqs = np.fft.fftfreq(len(displacement_signal), t[1] - t[0])
            
            power_disp = np.abs(fft_disp)**2
            power_ca = np.abs(fft_ca)**2
            
            # Dominant frequencies
            positive_freqs = freqs[1:len(freqs)//2]
            positive_power_disp = power_disp[1:len(power_disp)//2]
            positive_power_ca = power_ca[1:len(power_ca)//2]
            
            if len(positive_power_disp) > 0:
                dominant_freq_disp = positive_freqs[np.argmax(positive_power_disp)]
                dominant_freq_ca = positive_freqs[np.argmax(positive_power_ca)]
            else:
                dominant_freq_disp = 0
                dominant_freq_ca = 0
            
            # Oscillation amplitudes
            disp_amplitude = np.std(displacement_signal)
            ca_amplitude = np.std(calcium_signal)
            
            oscillatory_responses[f'cell_{cell_idx}'] = {
                'position': cell_positions[cell_idx],
                'dominant_freq_displacement': dominant_freq_disp,
                'dominant_freq_calcium': dominant_freq_ca,
                'displacement_amplitude': disp_amplitude,
                'calcium_amplitude': ca_amplitude,
                'mechanotransduction_correlation': mechanotransduction_correlations[cell_idx] if cell_idx < len(mechanotransduction_correlations) else 0
            }
        
        # Tissue-level coordination
        # Calculate phase relationships between distant cells
        phase_coordination = []
        
        for i in range(0, n_cells, n_cells//10):  # Sample every 10% of tissue
            for j in range(i + n_cells//5, n_cells, n_cells//10):  # Compare with distant cells
                if j < n_cells:
                    # Phase analysis using Hilbert transform
                    signal_i = calcium_history[i]
                    signal_j = calcium_history[j]
                    
                    analytic_i = signal.hilbert(signal_i)
                    analytic_j = signal.hilbert(signal_j)
                    
                    phase_i = np.angle(analytic_i)
                    phase_j = np.angle(analytic_j)
                    
                    phase_diff = phase_i - phase_j
                    phase_coherence = np.abs(np.mean(np.exp(1j * phase_diff)))
                    
                    distance = abs(cell_positions[j] - cell_positions[i])
                    phase_coordination.append((distance, phase_coherence))
        
        # Calculate mean tissue coordination
        if phase_coordination:
            distances, coherences = zip(*phase_coordination)
            mean_tissue_coordination = np.mean(coherences)
        else:
            mean_tissue_coordination = 0
        
        results = {
            'n_cells': n_cells,
            'cell_positions': cell_positions,
            'simulation_time': simulation_time,
            'time': t,
            'displacement_history': displacement_history,
            'velocity_history': velocity_history,
            'calcium_history': calcium_history,
            'wave_speed': wave_speed,
            'mechanotransduction_correlations': mechanotransduction_correlations,
            'mean_mechanotransduction_efficiency': mean_mechanotransduction_efficiency,
            'oscillatory_responses': oscillatory_responses,
            'phase_coordination': phase_coordination,
            'mean_tissue_coordination': mean_tissue_coordination,
            'mechanical_wave_validated': wave_speed > 0,
            'mechanotransduction_validated': mean_mechanotransduction_efficiency > 0.3,
            'tissue_coordination_validated': mean_tissue_coordination > 0.3
        }
        
        print(f"   ✅ Cells simulated: {n_cells}")
        print(f"   ✅ Wave propagation speed: {wave_speed:.2e} m/s")
        print(f"   ✅ Mechanotransduction efficiency: {mean_mechanotransduction_efficiency:.3f}")
        print(f"   ✅ Tissue coordination: {mean_tissue_coordination:.3f}")
        print(f"   ✅ Mechanotransduction validation: {'✅ VALIDATED' if results['mechanotransduction_validated'] else '❌ FAILED'}")
        
        return results
    
    def run_comprehensive_tissue_validation(self):
        """
        Run all tissue oscillatory validation experiments
        """
        print("\n🧪 COMPREHENSIVE TISSUE OSCILLATORY VALIDATION")
        print("="*55)
        
        # Run all experiments
        exp1_results = self.validate_cell_cell_communication_networks()
        exp2_results = self.validate_morphogenetic_oscillatory_patterns()
        exp3_results = self.validate_mechanotransduction_oscillations()
        
        # Store results
        self.results = {
            'cell_communication_networks': exp1_results,
            'morphogenetic_patterns': exp2_results,
            'mechanotransduction_oscillations': exp3_results
        }
        
        # Generate visualizations
        self._generate_tissue_visualizations()
        
        # Save results
        self._save_results()
        
        print(f"\n🌟 Tissue validation completed! Results saved in: {self.results_dir}")
        
        return self.results
    
    def _generate_tissue_visualizations(self):
        """Generate comprehensive visualizations for all tissue experiments"""
        fig, axes = plt.subplots(3, 3, figsize=(18, 15))
        fig.suptitle('Tissue Oscillatory Dynamics - Comprehensive Validation', fontsize=16, fontweight='bold')
        
        # Experiment 1: Cell Communication Networks
        exp1 = self.results['cell_communication_networks']
        
        # Network visualization
        ax1 = axes[0, 0]
        G = exp1['gap_junction_network']
        pos = {i: tuple(exp1['cell_positions'][i]) for i in range(exp1['n_cells'])}
        
        # Sample subset for visualization
        sample_nodes = list(range(0, exp1['n_cells'], max(1, exp1['n_cells']//50)))
        G_sample = G.subgraph(sample_nodes)
        pos_sample = {node: pos[node] for node in sample_nodes}
        
        nx.draw(G_sample, pos_sample, ax=ax1, node_size=10, node_color='lightblue',
                edge_color='gray', alpha=0.7, with_labels=False)
        ax1.set_title('Gap Junction Network')
        ax1.set_xlabel('Position (m)')
        ax1.set_ylabel('Position (m)')
        
        # Synchronization matrix
        ax2 = axes[0, 1]
        sync_matrix_sample = exp1['synchronization_matrix'][:50, :50]  # Sample for visualization
        im = ax2.imshow(sync_matrix_sample, cmap='viridis', aspect='auto')
        ax2.set_title('Cell Synchronization Matrix')
        ax2.set_xlabel('Cell Index')
        ax2.set_ylabel('Cell Index')
        plt.colorbar(im, ax=ax2)
        
        # Synchronization vs distance
        ax3 = axes[0, 2]
        distance_centers = (exp1['distance_bins'][:-1] + exp1['distance_bins'][1:]) / 2
        ax3.plot(distance_centers * 1e6, exp1['sync_vs_distance'], 'o-', linewidth=2, markersize=6)
        ax3.set_xlabel('Distance (μm)')
        ax3.set_ylabel('Synchronization')
        ax3.set_title('Synchronization vs Distance')
        ax3.grid(True, alpha=0.3)
        
        # Experiment 2: Morphogenetic Patterns
        exp2 = self.results['morphogenetic_patterns']
        
        # Final pattern
        ax4 = axes[1, 0]
        final_activator = exp2['activator_evolution'][-1]
        im = ax4.imshow(final_activator, cmap='RdYlBu', aspect='auto')
        ax4.set_title('Final Morphogenetic Pattern')
        ax4.set_xlabel('X Position')
        ax4.set_ylabel('Y Position')
        plt.colorbar(im, ax=ax4)
        
        # Pattern evolution metrics
        ax5 = axes[1, 1]
        pattern_times = [m['time'] for m in exp2['pattern_metrics']]
        pattern_contrasts = [m['pattern_contrast'] for m in exp2['pattern_metrics']]
        wavelengths = [m['dominant_wavelength'] for m in exp2['pattern_metrics']]
        
        ax5_twin = ax5.twinx()
        
        line1 = ax5.plot(pattern_times, pattern_contrasts, 'b-', label='Pattern Contrast', linewidth=2)
        line2 = ax5_twin.plot(pattern_times, wavelengths, 'r-', label='Wavelength', linewidth=2)
        
        ax5.set_xlabel('Time (s)')
        ax5.set_ylabel('Pattern Contrast', color='b')
        ax5_twin.set_ylabel('Dominant Wavelength', color='r')
        ax5.set_title('Pattern Evolution Metrics')
        ax5.grid(True, alpha=0.3)
        
        # Spatial oscillations
        ax6 = axes[1, 2]
        for loc_name, data in exp2['spatial_oscillations'].items():
            ax6.plot(exp2['time'], data['activator_timeseries'], 
                    label=f'{loc_name}', alpha=0.8)
        ax6.set_xlabel('Time (s)')
        ax6.set_ylabel('Activator Concentration')
        ax6.set_title('Temporal Oscillations at Different Locations')
        ax6.legend()
        ax6.grid(True, alpha=0.3)
        
        # Experiment 3: Mechanotransduction
        exp3 = self.results['mechanotransduction_oscillations']
        
        # Mechanical wave propagation
        ax7 = axes[2, 0]
        positions_mm = exp3['cell_positions'] * 1e3  # Convert to mm
        time_subset = exp3['time'][:500]  # First portion of simulation
        
        # Show displacement evolution for sample of cells
        for cell_idx in range(0, exp3['n_cells'], exp3['n_cells']//5):
            displacement_data = exp3['displacement_history'][cell_idx, :500] * 1e6  # Convert to μm
            ax7.plot(time_subset, displacement_data, 
                    label=f'Cell {cell_idx}', alpha=0.8)
        
        ax7.set_xlabel('Time (s)')
        ax7.set_ylabel('Displacement (μm)')
        ax7.set_title('Mechanical Wave Propagation')
        ax7.legend()
        ax7.grid(True, alpha=0.3)
        
        # Mechanotransduction efficiency
        ax8 = axes[2, 1]
        cell_indices = range(len(exp3['mechanotransduction_correlations']))
        ax8.plot(cell_indices, exp3['mechanotransduction_correlations'], 'o-', alpha=0.8)
        ax8.set_xlabel('Cell Index')
        ax8.set_ylabel('Stress-Calcium Correlation')
        ax8.set_title('Mechanotransduction Efficiency')
        ax8.grid(True, alpha=0.3)
        
        # Phase coordination vs distance
        ax9 = axes[2, 2]
        if exp3['phase_coordination']:
            distances, coherences = zip(*exp3['phase_coordination'])
            distances_um = np.array(distances) * 1e6  # Convert to μm
            
            ax9.scatter(distances_um, coherences, alpha=0.6, s=30)
            ax9.set_xlabel('Distance (μm)')
            ax9.set_ylabel('Phase Coherence')
            ax9.set_title('Tissue Phase Coordination')
            ax9.grid(True, alpha=0.3)
        
        plt.tight_layout()
        plt.savefig(self.results_dir / 'tissue_validation_comprehensive.png', 
                   dpi=300, bbox_inches='tight')
        plt.close()
        
        print("   📊 Comprehensive tissue visualizations generated")
    
    def _save_results(self):
        """Save all results to files"""
        # Prepare JSON-serializable results
        json_results = {}
        for key, value in self.results.items():
            json_results[key] = {}
            for subkey, subvalue in value.items():
                if isinstance(subvalue, np.ndarray):
                    json_results[key][subkey] = f"Array shape: {subvalue.shape}"
                elif isinstance(subvalue, dict):
                    nested_dict = {}
                    for k, v in subvalue.items():
                        if isinstance(v, np.ndarray):
                            nested_dict[k] = f"Array shape: {v.shape}"
                        elif isinstance(v, dict):
                            nested_dict[k] = {kk: (f"Array shape: {vv.shape}" if isinstance(vv, np.ndarray) 
                                                   else float(vv) if isinstance(vv, np.number) 
                                                   else vv) for kk, vv in v.items()}
                        elif isinstance(v, (list, tuple)) and len(v) > 0 and isinstance(v[0], (tuple, list)):
                            nested_dict[k] = f"List of {len(v)} coordinate tuples"
                        else:
                            nested_dict[k] = float(v) if isinstance(v, np.number) else v
                    json_results[key][subkey] = nested_dict
                elif isinstance(subvalue, (nx.Graph, nx.DiGraph)):
                    json_results[key][subkey] = f"NetworkX graph with {len(subvalue.nodes())} nodes"
                elif isinstance(subvalue, list) and len(subvalue) > 0 and isinstance(subvalue[0], dict):
                    json_results[key][subkey] = f"List of {len(subvalue)} result objects"
                else:
                    json_results[key][subkey] = float(subvalue) if isinstance(subvalue, np.number) else subvalue
        
        with open(self.results_dir / 'tissue_validation_summary.json', 'w') as f:
            json.dump(json_results, f, indent=2)
        
        # Save detailed numerical results as HDF5
        with h5py.File(self.results_dir / 'tissue_validation_detailed.h5', 'w') as f:
            for exp_name, exp_results in self.results.items():
                group = f.create_group(exp_name)
                for key, value in exp_results.items():
                    if isinstance(value, np.ndarray):
                        group.create_dataset(key, data=value)
                    elif isinstance(value, (int, float, bool)):
                        group.attrs[key] = value
                    elif isinstance(value, str):
                        group.attrs[key] = value
        
        print("   💾 Results saved to JSON and HDF5 files")

if __name__ == "__main__":
    validator = TissueOscillatoryValidator()
    results = validator.run_comprehensive_tissue_validation()
    
    print("\n🧪 TISSUE VALIDATION SUMMARY:")
    print(f"Cell Communication Networks: {'✅ VALIDATED' if results['cell_communication_networks']['communication_validated'] else '❌ FAILED'}")
    print(f"Morphogenetic Patterns: {'✅ VALIDATED' if results['morphogenetic_patterns']['morphogenetic_validated'] else '❌ FAILED'}")
    print(f"Mechanotransduction Oscillations: {'✅ VALIDATED' if results['mechanotransduction_oscillations']['mechanotransduction_validated'] else '❌ FAILED'}")
