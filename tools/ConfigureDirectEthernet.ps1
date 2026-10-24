param([ValidateSet('Direct','Dhcp')][string]$Mode = 'Direct')
$ErrorActionPreference = 'Stop'
Start-Transcript -Path (Join-Path $PSScriptRoot 'ethernet-setup.log') -Force | Out-Null
try {
# Only the USB Ethernet adapter observed on this laptop; never change WLAN.
$adapterGuid = [guid]'C73A7AD9-9976-45C4-9E73-34C3EDF79418'
$adapter = Get-NetAdapter | Where-Object { [guid]$_.InterfaceGuid -eq $adapterGuid }
if (@($adapter).Count -ne 1) { throw 'Der erwartete USB-LAN-Adapter wurde nicht eindeutig gefunden.' }
$index = $adapter.ifIndex
$ip = '192.168.77.1'
$existing = @(Get-NetIPAddress -InterfaceIndex $index -AddressFamily IPv4 -ErrorAction SilentlyContinue)
if ($Mode -eq 'Direct') {
    if ($adapter.Status -ne 'Up') { throw 'USB-LAN-Verbindung ist nicht aktiv.' }
    $unexpected = @($existing | Where-Object { $_.IPAddress -notlike '169.254.*' -and $_.IPAddress -ne $ip })
    if ($unexpected.Count) { throw 'Adapter besitzt bereits eine andere IPv4-Adresse. Keine automatische Aenderung.' }
    $defaultRoutes = @(Get-NetRoute -InterfaceIndex $index -AddressFamily IPv4 -DestinationPrefix '0.0.0.0/0' -ErrorAction SilentlyContinue)
    if ($defaultRoutes.Count) { throw 'Adapter besitzt eine Standardroute. Keine automatische Aenderung.' }
    if (-not ($existing | Where-Object { $_.IPAddress -eq $ip })) {
        # Windows disables DHCP on this adapter when adding the static address.
        New-NetIPAddress -InterfaceIndex $index -AddressFamily IPv4 -IPAddress $ip -PrefixLength 24 | Out-Null
    }
} else {
    if ($existing | Where-Object { $_.IPAddress -eq $ip }) {
        Remove-NetIPAddress -InterfaceIndex $index -IPAddress $ip -Confirm:$false
    }
    Set-NetIPInterface -InterfaceIndex $index -AddressFamily IPv4 -Dhcp Enabled
}
Get-NetIPAddress -InterfaceIndex $index -AddressFamily IPv4 | Select-Object InterfaceAlias,IPAddress,PrefixLength,AddressState
} catch {
    Write-Output $_.Exception.Message
    throw
} finally {
    Stop-Transcript | Out-Null
}
