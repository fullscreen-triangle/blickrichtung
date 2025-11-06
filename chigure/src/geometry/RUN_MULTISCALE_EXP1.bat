@echo off
REM Run Multi-Scale Oscillatory Experiment 1 (Memory-Safe)
echo ========================================
echo RUNNING MULTI-SCALE OSCILLATORY EXPERIMENT 1
echo Hierarchical Scale Synchronization
echo ========================================
python run_single_experiment.py --validator multiscale --experiment 1
pause

