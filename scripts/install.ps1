$ErrorActionPreference = 'Stop'

$ScriptRoot = Split-Path -Parent $MyInvocation.MyCommand.Path
$BootstrapScript = Join-Path $ScriptRoot 'bootstrap_claude_windows.py'

function Resolve-PythonCommand {
    if (Get-Command py -ErrorAction SilentlyContinue) {
        return @('py', '-3')
    }
    if (Get-Command python -ErrorAction SilentlyContinue) {
        return @('python')
    }
    if (Get-Command python3 -ErrorAction SilentlyContinue) {
        return @('python3')
    }

    throw 'Python 3 was not found in PATH. Please install Python 3 and try again.'
}

$PythonCommand = Resolve-PythonCommand
$Arguments = @()
if ($PythonCommand.Length -gt 1) {
    $Arguments += $PythonCommand[1..($PythonCommand.Length - 1)]
}
$Arguments += $BootstrapScript
$Arguments += $args

Write-Host 'Running Claude bootstrap installer...'
& $PythonCommand[0] @Arguments
