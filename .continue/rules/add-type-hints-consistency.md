---
globs: src/trading_engine/*.py
description: >-
  Maintain type safety and consistency throughout the trading engine modules to
  improve code maintainability and reduce runtime errors.

  This rule should apply to all files in the src/trading_engine directory.
alwaysApply: false
---

Ensure consistent type hints across all modules in the trading engine, particularly for:
- Return types of all methods
- Parameter types for all function/method signatures
- Consistent use of pandas DataFrame types where appropriate
- Proper typing for datetime objects and time intervals