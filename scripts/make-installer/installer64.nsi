; basic script template for NSIS installers
;
; Written by Philip Chu
; Copyright (c) 2004-2005 Technicat, LLC
;
; This software is provided 'as-is', without any express or implied warranty.
; In no event will the authors be held liable for any damages arising from the use of this software.
 
; Permission is granted to anyone to use this software for any purpose,
; including commercial applications, and to alter it ; and redistribute
; it freely, subject to the following restrictions:
 
;    1. The origin of this software must not be misrepresented; you must not claim that
;       you wrote the original software. If you use this software in a product, an
;       acknowledgment in the product documentation would be appreciated but is not required.
 
;    2. Altered source versions must be plainly marked as such, and must not be
;       misrepresented as being the original software.
 
;    3. This notice may not be removed or altered from any source distribution.

; add If/Endif macros
!include LogicLib.nsh
 
!define setup "neuropype-setup-1.x.x-x64.exe"
 
; change this to wherever the files to be packaged reside
!define srcdir "."
 
!define company "Qusp"
 
!define prodname "NeuroPype (64-bit)"
!define exec "neuropype.bat"
 
; optional stuff
 
; Set the text which prompts the user to enter the installation directory
; DirText "My Description Here."
 
; text file to open in notepad after installation
; !define notefile "README.txt"
 
; license text file
!define licensefile license.rtf
 
; icons must be Microsoft .ICO files
!define icon "neuropype.ico"
 
; installer background screen
; !define screenimage background.bmp
 
; file containing list of file-installation commands
!define files "files.nsi"
 
; file containing list of file-uninstall commands
!define unfiles "unfiles.nsi"
 
; registry stuff
 
!define regkey "Software\${company}\${prodname}"
!define uninstkey "Software\Microsoft\Windows\CurrentVersion\Uninstall\${prodname}"
 
!define startmenu "$SMPROGRAMS\${company}\${prodname}"
!define uninstaller "uninstall.exe"
 
;--------------------------------
 
XPStyle on
ShowInstDetails hide
ShowUninstDetails hide
 
Name "${prodname}"
Caption "${prodname}"
 
!ifdef icon
Icon "${icon}"
!endif
 
OutFile "${setup}"
 
SetDateSave on
SetDatablockOptimize on
CRCCheck on
SilentInstall normal
 
InstallDir "$PROGRAMFILES64\${company}\${prodname}"
InstallDirRegKey HKLM "${regkey}" ""
 
!ifdef licensefile
LicenseText "License"
LicenseData "${srcdir}\${licensefile}"
!endif
 
; pages
; we keep it simple - leave out selectable installation types
 
!ifdef licensefile
Page license
!endif
 
; Page components
Page directory
Page instfiles
 
UninstPage uninstConfirm
UninstPage instfiles
 
;--------------------------------
 
AutoCloseWindow false
ShowInstDetails show
 
 
!ifdef screenimage
 
; set up background image
; uses BgImage plugin
 
Function .onGUIInit
	; extract background BMP into temp plugin directory
	InitPluginsDir
	File /oname=$PLUGINSDIR\1.bmp "${screenimage}"
 
	BgImage::SetBg /NOUNLOAD /FILLSCREEN $PLUGINSDIR\1.bmp
	BgImage::Redraw /NOUNLOAD
FunctionEnd
 
Function .onGUIEnd
	; Destroy must not have /NOUNLOAD so NSIS will be able to unload and delete BgImage before it exits
	BgImage::Destroy
FunctionEnd
 
!endif
 
; uninstall previous section
Section 

    ; Check for uninstaller.
    ReadRegStr $R0 HKLM "${regkey}" "Install_Dir"

    ${If} $R0 == ""        
        Goto Done
    ${EndIf}

    DetailPrint "Removing previous installation."    

    ; Run the uninstaller silently.
    ExecWait '"$R0\uninstall.exe" _?=$R0'

    Done:
    
SectionEnd

; beginning (invisible) section
Section
 
  WriteRegStr HKLM "${regkey}" "Install_Dir" "$INSTDIR"
  ; write uninstall strings
  WriteRegStr HKLM "${uninstkey}" "DisplayName" "${prodname} (remove only)"
  WriteRegStr HKLM "${uninstkey}" "UninstallString" '"$INSTDIR\${uninstaller}"'
 
!ifdef filetype
  WriteRegStr HKCR "${filetype}" "" "${prodname}"
!endif
 
  WriteRegStr HKCR "${prodname}\Shell\open\command\" "" '"$INSTDIR\${exec} "%1"'
 
!ifdef icon
  WriteRegStr HKCR "${prodname}\DefaultIcon" "" "$INSTDIR\${icon}"
!endif
 
  SetOutPath $INSTDIR
 
 
; package all files, recursively, preserving attributes
; assume files are in the correct places
File /a "${srcdir}\${exec}"
 
!ifdef licensefile
File /a "${srcdir}\${licensefile}"
!endif
 
!ifdef notefile
File /a "${srcdir}\${notefile}"
!endif
 
!ifdef icon
File /a "${srcdir}\${icon}"
!endif
 
; any application-specific files
!ifdef files
!include "${files}"
!endif
 
  WriteUninstaller "${uninstaller}"
  
; register python venv
SetOutPath "$INSTDIR"
ExpandEnvStrings $0 %COMSPEC%
ExecWait "$INSTDIR\postinstall.cmd"
Delete "$INSTDIR\postinstall.cmd"
 
SectionEnd
 
; create shortcuts
Section
  SetShellVarContext all
  
  CreateDirectory "${startmenu}"
  SetOutPath $INSTDIR ; for working directory
!ifdef icon
  CreateShortCut "${startmenu}\${prodname}.lnk" "$INSTDIR\${exec}" "" "$INSTDIR\${icon}"
  CreateShortCut "$DESKTOP\${prodname}.lnk" "$INSTDIR\${exec}" "" "$INSTDIR\${icon}"
!else
  CreateShortCut "${startmenu}\${prodname}.lnk" "$INSTDIR\${exec}"
  CreateShortCut "$DESKTOP\${prodname}.lnk" "$INSTDIR\${exec}"
!endif

CreateShortCut "${startmenu}\Lab Recorder.lnk" "$INSTDIR\labrecorder.bat"
CreateShortCut "${startmenu}\Installation.lnk" "$INSTDIR"

SectionEnd
 
; Uninstaller
; All section names prefixed by "Un" will be in the uninstaller
 
UninstallText "This will uninstall ${prodname}."
 
!ifdef icon
UninstallIcon "${icon}"
!endif
 
Section "Uninstall"
  
  DeleteRegKey HKLM "${uninstkey}"
  DeleteRegKey HKLM "${regkey}"
 
  Delete "${startmenu}\*.*"
  Delete "${startmenu}"
  RMDir "$SMPROGRAMS\${company}\${prodname}"  
  RMDir "$SMPROGRAMS\${company}"  
  Delete "$DESKTOP\${prodname}.lnk"

  ; also delete from all-users folder
  SetShellVarContext all
  Delete "${startmenu}\*.*"
  Delete "${startmenu}"
  RMDir "$SMPROGRAMS\${company}\${prodname}"  
  RMDir "$SMPROGRAMS\${company}"  
  Delete "$DESKTOP\${prodname}.lnk"


!ifdef licensefile
Delete "$INSTDIR\${licensefile}"
!endif
 
!ifdef notefile
Delete "$INSTDIR\${notefile}"
!endif
 
!ifdef icon
Delete "$INSTDIR\${icon}"
!endif
 
Delete "$INSTDIR\${exec}"

; delete files generated dynamically during installation
Delete "$INSTDIR\python\qt.conf"
Delete "$INSTDIR\python\Lib\site-packages\*.*"
Delete "$INSTDIR\python\Scripts\*.*"

!ifdef unfiles
!include "${unfiles}"
!endif

Delete "$INSTDIR\uninstall.exe"

RMDir "$INSTDIR"
RMDir "$PROGRAMFILES64\${company}"

SectionEnd

