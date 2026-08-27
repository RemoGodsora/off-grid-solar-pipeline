<#
.SYNOPSIS
Install the FS CLI Binary for a target platform.

.DESCRIPTION
This script installs the FS CLI Binary. It allows specifying the version, target platform, and installation location.

.PARAMETER Update
Updates to latest or specified version.

.PARAMETER Version
Version of the CLI to install. Default is the latest release.

.PARAMETER Target
Install the release compiled for the specified target OS.

.PARAMETER To
Location where to install the binary. Default is C:\Program Files.

.EXAMPLE
.\install.ps1 -Update

.EXAMPLE
.\install.ps1 -Version "1.2.3" -Target "Windows" -To "C:\MyFolder"
#>

param(
    [switch]$Update,
    [string]$Version,
    [string]$Target,
    [string]$To = "C:\Program Files"
)


function Write-Log {
    param($Message)
    Write-Host "install.ps1: $Message"
}

function Write-ErrorLog {
    param($Message)
    Write-Error "install.ps1: ERROR $Message"
}

# Check for required commands
function Test-Need {
    param($Command)
    if (-not (Get-Command $Command -ErrorAction SilentlyContinue)) {
        Write-ErrorLog "need $Command (command not found)"
        exit 1
    }
}

# Process arguments
if ($PSBoundParameters.ContainsKey('Help')) {
    Get-Help $MyInvocation.MyCommand.Name
    exit 0
}

# Main script logic starts here

# Define the URL to fetch the latest version
$fetchLatest = "https://public.cdn.getdbt.com/fs/latest.json"

# Check for current installed version
$currentVersion = $null
$fsPath = Join-Path -Path $To -ChildPath "fs.exe"
if (Test-Path $fsPath) {
    try {
        $versionOutput = & $fsPath --version 2>$null
        if ($versionOutput -match '\s+v?(\d+\.\d+\.\d+)') {
            $currentVersion = $Matches[1]
            Write-Log "Current installed version: $currentVersion"
        }
    } catch {
        Write-Log "Could not determine current version"
    }
}

# Check if a specific version is provided
if ([string]::IsNullOrEmpty($Version)) {
    Write-Log "Downloading $fetchLatest"
    $versionInfo = Invoke-RestMethod -Uri $fetchLatest
    $version = $versionInfo -replace '^v', ''
    Write-Log "Version: latest ($version)"
    
    # If current version matches latest exit
    if (($currentVersion -eq $version)) {
        Write-Host "`nLatest version $version is already installed.`n"
        exit 0
    }
} else {
    Write-Log "Version: $version"
    
    # If current version matches requested version, exit
    if (($currentVersion -eq $version)) {
        Write-Host "`nVersion $version is already installed.`n"
        exit 0
    }
}


# Determine CPU architecture and operating system
$cpuArchTarget = switch -Wildcard ((Get-WmiObject Win32_Processor).Architecture) {
    0 { "x86" }
    9 { "x64" }
    # Add more cases if needed for different architectures
    Default { "unknown" }
}

$operatingSystem = "windows" # Since this script is intended for Windows

# Log the information
Write-Log "CPU Architecture: $cpuArchTarget"
Write-Log "Operating System: $operatingSystem"

if ([string]::IsNullOrEmpty($Target)) {
    # Check CPU architecture and set target for supported architecture
    if ($cpuArchTarget -eq "x64") {
        $target = "x86_64-pc-windows-msvc"
    } else {
        Write-ErrorLog "Unsupported CPU Architecture: $cpuArchTarget"
        exit 1
    }
}

# Log the target
Write-Log "Target: $target"

# Setting the default installation destination if not specified
if ([string]::IsNullOrEmpty($To)) {
    # Install to user's AppData folder which doesn't require admin privileges
    $dest = Join-Path -Path $env:USERPROFILE -ChildPath ".local\bin"
} else {
    $dest = $To
}

Write-Log "Installing to: $dest"

# Construct the download URL for the zip file
$url = "https://public.cdn.getdbt.com/fs/fs-v$version-$target.zip"

Write-Log "Downloading: $url"

# Create a temporary directory for the download
$td = New-Item -ItemType Directory -Force -Path ([System.IO.Path]::GetTempPath() + [System.Guid]::NewGuid().ToString())

# Download the zip file
Invoke-WebRequest -Uri $url -OutFile "$td\fs.zip"

# Extract the contents of the zip file
Expand-Archive -Path "$td\fs.zip" -DestinationPath $td -Force

# Iterate over files in the temporary directory
Get-ChildItem -Path $td -File | ForEach-Object {
    $filePath = $_.FullName

    # Check if the file is executable (in Windows, you might check for .exe extension or similar)
    if ($_.Extension -ne ".exe") {
        return
    }

    $destFilePath = Join-Path -Path $dest -ChildPath $_.Name

    # Check for existing installation
    if (Test-Path -Path $destFilePath) {
        if (-not $Update) {
            Write-ErrorLog "fs already exists in $dest"
            exit 1
        } else {
            # Remove the existing file if updating
            Remove-Item -Path $destFilePath -Force
        }
    }

    # Create destination directory if it doesn't exist
    if (-not (Test-Path -Path $dest)) {
        New-Item -Path $dest -ItemType Directory -Force
    }

    # Copy the file to the destination
    Copy-Item -Path $filePath -Destination $destFilePath -Force
}

# Add the installation destination to the user PATH if it's not already there
$userPath = [Environment]::GetEnvironmentVariable('Path', [EnvironmentVariableTarget]::User)
if (-not $userPath.Split(';').Contains($dest)) {
    $newUserPath = $userPath + ';' + $dest
    [Environment]::SetEnvironmentVariable('Path', $newUserPath, [EnvironmentVariableTarget]::User)
    Write-Log "Added $dest to user PATH."
}

Write-Host "`nSuccessfully installed fs v$version to $dest\fs`n"
Write-Host "Run 'fs --help' to get started`n"

# Clean up the temporary directory
Remove-Item -Path $td -Recurse -Force