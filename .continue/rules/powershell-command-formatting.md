---
globs: '"src/**/*.ps1\n**/*.cmd\n**/*.bat\n**/*.sh"'
description: Prevents common PowerShell errors when creating directory
  structures by ensuring proper parameter usage and path formatting.
alwaysApply: true
---

When creating folder structures in PowerShell:
1. Use `New-Item` for directory creation
2. Always specify paths explicitly with `-Path` parameter
3. Use `-Force` flag to overwrite existing directories
4. Structure commands in this format:
```powershell
New-Item -ItemType Directory -Path 'path/to/dir' -Force
```