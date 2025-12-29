---
globs: '"**/*.ps1\n**/*.cmd\n**/*.bat\n**/*.sh\n**/*.txt"  # Expanded to common
  shell script files'
description: Ensures proper execution of multi-line commands in PowerShell by
  preventing issues with line breaks and quotes.
alwaysApply: true
---

For multi-line PowerShell commands, always use this format:
```powershell
powershell -command "<command1>; <command2>; ..."
```
Or for simple commands:
```powershell
cd path; mkdir dir -Force
```