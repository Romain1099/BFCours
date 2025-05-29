@echo off
echo ========================================
echo Compilation des Cartes auto-correctives
echo ========================================
echo.

:menu
echo Choisissez le mode de compilation :
echo 1. Version simple (pdfLaTeX) - Recommande
echo 2. Version complete (LuaLaTeX avec bfcours)
echo 3. Quitter
echo.
set /p choix="Votre choix (1, 2 ou 3) : "

if "%choix%"=="1" goto simple
if "%choix%"=="2" goto complete
if "%choix%"=="3" goto fin
goto menu

:simple
echo.
echo Compilation avec pdfLaTeX...
pdflatex Cartes_equations_simple.tex
echo.
echo Compilation terminee !
echo Le fichier Cartes_equations_simple.pdf a ete genere.
goto fin

:complete
echo.
echo Compilation avec LuaLaTeX...
lualatex Cartes_equations.tex
echo.
echo Compilation terminee !
echo Le fichier Cartes_equations.pdf a ete genere.
goto fin

:fin
echo.
pause