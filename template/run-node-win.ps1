# -----------------------------------------------------------------------------
# Este arquivo instala as dependencias do Node necessarias para gerar o 
# APK/AAB para Android e o IPA para IOS
# -----------------------------------------------------------------------------

$StartTime = $(get-date)
Write-Host "Stage - Node Install ----------------------------------------------------------"
try {
    npm install --legacy-peer-deps
    npm run configure
    Write-Host "Node Install Stage Completed Successfully!"
}
catch {
    Write-Error "Error when executing Node Install"
}

$elapsedTime = $(get-date) - $StartTime
Write-Host "Elapsed Time: $elapsedTime"
exit $LASTEXITCODE # 0 for success and 1 for failure
