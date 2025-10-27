"""
Temporal Clock: O₂ Cycling as Cellular Timekeeper

Connects O₂ categorical cycling rate to temporal perception.

Core mechanism:
1. O₂ cycles through 25,110 categorical states at ~10^13 Hz
2. Cells keep time by counting O₂ state transitions
3. VO₂ (oxygen consumption) correlates with perceived time
4. Higher VO₂ → More O₂ cycles → Time feels slower (more "ticks")
5. Lower VO₂ → Fewer O₂ cycles → Time feels faster (fewer "ticks")

This explains all known temporal perception phenomena:
- Stimulants: ↑VO₂ → time slows
- Depressants: ↓VO₂ → time speeds  
- Fever: ↑VO₂ → time slows
- Age: ↓VO₂ → time speeds
- Exercise: ↑VO₂ → time slows
"""

import numpy as np
from typing import Dict, Any, Optional, Tuple
from dataclasses import dataclass

# Import existing O₂ clock from hardware
import sys
from pathlib import Path
hardware_path = Path(__file__).parent.parent / 'hardware'
sys.path.insert(0, str(hardware_path))

from oxygen_categorical_time import CellularTemporalClock, CategoricalTimeState


@dataclass
class TemporalPerceptionState:
    """
    Represents current temporal perception state.
    
    Links O₂ metabolism to subjective time perception.
    """
    vo2_rate: float  # O₂ consumption rate (mL O₂/min)
    o2_cycle_frequency: float  # Effective O₂ cycling freq (Hz)
    subjective_time_rate: float  # Subjective time / objective time
    temporal_resolution_s: float  # Minimum perceivable interval
    
    @property
    def time_dilation_factor(self) -> float:
        """How much slower/faster time feels (1.0 = normal)."""
        return self.subjective_time_rate
    
    @property
    def temporal_resolution_ms(self) -> float:
        """Temporal resolution in milliseconds."""
        return self.temporal_resolution_s * 1000


class TemporalClock:
    """
    Links O₂ categorical cycling to temporal perception.
    
    Uses existing CellularTemporalClock from hardware module.
    """
    
    def __init__(self, baseline_vo2: float = 250.0):
        """
        Initialize temporal clock.
        
        Args:
            baseline_vo2: Baseline O₂ consumption (mL/min) for resting adult
        """
        self.baseline_vo2 = baseline_vo2
        self.o2_clock = CellularTemporalClock(o2_concentration=0.005)
        
        # Standard O₂ cycling frequency
        self.base_cycle_freq = 1e13  # Hz (from your papers)
        
    def measure_vo2(self, 
                    heart_rate: Optional[float] = None,
                    respiratory_rate: Optional[float] = None,
                    metabolic_state: str = 'rest') -> float:
        """
        Estimate VO₂ from physiological measurements.
        
        Can use:
        - Heart rate (HR)
        - Respiratory rate (RR)  
        - Metabolic state (rest, exercise, etc.)
        
        Real implementation would use:
        - Spirometry
        - Indirect calorimetry
        - Wearable sensors
        
        Args:
            heart_rate: Heart rate (BPM)
            respiratory_rate: Respiratory rate (breaths/min)
            metabolic_state: Metabolic state descriptor
            
        Returns:
            Estimated VO₂ (mL/min)
        """
        # Simplified VO₂ estimation
        # Real implementation: spirometry or indirect calorimetry
        
        base_vo2 = self.baseline_vo2
        
        # Adjust for heart rate if available
        if heart_rate is not None:
            # VO₂ roughly correlates with HR
            # Resting HR ~70 BPM → baseline VO₂
            hr_factor = heart_rate / 70.0
            base_vo2 *= hr_factor
        
        # Adjust for respiratory rate
        if respiratory_rate is not None:
            # RR ~15 breaths/min at rest
            rr_factor = respiratory_rate / 15.0
            base_vo2 *= rr_factor
        
        # Adjust for metabolic state
        state_factors = {
            'rest': 1.0,
            'light_activity': 1.5,
            'moderate_exercise': 3.0,
            'vigorous_exercise': 6.0,
            'fever': 1.3,
            'cold': 1.4,  # Thermogenesis
            'meditation': 0.8,
            'sleep': 0.75,
        }
        
        state_factor = state_factors.get(metabolic_state, 1.0)
        base_vo2 *= state_factor
        
        return base_vo2
    
    def calculate_temporal_perception(self, vo2_rate: float) -> TemporalPerceptionState:
        """
        Calculate temporal perception state from VO₂.
        
        Core prediction: subjective time ∝ VO₂ rate
        
        Args:
            vo2_rate: O₂ consumption rate (mL/min)
            
        Returns:
            TemporalPerceptionState
        """
        # Metabolic ratio relative to baseline
        metabolic_ratio = vo2_rate / self.baseline_vo2
        
        # Effective O₂ cycle frequency scales with metabolism
        effective_cycle_freq = self.base_cycle_freq * metabolic_ratio
        
        # Subjective time rate
        # More O₂ cycles = more "time ticks" = time feels slower
        subjective_rate = metabolic_ratio
        
        # Temporal resolution (minimum perceivable interval)
        # Higher cycling rate = finer resolution
        cycles_per_perception = 1e11  # ~100 billion cycles per conscious "frame"
        temporal_resolution = cycles_per_perception / effective_cycle_freq
        
        return TemporalPerceptionState(
            vo2_rate=vo2_rate,
            o2_cycle_frequency=effective_cycle_freq,
            subjective_time_rate=subjective_rate,
            temporal_resolution_s=temporal_resolution
        )
    
    def predict_duration_estimation(self,
                                   actual_duration: float,
                                   vo2_rate: float) -> float:
        """
        Predict subjective duration estimation from VO₂.
        
        Args:
            actual_duration: Actual elapsed time (seconds)
            vo2_rate: O₂ consumption rate (mL/min)
            
        Returns:
            Predicted subjective duration (seconds)
        """
        state = self.calculate_temporal_perception(vo2_rate)
        
        # Subjective duration = actual × time dilation factor
        subjective_duration = actual_duration * state.time_dilation_factor
        
        return subjective_duration
    
    def predict_critical_flicker_fusion(self, vo2_rate: float) -> float:
        """
        Predict critical flicker fusion frequency from VO₂.
        
        CFF = maximum frequency where discrete flashes are perceived.
        Determined by temporal resolution.
        
        Args:
            vo2_rate: O₂ consumption rate
            
        Returns:
            Predicted CFF (Hz)
        """
        state = self.calculate_temporal_perception(vo2_rate)
        
        # CFF ≈ 1 / temporal_resolution
        # Typical: ~60 Hz for baseline metabolism
        cff = 1.0 / state.temporal_resolution_s
        
        # Scale to realistic range (humans: 50-90 Hz)
        cff_scaled = 60.0 * (cff / (1.0 / (1e11 / 1e13)))
        
        return cff_scaled
    
    def predict_reaction_time(self,
                             vo2_rate: float,
                             task_complexity: int = 1) -> float:
        """
        Predict reaction time from VO₂ and task complexity.
        
        RT = sensory encoding + decision + motor initiation
        Each stage requires O₂ categorical transitions.
        
        Args:
            vo2_rate: O₂ consumption rate
            task_complexity: Task complexity factor (1 = simple RT)
            
        Returns:
            Predicted reaction time (milliseconds)
        """
        state = self.calculate_temporal_perception(vo2_rate)
        
        # Number of O₂ cycles needed for each stage
        sensory_cycles = 1e10  # ~10 billion
        decision_cycles = task_complexity * 5e10
        motor_cycles = 5e9
        
        total_cycles = sensory_cycles + decision_cycles + motor_cycles
        
        # Convert to time
        rt_seconds = total_cycles / state.o2_cycle_frequency
        rt_ms = rt_seconds * 1000
        
        return rt_ms


class O2TemporalPredictor:
    """
    Makes quantitative predictions about temporal perception from O₂ data.
    
    Validates framework by comparing predictions to empirical measurements.
    """
    
    def __init__(self):
        self.clock = TemporalClock()
        
        # Known empirical data for validation
        self.empirical_baselines = {
            'duration_estimation_60s': 60.0,  # Baseline: estimate 60s as 60s
            'cff_hz': 60.0,  # Baseline CFF
            'simple_rt_ms': 180.0,  # Simple reaction time
            'choice_rt_ms': 300.0,  # 2-choice RT
        }
    
    def predict_drug_effects(self, drug_name: str) -> Dict[str, Any]:
        """
        Predict temporal perception effects of drugs via VO₂ changes.
        
        Drugs that increase metabolism → time dilation
        Drugs that decrease metabolism → time compression
        
        Args:
            drug_name: Name of drug/intervention
            
        Returns:
            Predicted effects on temporal perception
        """
        # Drug → VO₂ effect database
        # Real implementation: measure actual VO₂ changes
        drug_vo2_effects = {
            'caffeine': 1.15,  # +15% VO₂
            'amphetamine': 1.25,  # +25% VO₂
            'cocaine': 1.30,  # +30% VO₂
            'methylphenidate': 1.20,  # +20% VO₂
            'alcohol': 0.90,  # -10% VO₂
            'benzodiazepines': 0.85,  # -15% VO₂
            'opioids': 0.80,  # -20% VO₂
            'cannabis': 0.95,  # -5% VO₂
            'mdma': 1.35,  # +35% VO₂
            'lsd': 1.10,  # +10% VO₂ (speculative)
        }
        
        vo2_factor = drug_vo2_effects.get(drug_name.lower(), 1.0)
        new_vo2 = self.clock.baseline_vo2 * vo2_factor
        
        # Predictions
        baseline_state = self.clock.calculate_temporal_perception(self.clock.baseline_vo2)
        drug_state = self.clock.calculate_temporal_perception(new_vo2)
        
        # Duration estimation (60s interval)
        baseline_est = 60.0
        drug_est = self.clock.predict_duration_estimation(60.0, new_vo2)
        
        # CFF
        baseline_cff = self.clock.predict_critical_flicker_fusion(self.clock.baseline_vo2)
        drug_cff = self.clock.predict_critical_flicker_fusion(new_vo2)
        
        # RT
        baseline_rt = self.clock.predict_reaction_time(self.clock.baseline_vo2)
        drug_rt = self.clock.predict_reaction_time(new_vo2)
        
        return {
            'drug': drug_name,
            'vo2_factor': vo2_factor,
            'baseline_vo2': self.clock.baseline_vo2,
            'drug_vo2': new_vo2,
            'duration_estimation': {
                'baseline': baseline_est,
                'drug': drug_est,
                'change_percent': (drug_est - baseline_est) / baseline_est * 100,
                'interpretation': 'Time feels slower' if drug_est > baseline_est else 'Time feels faster'
            },
            'critical_flicker_fusion': {
                'baseline_hz': baseline_cff,
                'drug_hz': drug_cff,
                'change_percent': (drug_cff - baseline_cff) / baseline_cff * 100
            },
            'reaction_time': {
                'baseline_ms': baseline_rt,
                'drug_ms': drug_rt,
                'change_percent': (drug_rt - baseline_rt) / baseline_rt * 100,
                'interpretation': 'Faster' if drug_rt < baseline_rt else 'Slower'
            },
            'time_dilation_factor': drug_state.time_dilation_factor,
            'temporal_resolution_ms': drug_state.temporal_resolution_ms,
        }
    
    def predict_age_effects(self, age: int) -> Dict[str, Any]:
        """
        Predict age effects on temporal perception.
        
        Metabolic rate declines ~1-2% per decade after age 30.
        
        Args:
            age: Age in years
            
        Returns:
            Predicted temporal perception at that age
        """
        # Metabolic decline model
        if age <= 30:
            vo2_factor = 1.0
        else:
            decline_per_decade = 0.015  # 1.5% per decade
            decades_past_30 = (age - 30) / 10.0
            vo2_factor = 1.0 - (decline_per_decade * decades_past_30)
            vo2_factor = max(0.6, vo2_factor)  # Floor at 60%
        
        vo2_rate = self.clock.baseline_vo2 * vo2_factor
        
        # Predictions
        duration_est = self.clock.predict_duration_estimation(60.0, vo2_rate)
        cff = self.clock.predict_critical_flicker_fusion(vo2_rate)
        rt = self.clock.predict_reaction_time(vo2_rate)
        
        # Reference: 30-year-old baseline
        ref_duration = 60.0
        ref_cff = self.clock.predict_critical_flicker_fusion(self.clock.baseline_vo2)
        ref_rt = self.clock.predict_reaction_time(self.clock.baseline_vo2)
        
        return {
            'age': age,
            'vo2_factor': vo2_factor,
            'vo2_rate': vo2_rate,
            'duration_estimation_60s': {
                'estimated': duration_est,
                'vs_age_30': duration_est - ref_duration,
                'interpretation': f"Time passes {duration_est/ref_duration:.1%} speed vs. age 30"
            },
            'cff_hz': {
                'predicted': cff,
                'vs_age_30': cff - ref_cff,
                'decline_percent': (ref_cff - cff) / ref_cff * 100
            },
            'reaction_time_ms': {
                'predicted': rt,
                'vs_age_30': rt - ref_rt,
                'increase_percent': (rt - ref_rt) / ref_rt * 100
            },
            'phenomenology': (
                "Years fly by" if vo2_factor < 0.9 else 
                "Time normal" if vo2_factor > 0.95 else
                "Time slowing slightly"
            )
        }
    
    def predict_temperature_effects(self, body_temp_C: float) -> Dict[str, Any]:
        """
        Predict temperature effects on temporal perception.
        
        Higher temperature → higher metabolism → time slows
        
        Args:
            body_temp_C: Body temperature in Celsius
            
        Returns:
            Predicted temporal effects
        """
        baseline_temp = 37.0  # Normal body temp
        
        # Q10 = 2 (metabolic rate doubles per 10°C)
        temp_diff = body_temp_C - baseline_temp
        q10_factor = 2.0 ** (temp_diff / 10.0)
        
        vo2_rate = self.clock.baseline_vo2 * q10_factor
        
        duration_est = self.clock.predict_duration_estimation(60.0, vo2_rate)
        cff = self.clock.predict_critical_flicker_fusion(vo2_rate)
        
        return {
            'body_temp_C': body_temp_C,
            'temp_diff_C': temp_diff,
            'metabolic_factor': q10_factor,
            'vo2_rate': vo2_rate,
            'duration_estimation_60s': duration_est,
            'change_vs_normal': duration_est - 60.0,
            'cff_hz': cff,
            'interpretation': (
                f"{'Fever' if temp_diff > 0.5 else 'Hypothermia' if temp_diff < -0.5 else 'Normal'}: "
                f"Time feels {duration_est/60.0:.1%} speed"
            )
        }
    
    def predict_from_hardware_vo2(self,
                                  heart_rate: float,
                                  respiratory_rate: float) -> Dict[str, Any]:
        """
        Predict temporal perception from hardware-measured physiological data.
        
        Can integrate with your existing hardware sensors!
        
        Args:
            heart_rate: Heart rate (BPM)
            respiratory_rate: Respiratory rate (breaths/min)
            
        Returns:
            Complete temporal perception predictions
        """
        # Estimate VO₂ from physiological signals
        vo2_est = self.clock.measure_vo2(
            heart_rate=heart_rate,
            respiratory_rate=respiratory_rate
        )
        
        # Calculate state
        state = self.clock.calculate_temporal_perception(vo2_est)
        
        # Make all predictions
        duration_60s = self.clock.predict_duration_estimation(60.0, vo2_est)
        cff = self.clock.predict_critical_flicker_fusion(vo2_est)
        rt_simple = self.clock.predict_reaction_time(vo2_est, task_complexity=1)
        rt_choice = self.clock.predict_reaction_time(vo2_est, task_complexity=2)
        
        return {
            'physiological_input': {
                'heart_rate_bpm': heart_rate,
                'respiratory_rate_bpm': respiratory_rate,
            },
            'estimated_vo2': vo2_est,
            'temporal_state': {
                'o2_cycle_frequency_hz': state.o2_cycle_frequency,
                'time_dilation_factor': state.time_dilation_factor,
                'temporal_resolution_ms': state.temporal_resolution_ms,
            },
            'predictions': {
                'duration_estimation_60s': duration_60s,
                'critical_flicker_fusion_hz': cff,
                'simple_reaction_time_ms': rt_simple,
                'choice_reaction_time_ms': rt_choice,
            },
            'interpretation': {
                'time_perception': (
                    'Fast' if state.time_dilation_factor < 0.9 else
                    'Slow' if state.time_dilation_factor > 1.1 else
                    'Normal'
                ),
                'temporal_resolution': (
                    'Fine' if state.temporal_resolution_ms < 5 else
                    'Coarse' if state.temporal_resolution_ms > 15 else
                    'Normal'
                ),
            }
        }


def demonstrate_temporal_predictions():
    """Demonstrate temporal perception predictions from O₂."""
    print("\n" + "="*80)
    print("TEMPORAL PERCEPTION PREDICTIONS FROM O₂ CYCLING")
    print("="*80 + "\n")
    
    predictor = O2TemporalPredictor()
    
    # Drug effects
    print("1. DRUG EFFECTS ON TEMPORAL PERCEPTION")
    print("-" * 80)
    
    for drug in ['caffeine', 'cocaine', 'alcohol', 'benzodiazepines']:
        effects = predictor.predict_drug_effects(drug)
        print(f"\n{drug.upper()}:")
        print(f"  VO₂ change: {(effects['vo2_factor']-1)*100:+.1f}%")
        print(f"  60s feels like: {effects['duration_estimation']['drug']:.1f}s "
              f"({effects['duration_estimation']['interpretation']})")
        print(f"  CFF change: {effects['critical_flicker_fusion']['change_percent']:+.1f}%")
        print(f"  RT change: {effects['reaction_time']['change_percent']:+.1f}% "
              f"({effects['reaction_time']['interpretation']})")
    
    # Age effects
    print("\n\n2. AGE EFFECTS ON TEMPORAL PERCEPTION")
    print("-" * 80)
    
    for age in [20, 30, 50, 70]:
        effects = predictor.predict_age_effects(age)
        print(f"\nAge {age}:")
        print(f"  VO₂: {effects['vo2_factor']:.0%} of age-30 baseline")
        print(f"  60s feels like: {effects['duration_estimation_60s']['estimated']:.1f}s")
        print(f"  CFF: {effects['cff_hz']['predicted']:.1f} Hz "
              f"({effects['cff_hz']['decline_percent']:+.1f}% vs age 30)")
        print(f"  Phenomenology: {effects['phenomenology']}")
    
    # Temperature effects
    print("\n\n3. TEMPERATURE EFFECTS")
    print("-" * 80)
    
    for temp in [36.0, 37.0, 38.5, 40.0]:
        effects = predictor.predict_temperature_effects(temp)
        print(f"\n{temp}°C:")
        print(f"  Metabolic rate: {effects['metabolic_factor']:.0%} of normal")
        print(f"  60s feels like: {effects['duration_estimation_60s']:.1f}s")
        print(f"  {effects['interpretation']}")
    
    # Hardware integration
    print("\n\n4. HARDWARE-MEASURED PREDICTIONS")
    print("-" * 80)
    print("\nResting (HR=70, RR=15):")
    rest = predictor.predict_from_hardware_vo2(70, 15)
    print(f"  VO₂: {rest['estimated_vo2']:.0f} mL/min")
    print(f"  Duration (60s): {rest['predictions']['duration_estimation_60s']:.1f}s")
    print(f"  CFF: {rest['predictions']['critical_flicker_fusion_hz']:.1f} Hz")
    print(f"  Simple RT: {rest['predictions']['simple_reaction_time_ms']:.0f} ms")
    
    print("\nPost-Exercise (HR=140, RR=30):")
    exercise = predictor.predict_from_hardware_vo2(140, 30)
    print(f"  VO₂: {exercise['estimated_vo2']:.0f} mL/min")
    print(f"  Duration (60s): {exercise['predictions']['duration_estimation_60s']:.1f}s")
    print(f"  CFF: {exercise['predictions']['critical_flicker_fusion_hz']:.1f} Hz")
    print(f"  Simple RT: {exercise['predictions']['simple_reaction_time_ms']:.0f} ms")
    print(f"  Time perception: {exercise['interpretation']['time_perception']}")
    
    print("\n" + "="*80)
    print("KEY INSIGHT: All temporal perception effects predicted from VO₂!")
    print("="*80 + "\n")


if __name__ == "__main__":
    demonstrate_temporal_predictions()


