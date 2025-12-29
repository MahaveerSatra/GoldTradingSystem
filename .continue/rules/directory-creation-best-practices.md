---
globs: '"**/*.ps1\n**/*.cmd\n**/*.bat\n**/*.sh\n**/*.py"'
description: Ensures reliable directory creation in PowerShell by following
  standardized parameter usage and path handling.
---

For directory creation in PowerShell:
1. Always use explicit path syntax with `-Path` parameter
2. Use `-Force` flag to handle existing directories
3. Structure commands as:
```powershell
New-Item -ItemType Directory -Path 'full/path/to/directory' -Force
```
4. For recursive directory operations:
```powershell
Get-ChildItem -Recurse 'parent_directory' | ForEach-Object { New-Item -ItemType Directory -Path $_.FullName -Force }
```