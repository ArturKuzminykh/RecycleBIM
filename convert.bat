@echo off
set ref=%1
cd /d D:\xampp-htdocs\RecycleBIM2
node xeokit-convert\convert2xkt.js -s "uploads\%ref%" -o "models_xkt\%ref%.xkt"