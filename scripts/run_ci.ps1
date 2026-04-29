param(
    [string]$Python = ""
)

$repoRoot = (Resolve-Path (Join-Path $PSScriptRoot "..")).Path

if (-not $Python) {
    $windowsVenvPython = Join-Path $repoRoot ".venv\Scripts\python.exe"
    $linuxVenvPython = Join-Path $repoRoot ".venv/bin/python"

    if (Test-Path $windowsVenvPython) {
        $Python = $windowsVenvPython
    }
    elseif (Test-Path $linuxVenvPython) {
        $Python = $linuxVenvPython
    }
    else {
        $Python = "python"
    }
}

$reportsRoot = Join-Path $repoRoot "reports"
$pytestReportDir = Join-Path $reportsRoot "pytest"
$flake8ReportDir = Join-Path $reportsRoot "flake8"

New-Item -ItemType Directory -Force -Path $pytestReportDir, $flake8ReportDir | Out-Null

Push-Location $repoRoot
try {
    & $Python -m pytest tests `
        "--html=$pytestReportDir/report.html" `
        "--self-contained-html" `
        "--junitxml=$pytestReportDir/junit.xml"
    $pytestExitCode = $LASTEXITCODE

    & $Python -m flake8 src tests `
        --config=.flake8 `
        --statistics `
        --tee `
        "--output-file=$flake8ReportDir/flake8.txt"
    $flake8TextExitCode = $LASTEXITCODE

    & $Python -m flake8 src tests `
        --config=.flake8 `
        --format=html `
        "--htmldir=$flake8ReportDir"
    $flake8HtmlExitCode = $LASTEXITCODE

    if ($pytestExitCode -ne 0 -or $flake8TextExitCode -ne 0 -or $flake8HtmlExitCode -ne 0) {
        exit 1
    }
}
finally {
    Pop-Location
}
