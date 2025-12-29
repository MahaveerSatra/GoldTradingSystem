---
globs: src/trading_engine/*.py
description: >-
  Improves robustness and maintainability by catching and handling exceptions
  gracefully in financial calculations.

  This should be applied to all methods in trading-related modules.
alwaysApply: false
---

Always use try-except blocks for error handling in all methods that process data, especially when dealing with financial calculations.
Ensure proper logging of errors and return meaningful error messages when exceptions occur.