@echo off
echo Nettoyage des fichiers temporaires...
echo.

del /q *.aux 2>nul
del /q *.log 2>nul
del /q *.out 2>nul
del /q *.synctex.gz 2>nul
del /q *.comp 2>nul
del /q *.voc 2>nul
del /q bfpoints_*.tex 2>nul

echo Nettoyage termine !
echo.
pause