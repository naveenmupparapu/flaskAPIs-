"""
Script to run all tests with coverage report.
Run this script to execute all tests and generate coverage report.

Usage:
    python run_tests.py
"""
import subprocess
import sys


def run_tests():
    """Run pytest with coverage."""
    print("=" * 60)
    print("Running Student Registration Application Tests")
    print("=" * 60)
    print()
    
    # Run pytest with coverage
    cmd = [
        sys.executable, '-m', 'pytest',
        'tests/',
        '-v',
        '--cov=app',
        '--cov-report=term-missing',
        '--cov-report=html:coverage_html',
        '--cov-fail-under=100',
        '-x'  # Stop on first failure
    ]
    
    result = subprocess.run(cmd)
    
    print()
    print("=" * 60)
    if result.returncode == 0:
        print("✓ All tests passed with 100% coverage!")
        print("  HTML coverage report generated in: coverage_html/")
    else:
        print("✗ Some tests failed or coverage is below 100%")
    print("=" * 60)
    
    return result.returncode


if __name__ == '__main__':
    sys.exit(run_tests())






