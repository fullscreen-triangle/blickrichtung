@echo off
REM Run BMD Frame Selection Experiment 1 (Memory-Safe)
echo ========================================
echo RUNNING BMD FRAME SELECTION EXPERIMENT 1
echo Frame Selection Probability Dynamics
echo ========================================
python run_single_experiment.py --validator bmd_frame --experiment 1
pause

