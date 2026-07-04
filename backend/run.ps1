$env:JAVA_HOME = "C:\Program Files\Microsoft\jdk-17.0.19.10-hotspot"
$env:PATH = "$env:JAVA_HOME\bin;$env:PATH"
Write-Host "Using Java:" -ForegroundColor Cyan
& "$env:JAVA_HOME\bin\java.exe" -version
Write-Host ""
.\mvnw spring-boot:run
