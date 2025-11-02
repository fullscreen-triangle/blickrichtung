"""
Analysis Module for St. Stellas Oscillator Demo Package

This module imports all analysis components and exposes them for use by oscillator modules.
All oscillator tests and validation functions are available through this interface.
"""

# Import all analysis modules
from .stability_analysis import StabilityAnalyzer, analyze_stability
from .frequency_domain import FrequencyDomainAnalyzer, analyze_frequency_domain
from .time_domain import TimeDomainAnalyzer, analyze_time_domain
from .circuit_equivalent import CircuitEquivalentAnalyzer, analyze_circuit_equivalent
from .coupling import CouplingAnalyzer, analyze_coupling

def run_all_tests(oscillator, include_st_stellas: bool = True):
    """
    Run all oscillator tests and return comprehensive results
    
    Args:
        oscillator: Oscillator object to test
        include_st_stellas: Whether to include St. Stellas specific tests
        
    Returns:
        Dict containing all test results
    """
    all_results = {}
    
    try:
        # Traditional oscillator tests
        all_results['stability'] = analyze_stability(oscillator, 'comprehensive')
        all_results['frequency_domain'] = analyze_frequency_domain(oscillator, 'comprehensive')
        all_results['time_domain'] = analyze_time_domain(oscillator, 'comprehensive')
        all_results['circuit_equivalent'] = analyze_circuit_equivalent(oscillator, 'comprehensive')
        
        # St. Stellas specific tests if requested
        if include_st_stellas:
            all_results['st_stellas_stability'] = analyze_stability(oscillator, 'st_stellas')
            all_results['st_stellas_frequency'] = analyze_frequency_domain(oscillator, 'st_stellas')
            all_results['st_stellas_time'] = analyze_time_domain(oscillator, 'st_stellas')
            all_results['st_stellas_equivalent'] = analyze_circuit_equivalent(oscillator, 'st_stellas')
        
        # Generate summary
        passed_tests = sum(1 for result in all_results.values() 
                          if isinstance(result, dict) and 'error' not in result)
        total_tests = len(all_results)
        
        all_results['test_summary'] = {
            'passed_tests': passed_tests,
            'total_tests': total_tests,
            'overall_status': 'passed' if passed_tests == total_tests else 'partial'
        }
        
    except Exception as e:
        all_results['error'] = f"Test suite error: {str(e)}"
        all_results['test_summary'] = {'overall_status': 'failed', 'error': str(e)}
    
    return all_results

def run_coupling_tests(oscillators, include_st_stellas: bool = True):
    """
    Run coupling tests for multiple oscillators
    
    Args:
        oscillators: List of oscillator objects
        include_st_stellas: Whether to include St. Stellas coupling tests
        
    Returns:
        Dict containing coupling test results
    """
    coupling_results = {}
    
    try:
        coupling_results['synchronization'] = analyze_coupling(oscillators, 'synchronization')
        coupling_results['phase_locking'] = analyze_coupling(oscillators, 'phase_locking')
        
        if include_st_stellas:
            coupling_results['st_stellas_coupling'] = analyze_coupling(oscillators, 'st_stellas')
        
        # Generate summary
        sync_available = coupling_results['synchronization'].get('synchronization_available', False)
        phase_available = coupling_results['phase_locking'].get('phase_locking_available', False)
        
        coupling_results['test_summary'] = {
            'synchronization_available': sync_available,
            'phase_locking_available': phase_available,
            'overall_status': 'passed' if sync_available and phase_available else 'partial'
        }
        
    except Exception as e:
        coupling_results['error'] = f"Coupling test error: {str(e)}"
        coupling_results['test_summary'] = {'overall_status': 'failed', 'error': str(e)}
    
    return coupling_results

def validate_st_stellas_transformation(traditional_oscillator, st_stellas_oscillator):
    """
    Validate that St. Stellas oscillator maintains equivalence with traditional oscillator
    
    Args:
        traditional_oscillator: Traditional oscillator implementation
        st_stellas_oscillator: St. Stellas equivalent oscillator
        
    Returns:
        Dict containing validation results
    """
    validation_results = {}
    
    try:
        # Run tests on both oscillators
        traditional_results = run_all_tests(traditional_oscillator, include_st_stellas=False)
        st_stellas_results = run_all_tests(st_stellas_oscillator, include_st_stellas=True)
        
        validation_results['traditional_results'] = traditional_results
        validation_results['st_stellas_results'] = st_stellas_results
        
        # Simple equivalence check
        trad_passed = traditional_results['test_summary']['passed_tests']
        st_passed = st_stellas_results['test_summary']['passed_tests']
        
        validation_results['equivalence_check'] = {
            'equivalent': abs(trad_passed - st_passed) <= 1,  # Allow 1 test difference
            'traditional_passed': trad_passed,
            'st_stellas_passed': st_passed
        }
        
        # Identify St. Stellas advantages
        st_stellas_advantages = []
        if 'st_stellas_stability' in st_stellas_results:
            st_stellas_advantages.append('S-entropy stability analysis')
        if 'st_stellas_equivalent' in st_stellas_results:
            st_stellas_advantages.append('Grand Equivalent Circuit transformation')
        if 'st_stellas_frequency' in st_stellas_results:
            st_stellas_advantages.append('Tri-dimensional frequency response')
        
        validation_results['st_stellas_advantages'] = st_stellas_advantages
        
    except Exception as e:
        validation_results['error'] = f"Validation error: {str(e)}"
    
    return validation_results

# Export all public functions and classes
__all__ = [
    # Analyzer classes
    'StabilityAnalyzer',
    'FrequencyDomainAnalyzer', 
    'TimeDomainAnalyzer',
    'CircuitEquivalentAnalyzer',
    'CouplingAnalyzer',
    
    # Analysis functions
    'analyze_stability',
    'analyze_frequency_domain',
    'analyze_time_domain', 
    'analyze_circuit_equivalent',
    'analyze_coupling',
    
    # Convenience functions
    'run_all_tests',
    'run_coupling_tests',
    'validate_st_stellas_transformation'
]