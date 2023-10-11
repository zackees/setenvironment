@echo off

:: RefreshEnv.cmd

:: Define a unique temporary directory for this script
SET "LOCAL_TEMP_DIR=%~dp0RefreshEnvTemp_%RANDOM%_%TIME:~0,2%%TIME:~3,2%%TIME:~6,2%"
mkdir "%LOCAL_TEMP_DIR%"
if not exist "%LOCAL_TEMP_DIR%" (
    echo Failed to create the temporary directory.
    echo Exiting script.
    exit /b
)

echo | set /p dummy="Refreshing environment variables from registry for cmd.exe. Please wait..."
goto main

:SetFromReg
    "%WinDir%\System32\Reg" QUERY "%~1" /v "%~2" > "%LOCAL_TEMP_DIR%\_envset.tmp" 2>NUL
    for /f "usebackq skip=2 tokens=2,*" %%A IN ("%LOCAL_TEMP_DIR%\_envset.tmp") do (
        echo/set "%~3=%%B"
    )
    goto :EOF

:GetRegEnv
    "%WinDir%\System32\Reg" QUERY "%~1" > "%LOCAL_TEMP_DIR%\_envget.tmp"
    for /f "usebackq skip=2" %%A IN ("%LOCAL_TEMP_DIR%\_envget.tmp") do (
        if /I not "%%~A"=="Path" (
            call :SetFromReg "%~1" "%%~A" "%%~A"
        )
    )
    goto :EOF
    

:main
    echo/@echo off >"%LOCAL_TEMP_DIR%\_env.cmd"

    call :GetRegEnv "HKLM\System\CurrentControlSet\Control\Session Manager\Environment" >> "%LOCAL_TEMP_DIR%\_env.cmd"
    call :GetRegEnv "HKCU\Environment" >> "%LOCAL_TEMP_DIR%\_env.cmd"

    call :SetFromReg "HKLM\System\CurrentControlSet\Control\Session Manager\Environment" Path Path_HKLM >> "%LOCAL_TEMP_DIR%\_env.cmd"
    call :SetFromReg "HKCU\Environment" Path Path_HKCU >> "%LOCAL_TEMP_DIR%\_env.cmd"

    echo/set "Path=%%Path_HKLM%%;%%Path_HKCU%%" >> "%LOCAL_TEMP_DIR%\_env.cmd"

    SET "OriginalUserName=%USERNAME%"
    SET "OriginalArchitecture=%PROCESSOR_ARCHITECTURE%"

    call "%LOCAL_TEMP_DIR%\_env.cmd"

    SET "USERNAME=%OriginalUserName%"
    SET "PROCESSOR_ARCHITECTURE=%OriginalArchitecture%"

    echo | set /p dummy="Finished."
    echo .

    :: Cleanup the temporary directory
    rmdir /s /q "%LOCAL_TEMP_DIR%"
