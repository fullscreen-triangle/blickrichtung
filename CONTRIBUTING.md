# Contributing to Blickrichtung

Thank you for your interest in contributing to the Consciousness Programming Framework! This document provides guidelines for contributing to the project.

---

## Table of Contents

1. [Code of Conduct](#code-of-conduct)
2. [How Can I Contribute?](#how-can-i-contribute)
3. [Development Setup](#development-setup)
4. [Coding Standards](#coding-standards)
5. [Submission Process](#submission-process)
6. [Review Process](#review-process)
7. [Scientific Standards](#scientific-standards)

---

## Code of Conduct

### Our Pledge

We are committed to providing a welcoming and inclusive environment for all contributors, regardless of:
- Background or identity
- Level of experience
- Nationality or language
- Institution or affiliation

### Expected Behavior

- **Be respectful**: Value diverse perspectives and experiences
- **Be constructive**: Provide helpful feedback and suggestions
- **Be collaborative**: Work together toward common goals
- **Be rigorous**: Maintain high scientific and technical standards

### Unacceptable Behavior

- Harassment, discrimination, or personal attacks
- Plagiarism or misrepresentation of work
- Sharing proprietary or confidential information
- Any conduct that violates scientific integrity

---

## How Can I Contribute?

### 1. Report Bugs

**Before submitting a bug report:**
- Check existing issues to avoid duplicates
- Verify the bug with the latest version
- Collect relevant information (OS, Python version, error messages)

**Bug Report Template:**
```markdown
**Description**: [Clear description of the bug]
**Expected Behavior**: [What should happen]
**Actual Behavior**: [What actually happens]
**Steps to Reproduce**:
1. [First step]
2. [Second step]
3. [...]

**Environment**:
- OS: [e.g., Windows 10, Ubuntu 20.04]
- Python version: [e.g., 3.9.7]
- Package versions: [from requirements.txt]

**Error Message**: [Full traceback if applicable]
```

### 2. Suggest Enhancements

We welcome suggestions for:
- New validation modules
- Improved visualizations
- Performance optimizations
- Documentation improvements
- New features

**Enhancement Template:**
```markdown
**Feature Description**: [What you want to add/change]
**Motivation**: [Why this is needed]
**Proposed Implementation**: [How it could work]
**Alternatives Considered**: [Other approaches]
**Impact**: [Who benefits and how]
```

### 3. Submit Code Contributions

Areas where contributions are especially welcome:

#### Computational Modules
- New drug property calculators
- Additional validation methodologies
- Alternative numerical methods
- Performance optimizations

#### Visualization Tools
- Interactive dashboards
- 3D phase space visualizations
- Animation tools for oscillatory dynamics
- Clinical data visualization

#### Documentation
- Tutorial notebooks
- Use case examples
- API documentation
- Translation to other languages

#### Testing
- Unit tests for existing modules
- Integration tests
- Validation against experimental data
- Benchmark suites

---

## Development Setup

### Prerequisites
- Python 3.8 or higher
- Git
- Virtual environment tool (venv or conda)
- LaTeX distribution (for documentation)

### Setup Steps

```bash
# 1. Fork the repository on GitHub
# 2. Clone your fork
git clone https://github.com/yourusername/blickrichtung.git
cd blickrichtung

# 3. Add upstream remote
git remote add upstream https://github.com/originalusername/blickrichtung.git

# 4. Create virtual environment
cd chigure
python -m venv .venv
source .venv/bin/activate  # On Windows: .venv\Scripts\activate

# 5. Install dependencies
pip install -r src/computing/requirements.txt

# 6. Install development dependencies
pip install pytest pytest-cov black flake8 mypy

# 7. Run tests to verify setup
cd src/computing
python run_all_validations.py
```

### Development Workflow

```bash
# 1. Create a feature branch
git checkout -b feature/your-feature-name

# 2. Make your changes
# [edit files]

# 3. Run tests
pytest tests/

# 4. Format code
black src/computing/
flake8 src/computing/

# 5. Commit changes
git add .
git commit -m "feat: add your feature description"

# 6. Push to your fork
git push origin feature/your-feature-name

# 7. Create pull request on GitHub
```

---

## Coding Standards

### Python Style

We follow **PEP 8** with some modifications:

```python
# Line length: 88 characters (Black default)
# Imports: grouped and sorted
import os
import sys
from typing import List, Dict, Optional

import numpy as np
import matplotlib.pyplot as plt

from computing.utils import helper_function

# Type hints required for public functions
def calculate_flux(
    glucose_input: float,
    coupling_strength: float,
    n_levels: int = 5
) -> Dict[str, np.ndarray]:
    """
    Calculate metabolic flux through hierarchical cascade.
    
    Args:
        glucose_input: Initial glucose concentration (mM)
        coupling_strength: O2-H+ coupling parameter (Hz)
        n_levels: Number of hierarchical levels (default: 5)
        
    Returns:
        Dictionary containing flux values at each level
        
    Raises:
        ValueError: If glucose_input is negative
    """
    if glucose_input < 0:
        raise ValueError("Glucose input must be non-negative")
    
    # Implementation
    results = {}
    # ...
    return results
```

### Naming Conventions

- **Functions**: `snake_case`
- **Classes**: `PascalCase`
- **Constants**: `UPPER_CASE`
- **Private members**: `_leading_underscore`

### Documentation

Every module, class, and public function must have docstrings:

```python
"""
Module: metabolic_flux_hierarchy.py

Implements the Metabolic Flux Hierarchy Analyzer for validating
hierarchical information processing in metabolic cascades.

Key Classes:
    - MetabolicLevel: Represents a single level in the hierarchy
    - MetabolicCascade: Simulates multi-level flux propagation

Functions:
    - simulate_cascade: Main simulation entry point
    - calculate_hierarchical_depth: Computes depth metric
"""
```

### Testing

All new code should include tests:

```python
# tests/test_metabolic_flux.py
import pytest
import numpy as np
from computing.metabolic_flux_hierarchy import simulate_cascade

def test_baseline_flux():
    """Test baseline metabolic flux simulation."""
    results = simulate_cascade(
        glucose_input=5.0,
        condition="baseline"
    )
    
    assert results["hierarchical_depth"] == pytest.approx(1.0, abs=0.01)
    assert 0.25 < results["end_to_end_flux"] < 0.35

def test_invalid_input():
    """Test error handling for invalid inputs."""
    with pytest.raises(ValueError):
        simulate_cascade(glucose_input=-1.0)
```

---

## Submission Process

### 1. Before Submitting

- [ ] Code passes all existing tests
- [ ] New tests added for new functionality
- [ ] Code formatted with Black
- [ ] No linting errors (flake8)
- [ ] Type hints checked (mypy)
- [ ] Documentation updated
- [ ] CHANGELOG.md updated

### 2. Commit Message Format

We use **Conventional Commits**:

```
<type>(<scope>): <subject>

<body>

<footer>
```

**Types:**
- `feat`: New feature
- `fix`: Bug fix
- `docs`: Documentation only
- `style`: Formatting changes
- `refactor`: Code restructuring
- `test`: Adding tests
- `chore`: Maintenance tasks

**Examples:**
```
feat(metabolic): add insulin sensitivity parameter

Implements variable insulin sensitivity in metabolic flux hierarchy.
Enables modeling of insulin resistance at different severity levels.

Closes #42
```

```
fix(kuramoto): correct phase wrapping in oscillator network

Phase values were not properly wrapped to [-π, π], causing
numerical instability in long simulations.
```

### 3. Pull Request

**PR Title**: Same format as commit messages

**PR Description Template:**
```markdown
## Description
[Brief description of changes]

## Motivation
[Why this change is needed]

## Changes Made
- [Change 1]
- [Change 2]
- [...]

## Testing
- [ ] All existing tests pass
- [ ] New tests added
- [ ] Manual testing performed

## Documentation
- [ ] Code comments added/updated
- [ ] Docstrings added/updated
- [ ] README updated (if needed)

## Related Issues
Closes #[issue number]

## Screenshots (if applicable)
[Add screenshots for UI changes]
```

---

## Review Process

### Timeline
- **Initial review**: Within 3-5 days
- **Feedback cycles**: 2-3 days per cycle
- **Merge decision**: After approval from 1-2 reviewers

### Review Criteria

Reviewers will check:

1. **Scientific Correctness**
   - Mathematical rigor
   - Physical plausibility
   - Agreement with experimental data

2. **Code Quality**
   - Follows coding standards
   - Well-documented
   - Efficient implementation

3. **Testing**
   - Adequate test coverage
   - Tests pass consistently
   - Edge cases handled

4. **Impact**
   - Doesn't break existing functionality
   - Integrates well with codebase
   - Clear benefits

### Feedback Response

- Be respectful and professional
- Address all feedback points
- Ask for clarification if needed
- Mark conversations as resolved when addressed

---

## Scientific Standards

### Computational Reproducibility

All computational results must be:
- **Deterministic**: Use fixed random seeds
- **Documented**: Clear parameter specifications
- **Validated**: Compared against experimental data when available

### Experimental Validation

When adding new predictions:
1. Specify **falsification criteria** (what would prove it wrong)
2. Estimate **experimental cost** and timeline
3. Identify **existing data** for validation
4. Propose **minimal experimental protocol**

### Citation Requirements

- Cite original sources for all methods
- Acknowledge prior work appropriately
- Update bibliography (phase_lock_computing.bib)

---

## Communication Channels

### GitHub Issues
- Bug reports
- Feature requests
- Technical discussions

### GitHub Discussions
- General questions
- Design proposals
- Community announcements

### Email
- Private inquiries
- Collaboration proposals
- Sensitive matters

### Monthly Video Calls (Coming Soon)
- Community updates
- Roadmap planning
- Live Q&A

---

## Recognition

Contributors will be acknowledged in:
- **CHANGELOG.md**: All accepted contributions
- **AUTHORS.md**: Significant contributors
- **Papers**: Contributors to specific research outputs
- **Project Website**: Community showcase (planned)

### Authorship Guidelines

For co-authorship on scientific papers:
- **Substantial intellectual contribution** to the research
- **Critical review** and approval of manuscript
- **Agreement to be accountable** for the work

Minor contributions are acknowledged in the acknowledgments section.

---

## Questions?

If you have questions about contributing:
- Check existing documentation
- Search closed issues
- Ask in GitHub Discussions
- Email the maintainer

We're here to help make your contribution successful!

---

## License

By contributing to Blickrichtung, you agree that your contributions will be licensed under the MIT License.

---

**Thank you for contributing to the future of consciousness programming!**

*Last Updated: December 2025*

