@echo off
setlocal

pushd

:: �茳�̃X�N���v�g�ɕK�v�ȃ��C�u������pip�ł܂Ƃ߂ăC���X�g�[��

set pipcmd=pip install -r requirements.txt
echo %pipcmd%
title %pipcmd%
call %pipcmd%
echo;

popd

exit /b