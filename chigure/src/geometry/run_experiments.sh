#!/bin/bash
# Unix/Linux/Mac script to run comprehensive experiments

echo "================================================================"
echo "OSCILLATORY CONSCIOUSNESS EXPERIMENTAL FRAMEWORK"
echo "================================================================"
echo ""

echo "Step 1: Testing imports..."
python3 test_imports.py
if [ $? -ne 0 ]; then
    echo ""
    echo "ERROR: Import tests failed. Please fix errors before continuing."
    exit 1
fi

echo ""
echo ""
echo "Step 2: Running comprehensive experiments..."
echo "This will take 10-40 minutes depending on your system and data."
echo "Results will be saved to: comprehensive_validation_results/"
echo ""

python3 run_comprehensive_experiments.py

echo ""
echo "================================================================"
echo "EXPERIMENTS COMPLETE"
echo "================================================================"
echo ""
echo "Results location: comprehensive_validation_results/"
echo "Main results file: comprehensive_validation_results/comprehensive_experimental_results.json"
echo ""
echo "Next steps:"
echo "1. Review comprehensive_experimental_results.json"
echo "2. Check individual validator results in subdirectories"
echo "3. View generated figures in figures/ folders"
echo "4. Integrate findings into research papers"
echo ""

