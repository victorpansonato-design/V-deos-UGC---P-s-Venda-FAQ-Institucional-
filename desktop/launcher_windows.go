// The launcher delegates to Windows PowerShell with its existing script policy.
package main

import (
	"errors"
	"fmt"
	"os"
	"os/exec"
	"path/filepath"
	"syscall"
	"unsafe"
)

const (
	createNoWindow = 0x08000000
	messageError   = 0x10
)

func main() {
	if err := openStudio(); err != nil {
		showProblem(err.Error())
		os.Exit(1)
	}
}

func openStudio() error {
	executable, err := os.Executable()
	if err != nil {
		return errors.New("O Windows não identificou a pasta do estúdio.")
	}
	script := filepath.Join(filepath.Dir(executable), "Studio.ps1")
	info, err := os.Stat(script)
	if err != nil || !info.Mode().IsRegular() {
		return errors.New("Mantenha Studio.ps1 na mesma pasta do executável.")
	}
	system, err := systemDirectory()
	if err != nil {
		return fmt.Errorf("O Windows não localizou a pasta de sistema: %w", err)
	}
	host := filepath.Join(system, "WindowsPowerShell", "v1.0", "powershell.exe")
	command := exec.Command(host, "-NoLogo", "-NoProfile", "-STA", "-File", script)
	command.SysProcAttr = &syscall.SysProcAttr{HideWindow: true, CreationFlags: createNoWindow}
	if err := command.Run(); err != nil {
		return fmt.Errorf("O estúdio foi encerrado com erro (%w). Confira os requisitos do pacote e a política de scripts com a TI.", err)
	}
	return nil
}

func systemDirectory() (string, error) {
	buffer := make([]uint16, 32768)
	procedure := syscall.NewLazyDLL("kernel32.dll").NewProc("GetSystemDirectoryW")
	length, _, failure := procedure.Call(uintptr(unsafe.Pointer(&buffer[0])), uintptr(len(buffer)))
	if length == 0 {
		return "", failure
	}
	if length >= uintptr(len(buffer)) {
		return "", errors.New("Caminho de sistema muito longo.")
	}
	return syscall.UTF16ToString(buffer), nil
}

func showProblem(message string) {
	text, _ := syscall.UTF16PtrFromString(message)
	title, _ := syscall.UTF16PtrFromString("Estúdio UniAnchieta")
	procedure := syscall.NewLazyDLL("user32.dll").NewProc("MessageBoxW")
	procedure.Call(0, uintptr(unsafe.Pointer(text)), uintptr(unsafe.Pointer(title)), messageError)
}
