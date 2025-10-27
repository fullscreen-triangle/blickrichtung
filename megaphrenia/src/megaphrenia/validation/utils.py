"""
Utilities for loading and analyzing validation results.

Functions for:
- Loading saved JSON results
- Comparing results across runs
- Aggregating multiple test results
- Generating summary reports
"""

import json
from pathlib import Path
from typing import Dict, List, Any, Optional
from datetime import datetime
import numpy as np


def load_results(filepath: Path) -> Dict[str, Any]:
    """
    Load validation results from JSON file.
    
    Args:
        filepath: Path to results JSON file
        
    Returns:
        Dictionary of results
    """
    with open(filepath, 'r') as f:
        return json.load(f)


def load_latest_results(category: str, test_name: Optional[str] = None) -> Dict[str, Any]:
    """
    Load most recent results for a category or test.
    
    Args:
        category: Category path (e.g., 'circuits')
        test_name: Optional test name to filter (e.g., 'half_adder')
        
    Returns:
        Most recent test results
    """
    results_dir = Path("validation_results") / category
    
    if not results_dir.exists():
        raise FileNotFoundError(f"No results found for category: {category}")
    
    # Find all JSON files
    if test_name:
        pattern = f"{test_name}_*.json"
    else:
        pattern = "*.json"
    
    files = list(results_dir.glob(pattern))
    
    if not files:
        raise FileNotFoundError(f"No results files found matching: {pattern}")
    
    # Sort by modification time, get most recent
    latest_file = max(files, key=lambda f: f.stat().st_mtime)
    
    return load_results(latest_file)


def compare_results(filepath1: Path, filepath2: Path) -> Dict[str, Any]:
    """
    Compare two validation results.
    
    Args:
        filepath1: First results file
        filepath2: Second results file
        
    Returns:
        Dictionary of comparison metrics
    """
    results1 = load_results(filepath1)
    results2 = load_results(filepath2)
    
    comparison = {
        "test_names": [
            results1["test_metadata"]["test_name"],
            results2["test_metadata"]["test_name"]
        ],
        "timestamps": [
            results1["test_metadata"]["timestamp"],
            results2["test_metadata"]["timestamp"]
        ],
        "durations": [
            results1["test_metadata"].get("test_duration_seconds", 0),
            results2["test_metadata"].get("test_duration_seconds", 0)
        ],
        "passed": [
            results1["results"]["validation"].get("passed", False),
            results2["results"]["validation"].get("passed", False)
        ]
    }
    
    # Compare statistics if available
    stats1 = results1["results"].get("statistics", {})
    stats2 = results2["results"].get("statistics", {})
    
    if stats1 and stats2:
        comparison["statistics_comparison"] = {}
        for key in set(stats1.keys()) & set(stats2.keys()):
            comparison["statistics_comparison"][key] = {
                "result1": stats1[key],
                "result2": stats2[key],
                "difference": abs(stats1[key] - stats2[key]) if isinstance(stats1[key], (int, float)) else None
            }
    
    return comparison


def aggregate_results(category: str, test_name: Optional[str] = None) -> Dict[str, Any]:
    """
    Aggregate all results for a category or test.
    
    Args:
        category: Category path
        test_name: Optional test name filter
        
    Returns:
        Aggregated statistics across all runs
    """
    results_dir = Path("validation_results") / category
    
    if not results_dir.exists():
        return {"error": f"Category not found: {category}"}
    
    # Find all matching files
    if test_name:
        pattern = f"{test_name}_*.json"
    else:
        pattern = "*.json"
    
    files = list(results_dir.glob(pattern))
    
    if not files:
        return {"error": f"No results found matching: {pattern}"}
    
    # Load all results
    all_results = [load_results(f) for f in files]
    
    # Aggregate
    aggregation = {
        "total_runs": len(all_results),
        "date_range": {
            "earliest": min(r["test_metadata"]["timestamp"] for r in all_results),
            "latest": max(r["test_metadata"]["timestamp"] for r in all_results)
        },
        "pass_rate": sum(1 for r in all_results if r["results"]["validation"].get("passed", False)) / len(all_results),
        "average_duration": np.mean([r["test_metadata"].get("test_duration_seconds", 0) for r in all_results])
    }
    
    # Aggregate statistics if available
    all_stats = [r["results"].get("statistics", {}) for r in all_results if r["results"].get("statistics")]
    
    if all_stats:
        # Get common keys across all runs
        common_keys = set.intersection(*[set(s.keys()) for s in all_stats])
        
        aggregation["statistics"] = {}
        for key in common_keys:
            values = [s[key] for s in all_stats if isinstance(s[key], (int, float))]
            if values:
                aggregation["statistics"][key] = {
                    "mean": float(np.mean(values)),
                    "std": float(np.std(values)),
                    "min": float(np.min(values)),
                    "max": float(np.max(values)),
                    "count": len(values)
                }
    
    return aggregation


def generate_summary_report(category: str, output_file: Optional[Path] = None) -> str:
    """
    Generate a text summary report for all tests in a category.
    
    Args:
        category: Category to summarize
        output_file: Optional file to write report to
        
    Returns:
        Summary report as string
    """
    results_dir = Path("validation_results") / category
    
    if not results_dir.exists():
        return f"No results found for category: {category}"
    
    # Get all test names
    files = list(results_dir.glob("*.json"))
    test_names = set(f.stem.rsplit('_', 2)[0] for f in files)  # Remove timestamp
    
    report_lines = [
        "="*60,
        f"VALIDATION SUMMARY: {category}",
        "="*60,
        f"Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}",
        f"Total test types: {len(test_names)}",
        f"Total runs: {len(files)}",
        ""
    ]
    
    # Aggregate each test type
    for test_name in sorted(test_names):
        agg = aggregate_results(category, test_name)
        
        if "error" not in agg:
            report_lines.extend([
                f"\nTest: {test_name}",
                "-"*40,
                f"  Runs: {agg['total_runs']}",
                f"  Pass rate: {agg['pass_rate']:.1%}",
                f"  Avg duration: {agg['average_duration']:.2f}s",
                f"  Date range: {agg['date_range']['earliest']} to {agg['date_range']['latest']}"
            ])
            
            if "statistics" in agg:
                report_lines.append("\n  Statistics:")
                for stat_name, stat_vals in agg["statistics"].items():
                    report_lines.append(
                        f"    {stat_name}: {stat_vals['mean']:.3f} ± {stat_vals['std']:.3f} "
                        f"(range: {stat_vals['min']:.3f} - {stat_vals['max']:.3f})"
                    )
    
    report_lines.extend([
        "",
        "="*60,
        "END OF REPORT",
        "="*60
    ])
    
    report = "\n".join(report_lines)
    
    # Save to file if requested
    if output_file:
        with open(output_file, 'w') as f:
            f.write(report)
        print(f"Report saved to: {output_file}")
    
    return report


# Example usage
if __name__ == "__main__":
    print("Validation Utilities Module")
    print("="*60)
    print("\nAvailable functions:")
    print("- load_results(filepath)")
    print("- load_latest_results(category, test_name)")
    print("- compare_results(filepath1, filepath2)")
    print("- aggregate_results(category, test_name)")
    print("- generate_summary_report(category, output_file)")
    print("\nRun these functions after validation tests have been executed.")

