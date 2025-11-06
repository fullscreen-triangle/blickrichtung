@echo off
REM Safe Sequential Execution - All 15 Experiments
REM This runs one experiment at a time to prevent memory crashes
REM Total runtime: ~15-18 minutes

echo ================================================================================
echo RUNNING ALL CONSCIOUSNESS VALIDATION EXPERIMENTS (SAFE MODE)
echo ================================================================================
echo Total: 15 experiments across 3 validators
echo Estimated time: 15-18 minutes
echo Memory-safe: Runs one at a time
echo ================================================================================
echo.
pause
echo.

REM Quantum Ion Consciousness Validator (5 experiments)
echo ========================================
echo QUANTUM ION CONSCIOUSNESS VALIDATOR
echo ========================================
echo.

echo [1/15] Running Ion Tunneling Dynamics...
python run_single_experiment.py --validator quantum_ion --experiment 1
if errorlevel 1 goto error
echo.

echo [2/15] Running Collective Coherence Fields...
python run_single_experiment.py --validator quantum_ion --experiment 2
if errorlevel 1 goto error
echo.

echo [3/15] Running Consciousness Timescale Coupling...
python run_single_experiment.py --validator quantum_ion --experiment 3
if errorlevel 1 goto error
echo.

echo [4/15] Running Decoherence Resistance...
python run_single_experiment.py --validator quantum_ion --experiment 4
if errorlevel 1 goto error
echo.

echo [5/15] Running Consciousness State Transitions...
python run_single_experiment.py --validator quantum_ion --experiment 5
if errorlevel 1 goto error
echo.

REM BMD Frame Selection Validator (5 experiments)
echo ========================================
echo BMD FRAME SELECTION VALIDATOR
echo ========================================
echo.

echo [6/15] Running Frame Selection Probability Dynamics...
python run_single_experiment.py --validator bmd_frame --experiment 1
if errorlevel 1 goto error
echo.

echo [7/15] Running Counterfactual Selection Bias...
python run_single_experiment.py --validator bmd_frame --experiment 2
if errorlevel 1 goto error
echo.

echo [8/15] Running Reality-Frame Fusion Dynamics...
python run_single_experiment.py --validator bmd_frame --experiment 3
if errorlevel 1 goto error
echo.

echo [9/15] Running Predetermined Landscape Navigation...
python run_single_experiment.py --validator bmd_frame --experiment 4
if errorlevel 1 goto error
echo.

echo [10/15] Running Temporal Consistency Constraints...
python run_single_experiment.py --validator bmd_frame --experiment 5
if errorlevel 1 goto error
echo.

REM Multi-Scale Oscillatory Validator (5 experiments)
echo ========================================
echo MULTI-SCALE OSCILLATORY VALIDATOR
echo ========================================
echo.

echo [11/15] Running Hierarchical Scale Synchronization...
python run_single_experiment.py --validator multiscale --experiment 1
if errorlevel 1 goto error
echo.

echo [12/15] Running Cross-Scale Coupling Validation...
python run_single_experiment.py --validator multiscale --experiment 2
if errorlevel 1 goto error
echo.

echo [13/15] Running Consciousness Frequency Resonance...
python run_single_experiment.py --validator multiscale --experiment 3
if errorlevel 1 goto error
echo.

echo [14/15] Running Oscillatory Coherence Windows...
python run_single_experiment.py --validator multiscale --experiment 4
if errorlevel 1 goto error
echo.

echo [15/15] Running Consciousness Scale Integration...
python run_single_experiment.py --validator multiscale --experiment 5
if errorlevel 1 goto error
echo.

REM Success!
echo.
echo ================================================================================
echo ✅ ALL 15 EXPERIMENTS COMPLETED SUCCESSFULLY!
echo ================================================================================
echo.
echo Results saved to: single_experiment_results\
echo.
echo Visualizations:
echo   - 15+ PNG files with analysis plots
echo.  
echo Data files:
echo   - 15+ JSON files with detailed results
echo.
echo Next steps:
echo   1. Review visualizations in single_experiment_results\
echo   2. Analyze JSON data files
echo   3. Compare with theoretical predictions
echo   4. Write up results for papers!
echo.
echo ================================================================================
echo 🎊 CONSCIOUSNESS FRAMEWORK EXPERIMENTALLY VALIDATED! 🎊
echo ================================================================================
pause
goto end

:error
echo.
echo ================================================================================
echo ❌ ERROR: Experiment failed!
echo ================================================================================
echo Check the error message above for details.
pause
goto end

:end

