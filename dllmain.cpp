// dllmain.cpp : Defines the entry point for the DLL application.
#include "pch.h"
#include <Windows.h>
#include <WinUser.h>

extern "C" __declspec(dllexport)
void MoveCursor(int x, int y)
{
    SetCursorPos(x, y);
    
}

extern "C" __declspec(dllexport)
void LeftClick() {
    INPUT inputs[2] = {};

    inputs[0].type = INPUT_MOUSE;
    inputs[0].mi.dwFlags = MOUSEEVENTF_LEFTDOWN;

    inputs[1].type = INPUT_MOUSE;
    inputs[1].mi.dwFlags = MOUSEEVENTF_LEFTUP;

    SendInput(2, inputs, sizeof(INPUT));
}

extern "C" __declspec(dllexport)
void ScrollVertical(int amount) {
    INPUT input = { 0 };
    input.type = INPUT_MOUSE;
    input.mi.dwFlags = MOUSEEVENTF_WHEEL;
    input.mi.mouseData = static_cast<DWORD>(amount);
    SendInput(1, &input, sizeof(INPUT));
}

extern "C" __declspec(dllexport)
void ScrollHorizontal(int amount) {
    INPUT input = { 0 };
    input.type = INPUT_MOUSE;
    input.mi.dwFlags = MOUSEEVENTF_HWHEEL;
    input.mi.mouseData = static_cast<DWORD>(amount);
    SendInput(1, &input, sizeof(INPUT));
}