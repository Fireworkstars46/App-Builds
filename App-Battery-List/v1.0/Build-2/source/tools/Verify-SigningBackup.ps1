param(
    [Parameter(Mandatory=$true)][string]$KeystorePath,
    [Parameter(Mandatory=$true)][string]$StorePassword,
    [string]$Alias = "appbatterylist-release"
)

$ErrorActionPreference = "Stop"
$ExpectedPath = Join-Path $PSScriptRoot "..\signing\EXPECTED_SIGNER_SHA256.txt"
$Expected = (Get-Content -Raw $ExpectedPath).Trim()
$Output = & keytool -list -v -keystore $KeystorePath -storepass $StorePassword -alias $Alias 2>&1
if ($LASTEXITCODE -ne 0) { throw ($Output -join "`n") }
$Line = $Output | Select-String -Pattern 'SHA256:' | Select-Object -First 1
if (-not $Line) { throw "Could not find SHA256 fingerprint in keytool output." }
$Actual = (($Line.Line -split 'SHA256:')[1]).Trim()
Write-Host "Expected: $Expected"
Write-Host "Actual:   $Actual"
if ($Actual -ne $Expected) {
    Write-Error "FAIL - signing identity mismatch."
    exit 1
}
Write-Host "PASS - recovered signing identity matches expected fingerprint."
