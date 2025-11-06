@echo off
REM Extended Validation Suite Runner
REM Runs all consciousness programming validation modules including clinical extensions

echo ================================================================================
echo CONSCIOUSNESS PROGRAMMING: EXTENDED VALIDATION SUITE
echo ================================================================================
echo.
echo This script will run 10 validation modules:
echo   CORE (5 modules):
echo     1. Electromagnetic Resonance Calculator
echo     2. Kuramoto Oscillator Network
echo     3. Categorical State Space Reduction
echo     4. BMD Phase Sorting
echo     5. Hierarchical BMD Composition
echo.
echo   EXTENSIONS (5 modules):
echo     6. Drug Properties Calculator
echo     7. Therapeutic Window Calculator
echo     8. Metabolic Flux Hierarchy
echo     9. Metabolic Hierarchy Mapper
echo    10. Metabolic Flux Protocol Generator
echo.
echo ================================================================================
echo.

REM Check if virtual environment is activated
if not defined VIRTUAL_ENV (
    echo WARNING: Virtual environment not detected!
    echo Please activate your virtual environment first:
    echo   .venv\Scripts\activate
    echo.
    pause
    exit /b 1
)

REM Check if in correct directory
if not exist "run_extended_validations.py" (
    echo ERROR: run_extended_validations.py not found!
    echo Please run this script from the chigure/src/computing directory.
    echo.
    pause
    exit /b 1
)

echo Running extended validation suite...
echo.
echo ================================================================================
echo.

python run_extended_validations.py --modules all

echo.
echo ================================================================================
echo VALIDATION SUITE COMPLETE
echo ================================================================================
echo.
echo Results saved to: chatelier/src/computing/results/
echo.
echo To run specific module groups:
echo   - Core only:       python run_extended_validations.py --modules core
echo   - Extensions only: python run_extended_validations.py --modules extensions
echo   - All modules:     python run_extended_validations.py --modules all
echo.
echo ================================================================================
echo.

pause

