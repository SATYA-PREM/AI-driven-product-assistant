$ws = New-Object -ComObject WScript.Shell
$desktop = [Environment]::GetFolderPath("Desktop")

# Create or update shortcut on Desktop
$shortcutPath = Join-Path $desktop "AI Pipeline Server.lnk"
$shortcut = $ws.CreateShortcut($shortcutPath)
$shortcut.TargetPath = "C:\Users\belam\Downloads\csv-pipeline\start_server.bat"
$shortcut.WorkingDirectory = "C:\Users\belam\Downloads\csv-pipeline"
$shortcut.Description = "Start Customer Feedback AI Pipeline Server"
$shortcut.Save()

# Also update existing start_server - Shortcut.lnk if present
$oldShortcutPath = Join-Path $desktop "start_server - Shortcut.lnk"
$oldShortcut = $ws.CreateShortcut($oldShortcutPath)
$oldShortcut.TargetPath = "C:\Users\belam\Downloads\csv-pipeline\start_server.bat"
$oldShortcut.WorkingDirectory = "C:\Users\belam\Downloads\csv-pipeline"
$oldShortcut.Description = "Start Customer Feedback AI Pipeline Server"
$oldShortcut.Save()

Write-Host "Created 'AI Pipeline Server.lnk' and updated 'start_server - Shortcut.lnk' on Desktop: $desktop"
