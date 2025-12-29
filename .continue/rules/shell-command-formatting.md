---
globs: |-
  **/*.ps1
  **/*.cmd
  **/*.bat
  src/**/*.{ps1,bat,cmd}
description: Prevents syntax errors in PowerShell by ensuring commands are
  properly formatted for execution in terminal environments.
alwaysApply: true
---

Always use PowerShell commands with proper escaping for multi-line commands by:
1. Using `powershell -command "..."` wrapper
2. Avoiding line breaks inside quotes
3. Using semicolons (`;`) for command separation when needed