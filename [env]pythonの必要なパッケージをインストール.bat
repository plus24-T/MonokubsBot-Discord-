@echo off
setlocal

pushd

:: 手元のスクリプトに必要なライブラリをpipでまとめてインストール

set pipcmd=pip install -r requirements.txt
echo %pipcmd%
title %pipcmd%
call %pipcmd%
echo;

popd

exit /b