# OpenLLMBench Runner Build Script
#
# Creates the standalone Windows OpenLLMBench Runner executable using
# PyInstaller.
#
# Current development requirements:
# - Windows
# - Python 3.14
# - PyInstaller 6.22.2 or compatible
#
# Build output is intentionally written outside the repository under:
#
#   %TEMP%\OpenLLMBench-runner-build\
#
# The resulting executable bundles the Python runtime and OpenLLMBench
# Runner/parser code. Benchmark protocol assets such as the model and
# llama-bench.exe are not bundled into the executable.
#
# The standalone executable has been validated through the complete
# Benchmark Protocol v1.0 Runner workflow, including submission manifest
# generation, canonical validation, and ZIP packaging.
#
# A PATH-isolation test also confirmed that the executable launches and
# performs environment verification when system Python is unavailable
# through PATH.
#
# A pristine Windows machine test remains a pre-public-beta distribution
# regression test.

$ErrorActionPreference = "Stop"

$RepositoryRoot = Split-Path -Parent $PSScriptRoot
$RunnerSource = Join-Path $PSScriptRoot "run_benchmark.py"

$BuildRoot = Join-Path $env:TEMP "OpenLLMBench-runner-build"
$DistPath = Join-Path $BuildRoot "dist"
$WorkPath = Join-Path $BuildRoot "build"
$SpecPath = Join-Path $BuildRoot "spec"

Write-Host ""
Write-Host "OpenLLMBench Runner Build"
Write-Host "========================="
Write-Host ""

Write-Host "Repository: $RepositoryRoot"
Write-Host "Source:     $RunnerSource"
Write-Host "Build root: $BuildRoot"
Write-Host ""

if (-not (Test-Path $RunnerSource)) {
    throw "Runner source not found: $RunnerSource"
}

Write-Host "Checking Python..."
python --version

Write-Host ""
Write-Host "Checking PyInstaller..."
python -m PyInstaller --version

Write-Host ""
Write-Host "Cleaning previous build..."
Remove-Item $BuildRoot -Recurse -Force -ErrorAction SilentlyContinue

New-Item -ItemType Directory -Path $DistPath -Force | Out-Null
New-Item -ItemType Directory -Path $WorkPath -Force | Out-Null
New-Item -ItemType Directory -Path $SpecPath -Force | Out-Null

Write-Host ""
Write-Host "Building OpenLLMBench-Runner.exe..."
Write-Host ""

Push-Location $RepositoryRoot

try {
    python -m PyInstaller `
        --noconfirm `
        --clean `
        --onefile `
        --console `
        --name "OpenLLMBench-Runner" `
        --distpath $DistPath `
        --workpath $WorkPath `
        --specpath $SpecPath `
        $RunnerSource

    if ($LASTEXITCODE -ne 0) {
        throw "PyInstaller exited with code $LASTEXITCODE."
    }
}
finally {
    Pop-Location
}

$Executable = Join-Path $DistPath "OpenLLMBench-Runner.exe"

if (-not (Test-Path $Executable)) {
    throw "Expected executable was not created: $Executable"
}

Write-Host ""
Write-Host "Build complete."
Write-Host ""
Write-Host "Executable:"
Write-Host $Executable
Write-Host ""

Get-Item $Executable |
    Select-Object Name, Length, LastWriteTime
