// Crash Monitor 4.2 Build 12
// Multi-app Windows tray crash monitor with a graphical program manager and installer UI.
// WER LocalDumps remains the default backend. OBS additionally gets an external enhanced fallback:
// one automatic pre-crash dump on extreme handle growth plus severe-exception/abnormal-exit dump attempts.
// Version 4.2 Build 12 expands the automated release test so formerly manual Windows checks are exercised automatically where safe.
// The persistent Safe Self-Test report stays in %LOCALAPPDATA%\Crash Monitor next to monitor.log.
// Isolated Safe Self-Test working data stays in Windows Temp so real settings/data stay untouched.
// Build 12 preserves Build 11's automation and fixes the Build 11 pre-report Safe Self-Test access violation
// by running the large release-test body on a dedicated worker stack with an explicit committed size.
// The automated Update/Repair staging, actual user-visible Start Menu shortcut launch, and guarded
// physical Explorer/taskbar restart with recovery are preserved.
// Environment-owned sign-in, Windows Search indexing, UAC approval, and AV/SmartScreen reputation remain reported honestly.
// Slow archive-tool subprocesses remain bounded.
// Real dump tests continue to use a separate isolated helper process. Partial reports are flushed continuously.
// Truly disruptive/environment-owned checks remain NOT TESTED.
// It preserves the live-safe OBS dump path and lossless sharing compression, adds Explorer/taskbar
// tray-icon recovery, bounds project logs, verifies settings writes, fixes installed version metadata,
// and replaces the cmd.exe/ping self-delete sequence with documented MoveFileEx cleanup.
// Successfully created dumps are packed into a standard ZIP with Windows' built-in tar tool.
// The ZIP is verified before the raw .dmp is removed. If the ZIP is still above the Discord Nitro
// upload limit, Crash Monitor splits it into sendable numbered parts and writes a reassembly .cmd.
// 4.1.5 fixed the OBS PSS dump path seen on Windows 10 systems where
// MiniDumpWriteDump can reject the HPSS descriptor with HRESULT_FROM_NT(STATUS_INVALID_HANDLE).
// The official HPSS MiniDumpWriteDump path is tried first; if that specific snapshot-handle path fails,
// Crash Monitor queries the PSS VA-clone process and writes the dump from the clone instead. The live
// OBS process is never used as the fallback dump source, so projectors stay live during file writing.
// There is no separate splitter bar: hover the top edge of the program-info box for the up/down resize cursor.
// Dragging that edge moves the boundary between the program list/buttons and the info box while keeping all controls visible.
// OBS projector-safe dump path: OBS is snapshotted first with Windows Process Snapshotting (PSS),
// then MiniDumpWriteDump writes from the snapshot instead of holding the live OBS process for the
// full file-write duration. TEST remains asynchronous; PRECRASH remains handle-focused.
// No process injection or remote code execution.


#define CM_VERSION_W L"4.2"
#define CM_BUILD_W L"12"
#define CM_VERSION_BUILD_W L"Crash Monitor 4.2 Build 12"

#define NULLPTR ((void*)0)
typedef unsigned char BYTE; typedef unsigned short WORD; typedef unsigned int UINT; typedef unsigned long DWORD; typedef long LONG; typedef long HRESULT; typedef unsigned long ULONG; typedef long long LONGLONG; typedef unsigned long long ULONGLONG; typedef unsigned long long ULONG_PTR; typedef ULONG_PTR SIZE_T; typedef int BOOL; typedef wchar_t WCHAR; typedef char CHAR; typedef void VOID; typedef void* PVOID; typedef void* HANDLE; typedef HANDLE HWND; typedef HANDLE HMONITOR; typedef HANDLE HINSTANCE; typedef HANDLE HICON; typedef HANDLE HCURSOR; typedef HANDLE HMENU; typedef HANDLE HMODULE; typedef HANDLE HKEY; typedef HANDLE HFONT; typedef HANDLE HGDIOBJ; typedef const WCHAR* LPCWSTR; typedef WCHAR* LPWSTR; typedef const CHAR* LPCSTR; typedef CHAR* LPSTR; typedef ULONG_PTR WPARAM; typedef LONGLONG LPARAM; typedef LONGLONG LRESULT; typedef LONGLONG LONG_PTR; typedef DWORD (__stdcall *LPTHREAD_START_ROUTINE)(PVOID);
#define WINAPI __stdcall
#define CALLBACK __stdcall
#define TRUE 1
#define FALSE 0
#define MAX_PATH 260
#define INVALID_HANDLE_VALUE ((HANDLE)(LONGLONG)-1)
#define ERROR_ALREADY_EXISTS 183
#define ERROR_SUCCESS 0L
#define ERROR_FILE_NOT_FOUND 2L
#define GENERIC_READ 0x80000000u
#define GENERIC_WRITE 0x40000000u
#define FILE_SHARE_READ 0x1u
#define FILE_SHARE_WRITE 0x2u
#define OPEN_EXISTING 3u
#define OPEN_ALWAYS 4u
#define FILE_ATTRIBUTE_NORMAL 0x80u
#define FILE_ATTRIBUTE_DIRECTORY 0x10u
#define INVALID_FILE_ATTRIBUTES 0xFFFFFFFFu
#define FILE_END 2u
#define TH32CS_SNAPPROCESS 0x2u
#define PROCESS_QUERY_LIMITED_INFORMATION 0x1000u
#define PROCESS_QUERY_INFORMATION 0x0400u
#define PROCESS_VM_READ 0x0010u
#define PROCESS_DUP_HANDLE 0x0040u
#define PROCESS_CREATE_PROCESS 0x0080u
#define PROCESS_TERMINATE 0x0001u
#define SYNCHRONIZE 0x00100000u
#define CREATE_ALWAYS 2u
#define WAIT_OBJECT_0 0u
#define WAIT_TIMEOUT 258u
#define EXCEPTION_DEBUG_EVENT 1u
#define CREATE_THREAD_DEBUG_EVENT 2u
#define CREATE_PROCESS_DEBUG_EVENT 3u
#define EXIT_THREAD_DEBUG_EVENT 4u
#define EXIT_PROCESS_DEBUG_EVENT 5u
#define LOAD_DLL_DEBUG_EVENT 6u
#define UNLOAD_DLL_DEBUG_EVENT 7u
#define OUTPUT_DEBUG_STRING_EVENT 8u
#define RIP_EVENT 9u
#define DBG_CONTINUE 0x00010002u
#define DBG_EXCEPTION_NOT_HANDLED 0x80010001u
#define OBS_PRECRASH_HANDLE_THRESHOLD 250000u
#define WM_DESTROY 0x0002u
#define WM_SIZE 0x0005u
#define WM_EXITSIZEMOVE 0x0232u
#define WM_SETCURSOR 0x0020u
#define WM_NCHITTEST 0x0084u
#define WM_NCMOUSEMOVE 0x00A0u
#define WM_NCLBUTTONDOWN 0x00A1u
#define WM_NCLBUTTONUP 0x00A2u
#define WM_CANCELMODE 0x001Fu
#define WM_CAPTURECHANGED 0x0215u
#define WM_MOUSEMOVE 0x0200u
#define WM_LBUTTONDOWN 0x0201u
#define WM_VSCROLL 0x0115u
#define WM_MOUSEWHEEL 0x020Au
#define WM_GETMINMAXINFO 0x0024u
#define WM_CLOSE 0x0010u
#define WM_COMMAND 0x0111u
#define WM_TIMER 0x0113u
#define WM_SETFONT 0x0030u
#define WM_SETICON 0x0080u
#define WM_APP 0x8000u
#define WM_RBUTTONUP 0x0205u
#define WM_LBUTTONUP 0x0202u
#define WM_LBUTTONDBLCLK 0x0203u
#define WM_CONTEXTMENU 0x007Bu
#define WM_SETTINGCHANGE 0x001Au
#define WM_TRAY (WM_APP+10)
#define WM_STATE (WM_APP+11)
#define WM_CAPTURED (WM_APP+12)
#define WM_CONFIG_CHANGED (WM_APP+13)
#define WM_TESTDONE (WM_APP+14)
#define WM_SHOW_EXISTING (WM_APP+15)
#define WM_SELFTESTDONE (WM_APP+16)
#define WM_SELFTESTPROGRESS (WM_APP+17)
#define SELFTEST_HANG_TIMEOUT_MS 180000u
#define ARCHIVE_TOOL_TIMEOUT_MS 120000u
#define SPLIT_IO_BUFFER_BYTES 1048576u
#define MEM_COMMIT 0x00001000u
#define MEM_RESERVE 0x00002000u
#define MEM_RELEASE 0x00008000u
#define PAGE_READWRITE 0x04u
#define CM_SELFTEST_TIMEOUT_CODE 0xE0420001u
#define CM_SELFTEST_LAUNCH_FAILED_CODE 0xE0420002u
#define ICON_SMALL 0
#define ICON_BIG 1
#define MB_OK 0x0u
#define MB_YESNO 0x4u
#define MB_ICONERROR 0x10u
#define MB_ICONQUESTION 0x20u
#define MB_ICONINFORMATION 0x40u
#define MB_ICONWARNING 0x30u
#define IDYES 6
#define SW_HIDE 0
#define SW_SHOWNORMAL 1
#define SW_SHOW 5
#define SW_MINIMIZE 6
#define SW_RESTORE 9
#define SMTO_ABORTIFHUNG 0x0002u
#define HWND_BROADCAST ((HWND)(ULONG_PTR)0xFFFFu)
#define SHCNE_ASSOCCHANGED 0x08000000L
#define SHCNF_IDLIST 0x0000u
#define SIZE_MINIMIZED 1
#define SPI_GETWORKAREA 0x0030u
#define MONITOR_DEFAULTTONEAREST 2u
#define MF_STRING 0x0u
#define MF_SEPARATOR 0x800u
#define MF_CHECKED 0x8u
#define MF_POPUP 0x10u
#define TPM_RIGHTBUTTON 0x2u
#define TPM_RETURNCMD 0x100u
#define NIM_ADD 0u
#define NIM_MODIFY 1u
#define NIM_DELETE 2u
#define NIF_MESSAGE 0x1u
#define NIF_ICON 0x2u
#define NIF_TIP 0x4u
#define NIF_INFO 0x10u
#define NIIF_INFO 1u
#define NIIF_WARNING 2u
#define NIIF_ERROR 3u
#define IDC_ARROW 32512
#define IDC_SIZENS 32645
#define HTTOP 12
#define GWLP_WNDPROC (-4)
#define REG_SZ 1u
#define REG_EXPAND_SZ 2u
#define REG_DWORD 4u
#define KEY_QUERY_VALUE 0x0001u
#define KEY_SET_VALUE 0x0002u
#define KEY_WRITE 0x00020006u
#define HKEY_CURRENT_USER ((HKEY)(ULONG_PTR)0xFFFFFFFF80000001ULL)
#define HKEY_LOCAL_MACHINE ((HKEY)(ULONG_PTR)0xFFFFFFFF80000002ULL)
#define GR_GDIOBJECTS 0u
#define GR_USEROBJECTS 1u
#define OFN_NOCHANGEDIR 0x8u
#define OFN_PATHMUSTEXIST 0x800u
#define OFN_FILEMUSTEXIST 0x1000u
#define OFN_EXPLORER 0x80000u
#define WS_OVERLAPPED 0x00000000L
#define WS_CAPTION 0x00C00000L
#define WS_SYSMENU 0x00080000L
#define WS_MINIMIZEBOX 0x00020000L
#define WS_MAXIMIZEBOX 0x00010000L
#define WS_THICKFRAME 0x00040000L
#define WS_VISIBLE 0x10000000L
#define WS_CHILD 0x40000000L
#define WS_BORDER 0x00800000L
#define WS_VSCROLL 0x00200000L
#define WS_TABSTOP 0x00010000L
#define WS_EX_CLIENTEDGE 0x00000200L
#define WS_EX_APPWINDOW 0x00040000L
#define WS_OVERLAPPEDWINDOW (WS_OVERLAPPED|WS_CAPTION|WS_SYSMENU|WS_THICKFRAME|WS_MINIMIZEBOX|WS_MAXIMIZEBOX)
#define BS_PUSHBUTTON 0x00000000L
#define BS_DEFPUSHBUTTON 0x00000001L
#define BS_AUTOCHECKBOX 0x00000003L
#define BS_GROUPBOX 0x00000007L
#define BST_UNCHECKED 0
#define BST_CHECKED 1
#define SS_LEFT 0x00000000L
#define SS_CENTER 0x00000001L
#define SS_ICON 0x00000003L
#define SS_NOPREFIX 0x00000080L
#define SS_NOTIFY 0x00000100L
#define SS_CENTERIMAGE 0x00000200L
#define SS_ETCHEDHORZ 0x00000010L
#define ES_READONLY 0x0800L
#define ES_MULTILINE 0x0004L
#define ES_AUTOVSCROLL 0x0040L
#define ES_AUTOHSCROLL 0x0080L
#define LBS_NOTIFY 0x0001L
#define LBS_NOINTEGRALHEIGHT 0x0100L
#define BN_CLICKED 0
#define LBN_DBLCLK 2
#define LBN_SELCHANGE 1
#define LB_ADDSTRING 0x0180u
#define LB_RESETCONTENT 0x0184u
#define LB_GETCURSEL 0x0188u
#define LB_SETCURSEL 0x0186u
#define LB_ERR (-1)
#define SB_LINEUP 0
#define SB_LINEDOWN 1
#define SB_PAGEUP 2
#define SB_PAGEDOWN 3
#define SB_THUMBPOSITION 4
#define SB_THUMBTRACK 5
#define SB_TOP 6
#define SB_BOTTOM 7
#define SB_ENDSCROLL 8
#define SB_VERT 1
#define SIF_RANGE 0x0001u
#define SIF_PAGE 0x0002u
#define SIF_POS 0x0004u
#define BM_GETCHECK 0x00F0u
#define BM_SETCHECK 0x00F1u
#define STM_SETICON 0x0170u
#define COLOR_WINDOW 5
#define FW_NORMAL 400
#define FW_SEMIBOLD 600
#define DEFAULT_CHARSET 1
#define OUT_DEFAULT_PRECIS 0
#define CLIP_DEFAULT_PRECIS 0
#define CLEARTYPE_QUALITY 5
#define DEFAULT_PITCH 0
#define FF_DONTCARE 0
#define MOVEFILE_REPLACE_EXISTING 0x1u
#define MOVEFILE_DELAY_UNTIL_REBOOT 0x4u
#define LOG_ROTATE_BYTES 5242880ULL
#define LOG_ROTATE_COUNT 5
#define CREATE_NEW_PROCESS_GROUP 0x00000200u
#define CREATE_NO_WINDOW 0x08000000u
#define INFINITE 0xFFFFFFFFu
#define DISCORD_PART_BYTES 475000000ULL
#define STATE_NEEDS_SETUP 0
#define STATE_WAITING 1
#define STATE_WATCHING 2
#define STATE_CAPTURED 3
#define STATE_ERROR 4
#define STATE_PAUSED 5
#define CLSCTX_INPROC_SERVER 0x1u
#define COINIT_APARTMENTTHREADED 0x2u
#define CSIDL_PROGRAMS 0x0002
#define CSIDL_DESKTOPDIRECTORY 0x0010
#define SHGFP_TYPE_CURRENT 0
#define MAX_TARGETS 32
#define MAX_RUNNING 64

// Main window controls
#define IDC_PROGRAMS 4100
#define IDC_ADD 4101
#define IDC_REMOVE 4102
#define IDC_TOGGLE 4103
#define IDC_REPAIR 4104
#define IDC_OPEN_DUMPS 4105
#define IDC_OPEN_DATA 4106
#define IDC_STARTUP 4107
#define IDC_PAUSE 4108
#define IDC_HIDE 4109
#define IDC_STATUS 4110
#define IDC_DETAILS 4111
#define IDC_HEADER 4112
#define IDC_DISPLAYMODE 4113
#define IDC_EXITAPP 4114
#define IDC_MINIMIZETRAY 4115
#define IDC_KEEPTRAYTASKBAR 4116
#define IDC_TEST_DUMP 4117
#define IDC_INFO_SPLITTER 4118
#define IDC_SAFE_SELF_TEST 4119
#define IDC_CLOSEXTRAY 4120
#define IDC_STARTMINIMIZED 4121
#define IDC_STARTPAUSED 4122
#define IDC_NOTIFICATIONS 4123
#define IDC_EXPORT_REPORT 4124
#define IDC_RESET_LAYOUT 4125

// Setup controls
#define IDC_SETUP_INSTALL 5101
#define IDC_SETUP_CANCEL 5102
#define IDC_SETUP_STARTUP 5103
#define IDC_SETUP_LAUNCH 5104
#define IDC_SETUP_PATH 5105
#define IDC_SETUP_STATUS 5106
#define IDC_SETUP_ICON 5107
#define IDC_SETUP_STARTMENU 5108
#define IDC_SETUP_DESKTOP 5109

// Tray commands
#define CMD_SHOW 1000
#define CMD_OPEN_CRASH 1001
#define CMD_OPEN_DATA 1002
#define CMD_STARTUP 1003
#define CMD_PAUSE 1004
#define CMD_ADD_PROGRAM 1005
#define CMD_ENABLE_WER 1006
#define CMD_DISABLE_WER 1007
#define CMD_EXIT 1008
#define CMD_TASKBAR 1009
#define CMD_UNINSTALL 1010
#define CMD_MINIMIZETRAY 1011
#define CMD_KEEPTRAYTASKBAR 1012
#define CMD_TEST_DUMP 1013
#define CMD_SAFE_SELF_TEST 1014
#define CMD_CLOSEXTRAY 1015
#define CMD_STARTMINIMIZED 1016
#define CMD_STARTPAUSED 1017
#define CMD_NOTIFICATIONS 1018
#define CMD_EXPORT_REPORT 1019
#define CMD_RESET_LAYOUT 1020
#define CMD_TOGGLE_BASE 2000
#define CMD_REMOVE_BASE 3000

struct FILETIME { DWORD dwLowDateTime; DWORD dwHighDateTime; };
struct SYSTEMTIME { WORD wYear,wMonth,wDayOfWeek,wDay,wHour,wMinute,wSecond,wMilliseconds; };
struct POINT { LONG x; LONG y; };
struct RECT { LONG left,top,right,bottom; };
struct MSG { HWND hwnd; UINT message; WPARAM wParam; LPARAM lParam; DWORD time; POINT pt; DWORD lPrivate; };
struct MINMAXINFO { POINT ptReserved; POINT ptMaxSize; POINT ptMaxPosition; POINT ptMinTrackSize; POINT ptMaxTrackSize; };
struct MONITORINFO_NATIVE { DWORD cbSize; RECT rcMonitor; RECT rcWork; DWORD dwFlags; };
struct SCROLLINFO { UINT cbSize; UINT fMask; int nMin; int nMax; UINT nPage; int nPos; int nTrackPos; };
struct GUID { DWORD Data1; WORD Data2; WORD Data3; BYTE Data4[8]; };
typedef LRESULT (CALLBACK *WNDPROC)(HWND,UINT,WPARAM,LPARAM);
struct WNDCLASSEXW { UINT cbSize; UINT style; WNDPROC lpfnWndProc; int cbClsExtra; int cbWndExtra; HINSTANCE hInstance; HICON hIcon; HCURSOR hCursor; HANDLE hbrBackground; LPCWSTR lpszMenuName; LPCWSTR lpszClassName; HICON hIconSm; };
struct NOTIFYICONDATAW { DWORD cbSize; HWND hWnd; UINT uID; UINT uFlags; UINT uCallbackMessage; HICON hIcon; WCHAR szTip[128]; DWORD dwState; DWORD dwStateMask; WCHAR szInfo[256]; union { UINT uTimeout; UINT uVersion; } DUMMYUNIONNAME; WCHAR szInfoTitle[64]; DWORD dwInfoFlags; GUID guidItem; HICON hBalloonIcon; };
struct OPENFILENAMEW { DWORD lStructSize; HWND hwndOwner; HINSTANCE hInstance; LPCWSTR lpstrFilter; LPWSTR lpstrCustomFilter; DWORD nMaxCustFilter; DWORD nFilterIndex; LPWSTR lpstrFile; DWORD nMaxFile; LPWSTR lpstrFileTitle; DWORD nMaxFileTitle; LPCWSTR lpstrInitialDir; LPCWSTR lpstrTitle; DWORD Flags; WORD nFileOffset; WORD nFileExtension; LPCWSTR lpstrDefExt; LPARAM lCustData; PVOID lpfnHook; LPCWSTR lpTemplateName; PVOID pvReserved; DWORD dwReserved; DWORD FlagsEx; };
struct SRWLOCK { PVOID Ptr; };
struct PROCESSENTRY32W { DWORD dwSize; DWORD cntUsage; DWORD th32ProcessID; ULONG_PTR th32DefaultHeapID; DWORD th32ModuleID; DWORD cntThreads; DWORD th32ParentProcessID; LONG pcPriClassBase; DWORD dwFlags; WCHAR szExeFile[MAX_PATH]; };
struct WIN32_FIND_DATAW { DWORD dwFileAttributes; FILETIME ftCreationTime; FILETIME ftLastAccessTime; FILETIME ftLastWriteTime; DWORD nFileSizeHigh; DWORD nFileSizeLow; DWORD dwReserved0; DWORD dwReserved1; WCHAR cFileName[MAX_PATH]; WCHAR cAlternateFileName[14]; };
struct STARTUPINFOW_NATIVE { DWORD cb; LPWSTR lpReserved; LPWSTR lpDesktop; LPWSTR lpTitle; DWORD dwX,dwY,dwXSize,dwYSize,dwXCountChars,dwYCountChars,dwFillAttribute,dwFlags; WORD wShowWindow,cbReserved2; BYTE* lpReserved2; HANDLE hStdInput,hStdOutput,hStdError; };
struct PROCESS_INFORMATION_NATIVE { HANDLE hProcess; HANDLE hThread; DWORD dwProcessId; DWORD dwThreadId; };
struct EXCEPTION_RECORD_NATIVE { DWORD ExceptionCode; DWORD ExceptionFlags; EXCEPTION_RECORD_NATIVE* ExceptionRecord; PVOID ExceptionAddress; DWORD NumberParameters; DWORD __pad; ULONG_PTR ExceptionInformation[15]; };
struct EXCEPTION_DEBUG_INFO_NATIVE { EXCEPTION_RECORD_NATIVE ExceptionRecord; DWORD dwFirstChance; DWORD __pad; };
struct CREATE_THREAD_DEBUG_INFO_NATIVE { HANDLE hThread; PVOID lpThreadLocalBase; PVOID lpStartAddress; };
struct CREATE_PROCESS_DEBUG_INFO_NATIVE { HANDLE hFile; HANDLE hProcess; HANDLE hThread; PVOID lpBaseOfImage; DWORD dwDebugInfoFileOffset; DWORD nDebugInfoSize; PVOID lpThreadLocalBase; PVOID lpStartAddress; PVOID lpImageName; WORD fUnicode; WORD __pad1; DWORD __pad2; };
struct EXIT_PROCESS_DEBUG_INFO_NATIVE { DWORD dwExitCode; };
struct LOAD_DLL_DEBUG_INFO_NATIVE { HANDLE hFile; PVOID lpBaseOfDll; DWORD dwDebugInfoFileOffset; DWORD nDebugInfoSize; PVOID lpImageName; WORD fUnicode; WORD __pad1; DWORD __pad2; };
union DEBUG_EVENT_UNION_NATIVE { EXCEPTION_DEBUG_INFO_NATIVE Exception; CREATE_THREAD_DEBUG_INFO_NATIVE CreateThread; CREATE_PROCESS_DEBUG_INFO_NATIVE CreateProcessInfo; EXIT_PROCESS_DEBUG_INFO_NATIVE ExitProcess; LOAD_DLL_DEBUG_INFO_NATIVE LoadDll; BYTE raw[160]; };
struct DEBUG_EVENT_NATIVE { DWORD dwDebugEventCode; DWORD dwProcessId; DWORD dwThreadId; DWORD __pad; DEBUG_EVENT_UNION_NATIVE u; };
static_assert(sizeof(EXCEPTION_RECORD_NATIVE)==152,"EXCEPTION_RECORD layout");
static_assert(sizeof(DEBUG_EVENT_NATIVE)==176,"DEBUG_EVENT layout");

// Minimal DbgHelp callback layout needed for IsProcessSnapshotCallback (callback type 16).
struct MINIDUMP_CALLBACK_INPUT_NATIVE { DWORD ProcessId; DWORD __pad0; HANDLE ProcessHandle; ULONG CallbackType; DWORD __pad1; };
union MINIDUMP_CALLBACK_OUTPUT_NATIVE { HRESULT Status; BYTE raw[64]; };
typedef BOOL (CALLBACK *MINIDUMP_CALLBACK_ROUTINE_NATIVE)(PVOID,const MINIDUMP_CALLBACK_INPUT_NATIVE*,MINIDUMP_CALLBACK_OUTPUT_NATIVE*);
struct MINIDUMP_CALLBACK_INFORMATION_NATIVE { MINIDUMP_CALLBACK_ROUTINE_NATIVE CallbackRoutine; PVOID CallbackParam; };

struct IShellLinkW;
struct IPersistFile;
struct IShellLinkWVtbl {
 HRESULT (WINAPI *QueryInterface)(IShellLinkW*,const GUID*,void**); ULONG (WINAPI *AddRef)(IShellLinkW*); ULONG (WINAPI *Release)(IShellLinkW*);
 HRESULT (WINAPI *GetPath)(IShellLinkW*,LPWSTR,int,void*,DWORD); HRESULT (WINAPI *GetIDList)(IShellLinkW*,void**); HRESULT (WINAPI *SetIDList)(IShellLinkW*,const void*);
 HRESULT (WINAPI *GetDescription)(IShellLinkW*,LPWSTR,int); HRESULT (WINAPI *SetDescription)(IShellLinkW*,LPCWSTR);
 HRESULT (WINAPI *GetWorkingDirectory)(IShellLinkW*,LPWSTR,int); HRESULT (WINAPI *SetWorkingDirectory)(IShellLinkW*,LPCWSTR);
 HRESULT (WINAPI *GetArguments)(IShellLinkW*,LPWSTR,int); HRESULT (WINAPI *SetArguments)(IShellLinkW*,LPCWSTR);
 HRESULT (WINAPI *GetHotkey)(IShellLinkW*,WORD*); HRESULT (WINAPI *SetHotkey)(IShellLinkW*,WORD);
 HRESULT (WINAPI *GetShowCmd)(IShellLinkW*,int*); HRESULT (WINAPI *SetShowCmd)(IShellLinkW*,int);
 HRESULT (WINAPI *GetIconLocation)(IShellLinkW*,LPWSTR,int,int*); HRESULT (WINAPI *SetIconLocation)(IShellLinkW*,LPCWSTR,int);
 HRESULT (WINAPI *SetRelativePath)(IShellLinkW*,LPCWSTR,DWORD); HRESULT (WINAPI *Resolve)(IShellLinkW*,HWND,DWORD); HRESULT (WINAPI *SetPath)(IShellLinkW*,LPCWSTR);
};
struct IShellLinkW { IShellLinkWVtbl* lpVtbl; };
struct IPersistFileVtbl { HRESULT (WINAPI *QueryInterface)(IPersistFile*,const GUID*,void**); ULONG (WINAPI *AddRef)(IPersistFile*); ULONG (WINAPI *Release)(IPersistFile*); HRESULT (WINAPI *GetClassID)(IPersistFile*,GUID*); HRESULT (WINAPI *IsDirty)(IPersistFile*); HRESULT (WINAPI *Load)(IPersistFile*,LPCWSTR,DWORD); HRESULT (WINAPI *Save)(IPersistFile*,LPCWSTR,BOOL); HRESULT (WINAPI *SaveCompleted)(IPersistFile*,LPCWSTR); HRESULT (WINAPI *GetCurFile)(IPersistFile*,LPWSTR*); };
struct IPersistFile { IPersistFileVtbl* lpVtbl; };
static const GUID CLSID_ShellLink={0x00021401,0x0000,0x0000,{0xC0,0x00,0x00,0x00,0x00,0x00,0x00,0x46}};
static const GUID IID_IShellLinkW={0x000214F9,0x0000,0x0000,{0xC0,0x00,0x00,0x00,0x00,0x00,0x00,0x46}};
static const GUID IID_IPersistFile={0x0000010b,0x0000,0x0000,{0xC0,0x00,0x00,0x00,0x00,0x00,0x00,0x46}};

extern "C" {
__declspec(dllimport) DWORD WINAPI GetModuleFileNameW(HMODULE,LPWSTR,DWORD);
__declspec(dllimport) HMODULE WINAPI GetModuleHandleW(LPCWSTR);
__declspec(dllimport) HMODULE WINAPI LoadLibraryW(LPCWSTR);
__declspec(dllimport) BOOL WINAPI FreeLibrary(HMODULE);
__declspec(dllimport) PVOID WINAPI GetProcAddress(HMODULE,LPCSTR);
__declspec(dllimport) LPWSTR WINAPI GetCommandLineW();
__declspec(dllimport) ULONGLONG WINAPI GetTickCount64();
__declspec(dllimport) DWORD WINAPI GetEnvironmentVariableW(LPCWSTR,LPWSTR,DWORD);
__declspec(dllimport) DWORD WINAPI GetTempPathW(DWORD,LPWSTR);
__declspec(dllimport) DWORD WINAPI GetCurrentProcessId();
__declspec(dllimport) BOOL WINAPI CreateDirectoryW(LPCWSTR,PVOID);
__declspec(dllimport) DWORD WINAPI GetFileAttributesW(LPCWSTR);
__declspec(dllimport) BOOL WINAPI CopyFileW(LPCWSTR,LPCWSTR,BOOL);
__declspec(dllimport) BOOL WINAPI MoveFileExW(LPCWSTR,LPCWSTR,DWORD);
__declspec(dllimport) BOOL WINAPI DeleteFileW(LPCWSTR);
__declspec(dllimport) BOOL WINAPI RemoveDirectoryW(LPCWSTR);
__declspec(dllimport) HANDLE WINAPI CreateMutexW(PVOID,BOOL,LPCWSTR);
__declspec(dllimport) DWORD WINAPI GetLastError();
__declspec(dllimport) BOOL WINAPI CloseHandle(HANDLE);
__declspec(dllimport) VOID WINAPI ExitProcess(UINT);
__declspec(dllimport) BOOL WINAPI TerminateProcess(HANDLE,UINT);
__declspec(dllimport) PVOID WINAPI VirtualAlloc(PVOID,SIZE_T,DWORD,DWORD);
__declspec(dllimport) BOOL WINAPI VirtualFree(PVOID,SIZE_T,DWORD);
__declspec(dllimport) HANDLE WINAPI CreateThread(PVOID,SIZE_T,LPTHREAD_START_ROUTINE,PVOID,DWORD,DWORD*);
__declspec(dllimport) DWORD WINAPI WaitForSingleObject(HANDLE,DWORD);
__declspec(dllimport) BOOL WINAPI DebugActiveProcess(DWORD);
__declspec(dllimport) BOOL WINAPI DebugActiveProcessStop(DWORD);
__declspec(dllimport) BOOL WINAPI DebugSetProcessKillOnExit(BOOL);
__declspec(dllimport) BOOL WINAPI WaitForDebugEvent(DEBUG_EVENT_NATIVE*,DWORD);
__declspec(dllimport) BOOL WINAPI ContinueDebugEvent(DWORD,DWORD,DWORD);
__declspec(dllimport) VOID WINAPI Sleep(DWORD);
__declspec(dllimport) HANDLE WINAPI CreateToolhelp32Snapshot(DWORD,DWORD);
__declspec(dllimport) BOOL WINAPI Process32FirstW(HANDLE,PROCESSENTRY32W*);
__declspec(dllimport) BOOL WINAPI Process32NextW(HANDLE,PROCESSENTRY32W*);
__declspec(dllimport) HANDLE WINAPI CreateFileW(LPCWSTR,DWORD,DWORD,PVOID,DWORD,DWORD,HANDLE);
__declspec(dllimport) BOOL WINAPI ReadFile(HANDLE,PVOID,DWORD,DWORD*,PVOID);
__declspec(dllimport) BOOL WINAPI WriteFile(HANDLE,const VOID*,DWORD,DWORD*,PVOID);
__declspec(dllimport) BOOL WINAPI CreateProcessW(LPCWSTR,LPWSTR,PVOID,PVOID,BOOL,DWORD,PVOID,LPCWSTR,STARTUPINFOW_NATIVE*,PROCESS_INFORMATION_NATIVE*);
__declspec(dllimport) BOOL WINAPI GetExitCodeProcess(HANDLE,DWORD*);
__declspec(dllimport) BOOL WINAPI FlushFileBuffers(HANDLE);
__declspec(dllimport) DWORD WINAPI SetFilePointer(HANDLE,LONG,LONG*,DWORD);
__declspec(dllimport) VOID WINAPI GetLocalTime(SYSTEMTIME*);
__declspec(dllimport) HANDLE WINAPI FindFirstFileW(LPCWSTR,WIN32_FIND_DATAW*);
__declspec(dllimport) BOOL WINAPI FindNextFileW(HANDLE,WIN32_FIND_DATAW*);
__declspec(dllimport) BOOL WINAPI FindClose(HANDLE);
__declspec(dllimport) BOOL WINAPI GetProcessHandleCount(HANDLE,DWORD*);
__declspec(dllimport) int WINAPI lstrlenW(LPCWSTR);
__declspec(dllimport) LPWSTR WINAPI lstrcpyW(LPWSTR,LPCWSTR);
__declspec(dllimport) LPWSTR WINAPI lstrcatW(LPWSTR,LPCWSTR);
__declspec(dllimport) int WINAPI lstrcmpiW(LPCWSTR,LPCWSTR);
__declspec(dllimport) int WINAPI WideCharToMultiByte(UINT,DWORD,LPCWSTR,int,LPSTR,int,LPCSTR,BOOL*);
__declspec(dllimport) HANDLE WINAPI OpenProcess(DWORD,BOOL,DWORD);
__declspec(dllimport) BOOL WINAPI QueryFullProcessImageNameW(HANDLE,DWORD,LPWSTR,DWORD*);
__declspec(dllimport) DWORD WINAPI GetPrivateProfileStringW(LPCWSTR,LPCWSTR,LPCWSTR,LPWSTR,DWORD,LPCWSTR);
__declspec(dllimport) UINT WINAPI GetPrivateProfileIntW(LPCWSTR,LPCWSTR,int,LPCWSTR);
__declspec(dllimport) BOOL WINAPI WritePrivateProfileStringW(LPCWSTR,LPCWSTR,LPCWSTR,LPCWSTR);
__declspec(dllimport) VOID WINAPI AcquireSRWLockShared(SRWLOCK*);
__declspec(dllimport) VOID WINAPI ReleaseSRWLockShared(SRWLOCK*);
__declspec(dllimport) VOID WINAPI AcquireSRWLockExclusive(SRWLOCK*);
__declspec(dllimport) VOID WINAPI ReleaseSRWLockExclusive(SRWLOCK*);
__declspec(dllimport) int WINAPI MessageBoxW(HWND,LPCWSTR,LPCWSTR,UINT);
__declspec(dllimport) WORD WINAPI RegisterClassExW(const WNDCLASSEXW*);
__declspec(dllimport) UINT WINAPI RegisterWindowMessageW(LPCWSTR);
__declspec(dllimport) HWND WINAPI CreateWindowExW(DWORD,LPCWSTR,LPCWSTR,DWORD,int,int,int,int,HWND,HMENU,HINSTANCE,PVOID);
__declspec(dllimport) LRESULT WINAPI DefWindowProcW(HWND,UINT,WPARAM,LPARAM);
__declspec(dllimport) BOOL WINAPI GetMessageW(MSG*,HWND,UINT,UINT);
__declspec(dllimport) BOOL WINAPI TranslateMessage(const MSG*);
__declspec(dllimport) LRESULT WINAPI DispatchMessageW(const MSG*);
__declspec(dllimport) BOOL WINAPI PostMessageW(HWND,UINT,WPARAM,LPARAM);
__declspec(dllimport) VOID WINAPI PostQuitMessage(int);
__declspec(dllimport) HMENU WINAPI CreatePopupMenu();
__declspec(dllimport) BOOL WINAPI AppendMenuW(HMENU,UINT,ULONG_PTR,LPCWSTR);
__declspec(dllimport) UINT WINAPI TrackPopupMenu(HMENU,UINT,int,int,int,HWND,const VOID*);
__declspec(dllimport) BOOL WINAPI DestroyMenu(HMENU);
__declspec(dllimport) BOOL WINAPI SetForegroundWindow(HWND);
__declspec(dllimport) BOOL WINAPI GetCursorPos(POINT*);
__declspec(dllimport) HCURSOR WINAPI LoadCursorW(HINSTANCE,LPCWSTR);
__declspec(dllimport) HCURSOR WINAPI SetCursor(HCURSOR);
__declspec(dllimport) HWND WINAPI SetCapture(HWND);
__declspec(dllimport) BOOL WINAPI ReleaseCapture();
__declspec(dllimport) LONG_PTR WINAPI SetWindowLongPtrW(HWND,int,LONG_PTR);
__declspec(dllimport) LRESULT WINAPI CallWindowProcW(WNDPROC,HWND,UINT,WPARAM,LPARAM);
__declspec(dllimport) int WINAPI wsprintfW(LPWSTR,LPCWSTR,...);
__declspec(dllimport) DWORD WINAPI GetGuiResources(HANDLE,DWORD);
__declspec(dllimport) BOOL WINAPI DestroyWindow(HWND);
__declspec(dllimport) HWND WINAPI FindWindowW(LPCWSTR,LPCWSTR);
__declspec(dllimport) DWORD WINAPI GetWindowThreadProcessId(HWND,DWORD*);
__declspec(dllimport) BOOL WINAPI ShowWindow(HWND,int);
__declspec(dllimport) BOOL WINAPI IsWindowVisible(HWND);
__declspec(dllimport) BOOL WINAPI UpdateWindow(HWND);
__declspec(dllimport) BOOL WINAPI SetWindowTextW(HWND,LPCWSTR);
__declspec(dllimport) LRESULT WINAPI SendMessageW(HWND,UINT,WPARAM,LPARAM);
__declspec(dllimport) BOOL WINAPI EnableWindow(HWND,BOOL);
__declspec(dllimport) BOOL WINAPI GetClientRect(HWND,RECT*);
__declspec(dllimport) BOOL WINAPI GetWindowRect(HWND,RECT*);
__declspec(dllimport) BOOL WINAPI SystemParametersInfoW(UINT,UINT,PVOID,UINT);
__declspec(dllimport) HMONITOR WINAPI MonitorFromRect(const RECT*,DWORD);
__declspec(dllimport) BOOL WINAPI GetMonitorInfoW(HMONITOR,MONITORINFO_NATIVE*);
__declspec(dllimport) UINT WINAPI GetDoubleClickTime();
__declspec(dllimport) int WINAPI SetScrollInfo(HWND,int,SCROLLINFO*,BOOL);
__declspec(dllimport) BOOL WINAPI MoveWindow(HWND,int,int,int,int,BOOL);
__declspec(dllimport) HWND WINAPI SetFocus(HWND);
__declspec(dllimport) ULONG_PTR WINAPI SetTimer(HWND,ULONG_PTR,UINT,PVOID);
__declspec(dllimport) BOOL WINAPI KillTimer(HWND,ULONG_PTR);
__declspec(dllimport) HICON WINAPI CreateIcon(HINSTANCE,int,int,BYTE,BYTE,const BYTE*,const BYTE*);
__declspec(dllimport) BOOL WINAPI DestroyIcon(HICON);
__declspec(dllimport) BOOL WINAPI Shell_NotifyIconW(DWORD,NOTIFYICONDATAW*);
__declspec(dllimport) HINSTANCE WINAPI ShellExecuteW(HWND,LPCWSTR,LPCWSTR,LPCWSTR,LPCWSTR,int);
__declspec(dllimport) HRESULT WINAPI SHGetFolderPathW(HWND,int,HANDLE,DWORD,LPWSTR);
__declspec(dllimport) LONG WINAPI RegOpenKeyExW(HKEY,LPCWSTR,DWORD,DWORD,HKEY*);
__declspec(dllimport) LONG WINAPI RegCreateKeyExW(HKEY,LPCWSTR,DWORD,LPWSTR,DWORD,DWORD,PVOID,HKEY*,DWORD*);
__declspec(dllimport) LONG WINAPI RegSetValueExW(HKEY,LPCWSTR,DWORD,DWORD,const BYTE*,DWORD);
__declspec(dllimport) LONG WINAPI RegDeleteValueW(HKEY,LPCWSTR);
__declspec(dllimport) LONG WINAPI RegDeleteTreeW(HKEY,LPCWSTR);
__declspec(dllimport) LONG WINAPI RegQueryValueExW(HKEY,LPCWSTR,DWORD*,DWORD*,BYTE*,DWORD*);
__declspec(dllimport) LONG WINAPI RegCloseKey(HKEY);
__declspec(dllimport) BOOL WINAPI GetOpenFileNameW(OPENFILENAMEW*);
__declspec(dllimport) HFONT WINAPI CreateFontW(int,int,int,int,int,DWORD,DWORD,DWORD,DWORD,DWORD,DWORD,DWORD,DWORD,LPCWSTR);
__declspec(dllimport) BOOL WINAPI DeleteObject(HGDIOBJ);
__declspec(dllimport) HRESULT WINAPI CoInitializeEx(PVOID,DWORD);
__declspec(dllimport) VOID WINAPI CoUninitialize();
__declspec(dllimport) HRESULT WINAPI CoCreateInstance(const GUID*,PVOID,DWORD,const GUID*,PVOID*);
}

extern "C" void* memcpy(void* dst,const void* src,SIZE_T n){BYTE*d=(BYTE*)dst;const BYTE*s=(const BYTE*)src;while(n--)*d++=*s++;return dst;}
extern "C" void* memset(void* dst,int c,SIZE_T n){BYTE*d=(BYTE*)dst;while(n--)*d++=(BYTE)c;return dst;}

struct TargetConfig { WCHAR exeName[MAX_PATH]; WCHAR fullPath[MAX_PATH*2]; BOOL enabled; };
struct RunningInfo { BOOL active; DWORD pid; WCHAR exeName[MAX_PATH]; DWORD threadCount; };

static HWND g_hwnd=0, g_list=0, g_status=0, g_details=0, g_startupBox=0, g_pauseBox=0, g_minimizeTrayBox=0, g_keepTrayTaskbarBox=0;
static HWND g_closeXTrayBox=0,g_startMinimizedBox=0,g_startPausedBox=0,g_notificationsBox=0;
static HWND g_header=0,g_subtitle=0,g_group=0,g_addBtn=0,g_toggleBtn=0,g_removeBtn=0,g_repairBtn=0,g_openDumpsBtn=0,g_openDataBtn=0,g_testDumpBtn=0,g_safeSelfTestBtn=0,g_displayBtn=0,g_exitBtn=0,g_footer=0;
static HWND g_exportReportBtn=0,g_resetLayoutBtn=0;
static WNDPROC g_oldDetailsProc=0; static BOOL g_detailsDragging=FALSE; static LONG g_detailsLastY=0;
static HANDLE g_worker=0; static volatile LONG g_exitFlag=0; static volatile LONG g_paused=0; static volatile LONG g_reconfigure=0; static volatile LONG g_activeCount=0;
static WCHAR g_baseDir[MAX_PATH*2],g_dumpRoot[MAX_PATH*2],g_logPath[MAX_PATH*2],g_configPath[MAX_PATH*2],g_exePath[MAX_PATH*2],g_installDir[MAX_PATH*2],g_installExe[MAX_PATH*2],g_lastCapturedFile[MAX_PATH*2];
static ULONGLONG g_lastDumpTime=0; static TargetConfig g_targets[MAX_TARGETS]; static int g_targetCount=0; static RunningInfo g_running[MAX_RUNNING]; static SRWLOCK g_lock={0}; static SRWLOCK g_logLock={0}; static NOTIFYICONDATAW g_nid;
static HICON g_appIcon=0; static HFONT g_font=0,g_titleFont=0; static int g_currentState=STATE_WAITING; static DWORD g_currentActive=0; static UINT g_taskbarCreatedMsg=0;
static BOOL g_trayOnly=FALSE,g_trayVisible=FALSE,g_hiddenToTray=FALSE,g_minimizeToTray=TRUE,g_keepTrayTaskbar=FALSE;
static BOOL g_closeXToTray=FALSE,g_startMinimized=FALSE,g_startPaused=FALSE,g_notificationsEnabled=TRUE,g_windowMinimized=FALSE;
static ULONGLONG g_lastTrayClickTick=0;
static BOOL g_selfTestLaunchIntercept=FALSE; static volatile LONG g_selfTestLaunchInterceptCount=0;
static volatile LONG g_safeSelfTestRunning=0; static HANDLE g_safeSelfTestThread=0;
static SRWLOCK g_safeSelfTestProgressLock={0}; static WCHAR g_safeSelfTestProgressText[512];
static volatile LONG g_safeSelfTestProgressIndex=0,g_safeSelfTestProgressTotal=39;
static volatile LONG g_taskbarRecoveryCount=0;
static WCHAR g_selfTestProgressPath[MAX_PATH*2];
static int g_mainScale=1000,g_mainOffsetX=0,g_mainOffsetY=0,g_mainFontScale=1000;
static int g_detailsHeight=122;
static SRWLOCK g_dumpWriteLock={0};
static volatile DWORD g_obsPreDumpPid=0,g_obsCrashDumpPid=0,g_obsDebugPid=0;
static volatile LONG g_obsDebugStop=0;
static HANDLE g_obsDebugThread=0;
struct ObsSnapshotJob { HANDLE snapshot; DWORD pid; DWORD handles; DWORD exceptionCode; DWORD firstChance; WCHAR exe[MAX_PATH]; WCHAR kind[32]; };
static ObsSnapshotJob g_obsSnapshotJob; static volatile LONG g_obsSnapshotJobRunning=0;
static volatile LONG g_testDumpRunning=0; static DWORD g_testDumpPid=0; static WCHAR g_testDumpExe[MAX_PATH];
static volatile LONG g_lastShareCompressed=0; static volatile LONG g_lastShareParts=0;
// Setup window controls are file-scope so the installer can resize responsively.
static HWND g_setupTitle=0,g_setupSubtitle=0,g_setupIcon=0,g_setupGroup=0,g_setupLocationLabel=0,g_setupPath=0;
static HWND g_setupStartMenu=0,g_setupDesktop=0,g_setupStartup=0,g_setupLaunch=0,g_setupNote=0,g_setupStatus=0,g_setupInstall=0,g_setupCancel=0;

static void ZeroMem(void*p,SIZE_T n){volatile BYTE*b=(volatile BYTE*)p;while(n--)*b++=0;}
static LPCWSTR ResPtr(UINT id){return(LPCWSTR)(ULONG_PTR)id;}
static ULONGLONG FtValue(const FILETIME&f){return((ULONGLONG)f.dwHighDateTime<<32)|f.dwLowDateTime;}
static void CopyWide(WCHAR*d,int cap,LPCWSTR s){if(!d||cap<=0)return;int i=0;if(s)while(s[i]&&i<cap-1){d[i]=s[i];i++;}d[i]=0;}
static LPCWSTR BaseNamePtr(LPCWSTR p){LPCWSTR b=p;if(!p)return L"";for(;*p;p++)if(*p==L'\\'||*p==L'/')b=p+1;return b;}
static BOOL PrefixI(LPCWSTR s,LPCWSTR p){if(!s||!p)return FALSE;while(*p){WCHAR a=*s,b=*p;if(a>=L'A'&&a<=L'Z')a+=32;if(b>=L'A'&&b<=L'Z')b+=32;if(a!=b)return FALSE;s++;p++;}return TRUE;}
static BOOL FileExists(LPCWSTR p){DWORD a=GetFileAttributesW(p);return a!=INVALID_FILE_ATTRIBUTES && !(a&FILE_ATTRIBUTE_DIRECTORY);}
static void EnsureDir(LPCWSTR p){CreateDirectoryW(p,NULLPTR);}
static UINT LowWord(WPARAM w){return (UINT)(w&0xFFFFu);} static UINT HighWord(WPARAM w){return (UINT)((w>>16)&0xFFFFu);}

static void BuildInstallPaths(){WCHAR local[MAX_PATH*2];ZeroMem(local,sizeof(local));if(!GetEnvironmentVariableW(L"LOCALAPPDATA",local,MAX_PATH*2))lstrcpyW(local,L"C:\\Temp");lstrcpyW(g_installDir,local);lstrcatW(g_installDir,L"\\Programs");EnsureDir(g_installDir);lstrcatW(g_installDir,L"\\Crash Monitor");lstrcpyW(g_installExe,g_installDir);lstrcatW(g_installExe,L"\\Crash Monitor.exe");}
static void BuildPaths(){WCHAR local[MAX_PATH*2];ZeroMem(local,sizeof(local));if(!GetEnvironmentVariableW(L"LOCALAPPDATA",local,MAX_PATH*2))lstrcpyW(local,L"C:\\Temp");lstrcpyW(g_baseDir,local);lstrcatW(g_baseDir,L"\\Crash Monitor");lstrcpyW(g_dumpRoot,g_baseDir);lstrcatW(g_dumpRoot,L"\\Dumps");lstrcpyW(g_logPath,g_baseDir);lstrcatW(g_logPath,L"\\monitor.log");lstrcpyW(g_configPath,g_baseDir);lstrcatW(g_configPath,L"\\targets.ini");EnsureDir(g_baseDir);EnsureDir(g_dumpRoot);GetModuleFileNameW(0,g_exePath,MAX_PATH*2);BuildInstallPaths();if(!FileExists(g_configPath)){WCHAR old[MAX_PATH*2];lstrcpyW(old,local);lstrcatW(old,L"\\Crash Monitor AV Safe\\targets.ini");if(FileExists(old))CopyFileW(old,g_configPath,FALSE);}}
static void AppendUtf8(HANDLE h,LPCWSTR s){CHAR b[4096];int n=WideCharToMultiByte(65001,0,s,-1,b,(int)sizeof(b),0,0);if(n>1){DWORD w=0;WriteFile(h,b,(DWORD)(n-1),&w,NULLPTR);}}
static ULONGLONG LogFileSize(LPCWSTR path){WIN32_FIND_DATAW f;ZeroMem(&f,sizeof(f));HANDLE h=FindFirstFileW(path,&f);if(h==INVALID_HANDLE_VALUE)return 0;FindClose(h);return ((ULONGLONG)f.nFileSizeHigh<<32)|f.nFileSizeLow;}
static void RotatedLogPath(int index,WCHAR*out,int cap){if(!out||cap<=0)return;if(index<=0){CopyWide(out,cap,g_logPath);return;}wsprintfW(out,L"%s\\monitor.%d.log",g_baseDir,index);}
static void RotateLogsIfNeeded(){if(LogFileSize(g_logPath)<LOG_ROTATE_BYTES)return;WCHAR src[MAX_PATH*2],dst[MAX_PATH*2];RotatedLogPath(LOG_ROTATE_COUNT,dst,MAX_PATH*2);DeleteFileW(dst);for(int i=LOG_ROTATE_COUNT-1;i>=1;i--){RotatedLogPath(i,src,MAX_PATH*2);RotatedLogPath(i+1,dst,MAX_PATH*2);if(FileExists(src))MoveFileExW(src,dst,MOVEFILE_REPLACE_EXISTING);}RotatedLogPath(1,dst,MAX_PATH*2);if(FileExists(g_logPath))MoveFileExW(g_logPath,dst,MOVEFILE_REPLACE_EXISTING);}
static void AppendLog(LPCWSTR t){AcquireSRWLockExclusive(&g_logLock);RotateLogsIfNeeded();HANDLE h=CreateFileW(g_logPath,GENERIC_WRITE,FILE_SHARE_READ|FILE_SHARE_WRITE,NULLPTR,OPEN_ALWAYS,FILE_ATTRIBUTE_NORMAL,0);if(h==INVALID_HANDLE_VALUE){ReleaseSRWLockExclusive(&g_logLock);return;}SetFilePointer(h,0,0,FILE_END);SYSTEMTIME st;GetLocalTime(&st);WCHAR head[96];wsprintfW(head,L"%04u-%02u-%02u %02u:%02u:%02u  ",st.wYear,st.wMonth,st.wDay,st.wHour,st.wMinute,st.wSecond);AppendUtf8(h,head);AppendUtf8(h,t);AppendUtf8(h,L"\r\n");CloseHandle(h);ReleaseSRWLockExclusive(&g_logLock);}
static BOOL WriteProfileChecked(LPCWSTR section,LPCWSTR key,LPCWSTR value){BOOL ok=WritePrivateProfileStringW(section,key,value,g_configPath);if(!ok){WCHAR line[384];wsprintfW(line,L"SETTINGS write FAILED section=%s key=%s err=%u",section,key,GetLastError());AppendLog(line);}return ok;}

static HICON BuildAppIcon(HINSTANCE inst){static BYTE andBits[128];static BYTE xorBits[32*32*4];ZeroMem(andBits,sizeof(andBits));ZeroMem(xorBits,sizeof(xorBits));for(int y=0;y<32;y++){for(int x=0;x<32;x++){int dx=2*x-31,dy=2*y-31;BOOL inside=(dx*dx+dy*dy)<=31*31;int row=31-y;int off=(row*32+x)*4;if(!inside){int bi=y*4+x/8;andBits[bi]|=(BYTE)(0x80>>(x&7));xorBits[off+3]=0;continue;}BYTE r=(BYTE)(25+y/3),g=(BYTE)(115+y),b=(BYTE)(225-y/3);xorBits[off+0]=b;xorBits[off+1]=g;xorBits[off+2]=r;xorBits[off+3]=255;}}
// white monitor outline and stand
for(int y=8;y<=22;y++)for(int x=6;x<=25;x++)if(x<=7||x>=24||y<=9||y>=21){int off=((31-y)*32+x)*4;xorBits[off]=255;xorBits[off+1]=255;xorBits[off+2]=255;xorBits[off+3]=255;}
for(int y=23;y<=24;y++)for(int x=14;x<=17;x++){int off=((31-y)*32+x)*4;xorBits[off]=255;xorBits[off+1]=255;xorBits[off+2]=255;xorBits[off+3]=255;}
for(int x=11;x<=20;x++){int y=25;int off=((31-y)*32+x)*4;xorBits[off]=255;xorBits[off+1]=255;xorBits[off+2]=255;xorBits[off+3]=255;}
// pulse line
int pts[12][2]={{8,16},{11,16},{13,13},{15,19},{17,11},{19,16},{23,16},{24,16},{0,0},{0,0},{0,0},{0,0}};for(int p=0;p<7;p++){int x0=pts[p][0],y0=pts[p][1],x1=pts[p+1][0],y1=pts[p+1][1];int ddx=x1-x0;if(ddx<0)ddx=-ddx;int sx=x0<x1?1:-1;int ddy=y1-y0;if(ddy<0)ddy=-ddy;int sy=y0<y1?1:-1;int err=ddx-ddy;for(;;){for(int oy=0;oy<2;oy++){int yy=y0+oy;if(yy>=0&&yy<32){int off=((31-yy)*32+x0)*4;xorBits[off]=255;xorBits[off+1]=255;xorBits[off+2]=255;xorBits[off+3]=255;}}if(x0==x1&&y0==y1)break;int e2=err*2;if(e2>-ddy){err-=ddy;x0+=sx;}if(e2<ddx){err+=ddx;y0+=sy;}}}
return CreateIcon(inst,32,32,1,32,andBits,xorBits);}

static BOOL QueryStartupNamedValue(LPCWSTR valueName,WCHAR*out,int cap){if(out&&cap>0)out[0]=0;HKEY h=0;if(RegOpenKeyExW(HKEY_CURRENT_USER,L"Software\\Microsoft\\Windows\\CurrentVersion\\Run",0,KEY_QUERY_VALUE,&h)!=ERROR_SUCCESS)return FALSE;DWORD ty=0,sz=(DWORD)(cap*sizeof(WCHAR));LONG r=RegQueryValueExW(h,valueName,0,&ty,(BYTE*)out,&sz);RegCloseKey(h);if(r!=ERROR_SUCCESS||ty!=REG_SZ)return FALSE;if(out&&cap>0)out[cap-1]=0;return TRUE;}
static BOOL IsStartupEnabled(){WCHAR q[MAX_PATH*2+64];if(QueryStartupNamedValue(L"Crash Monitor",q,MAX_PATH*2+64))return TRUE;return QueryStartupNamedValue(L"Crash Monitor AV Safe",q,MAX_PATH*2+64);}
static BOOL SetStartupNamedValue(LPCWSTR valueName,LPCWSTR path,BOOL on){HKEY h=0;DWORD disp=0;if(RegCreateKeyExW(HKEY_CURRENT_USER,L"Software\\Microsoft\\Windows\\CurrentVersion\\Run",0,0,0,KEY_WRITE,NULLPTR,&h,&disp)!=ERROR_SUCCESS)return FALSE;LONG r;if(on){WCHAR q[MAX_PATH*2+32];lstrcpyW(q,L"\"");lstrcatW(q,path);lstrcatW(q,L"\"");r=RegSetValueExW(h,valueName,0,REG_SZ,(BYTE*)q,(DWORD)((lstrlenW(q)+1)*sizeof(WCHAR)));}else{r=RegDeleteValueW(h,valueName);if(r==ERROR_FILE_NOT_FOUND)r=ERROR_SUCCESS;}RegCloseKey(h);return r==ERROR_SUCCESS;}
static BOOL SetStartupPath(LPCWSTR path,BOOL on){BOOL ok=SetStartupNamedValue(L"Crash Monitor",path,on);HKEY h=0;if(RegOpenKeyExW(HKEY_CURRENT_USER,L"Software\\Microsoft\\Windows\\CurrentVersion\\Run",0,KEY_SET_VALUE,&h)==ERROR_SUCCESS){RegDeleteValueW(h,L"Crash Monitor AV Safe");RegCloseKey(h);}return ok;}
static BOOL SetStartup(BOOL on){return SetStartupPath(g_installExe,on);}

static BOOL GetTrayOnlySetting(){return GetPrivateProfileIntW(L"Settings",L"TrayOnly",0,g_configPath)?TRUE:FALSE;}
static BOOL SaveTrayOnlySetting(BOOL on){if(!WriteProfileChecked(L"Settings",L"TrayOnly",on?L"1":L"0"))return FALSE;BOOL got=GetTrayOnlySetting();if(got!=on){AppendLog(L"SETTINGS verify FAILED key=TrayOnly");return FALSE;}return TRUE;}
static BOOL GetMinimizeToTraySetting(){return GetPrivateProfileIntW(L"Settings",L"MinimizeToTray",1,g_configPath)?TRUE:FALSE;}
static BOOL SaveMinimizeToTraySetting(BOOL on){if(!WriteProfileChecked(L"Settings",L"MinimizeToTray",on?L"1":L"0"))return FALSE;BOOL got=GetMinimizeToTraySetting();if(got!=on){AppendLog(L"SETTINGS verify FAILED key=MinimizeToTray");return FALSE;}return TRUE;}
static BOOL GetKeepTrayTaskbarSetting(){return GetPrivateProfileIntW(L"Settings",L"KeepTrayWithTaskbar",0,g_configPath)?TRUE:FALSE;}
static BOOL SaveKeepTrayTaskbarSetting(BOOL on){if(!WriteProfileChecked(L"Settings",L"KeepTrayWithTaskbar",on?L"1":L"0"))return FALSE;BOOL got=GetKeepTrayTaskbarSetting();if(got!=on){AppendLog(L"SETTINGS verify FAILED key=KeepTrayWithTaskbar");return FALSE;}return TRUE;}
static int GetDetailsHeightSetting(){int v=(int)GetPrivateProfileIntW(L"Settings",L"DetailsHeight",122,g_configPath);if(v<70)v=70;if(v>270)v=270;return v;}
static BOOL SaveDetailsHeightSetting(){WCHAR n[32];wsprintfW(n,L"%d",g_detailsHeight);if(!WriteProfileChecked(L"Settings",L"DetailsHeight",n))return FALSE;BOOL ok=GetDetailsHeightSetting()==g_detailsHeight;if(!ok)AppendLog(L"SETTINGS verify FAILED key=DetailsHeight");return ok;}
static BOOL GetCloseXToTraySetting(){return GetPrivateProfileIntW(L"Settings",L"CloseXToTray",0,g_configPath)?TRUE:FALSE;}
static BOOL SaveCloseXToTraySetting(BOOL on){if(!WriteProfileChecked(L"Settings",L"CloseXToTray",on?L"1":L"0"))return FALSE;BOOL got=GetCloseXToTraySetting();if(got!=on){AppendLog(L"SETTINGS verify FAILED key=CloseXToTray");return FALSE;}return TRUE;}
static BOOL GetStartMinimizedSetting(){return GetPrivateProfileIntW(L"Settings",L"StartMinimized",0,g_configPath)?TRUE:FALSE;}
static BOOL SaveStartMinimizedSetting(BOOL on){if(!WriteProfileChecked(L"Settings",L"StartMinimized",on?L"1":L"0"))return FALSE;BOOL got=GetStartMinimizedSetting();if(got!=on){AppendLog(L"SETTINGS verify FAILED key=StartMinimized");return FALSE;}return TRUE;}
static BOOL GetStartPausedSetting(){return GetPrivateProfileIntW(L"Settings",L"StartPaused",0,g_configPath)?TRUE:FALSE;}
static BOOL SaveStartPausedSetting(BOOL on){if(!WriteProfileChecked(L"Settings",L"StartPaused",on?L"1":L"0"))return FALSE;BOOL got=GetStartPausedSetting();if(got!=on){AppendLog(L"SETTINGS verify FAILED key=StartPaused");return FALSE;}return TRUE;}
static BOOL GetNotificationsSetting(){return GetPrivateProfileIntW(L"Settings",L"Notifications",1,g_configPath)?TRUE:FALSE;}
static BOOL SaveNotificationsSetting(BOOL on){if(!WriteProfileChecked(L"Settings",L"Notifications",on?L"1":L"0"))return FALSE;BOOL got=GetNotificationsSetting();if(got!=on){AppendLog(L"SETTINGS verify FAILED key=Notifications");return FALSE;}return TRUE;}
static int ParseSignedInt(LPCWSTR s,int fallback){if(!s||!*s)return fallback;BOOL neg=FALSE;if(*s==L'-'){neg=TRUE;s++;}int v=0;BOOL any=FALSE;while(*s>=L'0'&&*s<=L'9'){any=TRUE;v=v*10+(*s-L'0');s++;}return any?(neg?-v:v):fallback;}
static BOOL ReadSignedSetting(LPCWSTR key,int*out){WCHAR b[64];b[0]=0;GetPrivateProfileStringW(L"Settings",key,L"",b,64,g_configPath);if(!b[0])return FALSE;if(out)*out=ParseSignedInt(b,0);return TRUE;}
static BOOL SaveSignedSetting(LPCWSTR key,int v){WCHAR b[64];wsprintfW(b,L"%d",v);if(!WriteProfileChecked(L"Settings",key,b))return FALSE;int got=0;return ReadSignedSetting(key,&got)&&got==v;}
static BOOL GetSavedWindowRectSetting(RECT*out){if(!out)return FALSE;int x=0,y=0,w=0,h=0;if(!ReadSignedSetting(L"WindowX",&x)||!ReadSignedSetting(L"WindowY",&y)||!ReadSignedSetting(L"WindowW",&w)||!ReadSignedSetting(L"WindowH",&h))return FALSE;if(w<680||h<500)return FALSE;out->left=x;out->top=y;out->right=x+w;out->bottom=y+h;return TRUE;}
static BOOL SaveWindowRectSetting(const RECT&r){int w=(int)(r.right-r.left),h=(int)(r.bottom-r.top);if(w<680||h<500)return FALSE;BOOL ok=SaveSignedSetting(L"WindowX",(int)r.left)&&SaveSignedSetting(L"WindowY",(int)r.top)&&SaveSignedSetting(L"WindowW",w)&&SaveSignedSetting(L"WindowH",h);if(!ok)AppendLog(L"SETTINGS verify FAILED key=WindowRect");return ok;}
static void PrimaryDefaultRect(RECT*out){RECT wa;wa.left=0;wa.top=0;wa.right=1180;wa.bottom=900;if(!SystemParametersInfoW(SPI_GETWORKAREA,0,&wa,0)){wa.left=0;wa.top=0;wa.right=1180;wa.bottom=900;}int aw=(int)(wa.right-wa.left),ah=(int)(wa.bottom-wa.top);int w=1180,h=900;if(w>aw)w=aw;if(h>ah)h=ah;if(w<680)w=680;if(h<500)h=500;out->left=wa.left+(aw-w)/2;out->top=wa.top+(ah-h)/2;out->right=out->left+w;out->bottom=out->top+h;}
static void ClampRectToVisibleWorkArea(RECT*r){if(!r)return;HMONITOR mon=MonitorFromRect(r,MONITOR_DEFAULTTONEAREST);MONITORINFO_NATIVE mi;ZeroMem(&mi,sizeof(mi));mi.cbSize=sizeof(mi);RECT wa;if(mon&&GetMonitorInfoW(mon,&mi))wa=mi.rcWork;else{PrimaryDefaultRect(&wa);int ww=(int)(wa.right-wa.left),hh=(int)(wa.bottom-wa.top);wa.left=wa.left;wa.top=wa.top;wa.right=wa.left+ww;wa.bottom=wa.top+hh;}int w=(int)(r->right-r->left),h=(int)(r->bottom-r->top);int aw=(int)(wa.right-wa.left),ah=(int)(wa.bottom-wa.top);if(w>aw)w=aw;if(h>ah)h=ah;if(w<680)w=680;if(h<500)h=500;if(r->left<wa.left)r->left=wa.left;if(r->top<wa.top)r->top=wa.top;if(r->left+w>wa.right)r->left=wa.right-w;if(r->top+h>wa.bottom)r->top=wa.bottom-h;r->right=r->left+w;r->bottom=r->top+h;}
static void SaveCurrentWindowRect(){if(!g_hwnd||g_hiddenToTray||g_windowMinimized)return;RECT r;if(GetWindowRect(g_hwnd,&r))SaveWindowRectSetting(r);}
static void ResetWindowLayout(){WriteProfileChecked(L"Settings",L"WindowX",(LPCWSTR)0);WriteProfileChecked(L"Settings",L"WindowY",(LPCWSTR)0);WriteProfileChecked(L"Settings",L"WindowW",(LPCWSTR)0);WriteProfileChecked(L"Settings",L"WindowH",(LPCWSTR)0);RECT r;PrimaryDefaultRect(&r);if(g_hwnd){MoveWindow(g_hwnd,r.left,r.top,r.right-r.left,r.bottom-r.top,TRUE);ShowWindow(g_hwnd,SW_RESTORE);g_windowMinimized=FALSE;g_hiddenToTray=FALSE;}AppendLog(L"Window layout reset to primary monitor work area");}
static void AddTrayIcon(); static void RemoveTrayIcon(); static void RefreshProgramList(); static void HideMainToTray();
static BOOL ApplyStartupSetting(BOOL on,BOOL showError){BOOL ok=SetStartup(on);if(ok)ok=IsStartupEnabled()==on;if(!ok){AppendLog(L"Startup setting update/verify FAILED");if(g_startupBox)SendMessageW(g_startupBox,BM_SETCHECK,IsStartupEnabled()?BST_CHECKED:BST_UNCHECKED,0);if(showError)MessageBoxW(g_hwnd,L"Windows could not update or verify Crash Monitor's Start with Windows setting.",L"Crash Monitor",MB_OK|MB_ICONERROR);return FALSE;}AppendLog(on?L"Start with Windows enabled":L"Start with Windows disabled");if(g_startupBox)SendMessageW(g_startupBox,BM_SETCHECK,on?BST_CHECKED:BST_UNCHECKED,0);return TRUE;}
static void ApplyPausedState(BOOL on){g_paused=on;g_reconfigure=1;if(g_pauseBox)SendMessageW(g_pauseBox,BM_SETCHECK,on?BST_CHECKED:BST_UNCHECKED,0);RefreshProgramList();}
static BOOL ApplyMinimizeToTraySetting(BOOL on,BOOL showError){BOOL old=g_minimizeToTray;if(!SaveMinimizeToTraySetting(on)){g_minimizeToTray=old;if(g_minimizeTrayBox)SendMessageW(g_minimizeTrayBox,BM_SETCHECK,old?BST_CHECKED:BST_UNCHECKED,0);if(showError)MessageBoxW(g_hwnd,L"Crash Monitor could not save and verify the Minimize to tray setting.",L"Crash Monitor",MB_OK|MB_ICONERROR);return FALSE;}g_minimizeToTray=on;if(g_minimizeTrayBox)SendMessageW(g_minimizeTrayBox,BM_SETCHECK,on?BST_CHECKED:BST_UNCHECKED,0);AppendLog(on?L"Minimize to tray enabled":L"Minimize to tray disabled");RefreshProgramList();return TRUE;}
static BOOL ApplyKeepTrayTaskbarSetting(BOOL on,BOOL showError,BOOL applyTray){BOOL old=g_keepTrayTaskbar;if(!SaveKeepTrayTaskbarSetting(on)){g_keepTrayTaskbar=old;if(g_keepTrayTaskbarBox)SendMessageW(g_keepTrayTaskbarBox,BM_SETCHECK,old?BST_CHECKED:BST_UNCHECKED,0);if(showError)MessageBoxW(g_hwnd,L"Crash Monitor could not save and verify the taskbar + tray setting.",L"Crash Monitor",MB_OK|MB_ICONERROR);return FALSE;}g_keepTrayTaskbar=on;if(g_keepTrayTaskbarBox)SendMessageW(g_keepTrayTaskbarBox,BM_SETCHECK,on?BST_CHECKED:BST_UNCHECKED,0);if(applyTray&&g_hwnd&&!g_trayOnly&&!g_hiddenToTray){if(g_keepTrayTaskbar)AddTrayIcon();else RemoveTrayIcon();}AppendLog(on?L"Taskbar + tray mode enabled":L"Taskbar + tray mode disabled");RefreshProgramList();return TRUE;}
static BOOL ApplyCloseXToTraySetting(BOOL on,BOOL showError){BOOL old=g_closeXToTray;if(!SaveCloseXToTraySetting(on)){g_closeXToTray=old;if(g_closeXTrayBox)SendMessageW(g_closeXTrayBox,BM_SETCHECK,old?BST_CHECKED:BST_UNCHECKED,0);if(showError)MessageBoxW(g_hwnd,L"Crash Monitor could not save and verify the Close/X behavior setting.",L"Crash Monitor",MB_OK|MB_ICONERROR);return FALSE;}g_closeXToTray=on;if(g_closeXTrayBox)SendMessageW(g_closeXTrayBox,BM_SETCHECK,on?BST_CHECKED:BST_UNCHECKED,0);AppendLog(on?L"Close/X to tray enabled":L"Close/X now exits the app");RefreshProgramList();return TRUE;}
static BOOL ApplyStartMinimizedSetting(BOOL on,BOOL showError){BOOL old=g_startMinimized;if(!SaveStartMinimizedSetting(on)){g_startMinimized=old;if(g_startMinimizedBox)SendMessageW(g_startMinimizedBox,BM_SETCHECK,old?BST_CHECKED:BST_UNCHECKED,0);if(showError)MessageBoxW(g_hwnd,L"Crash Monitor could not save and verify Start minimized.",L"Crash Monitor",MB_OK|MB_ICONERROR);return FALSE;}g_startMinimized=on;if(g_startMinimizedBox)SendMessageW(g_startMinimizedBox,BM_SETCHECK,on?BST_CHECKED:BST_UNCHECKED,0);AppendLog(on?L"Start minimized on next launch enabled":L"Start minimized on next launch disabled");RefreshProgramList();return TRUE;}
static BOOL ApplyStartPausedSetting(BOOL on,BOOL showError){BOOL old=g_startPaused;if(!SaveStartPausedSetting(on)){g_startPaused=old;if(g_startPausedBox)SendMessageW(g_startPausedBox,BM_SETCHECK,old?BST_CHECKED:BST_UNCHECKED,0);if(showError)MessageBoxW(g_hwnd,L"Crash Monitor could not save and verify Start paused.",L"Crash Monitor",MB_OK|MB_ICONERROR);return FALSE;}g_startPaused=on;if(g_startPausedBox)SendMessageW(g_startPausedBox,BM_SETCHECK,on?BST_CHECKED:BST_UNCHECKED,0);AppendLog(on?L"Start paused on next launch enabled":L"Start paused on next launch disabled");RefreshProgramList();return TRUE;}
static BOOL ApplyNotificationsSetting(BOOL on,BOOL showError){BOOL old=g_notificationsEnabled;if(!SaveNotificationsSetting(on)){g_notificationsEnabled=old;if(g_notificationsBox)SendMessageW(g_notificationsBox,BM_SETCHECK,old?BST_CHECKED:BST_UNCHECKED,0);if(showError)MessageBoxW(g_hwnd,L"Crash Monitor could not save and verify Notifications.",L"Crash Monitor",MB_OK|MB_ICONERROR);return FALSE;}g_notificationsEnabled=on;if(g_notificationsBox)SendMessageW(g_notificationsBox,BM_SETCHECK,on?BST_CHECKED:BST_UNCHECKED,0);AppendLog(on?L"Tray notifications enabled":L"Tray notifications disabled");RefreshProgramList();return TRUE;}
static BOOL CreateShortcutFileToTargetArgs(LPCWSTR linkPath,LPCWSTR targetExe,LPCWSTR workDir,LPCWSTR args){HRESULT hr=CoInitializeEx(NULLPTR,COINIT_APARTMENTTHREADED);BOOL uninit=(hr>=0);IShellLinkW* sl=0;HRESULT cr=CoCreateInstance(&CLSID_ShellLink,NULLPTR,CLSCTX_INPROC_SERVER,&IID_IShellLinkW,(PVOID*)&sl);BOOL ok=FALSE;if(cr>=0&&sl){sl->lpVtbl->SetPath(sl,targetExe);sl->lpVtbl->SetArguments(sl,args?args:L"");sl->lpVtbl->SetWorkingDirectory(sl,workDir);sl->lpVtbl->SetDescription(sl,L"Crash Monitor - external crash reports for Windows applications");sl->lpVtbl->SetIconLocation(sl,targetExe,0);IPersistFile* pf=0;if(sl->lpVtbl->QueryInterface(sl,&IID_IPersistFile,(PVOID*)&pf)>=0&&pf){ok=pf->lpVtbl->Save(pf,linkPath,TRUE)>=0;pf->lpVtbl->Release(pf);}sl->lpVtbl->Release(sl);}if(uninit)CoUninitialize();return ok;}
static BOOL CreateShortcutFileToTarget(LPCWSTR linkPath,LPCWSTR targetExe,LPCWSTR workDir){return CreateShortcutFileToTargetArgs(linkPath,targetExe,workDir,L"--app");}
static BOOL CreateShortcutFile(LPCWSTR linkPath){return CreateShortcutFileToTarget(linkPath,g_installExe,g_installDir);}
static BOOL ShortcutPath(int csidl,WCHAR*out){out[0]=0;if(SHGetFolderPathW(0,csidl,0,SHGFP_TYPE_CURRENT,out)<0)return FALSE;lstrcatW(out,L"\\Crash Monitor.lnk");return TRUE;}
static BOOL SetShortcuts(BOOL startMenu,BOOL desktop){BOOL ok=TRUE;WCHAR p[MAX_PATH*2];if(ShortcutPath(CSIDL_PROGRAMS,p)){if(startMenu){if(!CreateShortcutFile(p))ok=FALSE;}else DeleteFileW(p);}else if(startMenu)ok=FALSE;if(ShortcutPath(CSIDL_DESKTOPDIRECTORY,p)){if(desktop){if(!CreateShortcutFile(p))ok=FALSE;}else DeleteFileW(p);}else if(desktop)ok=FALSE;return ok;}
static BOOL RegisterAppPath(){HKEY h=0;DWORD disp=0;if(RegCreateKeyExW(HKEY_CURRENT_USER,L"Software\\Microsoft\\Windows\\CurrentVersion\\App Paths\\Crash Monitor.exe",0,0,0,KEY_WRITE,NULLPTR,&h,&disp)!=ERROR_SUCCESS)return FALSE;LONG r=RegSetValueExW(h,(LPCWSTR)0,0,REG_SZ,(BYTE*)g_installExe,(DWORD)((lstrlenW(g_installExe)+1)*sizeof(WCHAR)));if(r==ERROR_SUCCESS)r=RegSetValueExW(h,L"Path",0,REG_SZ,(BYTE*)g_installDir,(DWORD)((lstrlenW(g_installDir)+1)*sizeof(WCHAR)));RegCloseKey(h);return r==ERROR_SUCCESS;}

static BOOL UnregisterWerOne(LPCWSTR exe);
static BOOL SetRegString(HKEY h,LPCWSTR name,LPCWSTR value){return RegSetValueExW(h,name,0,REG_SZ,(const BYTE*)value,(DWORD)((lstrlenW(value)+1)*sizeof(WCHAR)))==ERROR_SUCCESS;}
static BOOL SetRegDword(HKEY h,LPCWSTR name,DWORD value){return RegSetValueExW(h,name,0,REG_DWORD,(const BYTE*)&value,sizeof(value))==ERROR_SUCCESS;}
static BOOL RegisterUninstallEntry(){
 HKEY h=0;DWORD disp=0;LPCWSTR key=L"Software\\Microsoft\\Windows\\CurrentVersion\\Uninstall\\Crash Monitor";
 if(RegCreateKeyExW(HKEY_CURRENT_USER,key,0,0,0,KEY_WRITE,NULLPTR,&h,&disp)!=ERROR_SUCCESS)return FALSE;
 WCHAR uninstall[MAX_PATH*2+64],quiet[MAX_PATH*2+64],date[16];SYSTEMTIME st;GetLocalTime(&st);
 lstrcpyW(uninstall,L"\"");lstrcatW(uninstall,g_installExe);lstrcatW(uninstall,L"\" --uninstall");
 lstrcpyW(quiet,L"\"");lstrcatW(quiet,g_installExe);lstrcatW(quiet,L"\" --uninstall-quiet");
 wsprintfW(date,L"%04u%02u%02u",st.wYear,st.wMonth,st.wDay);
 DWORD one=1,estimated=128;
 BOOL ok=SetRegString(h,L"DisplayName",L"Crash Monitor")&&SetRegString(h,L"DisplayVersion",CM_VERSION_W)&&SetRegString(h,L"Publisher",L"Crash Monitor")&&SetRegString(h,L"InstallLocation",g_installDir)&&SetRegString(h,L"DisplayIcon",g_installExe)&&SetRegString(h,L"UninstallString",uninstall)&&SetRegString(h,L"QuietUninstallString",quiet)&&SetRegString(h,L"InstallDate",date)&&SetRegDword(h,L"NoModify",one)&&SetRegDword(h,L"NoRepair",one)&&SetRegDword(h,L"EstimatedSize",estimated);
 RegCloseKey(h);return ok;
}
static void NotifyAppsListChanged(){SendMessageW(HWND_BROADCAST,WM_SETTINGCHANGE,0,(LPARAM)L"Software\\Microsoft\\Windows\\CurrentVersion\\Uninstall");}
static void UnregisterAppEntries(){
 RegDeleteTreeW(HKEY_CURRENT_USER,L"Software\\Microsoft\\Windows\\CurrentVersion\\App Paths\\Crash Monitor.exe");
 RegDeleteTreeW(HKEY_CURRENT_USER,L"Software\\Microsoft\\Windows\\CurrentVersion\\Uninstall\\Crash Monitor");
 NotifyAppsListChanged();
}
static BOOL IsDotDir(LPCWSTR n){return (n[0]==L'.'&&n[1]==0)||(n[0]==L'.'&&n[1]==L'.'&&n[2]==0);}
static void RemoveTree(LPCWSTR path){
 WCHAR pat[MAX_PATH*2],child[MAX_PATH*2];lstrcpyW(pat,path);lstrcatW(pat,L"\\*");WIN32_FIND_DATAW fd;HANDLE fh=FindFirstFileW(pat,&fd);
 if(fh!=INVALID_HANDLE_VALUE){do{if(IsDotDir(fd.cFileName))continue;lstrcpyW(child,path);lstrcatW(child,L"\\");lstrcatW(child,fd.cFileName);if(fd.dwFileAttributes&FILE_ATTRIBUTE_DIRECTORY)RemoveTree(child);else DeleteFileW(child);}while(FindNextFileW(fh,&fd));FindClose(fh);}RemoveDirectoryW(path);
}
static void CloseRunningCrashMonitor(){LPCWSTR classes[10]={L"CrashMonitorMainClass411",L"CrashMonitorMainClass39",L"CrashMonitorMainClass38",L"CrashMonitorMainClass37",L"CrashMonitorMainClass36",L"CrashMonitorMainClass35",L"CrashMonitorMainClass34",L"CrashMonitorMainClass33",L"CrashMonitorMainClass32",L"CrashMonitorMainClass31"};for(int i=0;i<10;i++){HWND w=FindWindowW(classes[i],L"Crash Monitor");if(w)SendMessageW(w,WM_COMMAND,(WPARAM)IDC_EXITAPP,0);}Sleep(700);}
static void RemoveAllWerNoUi(){AcquireSRWLockShared(&g_lock);for(int i=0;i<g_targetCount;i++)UnregisterWerOne(g_targets[i].exeName);ReleaseSRWLockShared(&g_lock);}
static void ScheduleFinalSelfDelete(){
 WCHAR tempDir[MAX_PATH*2];ZeroMem(tempDir,sizeof(tempDir));DWORD n=GetTempPathW(MAX_PATH*2,tempDir);BOOL moved=FALSE;if(n>0&&n<MAX_PATH*2){WCHAR tempExe[MAX_PATH*2];wsprintfW(tempExe,L"%sCrashMonitor-Uninstall-%u.exe",tempDir,GetCurrentProcessId());DeleteFileW(tempExe);if(MoveFileExW(g_installExe,tempExe,MOVEFILE_REPLACE_EXISTING)){moved=TRUE;MoveFileExW(tempExe,(LPCWSTR)0,MOVEFILE_DELAY_UNTIL_REBOOT);RemoveDirectoryW(g_installDir);}}if(!moved)MoveFileExW(g_installExe,(LPCWSTR)0,MOVEFILE_DELAY_UNTIL_REBOOT);
}
static void RemoveLegacyData(){WCHAR local[MAX_PATH*2],old[MAX_PATH*2];ZeroMem(local,sizeof(local));if(!GetEnvironmentVariableW(L"LOCALAPPDATA",local,MAX_PATH*2))return;lstrcpyW(old,local);lstrcatW(old,L"\\Crash Monitor AV Safe");RemoveTree(old);}
static void DoUninstallAdmin(BOOL quiet){
 CloseRunningCrashMonitor();UnregisterAppEntries();SetStartupPath(g_installExe,FALSE);SetShortcuts(FALSE,FALSE);RemoveAllWerNoUi();RemoveTree(g_baseDir);RemoveLegacyData();
 WCHAR pat[MAX_PATH*2],child[MAX_PATH*2];lstrcpyW(pat,g_installDir);lstrcatW(pat,L"\\*");WIN32_FIND_DATAW fd;HANDLE fh=FindFirstFileW(pat,&fd);if(fh!=INVALID_HANDLE_VALUE){do{if(IsDotDir(fd.cFileName))continue;lstrcpyW(child,g_installDir);lstrcatW(child,L"\\");lstrcatW(child,fd.cFileName);if(lstrcmpiW(child,g_exePath)==0)continue;if(fd.dwFileAttributes&FILE_ATTRIBUTE_DIRECTORY)RemoveTree(child);else DeleteFileW(child);}while(FindNextFileW(fh,&fd));FindClose(fh);}
 ScheduleFinalSelfDelete();if(!quiet)MessageBoxW(0,L"Crash Monitor was uninstalled.\n\nIts settings, logs, crash dumps, shortcuts, startup entry, Windows Search/App registration, and Crash Monitor WER dump registrations were removed. The final executable is removed immediately when Windows allows it; if Windows keeps the running image locked, deletion is scheduled for the next reboot.",L"Crash Monitor Uninstall",MB_OK|MB_ICONINFORMATION);
}
static void BeginUninstall(BOOL quiet){
 if(!quiet){int r=MessageBoxW(0,L"Uninstall Crash Monitor?\n\nThis removes the app, its settings/logs, saved crash dumps, shortcuts, startup entry, and Crash Monitor-created Windows crash-dump registrations.",L"Crash Monitor Uninstall",MB_YESNO|MB_ICONQUESTION);if(r!=IDYES)return;}
 CloseRunningCrashMonitor();LPCWSTR arg=quiet?L"--uninstall-admin-quiet":L"--uninstall-admin";HINSTANCE r=ShellExecuteW(0,L"runas",g_installExe,arg,0,SW_HIDE);if((ULONG_PTR)r<=32&&!quiet)MessageBoxW(0,L"Windows did not allow the administrator step, so Crash Monitor was not fully uninstalled.",L"Crash Monitor Uninstall",MB_OK|MB_ICONERROR);
}

static void SaveTargetsLocked(){WCHAR n[32];wsprintfW(n,L"%d",g_targetCount);WriteProfileChecked(L"Targets",L"Count",n);for(int i=0;i<MAX_TARGETS;i++){WCHAR k[32];if(i<g_targetCount){wsprintfW(k,L"Name%d",i);WriteProfileChecked(L"Targets",k,g_targets[i].exeName);wsprintfW(k,L"Path%d",i);WriteProfileChecked(L"Targets",k,g_targets[i].fullPath);wsprintfW(k,L"Enabled%d",i);WriteProfileChecked(L"Targets",k,g_targets[i].enabled?L"1":L"0");}else{wsprintfW(k,L"Name%d",i);WriteProfileChecked(L"Targets",k,(LPCWSTR)0);wsprintfW(k,L"Path%d",i);WriteProfileChecked(L"Targets",k,(LPCWSTR)0);wsprintfW(k,L"Enabled%d",i);WriteProfileChecked(L"Targets",k,(LPCWSTR)0);}}}
static void LoadTargets(){AcquireSRWLockExclusive(&g_lock);g_targetCount=0;UINT c=GetPrivateProfileIntW(L"Targets",L"Count",0,g_configPath);if(c>MAX_TARGETS)c=MAX_TARGETS;for(UINT i=0;i<c;i++){TargetConfig t;ZeroMem(&t,sizeof(t));WCHAR k[32];wsprintfW(k,L"Name%u",i);GetPrivateProfileStringW(L"Targets",k,L"",t.exeName,MAX_PATH,g_configPath);if(!t.exeName[0])continue;wsprintfW(k,L"Path%u",i);GetPrivateProfileStringW(L"Targets",k,L"",t.fullPath,MAX_PATH*2,g_configPath);wsprintfW(k,L"Enabled%u",i);t.enabled=GetPrivateProfileIntW(L"Targets",k,1,g_configPath)?TRUE:FALSE;g_targets[g_targetCount++]=t;}if(g_targetCount==0){ZeroMem(&g_targets[0],sizeof(TargetConfig));CopyWide(g_targets[0].exeName,MAX_PATH,L"obs64.exe");g_targets[0].enabled=TRUE;g_targetCount=1;SaveTargetsLocked();}ReleaseSRWLockExclusive(&g_lock);}
static BOOL QueryProcessPath(DWORD pid,WCHAR*out,int cap){out[0]=0;HANDLE h=OpenProcess(PROCESS_QUERY_LIMITED_INFORMATION,FALSE,pid);if(!h)return FALSE;DWORD n=cap;BOOL ok=QueryFullProcessImageNameW(h,0,out,&n);CloseHandle(h);return ok;}
static BOOL TargetMatch(const TargetConfig&t,const PROCESSENTRY32W&p){if(!t.enabled||lstrcmpiW(t.exeName,p.szExeFile)!=0)return FALSE;if(!t.fullPath[0])return TRUE;WCHAR q[MAX_PATH*2];if(!QueryProcessPath(p.th32ProcessID,q,MAX_PATH*2))return FALSE;return lstrcmpiW(q,t.fullPath)==0;}
static BOOL AddTargetPath(LPCWSTR path){LPCWSTR b=BaseNamePtr(path);if(!b||!b[0])return FALSE;AcquireSRWLockExclusive(&g_lock);for(int i=0;i<g_targetCount;i++)if(lstrcmpiW(g_targets[i].exeName,b)==0&&(!g_targets[i].fullPath[0]||lstrcmpiW(g_targets[i].fullPath,path)==0)){CopyWide(g_targets[i].fullPath,MAX_PATH*2,path);g_targets[i].enabled=TRUE;SaveTargetsLocked();ReleaseSRWLockExclusive(&g_lock);g_reconfigure=1;return TRUE;}if(g_targetCount>=MAX_TARGETS){ReleaseSRWLockExclusive(&g_lock);return FALSE;}TargetConfig&t=g_targets[g_targetCount++];ZeroMem(&t,sizeof(t));CopyWide(t.exeName,MAX_PATH,b);CopyWide(t.fullPath,MAX_PATH*2,path);t.enabled=TRUE;SaveTargetsLocked();ReleaseSRWLockExclusive(&g_lock);g_reconfigure=1;return TRUE;}

static LRESULT CALLBACK MainWndProc(HWND,UINT,WPARAM,LPARAM);
static void HandleTrayCommand(HWND,UINT);
static void MoveToTrayMode(); static void MoveToTaskbarMode(); static void MinimizeIntoTray(); static void HandleMainClose(HWND);
static BOOL WriteDiagnosticReportFile(LPCWSTR);
static BOOL WriteExternalDump(DWORD,LPCWSTR,LPCWSTR,DWORD,DWORD,DWORD);
static BOOL SplitArchiveForLimit(LPCWSTR,ULONGLONG,int*);
static ULONGLONG FileSize64(LPCWSTR);
static BOOL VerifyArchive(LPCWSTR,LPCWSTR);
static BOOL RegisterWerAt(HKEY,LPCWSTR,LPCWSTR); static BOOL IsWerConfiguredAt(HKEY,LPCWSTR,LPCWSTR); static BOOL UnregisterWerAt(HKEY,LPCWSTR);
static BOOL CommandValue(LPCWSTR,WCHAR*,int);
static void SelfTestWrite(HANDLE h,LPCWSTR status,LPCWSTR name){WCHAR line[768];wsprintfW(line,L"%s - %s\r\n",status,name);AppendUtf8(h,line);FlushFileBuffers(h);}
static BOOL BuildSafeSelfTestArtifactPath(LPCWSTR leaf,WCHAR*out,int cap){if(!out||cap<=0)return FALSE;WCHAR local[MAX_PATH*2];ZeroMem(local,sizeof(local));if(!GetEnvironmentVariableW(L"LOCALAPPDATA",local,MAX_PATH*2))return FALSE;lstrcpyW(out,local);lstrcatW(out,L"\\Crash Monitor");EnsureDir(out);lstrcatW(out,L"\\");lstrcatW(out,leaf);return lstrlenW(out)<cap;}
static void WriteSelfTestProgressSnapshot(LPCWSTR line){if(!g_selfTestProgressPath[0]||!line)return;HANDLE ph=CreateFileW(g_selfTestProgressPath,GENERIC_WRITE,FILE_SHARE_READ|FILE_SHARE_WRITE,NULLPTR,CREATE_ALWAYS,FILE_ATTRIBUTE_NORMAL,0);if(ph==INVALID_HANDLE_VALUE)return;DWORD bytes=(DWORD)((lstrlenW(line)+1)*sizeof(WCHAR)),wrote=0;WriteFile(ph,line,bytes,&wrote,NULLPTR);FlushFileBuffers(ph);CloseHandle(ph);}
static void SelfTestProgress(HANDLE h,int index,int total,LPCWSTR name){WCHAR line[900];wsprintfW(line,L"RUNNING %d/%d - %s\r\n",index,total,name);AppendUtf8(h,line);FlushFileBuffers(h);WriteSelfTestProgressSnapshot(line);}
static BOOL ReadSelfTestProgressSnapshot(WCHAR*out,int cap){if(!out||cap<2)return FALSE;out[0]=0;WCHAR path[MAX_PATH*2];if(!BuildSafeSelfTestArtifactPath(L"CrashMonitor-SafeSelfTest-v4.2-Build12.progress",path,MAX_PATH*2))return FALSE;HANDLE h=CreateFileW(path,GENERIC_READ,FILE_SHARE_READ|FILE_SHARE_WRITE,NULLPTR,OPEN_EXISTING,FILE_ATTRIBUTE_NORMAL,0);if(h==INVALID_HANDLE_VALUE)return FALSE;DWORD maxBytes=(DWORD)((cap-1)*sizeof(WCHAR)),got=0;BOOL ok=ReadFile(h,out,maxBytes,&got,NULLPTR);CloseHandle(h);if(!ok||got<sizeof(WCHAR)){out[0]=0;return FALSE;}int chars=(int)(got/sizeof(WCHAR));if(chars>=cap)chars=cap-1;out[chars]=0;while(chars>0&&(out[chars-1]==L'\r'||out[chars-1]==L'\n'||out[chars-1]==0))out[--chars]=0;return chars>0;}
static void ParseSelfTestProgressNumbers(LPCWSTR text,LONG*outIndex,LONG*outTotal){if(outIndex)*outIndex=0;if(outTotal)*outTotal=39;if(!text)return;LPCWSTR p=text;while(*p&&(*p<L'0'||*p>L'9'))p++;LONG a=0,b=0;while(*p>=L'0'&&*p<=L'9'){a=a*10+(*p-L'0');p++;}if(*p==L'/')p++;while(*p>=L'0'&&*p<=L'9'){b=b*10+(*p-L'0');p++;}if(outIndex&&a>0)*outIndex=a;if(outTotal&&b>0)*outTotal=b;}
static BOOL RunSelfTestSubprocess(LPCWSTR arg,DWORD expectedExit){WCHAR exe[MAX_PATH*2];ZeroMem(exe,sizeof(exe));if(!GetModuleFileNameW(0,exe,MAX_PATH*2))return FALSE;WCHAR cmd[MAX_PATH*2+128];lstrcpyW(cmd,L"\"");lstrcatW(cmd,exe);lstrcatW(cmd,L"\" ");lstrcatW(cmd,arg);STARTUPINFOW_NATIVE si;PROCESS_INFORMATION_NATIVE pi;ZeroMem(&si,sizeof(si));ZeroMem(&pi,sizeof(pi));si.cb=sizeof(si);if(!CreateProcessW(exe,cmd,NULLPTR,NULLPTR,FALSE,CREATE_NO_WINDOW,NULLPTR,(LPCWSTR)0,&si,&pi))return FALSE;DWORD wr=WaitForSingleObject(pi.hProcess,5000);DWORD ec=0xFFFFFFFFu;if(wr==WAIT_OBJECT_0)GetExitCodeProcess(pi.hProcess,&ec);CloseHandle(pi.hThread);CloseHandle(pi.hProcess);return wr==WAIT_OBJECT_0&&ec==expectedExit;}
static int RunSelfTestShortcutMarkerChild(){WCHAR marker[MAX_PATH*2];ZeroMem(marker,sizeof(marker));if(!CommandValue(L"--selftest-shortcut-marker=",marker,MAX_PATH*2))return 2;HANDLE h=CreateFileW(marker,GENERIC_WRITE,FILE_SHARE_READ|FILE_SHARE_WRITE,NULLPTR,CREATE_ALWAYS,FILE_ATTRIBUTE_NORMAL,0);if(h==INVALID_HANDLE_VALUE)return 3;DWORD wrote=0;LPCWSTR text=L"Crash Monitor Build 12 shortcut launch marker";BOOL ok=WriteFile(h,text,(DWORD)(lstrlenW(text)*sizeof(WCHAR)),&wrote,NULLPTR);FlushFileBuffers(h);CloseHandle(h);return ok?0:4;}
static BOOL WaitForSelfTestMarker(LPCWSTR marker,DWORD timeoutMs){ULONGLONG start=GetTickCount64();while(GetTickCount64()-start<timeoutMs){if(FileExists(marker))return TRUE;Sleep(50);}return FileExists(marker);}
static BOOL CopyInstallImageForUpdate(LPCWSTR sourceExe,LPCWSTR destExe){if(!sourceExe||!destExe||!sourceExe[0]||!destExe[0])return FALSE;if(lstrcmpiW(sourceExe,destExe)==0)return TRUE;return CopyFileW(sourceExe,destExe,FALSE);}
static int RestartExplorerAndVerifyTrayRecovery(HWND testWindow){if(!testWindow)return -1;HWND tray=FindWindowW(L"Shell_TrayWnd",(LPCWSTR)0);if(!tray)return -1;DWORD shellPid=0;GetWindowThreadProcessId(tray,&shellPid);if(!shellPid||shellPid==GetCurrentProcessId())return -1;HANDLE shell=OpenProcess(PROCESS_TERMINATE|SYNCHRONIZE,FALSE,shellPid);if(!shell)return -1;LONG before=g_taskbarRecoveryCount;BOOL killed=TerminateProcess(shell,0);if(killed)WaitForSingleObject(shell,5000);CloseHandle(shell);if(!killed)return -1;ULONGLONG firstWait=GetTickCount64();while(GetTickCount64()-firstWait<2500ULL){MSG msg;SetTimer(testWindow,98,100,NULLPTR);if(GetMessageW(&msg,0,0,0)>0){TranslateMessage(&msg);DispatchMessageW(&msg);}KillTimer(testWindow,98);if(FindWindowW(L"Shell_TrayWnd",(LPCWSTR)0)&&g_taskbarRecoveryCount>before&&g_trayVisible)return 1;}if(!FindWindowW(L"Shell_TrayWnd",(LPCWSTR)0))ShellExecuteW(0,L"open",L"explorer.exe",0,0,SW_SHOWNORMAL);ULONGLONG secondWait=GetTickCount64();while(GetTickCount64()-secondWait<12000ULL){MSG msg;SetTimer(testWindow,98,100,NULLPTR);if(GetMessageW(&msg,0,0,0)>0){TranslateMessage(&msg);DispatchMessageW(&msg);}KillTimer(testWindow,98);if(FindWindowW(L"Shell_TrayWnd",(LPCWSTR)0)&&g_taskbarRecoveryCount>before&&g_trayVisible)return 1;}if(!FindWindowW(L"Shell_TrayWnd",(LPCWSTR)0))ShellExecuteW(0,L"open",L"explorer.exe",0,0,SW_SHOWNORMAL);return 0;}
static LRESULT CALLBACK SelfTestTrayWndProc(HWND h,UINT m,WPARAM w,LPARAM l){if(g_taskbarCreatedMsg&&m==g_taskbarCreatedMsg)return MainWndProc(h,m,w,l);return DefWindowProcW(h,m,w,l);}
static BOOL SelfTestArchivePathFromLast(WCHAR*out,int cap){if(!out||cap<=0||!g_lastCapturedFile[0])return FALSE;lstrcpyW(out,g_dumpRoot);lstrcatW(out,L"\\");lstrcatW(out,g_lastCapturedFile);return FileExists(out)&&FileSize64(out)>0;}
static BOOL SelfTestVerifyZipPath(LPCWSTR zip){WCHAR root[MAX_PATH*2];if(!GetEnvironmentVariableW(L"SystemRoot",root,MAX_PATH*2))lstrcpyW(root,L"C:\\Windows");WCHAR tar[MAX_PATH*2];lstrcpyW(tar,root);lstrcatW(tar,L"\\System32\\tar.exe");return FileExists(tar)&&VerifyArchive(tar,zip);}
static BOOL StartSelfTestDumpTarget(PROCESS_INFORMATION_NATIVE* pi,WCHAR* marker,int markerCap){if(!pi||!marker||markerCap<=0)return FALSE;ZeroMem(pi,sizeof(*pi));WCHAR exe[MAX_PATH*2];ZeroMem(exe,sizeof(exe));if(!GetModuleFileNameW(0,exe,MAX_PATH*2))return FALSE;wsprintfW(marker,L"%s\\SafeSelfTest-DumpTarget-%u-%u.flag",g_baseDir,GetCurrentProcessId(),(UINT)(GetTickCount64()&0xFFFFFFFFu));HANDLE mh=CreateFileW(marker,GENERIC_WRITE,FILE_SHARE_READ|FILE_SHARE_WRITE,NULLPTR,CREATE_ALWAYS,FILE_ATTRIBUTE_NORMAL,0);if(mh==INVALID_HANDLE_VALUE)return FALSE;CloseHandle(mh);WCHAR cmd[MAX_PATH*4];lstrcpyW(cmd,L"\"");lstrcatW(cmd,exe);lstrcatW(cmd,L"\" --selftest-dump-target=\"");lstrcatW(cmd,marker);lstrcatW(cmd,L"\"");STARTUPINFOW_NATIVE si;ZeroMem(&si,sizeof(si));si.cb=sizeof(si);if(!CreateProcessW(exe,cmd,NULLPTR,NULLPTR,FALSE,CREATE_NO_WINDOW,NULLPTR,(LPCWSTR)0,&si,pi)){DeleteFileW(marker);return FALSE;}Sleep(150);if(WaitForSingleObject(pi->hProcess,0)==WAIT_OBJECT_0){CloseHandle(pi->hThread);CloseHandle(pi->hProcess);DeleteFileW(marker);ZeroMem(pi,sizeof(*pi));return FALSE;}return TRUE;}
static int RunSelfTestDumpTargetChild(){WCHAR marker[MAX_PATH*2];ZeroMem(marker,sizeof(marker));if(!CommandValue(L"--selftest-dump-target=",marker,MAX_PATH*2))return 2;ULONGLONG start=GetTickCount64();while(FileExists(marker)&&GetTickCount64()-start<120000ULL)Sleep(100);return 0;}
static BOOL SelfTestCreateDumpKind(LPCWSTR exeName,LPCWSTR kind){g_lastCapturedFile[0]=0;g_lastShareCompressed=0;g_lastShareParts=0;PROCESS_INFORMATION_NATIVE pi;WCHAR marker[MAX_PATH*2];if(!StartSelfTestDumpTarget(&pi,marker,MAX_PATH*2))return FALSE;DWORD hc=0;GetProcessHandleCount(pi.hProcess,&hc);BOOL ok=WriteExternalDump(pi.dwProcessId,exeName,kind,hc,0,0);DeleteFileW(marker);DWORD wr=WaitForSingleObject(pi.hProcess,5000);CloseHandle(pi.hThread);CloseHandle(pi.hProcess);WCHAR out[MAX_PATH*2];ZeroMem(out,sizeof(out));return wr==WAIT_OBJECT_0&&ok&&g_lastShareCompressed&&g_lastShareParts==1&&SelfTestArchivePathFromLast(out,MAX_PATH*2)&&SelfTestVerifyZipPath(out);}
#define SELFTEST_EXEC_STACK_COMMIT 262144u
static int RunSafeSelfTestBody();
static volatile LONG g_safeSelfTestWorkerResult=2;
static DWORD WINAPI SafeSelfTestExecutionWorker(PVOID){g_safeSelfTestWorkerResult=(LONG)RunSafeSelfTestBody();return 0;}
static int RunSafeSelfTest(){g_safeSelfTestWorkerResult=2;HANDLE th=CreateThread(NULLPTR,SELFTEST_EXEC_STACK_COMMIT,SafeSelfTestExecutionWorker,NULLPTR,0,0);if(!th){MessageBoxW(0,L"Crash Monitor could not start the Safe Self-Test execution worker with its dedicated stack.",L"Crash Monitor Safe Self-Test",MB_OK|MB_ICONERROR);return 2;}DWORD wr=WaitForSingleObject(th,0xFFFFFFFFu);CloseHandle(th);if(wr!=WAIT_OBJECT_0){MessageBoxW(0,L"Crash Monitor could not wait for the Safe Self-Test execution worker.",L"Crash Monitor Safe Self-Test",MB_OK|MB_ICONERROR);return 2;}return (int)g_safeSelfTestWorkerResult;}
static int RunSafeSelfTestBody(){
 WCHAR tmpBase[MAX_PATH*2];ZeroMem(tmpBase,sizeof(tmpBase));DWORD tn=GetTempPathW(MAX_PATH*2,tmpBase);if(!(tn>0&&tn<MAX_PATH*2)){MessageBoxW(0,L"Crash Monitor could not resolve the Windows temporary folder for isolated Safe Self-Test working data.",L"Crash Monitor Safe Self-Test",MB_OK|MB_ICONERROR);return 2;}
 WCHAR local[MAX_PATH*2];ZeroMem(local,sizeof(local));if(!GetEnvironmentVariableW(L"LOCALAPPDATA",local,MAX_PATH*2)){MessageBoxW(0,L"Crash Monitor could not resolve LOCALAPPDATA for the Safe Self-Test report.",L"Crash Monitor Safe Self-Test",MB_OK|MB_ICONERROR);return 2;}
 WCHAR reportDir[MAX_PATH*2];lstrcpyW(reportDir,local);lstrcatW(reportDir,L"\\Crash Monitor");EnsureDir(reportDir);
 WCHAR report[MAX_PATH*2];wsprintfW(report,L"%s\\CrashMonitor-SafeSelfTest-v4.2-Build12.txt",reportDir);wsprintfW(g_selfTestProgressPath,L"%s\\CrashMonitor-SafeSelfTest-v4.2-Build12.progress",reportDir);DeleteFileW(g_selfTestProgressPath);HANDLE rh=CreateFileW(report,GENERIC_WRITE,FILE_SHARE_READ,NULLPTR,CREATE_ALWAYS,FILE_ATTRIBUTE_NORMAL,0);if(rh==INVALID_HANDLE_VALUE){MessageBoxW(0,L"Crash Monitor could not create the Safe Self-Test report in its project data/log folder.",L"Crash Monitor Safe Self-Test",MB_OK|MB_ICONERROR);return 2;}
 AppendUtf8(rh,L"Crash Monitor v4.2 Build 12 - AUTOMATED RELEASE SELF-TEST\r\n=========================================================\r\nPersistent report location: %LOCALAPPDATA%\\Crash Monitor (next to monitor.log).\r\nUses isolated project-owned temporary settings/data and real production code paths wherever safe.\r\nBuild 12 preserves the automated Update/Repair, Start Menu shortcut launch, and guarded Explorer/taskbar restart checks, and fixes the Build 11 pre-report access violation with a dedicated Safe Self-Test execution stack.\r\nExplorer/taskbar may disappear briefly during test 27 and is restarted automatically. Real sign-in, asynchronous Windows Search indexing, UAC approval, and AV/SmartScreen reputation remain environment-owned.\r\nReal Crash Monitor settings, monitored-program data, startup registration, WER LocalDumps registration, and dump files are not modified by the isolated checks.\r\n\r\n");int pass=0,fail=0,skipped=0;
 SelfTestProgress(rh,1,39,L"persistent Safe Self-Test report creation");
 BOOL reportOk=GetFileAttributesW(report)!=INVALID_FILE_ATTRIBUTES;SelfTestWrite(rh,reportOk?L"PASS":L"FAIL",L"persistent Safe Self-Test report created in Crash Monitor data/log folder");if(reportOk)pass++;else fail++;
 SelfTestProgress(rh,2,39,L"isolated temporary test folder");
 WCHAR root[MAX_PATH*2];ZeroMem(root,sizeof(root));wsprintfW(root,L"%sCrashMonitor-SafeSelfTest-Work-%u",tmpBase,GetCurrentProcessId());RemoveTree(root);EnsureDir(root);BOOL pathOk=GetFileAttributesW(root)!=INVALID_FILE_ATTRIBUTES;SelfTestWrite(rh,pathOk?L"PASS":L"FAIL",L"isolated project-owned temporary test folder");if(pathOk)pass++;else fail++;
 if(pathOk){CopyWide(g_baseDir,MAX_PATH*2,root);lstrcpyW(g_dumpRoot,root);lstrcatW(g_dumpRoot,L"\\Dumps");EnsureDir(g_dumpRoot);lstrcpyW(g_logPath,root);lstrcatW(g_logPath,L"\\monitor.log");lstrcpyW(g_configPath,root);lstrcatW(g_configPath,L"\\targets.ini");GetModuleFileNameW(0,g_exePath,MAX_PATH*2);CopyWide(g_installExe,MAX_PATH*2,g_exePath);CopyWide(g_installDir,MAX_PATH*2,root);}
 SelfTestProgress(rh,3,39,L"Minimize-to-tray setter + persistence");
 BOOL t=pathOk&&ApplyMinimizeToTraySetting(FALSE,FALSE)&&!g_minimizeToTray&&GetMinimizeToTraySetting()==FALSE&&ApplyMinimizeToTraySetting(TRUE,FALSE)&&g_minimizeToTray&&GetMinimizeToTraySetting()==TRUE;SelfTestWrite(rh,t?L"PASS":L"FAIL",L"Minimize-to-tray immediate production setter + write/read persistence");if(t)pass++;else fail++;
 SelfTestProgress(rh,4,39,L"taskbar+tray setter + persistence");
 t=pathOk&&ApplyKeepTrayTaskbarSetting(TRUE,FALSE,FALSE)&&g_keepTrayTaskbar&&GetKeepTrayTaskbarSetting()==TRUE&&ApplyKeepTrayTaskbarSetting(FALSE,FALSE,FALSE)&&!g_keepTrayTaskbar&&GetKeepTrayTaskbarSetting()==FALSE;SelfTestWrite(rh,t?L"PASS":L"FAIL",L"taskbar+tray immediate production setter + write/read persistence");if(t)pass++;else fail++;
 SelfTestProgress(rh,5,39,L"display-mode persistence");
 t=pathOk&&SaveTrayOnlySetting(TRUE)&&GetTrayOnlySetting()==TRUE&&SaveTrayOnlySetting(FALSE)&&GetTrayOnlySetting()==FALSE;SelfTestWrite(rh,t?L"PASS":L"FAIL",L"display-mode persistence write/read production path");if(t)pass++;else fail++;
 SelfTestProgress(rh,6,39,L"Close/X-to-tray setter + persistence");
 t=pathOk&&ApplyCloseXToTraySetting(TRUE,FALSE)&&g_closeXToTray&&GetCloseXToTraySetting()==TRUE&&ApplyCloseXToTraySetting(FALSE,FALSE)&&!g_closeXToTray&&GetCloseXToTraySetting()==FALSE;SelfTestWrite(rh,t?L"PASS":L"FAIL",L"Close/X-to-tray immediate production setter + write/read persistence");if(t)pass++;else fail++;
 SelfTestProgress(rh,7,39,L"Start-minimized persistence");
 t=pathOk&&ApplyStartMinimizedSetting(TRUE,FALSE)&&g_startMinimized&&GetStartMinimizedSetting()==TRUE&&ApplyStartMinimizedSetting(FALSE,FALSE)&&!g_startMinimized&&GetStartMinimizedSetting()==FALSE;SelfTestWrite(rh,t?L"PASS":L"FAIL",L"Start-minimized next-launch setting + write/read persistence");if(t)pass++;else fail++;
 SelfTestProgress(rh,8,39,L"Start-paused persistence");
 t=pathOk&&ApplyStartPausedSetting(TRUE,FALSE)&&g_startPaused&&GetStartPausedSetting()==TRUE&&ApplyStartPausedSetting(FALSE,FALSE)&&!g_startPaused&&GetStartPausedSetting()==FALSE;SelfTestWrite(rh,t?L"PASS":L"FAIL",L"Start-paused next-launch setting + write/read persistence");if(t)pass++;else fail++;
 SelfTestProgress(rh,9,39,L"Notifications setter + persistence");
 t=pathOk&&ApplyNotificationsSetting(FALSE,FALSE)&&!g_notificationsEnabled&&GetNotificationsSetting()==FALSE&&ApplyNotificationsSetting(TRUE,FALSE)&&g_notificationsEnabled&&GetNotificationsSetting()==TRUE;SelfTestWrite(rh,t?L"PASS":L"FAIL",L"Notifications immediate production setter + write/read persistence");if(t)pass++;else fail++;
 SelfTestProgress(rh,10,39,L"window X/Y/W/H persistence");
 RECT sr;sr.left=-100;sr.top=50;sr.right=980;sr.bottom=850;t=pathOk&&SaveWindowRectSetting(sr);RECT rr;ZeroMem(&rr,sizeof(rr));t=t&&GetSavedWindowRectSetting(&rr)&&rr.left==sr.left&&rr.top==sr.top&&rr.right==sr.right&&rr.bottom==sr.bottom;SelfTestWrite(rh,t?L"PASS":L"FAIL",L"window X/Y/W/H write -> reload/read -> compare");if(t)pass++;else fail++;
 SelfTestProgress(rh,11,39,L"details-height persistence");
 g_detailsHeight=173;t=pathOk&&SaveDetailsHeightSetting()&&GetDetailsHeightSetting()==173;SelfTestWrite(rh,t?L"PASS":L"FAIL",L"details-height persistence write/read production path");if(t)pass++;else fail++;
 SelfTestProgress(rh,12,39,L"session Pause production state");
 g_reconfigure=0;ApplyPausedState(TRUE);t=(g_paused!=0&&g_reconfigure!=0);ApplyPausedState(FALSE);t=t&&(g_paused==0);SelfTestWrite(rh,t?L"PASS":L"FAIL",L"session-only Pause production setter immediate runtime state");if(t)pass++;else fail++;
 SelfTestProgress(rh,13,39,L"isolated X-to-exit termination");
 t=RunSelfTestSubprocess(L"--selftest-close-x-exit-child",0);SelfTestWrite(rh,t?L"PASS":L"FAIL",L"main-window X with Close/X-to-tray OFF terminates isolated child through production WM_CLOSE -> RequestExit path");if(t)pass++;else fail++;
 SelfTestProgress(rh,14,39,L"isolated Exit App termination");
 t=RunSelfTestSubprocess(L"--selftest-exit-button-child",0);SelfTestWrite(rh,t?L"PASS":L"FAIL",L"main Exit App control terminates isolated child through shared production RequestExit path");if(t)pass++;else fail++;
 SelfTestProgress(rh,15,39,L"monitored-program persistence round-trip");
 if(pathOk){AcquireSRWLockExclusive(&g_lock);ZeroMem(g_targets,sizeof(g_targets));g_targetCount=2;CopyWide(g_targets[0].exeName,MAX_PATH,L"obs64.exe");CopyWide(g_targets[0].fullPath,MAX_PATH*2,L"C:\\SelfTest\\obs64.exe");g_targets[0].enabled=TRUE;CopyWide(g_targets[1].exeName,MAX_PATH,L"SelfTestApp.exe");CopyWide(g_targets[1].fullPath,MAX_PATH*2,L"C:\\SelfTest\\SelfTestApp.exe");g_targets[1].enabled=FALSE;SaveTargetsLocked();ZeroMem(g_targets,sizeof(g_targets));g_targetCount=0;ReleaseSRWLockExclusive(&g_lock);LoadTargets();AcquireSRWLockShared(&g_lock);t=g_targetCount==2&&lstrcmpiW(g_targets[0].exeName,L"obs64.exe")==0&&g_targets[0].enabled&&lstrcmpiW(g_targets[1].exeName,L"SelfTestApp.exe")==0&&!g_targets[1].enabled;ReleaseSRWLockShared(&g_lock);}else t=FALSE;SelfTestWrite(rh,t?L"PASS":L"FAIL",L"monitored-program persistence write -> reload/read -> compare");if(t)pass++;else fail++;
 SelfTestProgress(rh,16,39,L"project-local production logging");
 AppendLog(L"SAFE SELF-TEST logging marker");t=pathOk&&LogFileSize(g_logPath)>0;SelfTestWrite(rh,t?L"PASS":L"FAIL",L"project-local production logging path");if(t)pass++;else fail++;
 SelfTestProgress(rh,17,39,L"bounded monitor.log rotation");
 if(pathOk){HANDLE lh=CreateFileW(g_logPath,GENERIC_WRITE,FILE_SHARE_READ|FILE_SHARE_WRITE,NULLPTR,OPEN_ALWAYS,FILE_ATTRIBUTE_NORMAL,0);if(lh!=INVALID_HANDLE_VALUE){SetFilePointer(lh,0,0,FILE_END);BYTE z[4096];ZeroMem(z,sizeof(z));DWORD wrote=0;for(int i=0;i<1300;i++)if(!WriteFile(lh,z,sizeof(z),&wrote,NULLPTR))break;CloseHandle(lh);}AppendLog(L"SAFE SELF-TEST rotation trigger");WCHAR r1[MAX_PATH*2];RotatedLogPath(1,r1,MAX_PATH*2);t=FileExists(r1)&&LogFileSize(g_logPath)>0&&LogFileSize(g_logPath)<LOG_ROTATE_BYTES;}else t=FALSE;SelfTestWrite(rh,t?L"PASS":L"FAIL",L"bounded monitor.log rotation through production AppendLog path");if(t)pass++;else fail++;
 SelfTestProgress(rh,18,39,L"missing-settings default recovery");
 if(pathOk){DeleteFileW(g_configPath);t=GetTrayOnlySetting()==FALSE&&GetMinimizeToTraySetting()==TRUE&&GetKeepTrayTaskbarSetting()==FALSE&&GetCloseXToTraySetting()==FALSE&&GetStartMinimizedSetting()==FALSE&&GetStartPausedSetting()==FALSE&&GetNotificationsSetting()==TRUE&&GetDetailsHeightSetting()==122;LoadTargets();AcquireSRWLockShared(&g_lock);t=t&&g_targetCount==1&&lstrcmpiW(g_targets[0].exeName,L"obs64.exe")==0&&g_targets[0].enabled;ReleaseSRWLockShared(&g_lock);}else t=FALSE;SelfTestWrite(rh,t?L"PASS":L"FAIL",L"missing settings recover to established defaults without touching real data");if(t)pass++;else fail++;
 SelfTestProgress(rh,19,39,L"single-instance mutex collision");
 HANDLE mx1=CreateMutexW(NULLPTR,FALSE,L"Local\\Crash_Monitor_31");HANDLE mx2=CreateMutexW(NULLPTR,FALSE,L"Local\\Crash_Monitor_31");DWORD me=GetLastError();t=mx1&&mx2&&me==ERROR_ALREADY_EXISTS;if(mx2)CloseHandle(mx2);if(mx1)CloseHandle(mx1);SelfTestWrite(rh,t?L"PASS":L"FAIL",L"intentional single-instance mutex collision detection");if(t)pass++;else fail++;

 HINSTANCE hi=(HINSTANCE)GetModuleHandleW(0);g_appIcon=BuildAppIcon(hi);g_taskbarCreatedMsg=RegisterWindowMessageW(L"TaskbarCreated");WNDCLASSEXW stwc;ZeroMem(&stwc,sizeof(stwc));stwc.cbSize=sizeof(stwc);stwc.lpfnWndProc=SelfTestTrayWndProc;stwc.hInstance=hi;stwc.hCursor=LoadCursorW(0,ResPtr(IDC_ARROW));stwc.hbrBackground=(HANDLE)(ULONG_PTR)(COLOR_WINDOW+1);stwc.lpszClassName=L"CrashMonitorSafeSelfTestClass411";RegisterClassExW(&stwc);HWND tw=CreateWindowExW(WS_EX_APPWINDOW,L"CrashMonitorSafeSelfTestClass411",L"Crash Monitor Safe Self-Test Window",WS_OVERLAPPEDWINDOW|WS_VISIBLE,120,120,720,520,0,0,hi,NULLPTR);g_hwnd=tw;ZeroMem(&g_nid,sizeof(g_nid));g_nid.cbSize=sizeof(g_nid);g_nid.hWnd=tw;g_nid.uID=91;g_nid.uCallbackMessage=WM_TRAY;g_nid.hIcon=g_appIcon;CopyWide(g_nid.szTip,128,L"Crash Monitor Safe Self-Test");
 if(tw){g_pauseBox=CreateWindowExW(0,L"BUTTON",L"Pause",WS_CHILD|WS_VISIBLE|BS_AUTOCHECKBOX,8,8,120,24,tw,0,hi,NULLPTR);g_minimizeTrayBox=CreateWindowExW(0,L"BUTTON",L"Minimize",WS_CHILD|WS_VISIBLE|BS_AUTOCHECKBOX,8,38,120,24,tw,0,hi,NULLPTR);g_keepTrayTaskbarBox=CreateWindowExW(0,L"BUTTON",L"Both",WS_CHILD|WS_VISIBLE|BS_AUTOCHECKBOX,8,68,120,24,tw,0,hi,NULLPTR);g_closeXTrayBox=CreateWindowExW(0,L"BUTTON",L"Close",WS_CHILD|WS_VISIBLE|BS_AUTOCHECKBOX,8,98,120,24,tw,0,hi,NULLPTR);g_startMinimizedBox=CreateWindowExW(0,L"BUTTON",L"StartMin",WS_CHILD|WS_VISIBLE|BS_AUTOCHECKBOX,8,128,120,24,tw,0,hi,NULLPTR);g_startPausedBox=CreateWindowExW(0,L"BUTTON",L"StartPause",WS_CHILD|WS_VISIBLE|BS_AUTOCHECKBOX,8,158,120,24,tw,0,hi,NULLPTR);g_notificationsBox=CreateWindowExW(0,L"BUTTON",L"Notify",WS_CHILD|WS_VISIBLE|BS_AUTOCHECKBOX,8,188,120,24,tw,0,hi,NULLPTR);}
 SelfTestProgress(rh,20,39,L"Settings/UI checkbox synchronization");
 t=tw&&ApplyMinimizeToTraySetting(TRUE,FALSE)&&SendMessageW(g_minimizeTrayBox,BM_GETCHECK,0,0)==BST_CHECKED&&ApplyKeepTrayTaskbarSetting(TRUE,FALSE,FALSE)&&SendMessageW(g_keepTrayTaskbarBox,BM_GETCHECK,0,0)==BST_CHECKED&&ApplyCloseXToTraySetting(TRUE,FALSE)&&SendMessageW(g_closeXTrayBox,BM_GETCHECK,0,0)==BST_CHECKED&&ApplyStartMinimizedSetting(TRUE,FALSE)&&SendMessageW(g_startMinimizedBox,BM_GETCHECK,0,0)==BST_CHECKED&&ApplyStartPausedSetting(TRUE,FALSE)&&SendMessageW(g_startPausedBox,BM_GETCHECK,0,0)==BST_CHECKED&&ApplyNotificationsSetting(FALSE,FALSE)&&SendMessageW(g_notificationsBox,BM_GETCHECK,0,0)==BST_UNCHECKED;ApplyPausedState(TRUE);t=t&&SendMessageW(g_pauseBox,BM_GETCHECK,0,0)==BST_CHECKED;ApplyPausedState(FALSE);SelfTestWrite(rh,t?L"PASS":L"FAIL",L"Settings <-> UI checkbox synchronization through production setters");if(t)pass++;else fail++;
 SelfTestProgress(rh,21,39,L"Reset Window Layout on primary monitor");
 if(tw){MoveWindow(tw,-6000,-6000,360,240,TRUE);RECT expected;PrimaryDefaultRect(&expected);ResetWindowLayout();RECT got;ZeroMem(&got,sizeof(got));GetWindowRect(tw,&got);t=got.left==expected.left&&got.top==expected.top&&(got.right-got.left)==(expected.right-expected.left)&&(got.bottom-got.top)==(expected.bottom-expected.top);}else t=FALSE;SelfTestWrite(rh,t?L"PASS":L"FAIL",L"Reset Window Layout moves actual window to OS primary-monitor work area");if(t)pass++;else fail++;
 SelfTestProgress(rh,22,39,L"taskbar-only / tray-only / both display modes");
 if(tw){ApplyKeepTrayTaskbarSetting(FALSE,FALSE,FALSE);MoveToTrayMode();t=g_trayOnly&&g_hiddenToTray&&g_trayVisible&&!IsWindowVisible(tw);MoveToTaskbarMode();t=t&&!g_trayOnly&&!g_hiddenToTray&&IsWindowVisible(tw)&&!g_trayVisible;ApplyKeepTrayTaskbarSetting(TRUE,FALSE,TRUE);t=t&&g_keepTrayTaskbar&&g_trayVisible&&IsWindowVisible(tw);ApplyKeepTrayTaskbarSetting(FALSE,FALSE,TRUE);}else t=FALSE;SelfTestWrite(rh,t?L"PASS":L"FAIL",L"taskbar-only / tray-only / taskbar+tray production display-mode behavior");if(t)pass++;else fail++;
 SelfTestProgress(rh,23,39,L"actual minimize-to-tray behavior");
 if(tw){ShowWindow(tw,SW_SHOW);g_hiddenToTray=FALSE;g_minimizeToTray=TRUE;MinimizeIntoTray();t=g_hiddenToTray&&g_trayVisible&&!IsWindowVisible(tw);RemoveTrayIcon();g_hiddenToTray=FALSE;ShowWindow(tw,SW_SHOW);}else t=FALSE;SelfTestWrite(rh,t?L"PASS":L"FAIL",L"actual minimize-to-tray hides isolated window and creates tray icon");if(t)pass++;else fail++;
 SelfTestProgress(rh,24,39,L"actual Close/X-to-tray behavior");
 if(tw){ShowWindow(tw,SW_SHOW);g_hiddenToTray=FALSE;g_closeXToTray=TRUE;HandleMainClose(tw);t=g_hiddenToTray&&g_trayVisible&&!IsWindowVisible(tw);RemoveTrayIcon();g_hiddenToTray=FALSE;ShowWindow(tw,SW_SHOW);g_closeXToTray=FALSE;}else t=FALSE;SelfTestWrite(rh,t?L"PASS":L"FAIL",L"actual Close/X-to-tray hides isolated window without terminating");if(t)pass++;else fail++;
 SelfTestProgress(rh,25,39,L"TaskbarCreated tray recovery handler");
 if(tw){g_trayOnly=TRUE;g_hiddenToTray=TRUE;AddTrayIcon();RemoveTrayIcon();MainWndProc(tw,g_taskbarCreatedMsg,0,0);t=g_trayVisible;RemoveTrayIcon();g_trayOnly=FALSE;g_hiddenToTray=FALSE;}else t=FALSE;SelfTestWrite(rh,t?L"PASS":L"FAIL",L"TaskbarCreated recovery handler re-adds actual tray icon without killing Explorer");if(t)pass++;else fail++;
 SelfTestProgress(rh,26,39,L"main and tray Safe Self-Test command equivalence");
 if(tw){g_selfTestLaunchIntercept=TRUE;g_selfTestLaunchInterceptCount=0;MainWndProc(tw,WM_COMMAND,(WPARAM)IDC_SAFE_SELF_TEST,0);HandleTrayCommand(tw,CMD_SAFE_SELF_TEST);t=g_selfTestLaunchInterceptCount==2;g_selfTestLaunchIntercept=FALSE;}else t=FALSE;SelfTestWrite(rh,t?L"PASS":L"FAIL",L"main-window and tray Safe Self-Test commands reach the same production launcher");if(t)pass++;else fail++;
 SelfTestProgress(rh,27,39,L"guarded physical Explorer/taskbar restart + tray recovery");
 int explorerResult=-1;if(tw){g_trayOnly=TRUE;g_hiddenToTray=TRUE;AddTrayIcon();explorerResult=RestartExplorerAndVerifyTrayRecovery(tw);RemoveTrayIcon();g_trayOnly=FALSE;g_hiddenToTray=FALSE;}if(explorerResult>0){SelfTestWrite(rh,L"PASS",L"physical Explorer.exe/taskbar restart completed and TaskbarCreated restored the isolated tray icon");pass++;}else if(explorerResult<0){SelfTestWrite(rh,L"SKIPPED",L"physical Explorer.exe/taskbar restart could not be started safely in this Windows session");skipped++;}else{SelfTestWrite(rh,L"FAIL",L"physical Explorer.exe/taskbar restart did not restore the isolated tray icon within the recovery timeout");fail++;}
 if(tw){RemoveTrayIcon();DestroyWindow(tw);}g_hwnd=0;g_pauseBox=0;g_minimizeTrayBox=0;g_keepTrayTaskbarBox=0;g_closeXTrayBox=0;g_startMinimizedBox=0;g_startPausedBox=0;g_notificationsBox=0;if(g_appIcon){DestroyIcon(g_appIcon);g_appIcon=0;}

 SelfTestProgress(rh,28,39,L"Start with Windows isolated registry engine");
 WCHAR sq[MAX_PATH*2+64];ZeroMem(sq,sizeof(sq));t=SetStartupNamedValue(L"Crash Monitor Safe Self-Test",g_exePath,TRUE)&&QueryStartupNamedValue(L"Crash Monitor Safe Self-Test",sq,MAX_PATH*2+64);WCHAR expectedQ[MAX_PATH*2+32];lstrcpyW(expectedQ,L"\"");lstrcatW(expectedQ,g_exePath);lstrcatW(expectedQ,L"\"");t=t&&lstrcmpiW(sq,expectedQ)==0&&SetStartupNamedValue(L"Crash Monitor Safe Self-Test",g_exePath,FALSE)&&!QueryStartupNamedValue(L"Crash Monitor Safe Self-Test",sq,MAX_PATH*2+64);SelfTestWrite(rh,t?L"PASS":L"FAIL",L"Start with Windows registry engine write/read/delete using isolated test value");if(t)pass++;else fail++;
 SelfTestProgress(rh,29,39,L"shortcut creation engine");
 WCHAR slink[MAX_PATH*2];lstrcpyW(slink,root);lstrcatW(slink,L"\\Crash Monitor Safe Self-Test.lnk");t=pathOk&&CreateShortcutFileToTarget(slink,g_exePath,root)&&FileExists(slink);DeleteFileW(slink);SelfTestWrite(rh,t?L"PASS":L"FAIL",L"Start Menu/Desktop shortcut creation engine using isolated .lnk path");if(t)pass++;else fail++;
 SelfTestProgress(rh,30,39,L"actual user-visible Start Menu shortcut launch");
 WCHAR programsDir[MAX_PATH*2];ZeroMem(programsDir,sizeof(programsDir));WCHAR liveLink[MAX_PATH*2];ZeroMem(liveLink,sizeof(liveLink));WCHAR shortcutMarker[MAX_PATH*2];ZeroMem(shortcutMarker,sizeof(shortcutMarker));WCHAR shortcutArgs[MAX_PATH*2+96];ZeroMem(shortcutArgs,sizeof(shortcutArgs));BOOL shortcutLaunchOk=SHGetFolderPathW(0,CSIDL_PROGRAMS,0,SHGFP_TYPE_CURRENT,programsDir)>=0;if(shortcutLaunchOk){wsprintfW(liveLink,L"%s\\Crash Monitor Safe Self-Test %u.lnk",programsDir,GetCurrentProcessId());wsprintfW(shortcutMarker,L"%s\\ShortcutLaunch-%u.flag",root,GetCurrentProcessId());DeleteFileW(shortcutMarker);DeleteFileW(liveLink);lstrcpyW(shortcutArgs,L"--selftest-shortcut-marker=\"");lstrcatW(shortcutArgs,shortcutMarker);lstrcatW(shortcutArgs,L"\"");shortcutLaunchOk=CreateShortcutFileToTargetArgs(liveLink,g_exePath,root,shortcutArgs)&&FileExists(liveLink);if(shortcutLaunchOk){HINSTANCE sh=ShellExecuteW(0,L"open",liveLink,0,programsDir,SW_SHOWNORMAL);shortcutLaunchOk=(ULONG_PTR)sh>32&&WaitForSelfTestMarker(shortcutMarker,5000);}}DeleteFileW(shortcutMarker);DeleteFileW(liveLink);SelfTestWrite(rh,shortcutLaunchOk?L"PASS":L"FAIL",L"actual temporary Start Menu shortcut launched an isolated Crash Monitor helper through Windows Shell");if(shortcutLaunchOk)pass++;else fail++;
 SelfTestProgress(rh,31,39,L"WER isolated registry engine");
 LPCWSTR werTestKey=L"Software\\CrashMonitor\\SafeSelfTest\\WER\\SelfTest.exe";t=pathOk&&RegisterWerAt(HKEY_CURRENT_USER,werTestKey,g_dumpRoot)&&IsWerConfiguredAt(HKEY_CURRENT_USER,werTestKey,g_dumpRoot)&&UnregisterWerAt(HKEY_CURRENT_USER,werTestKey);HKEY wh=0;t=t&&(RegOpenKeyExW(HKEY_CURRENT_USER,werTestKey,0,KEY_QUERY_VALUE,&wh)!=ERROR_SUCCESS);if(wh)RegCloseKey(wh);RegDeleteTreeW(HKEY_CURRENT_USER,L"Software\\CrashMonitor\\SafeSelfTest");SelfTestWrite(rh,t?L"PASS":L"FAIL",L"WER LocalDumps registry payload engine write/read/remove using isolated HKCU test key");if(t)pass++;else fail++;
 SelfTestProgress(rh,32,39,L"diagnostic report writer");
 WCHAR diag[MAX_PATH*2];lstrcpyW(diag,root);lstrcatW(diag,L"\\CrashMonitor-Diagnostic-SafeSelfTest.txt");t=pathOk&&WriteDiagnosticReportFile(diag)&&FileExists(diag)&&FileSize64(diag)>0;DeleteFileW(diag);SelfTestWrite(rh,t?L"PASS":L"FAIL",L"Export Diagnostic Report production writer creates project-local report");if(t)pass++;else fail++;

 SelfTestProgress(rh,33,39,L"isolated helper TEST full dump + ZIP verification");
 t=pathOk&&SelfTestCreateDumpKind(L"CrashMonitorSafeSelfTest.exe",L"TEST");SelfTestWrite(rh,t?L"PASS":L"FAIL",L"real TEST full dump against isolated helper process + lossless ZIP verification");if(t)pass++;else fail++;
 SelfTestProgress(rh,34,39,L"isolated helper PRECRASH dump + ZIP verification");
 t=pathOk&&SelfTestCreateDumpKind(L"CrashMonitorSafeSelfTest.exe",L"PRECRASH");SelfTestWrite(rh,t?L"PASS":L"FAIL",L"real PRECRASH handle-focused dump against isolated helper process + ZIP verification");if(t)pass++;else fail++;
 SelfTestProgress(rh,35,39,L"isolated helper CRASH full dump + ZIP verification");
 t=pathOk&&SelfTestCreateDumpKind(L"CrashMonitorSafeSelfTest.exe",L"CRASH");SelfTestWrite(rh,t?L"PASS":L"FAIL",L"real CRASH full dump against isolated helper process + lossless ZIP verification");if(t)pass++;else fail++;
 SelfTestProgress(rh,36,39,L"isolated helper EXITCRASH full dump + ZIP verification");
 t=pathOk&&SelfTestCreateDumpKind(L"CrashMonitorSafeSelfTest.exe",L"EXITCRASH");SelfTestWrite(rh,t?L"PASS":L"FAIL",L"real EXITCRASH full dump against isolated helper process + lossless ZIP verification");if(t)pass++;else fail++;
 SelfTestProgress(rh,37,39,L"isolated helper OBS PSS snapshot / VA-clone TEST dump + ZIP verification");
 t=pathOk&&SelfTestCreateDumpKind(L"obs64.exe",L"TEST");SelfTestWrite(rh,t?L"PASS":L"FAIL",L"OBS enhanced PSS snapshot / VA-clone TEST dump path against isolated helper process + ZIP verification");if(t)pass++;else fail++;
 SelfTestProgress(rh,38,39,L"forced archive splitting + reassembly regression (Build 9 boundary rollover)");
 WCHAR splitFile[MAX_PATH*2];lstrcpyW(splitFile,g_dumpRoot);lstrcatW(splitFile,L"\\SafeSelfTest-forced-split.zip");HANDLE sf=CreateFileW(splitFile,GENERIC_WRITE,FILE_SHARE_READ,NULLPTR,CREATE_ALWAYS,FILE_ATTRIBUTE_NORMAL,0);BOOL sourceOk=FALSE;if(sf!=INVALID_HANDLE_VALUE){BYTE seed[8192];for(int i=0;i<(int)sizeof(seed);i++)seed[i]=(BYTE)(i&0xFF);DWORD sw=0;sourceOk=WriteFile(sf,seed,sizeof(seed),&sw,NULLPTR)&&sw==sizeof(seed);CloseHandle(sf);}int parts=0;t=sourceOk&&FileExists(splitFile)&&SplitArchiveForLimit(splitFile,2048ULL,&parts)&&parts==4;ULONGLONG verifyOffset=0;BYTE verifyBuf[512];for(int i=1;i<=4&&t;i++){WCHAR pn[MAX_PATH*2];wsprintfW(pn,L"%s.%03u",splitFile,(UINT)i);t=t&&FileExists(pn)&&FileSize64(pn)==2048ULL;if(t){HANDLE ph=CreateFileW(pn,GENERIC_READ,FILE_SHARE_READ,NULLPTR,OPEN_EXISTING,FILE_ATTRIBUTE_NORMAL,0);if(ph==INVALID_HANDLE_VALUE)t=FALSE;else{DWORD rg=0;while(t&&ReadFile(ph,verifyBuf,sizeof(verifyBuf),&rg,NULLPTR)&&rg>0){for(DWORD j=0;j<rg;j++)if(verifyBuf[j]!=(BYTE)((verifyOffset+j)&0xFF)){t=FALSE;break;}verifyOffset+=rg;}CloseHandle(ph);}}}WCHAR p5[MAX_PATH*2];wsprintfW(p5,L"%s.%03u",splitFile,5u);t=t&&verifyOffset==8192ULL&&!FileExists(p5);WCHAR rs[MAX_PATH*2];lstrcpyW(rs,splitFile);lstrcatW(rs,L".REASSEMBLE.cmd");t=t&&FileExists(rs);SelfTestWrite(rh,t?L"PASS":L"FAIL",L"forced archive splitting crosses part boundaries safely, preserves byte order, creates exactly four deterministic parts, and writes reassembly script");if(t)pass++;else fail++;
 SelfTestProgress(rh,39,39,L"isolated Update/Repair image replacement + user-data preservation");
 WCHAR updRoot[MAX_PATH*2],updPrograms[MAX_PATH*2],updInstall[MAX_PATH*2],updExe[MAX_PATH*2],updData[MAX_PATH*2],updIni[MAX_PATH*2],updDump[MAX_PATH*2];lstrcpyW(updRoot,root);lstrcatW(updRoot,L"\\UpdateRepair");EnsureDir(updRoot);lstrcpyW(updPrograms,updRoot);lstrcatW(updPrograms,L"\\Programs");EnsureDir(updPrograms);lstrcpyW(updInstall,updPrograms);lstrcatW(updInstall,L"\\Crash Monitor");EnsureDir(updInstall);lstrcpyW(updExe,updInstall);lstrcatW(updExe,L"\\Crash Monitor.exe");lstrcpyW(updData,updRoot);lstrcatW(updData,L"\\Data");EnsureDir(updData);lstrcpyW(updIni,updData);lstrcatW(updIni,L"\\targets.ini");lstrcpyW(updDump,updData);lstrcatW(updDump,L"\\preserve.dmp");HANDLE oldExe=CreateFileW(updExe,GENERIC_WRITE,FILE_SHARE_READ,NULLPTR,CREATE_ALWAYS,FILE_ATTRIBUTE_NORMAL,0);BOOL oldOk=FALSE;if(oldExe!=INVALID_HANDLE_VALUE){BYTE oldBytes[64];for(int oi=0;oi<64;oi++)oldBytes[oi]=(BYTE)(0xA0u+(oi&0x0Fu));DWORD ow=0;oldOk=WriteFile(oldExe,oldBytes,sizeof(oldBytes),&ow,NULLPTR)&&ow==sizeof(oldBytes);CloseHandle(oldExe);}BOOL iniOk=WritePrivateProfileStringW(L"SelfTest",L"Preserve",L"Build10UserData",updIni);HANDLE dh=CreateFileW(updDump,GENERIC_WRITE,FILE_SHARE_READ,NULLPTR,CREATE_ALWAYS,FILE_ATTRIBUTE_NORMAL,0);BOOL dumpOk=FALSE;if(dh!=INVALID_HANDLE_VALUE){BYTE db[128];for(int di=0;di<128;di++)db[di]=(BYTE)(di^0x5A);DWORD dw=0;dumpOk=WriteFile(dh,db,sizeof(db),&dw,NULLPTR)&&dw==sizeof(db);CloseHandle(dh);}ULONGLONG currentExeSize=FileSize64(g_exePath);BOOL updateOk=oldOk&&iniOk&&dumpOk&&currentExeSize>0&&CopyInstallImageForUpdate(g_exePath,updExe)&&FileSize64(updExe)==currentExeSize;WCHAR preserve[64];ZeroMem(preserve,sizeof(preserve));GetPrivateProfileStringW(L"SelfTest",L"Preserve",L"",preserve,64,updIni);updateOk=updateOk&&lstrcmpiW(preserve,L"Build10UserData")==0&&FileExists(updDump)&&FileSize64(updDump)==128ULL;SelfTestWrite(rh,updateOk?L"PASS":L"FAIL",L"production Update/Repair image-replacement helper overwrites staged old app bytes while preserving isolated settings and dump data");if(updateOk)pass++;else fail++;

 AppendUtf8(rh,L"RUNNING 39/39 - cleanup and final report\r\n");FlushFileBuffers(rh);WriteSelfTestProgressSnapshot(L"RUNNING 39/39 - cleanup and final report\r\n");
 if(root[0])RemoveTree(root);
 AppendUtf8(rh,L"\r\nNOT TESTED - actual Windows sign-out/reboot proving Start with Windows launches at sign-in (registration/command engine is automated)\r\nNOT TESTED - asynchronous Windows Search indexing/discovery timing (actual Start Menu shortcut creation + launch is automated)\r\nNOT TESTED - real HKLM WER enable/disable UAC elevation approval flow (isolated registry engine is automated)\r\nNOT TESTED - Bitdefender/SmartScreen reputation result\r\n\r\n");WCHAR sum[192];wsprintfW(sum,L"RUNTIME SAFE SELF-TEST TOTALS: PASS=%d FAIL=%d SKIPPED=%d NOT_TESTED=4\r\n",pass,fail,skipped);AppendUtf8(rh,sum);AppendUtf8(rh,L"SAFE SELF-TEST FINISHED\r\n");FlushFileBuffers(rh);CloseHandle(rh);return fail?1:0;
}

static int FindTargetByPath(LPCWSTR path){int found=-1;AcquireSRWLockShared(&g_lock);for(int i=0;i<g_targetCount;i++){if(g_targets[i].fullPath[0]&&lstrcmpiW(g_targets[i].fullPath,path)==0){found=i;break;}}ReleaseSRWLockShared(&g_lock);return found;}
static BOOL RunElevatedSetOne(LPCWSTR exe,BOOL enable);
static void SetTargetEnabled(int i,BOOL enabled){AcquireSRWLockExclusive(&g_lock);if(i>=0&&i<g_targetCount){g_targets[i].enabled=enabled;SaveTargetsLocked();g_reconfigure=1;}ReleaseSRWLockExclusive(&g_lock);}
static void ToggleTargetWithWer(int i){WCHAR exe[MAX_PATH];exe[0]=0;BOOL newState=FALSE;AcquireSRWLockShared(&g_lock);if(i>=0&&i<g_targetCount){CopyWide(exe,MAX_PATH,g_targets[i].exeName);newState=!g_targets[i].enabled;}ReleaseSRWLockShared(&g_lock);if(!exe[0])return;if(!RunElevatedSetOne(exe,newState))return;SetTargetEnabled(i,newState);WCHAR line[512];wsprintfW(line,L"PROGRAM %s changed to %s; Windows crash dump registration update launched",exe,newState?L"ON":L"OFF");AppendLog(line);}
static void RemoveTarget(int i,WCHAR*outName){if(outName)outName[0]=0;AcquireSRWLockExclusive(&g_lock);if(i>=0&&i<g_targetCount){if(outName)CopyWide(outName,MAX_PATH,g_targets[i].exeName);for(int j=i;j<g_targetCount-1;j++)g_targets[j]=g_targets[j+1];g_targetCount--;SaveTargetsLocked();g_reconfigure=1;}ReleaseSRWLockExclusive(&g_lock);}
static BOOL AddProgramDialog(HWND owner,WCHAR*outPath,int cap){if(outPath&&cap>0)outPath[0]=0;WCHAR f[MAX_PATH*2];ZeroMem(f,sizeof(f));static const WCHAR filter[]=L"Programs (*.exe)\0*.exe\0All files (*.*)\0*.*\0\0";OPENFILENAMEW o;ZeroMem(&o,sizeof(o));o.lStructSize=sizeof(o);o.hwndOwner=owner;o.lpstrFilter=filter;o.lpstrFile=f;o.nMaxFile=MAX_PATH*2;o.lpstrTitle=L"Choose a program to monitor";o.Flags=OFN_EXPLORER|OFN_FILEMUSTEXIST|OFN_PATHMUSTEXIST|OFN_NOCHANGEDIR;if(!GetOpenFileNameW(&o))return FALSE;if(!AddTargetPath(f))return FALSE;if(outPath&&cap>0)CopyWide(outPath,cap,f);return TRUE;}

static void WerKeyPath(LPCWSTR exe,WCHAR*out){lstrcpyW(out,L"SOFTWARE\\Microsoft\\Windows\\Windows Error Reporting\\LocalDumps\\");lstrcatW(out,exe);}
static BOOL IsWerConfiguredAt(HKEY root,LPCWSTR key,LPCWSTR dumpRoot){HKEY h=0;if(RegOpenKeyExW(root,key,0,KEY_QUERY_VALUE,&h)!=ERROR_SUCCESS)return FALSE;DWORD ty=0,v=0,sz=sizeof(v);BOOL ok=RegQueryValueExW(h,L"DumpType",0,&ty,(BYTE*)&v,&sz)==ERROR_SUCCESS&&ty==REG_DWORD&&v==2;WCHAR folder[MAX_PATH*2];ZeroMem(folder,sizeof(folder));DWORD fty=0,fsz=sizeof(folder);if(ok)ok=RegQueryValueExW(h,L"DumpFolder",0,&fty,(BYTE*)folder,&fsz)==ERROR_SUCCESS&&(fty==REG_SZ||fty==REG_EXPAND_SZ)&&lstrcmpiW(folder,dumpRoot)==0;RegCloseKey(h);return ok;}
static BOOL RegisterWerAt(HKEY root,LPCWSTR key,LPCWSTR dumpRoot){HKEY h=0;DWORD disp=0;LONG r=RegCreateKeyExW(root,key,0,0,0,KEY_WRITE,NULLPTR,&h,&disp);if(r!=ERROR_SUCCESS)return FALSE;DWORD type=2,count=10,marker=1;r=RegSetValueExW(h,L"DumpFolder",0,REG_EXPAND_SZ,(BYTE*)dumpRoot,(DWORD)((lstrlenW(dumpRoot)+1)*sizeof(WCHAR)));if(r==ERROR_SUCCESS)r=RegSetValueExW(h,L"DumpType",0,REG_DWORD,(BYTE*)&type,sizeof(type));if(r==ERROR_SUCCESS)r=RegSetValueExW(h,L"DumpCount",0,REG_DWORD,(BYTE*)&count,sizeof(count));if(r==ERROR_SUCCESS)r=RegSetValueExW(h,L"CrashMonitor",0,REG_DWORD,(BYTE*)&marker,sizeof(marker));RegCloseKey(h);return r==ERROR_SUCCESS;}
static BOOL UnregisterWerAt(HKEY root,LPCWSTR key){HKEY h=0;if(RegOpenKeyExW(root,key,0,KEY_QUERY_VALUE,&h)!=ERROR_SUCCESS)return TRUE;DWORD ty=0,v=0,sz=sizeof(v);BOOL ours=RegQueryValueExW(h,L"CrashMonitor",0,&ty,(BYTE*)&v,&sz)==ERROR_SUCCESS&&ty==REG_DWORD&&v==1;if(!ours){ty=0;v=0;sz=sizeof(v);ours=RegQueryValueExW(h,L"CrashMonitorAVSafe",0,&ty,(BYTE*)&v,&sz)==ERROR_SUCCESS&&ty==REG_DWORD&&v==1;}RegCloseKey(h);if(!ours)return TRUE;LONG r=RegDeleteTreeW(root,key);return r==ERROR_SUCCESS||r==ERROR_FILE_NOT_FOUND;}
static BOOL IsWerConfigured(LPCWSTR exe){WCHAR p[768];WerKeyPath(exe,p);return IsWerConfiguredAt(HKEY_LOCAL_MACHINE,p,g_dumpRoot);}
static BOOL RegisterWerOne(LPCWSTR exe){WCHAR p[768];WerKeyPath(exe,p);return RegisterWerAt(HKEY_LOCAL_MACHINE,p,g_dumpRoot);}
static BOOL UnregisterWerOne(LPCWSTR exe){WCHAR p[768];WerKeyPath(exe,p);return UnregisterWerAt(HKEY_LOCAL_MACHINE,p);}
static BOOL CommandHas(LPCWSTR needle){LPCWSTR c=GetCommandLineW();if(!c||!needle)return FALSE;int n=lstrlenW(needle);for(;*c;c++){int i=0;while(i<n&&c[i]&&c[i]==needle[i])i++;if(i==n)return TRUE;}return FALSE;}
static BOOL CommandValue(LPCWSTR key,WCHAR*out,int cap){out[0]=0;LPCWSTR c=GetCommandLineW();int n=lstrlenW(key);for(;c&&*c;c++){int i=0;while(i<n&&c[i]&&c[i]==key[i])i++;if(i==n){LPCWSTR p=c+n;BOOL quoted=FALSE;if(*p==L'\"'){quoted=TRUE;p++;}int j=0;while(*p&&j<cap-1){if(quoted&&*p==L'\"')break;if(!quoted&&(*p==L' '||*p==L'\t'))break;out[j++]=*p++;}out[j]=0;return j>0;}}return FALSE;}
static void RunElevatedHelper(BOOL enable){LPCWSTR arg=enable?L"--wer-enable-all":L"--wer-disable-all";HINSTANCE r=ShellExecuteW(g_hwnd,L"runas",g_installExe,arg,0,SW_HIDE);if((ULONG_PTR)r<=32)MessageBoxW(g_hwnd,L"Windows did not allow the administrator step. Crash dump settings were not changed.",L"Crash Monitor",MB_OK|MB_ICONERROR);}
static BOOL RunElevatedSetOne(LPCWSTR exe,BOOL enable){WCHAR arg[512];lstrcpyW(arg,enable?L"--wer-enable-one=\"":L"--wer-remove-one=\"");lstrcatW(arg,exe);lstrcatW(arg,L"\"");HINSTANCE r=ShellExecuteW(g_hwnd,L"runas",g_installExe,arg,0,SW_HIDE);if((ULONG_PTR)r<=32){MessageBoxW(g_hwnd,enable?L"Windows did not allow the administrator step, so the program stayed OFF.":L"Windows did not allow the administrator step, so the program stayed ON.",L"Crash Monitor",MB_OK|MB_ICONWARNING);return FALSE;}return TRUE;}
static void RunElevatedRemoveOne(LPCWSTR exe){RunElevatedSetOne(exe,FALSE);}
static void DoWerOne(LPCWSTR exe,BOOL enable){BOOL ok=enable?RegisterWerOne(exe):UnregisterWerOne(exe);WCHAR line[512];wsprintfW(line,L"WER %s %s: %s",enable?L"enable":L"disable",exe,ok?L"success":L"FAILED");AppendLog(line);if(!ok)MessageBoxW(0,enable?L"Windows could not enable crash dumps for that program. Use Enable / Repair Crash Dumps and try again.":L"Windows could not remove Crash Monitor crash dumps for that program. Its OFF setting may not be complete.",L"Crash Monitor",MB_OK|MB_ICONERROR);}
static void DoWerHelper(BOOL enable){int ok=0,fail=0;AcquireSRWLockShared(&g_lock);for(int i=0;i<g_targetCount;i++){BOOL r;if(enable)r=g_targets[i].enabled?RegisterWerOne(g_targets[i].exeName):UnregisterWerOne(g_targets[i].exeName);else r=UnregisterWerOne(g_targets[i].exeName);if(r)ok++;else fail++;}ReleaseSRWLockShared(&g_lock);WCHAR msg[512];if(enable)wsprintfW(msg,L"Windows crash dumps enabled/repaired for configured programs.\n\nSuccessful: %d\nFailed: %d\n\nDump folder:\n%s",ok,fail,g_dumpRoot);else wsprintfW(msg,L"Crash Monitor's Windows dump registrations were removed.\n\nSuccessful: %d\nFailed: %d",ok,fail);MessageBoxW(0,msg,L"Crash Monitor",fail?MB_ICONWARNING|MB_OK:MB_ICONINFORMATION|MB_OK);}

static ULONGLONG ScanNewestDump(WCHAR*outName){WCHAR mask[MAX_PATH*2];lstrcpyW(mask,g_dumpRoot);lstrcatW(mask,L"\\*.dmp");WIN32_FIND_DATAW f;ZeroMem(&f,sizeof(f));HANDLE h=FindFirstFileW(mask,&f);ULONGLONG best=0;outName[0]=0;if(h==INVALID_HANDLE_VALUE)return 0;do{if(!(f.dwFileAttributes&FILE_ATTRIBUTE_DIRECTORY)){ULONGLONG t=FtValue(f.ftLastWriteTime);if(t>=best){best=t;CopyWide(outName,MAX_PATH*2,f.cFileName);}}}while(FindNextFileW(h,&f));FindClose(h);return best;}
static BOOL CopyNewest(LPCWSTR dir,LPCWSTR pattern,LPCWSTR dst){WCHAR mask[MAX_PATH*2];lstrcpyW(mask,dir);lstrcatW(mask,L"\\");lstrcatW(mask,pattern);WIN32_FIND_DATAW f;HANDLE h=FindFirstFileW(mask,&f);if(h==INVALID_HANDLE_VALUE)return FALSE;ULONGLONG best=0;WCHAR n[MAX_PATH];n[0]=0;do{if(!(f.dwFileAttributes&FILE_ATTRIBUTE_DIRECTORY)){ULONGLONG t=FtValue(f.ftLastWriteTime);if(t>=best){best=t;CopyWide(n,MAX_PATH,f.cFileName);}}}while(FindNextFileW(h,&f));FindClose(h);if(!n[0])return FALSE;WCHAR src[MAX_PATH*2];lstrcpyW(src,dir);lstrcatW(src,L"\\");lstrcatW(src,n);return CopyFileW(src,dst,FALSE);}
static void CopyObsLog(){WCHAR app[MAX_PATH*2];app[0]=0;if(!GetEnvironmentVariableW(L"APPDATA",app,MAX_PATH*2))return;WCHAR logs[MAX_PATH*2];lstrcpyW(logs,app);lstrcatW(logs,L"\\obs-studio\\logs");SYSTEMTIME st;GetLocalTime(&st);WCHAR dst[MAX_PATH*2];wsprintfW(dst,L"%s\\OBS-log-%04u%02u%02u-%02u%02u%02u.txt",g_dumpRoot,st.wYear,st.wMonth,st.wDay,st.wHour,st.wMinute,st.wSecond);CopyNewest(logs,L"*.txt",dst);}
static ULONGLONG FileSize64(LPCWSTR path){WIN32_FIND_DATAW f;ZeroMem(&f,sizeof(f));HANDLE h=FindFirstFileW(path,&f);if(h==INVALID_HANDLE_VALUE)return 0;FindClose(h);return ((ULONGLONG)f.nFileSizeHigh<<32)|f.nFileSizeLow;}
static void ReplaceDmpWithZip(LPCWSTR dmp,WCHAR*out,int cap){CopyWide(out,cap,dmp);int n=lstrlenW(out);if(n>=4&&out[n-4]==L'.'&&(out[n-3]==L'd'||out[n-3]==L'D')&&(out[n-2]==L'm'||out[n-2]==L'M')&&(out[n-1]==L'p'||out[n-1]==L'P')){out[n-3]=L'z';out[n-2]=L'i';out[n-1]=L'p';}else if(n+4<cap)lstrcatW(out,L".zip");}
static BOOL RunArchiveCommand(LPCWSTR tarPath,LPCWSTR args,DWORD*outExit){if(outExit)*outExit=0xFFFFFFFFu;WCHAR cmd[4096];lstrcpyW(cmd,L"\"");lstrcatW(cmd,tarPath);lstrcatW(cmd,L"\" ");lstrcatW(cmd,args);STARTUPINFOW_NATIVE si;PROCESS_INFORMATION_NATIVE pi;ZeroMem(&si,sizeof(si));ZeroMem(&pi,sizeof(pi));si.cb=sizeof(si);if(!CreateProcessW(tarPath,cmd,NULLPTR,NULLPTR,FALSE,CREATE_NO_WINDOW,NULLPTR,g_dumpRoot,&si,&pi))return FALSE;DWORD wr=WaitForSingleObject(pi.hProcess,ARCHIVE_TOOL_TIMEOUT_MS);DWORD ec=0xFFFFFFFFu;if(wr==WAIT_TIMEOUT){TerminateProcess(pi.hProcess,WAIT_TIMEOUT);WaitForSingleObject(pi.hProcess,2000);ec=WAIT_TIMEOUT;}else if(wr==WAIT_OBJECT_0)GetExitCodeProcess(pi.hProcess,&ec);CloseHandle(pi.hThread);CloseHandle(pi.hProcess);if(outExit)*outExit=ec;return ec==0;}
static BOOL VerifyArchive(LPCWSTR tarPath,LPCWSTR zip){WCHAR args[1600];lstrcpyW(args,L"-tf \"");lstrcatW(args,zip);lstrcatW(args,L"\"");DWORD ec=0;return RunArchiveCommand(tarPath,args,&ec)&&ec==0;}
static BOOL WriteReassembleScript(LPCWSTR zip,int parts){WCHAR script[MAX_PATH*2];lstrcpyW(script,zip);lstrcatW(script,L".REASSEMBLE.cmd");HANDLE h=CreateFileW(script,GENERIC_WRITE,FILE_SHARE_READ,NULLPTR,CREATE_ALWAYS,FILE_ATTRIBUTE_NORMAL,0);if(h==INVALID_HANDLE_VALUE)return FALSE;AppendUtf8(h,L"@echo off\r\nsetlocal\r\ncd /d \"%~dp0\"\r\n");WCHAR line[16384];lstrcpyW(line,L"copy /b ");LPCWSTR base=BaseNamePtr(zip);for(int i=1;i<=parts;i++){WCHAR one[1024];wsprintfW(one,L"\"%s.%03u\"",base,(UINT)i);if(i>1)lstrcatW(line,L"+");lstrcatW(line,one);}lstrcatW(line,L" \"");lstrcatW(line,base);lstrcatW(line,L"\" >nul\r\n");AppendUtf8(h,line);AppendUtf8(h,L"if errorlevel 1 (\r\n  echo Reassembly failed. Make sure every numbered part is in this folder.\r\n  pause\r\n  exit /b 1\r\n)\r\necho Rebuilt the full archive successfully.\r\necho Extract the ZIP normally to get the original full .dmp file.\r\npause\r\n");CloseHandle(h);return TRUE;}
static BOOL SplitArchiveForLimit(LPCWSTR zip,ULONGLONG partLimit,int*outParts){if(outParts)*outParts=0;ULONGLONG size=FileSize64(zip);if(size==0||partLimit==0)return FALSE;if(size<=partLimit){if(outParts)*outParts=1;return TRUE;}HANDLE in=CreateFileW(zip,GENERIC_READ,FILE_SHARE_READ,NULLPTR,OPEN_EXISTING,FILE_ATTRIBUTE_NORMAL,0);if(in==INVALID_HANDLE_VALUE)return FALSE;BYTE* buf=(BYTE*)VirtualAlloc(NULLPTR,SPLIT_IO_BUFFER_BYTES,MEM_RESERVE|MEM_COMMIT,PAGE_READWRITE);if(!buf){CloseHandle(in);return FALSE;}DWORD got=0;int nextPart=1,completedParts=0;HANDLE out=INVALID_HANDLE_VALUE;ULONGLONG partBytes=0;BOOL ok=TRUE;while(TRUE){if(!ReadFile(in,buf,SPLIT_IO_BUFFER_BYTES,&got,NULLPTR)){ok=FALSE;break;}if(got==0)break;DWORD off=0;while(off<got){if(out==INVALID_HANDLE_VALUE){WCHAR pn[MAX_PATH*2];wsprintfW(pn,L"%s.%03u",zip,(UINT)nextPart);out=CreateFileW(pn,GENERIC_WRITE,FILE_SHARE_READ,NULLPTR,CREATE_ALWAYS,FILE_ATTRIBUTE_NORMAL,0);if(out==INVALID_HANDLE_VALUE){ok=FALSE;break;}partBytes=0;}ULONGLONG room=partLimit-partBytes;if(room==0){ok=FALSE;break;}DWORD n=(DWORD)(((ULONGLONG)(got-off)<room)?(got-off):room);if(n==0){ok=FALSE;break;}DWORD wrote=0;if(!WriteFile(out,buf+off,n,&wrote,NULLPTR)||wrote!=n){ok=FALSE;break;}off+=n;partBytes+=n;if(partBytes==partLimit){FlushFileBuffers(out);CloseHandle(out);out=INVALID_HANDLE_VALUE;completedParts++;nextPart++;}}if(!ok)break;}if(out!=INVALID_HANDLE_VALUE){FlushFileBuffers(out);CloseHandle(out);out=INVALID_HANDLE_VALUE;if(partBytes>0)completedParts++;}CloseHandle(in);VirtualFree(buf,0,MEM_RELEASE);if(!ok||completedParts<1)return FALSE;if(!WriteReassembleScript(zip,completedParts))return FALSE;if(outParts)*outParts=completedParts;return TRUE;}
static BOOL SplitArchiveForDiscord(LPCWSTR zip,int*outParts){return SplitArchiveForLimit(zip,DISCORD_PART_BYTES,outParts);}
static BOOL CompressDumpForSharing(LPCWSTR dmp,WCHAR*outDisplay,int displayCap){g_lastShareCompressed=0;g_lastShareParts=0;if(outDisplay)CopyWide(outDisplay,displayCap,BaseNamePtr(dmp));ULONGLONG original=FileSize64(dmp);if(!original)return FALSE;WCHAR root[MAX_PATH*2];if(!GetEnvironmentVariableW(L"SystemRoot",root,MAX_PATH*2))lstrcpyW(root,L"C:\\Windows");WCHAR tar[MAX_PATH*2];lstrcpyW(tar,root);lstrcatW(tar,L"\\System32\\tar.exe");if(!FileExists(tar)){AppendLog(L"SHARE ZIP skipped: Windows tar.exe was not found; original .dmp kept");return FALSE;}WCHAR zip[MAX_PATH*2];ReplaceDmpWithZip(dmp,zip,MAX_PATH*2);DeleteFileW(zip);WCHAR args[2400];lstrcpyW(args,L"-caf \"");lstrcatW(args,zip);lstrcatW(args,L"\" -C \"");lstrcatW(args,g_dumpRoot);lstrcatW(args,L"\" \"");lstrcatW(args,BaseNamePtr(dmp));lstrcatW(args,L"\"");DWORD ec=0;if(!RunArchiveCommand(tar,args,&ec)||!FileExists(zip)||FileSize64(zip)==0){WCHAR line[512];wsprintfW(line,L"SHARE ZIP FAILED tar exit=%u; original .dmp kept",ec);AppendLog(line);DeleteFileW(zip);return FALSE;}if(!VerifyArchive(tar,zip)){AppendLog(L"SHARE ZIP verification FAILED; archive removed and original .dmp kept");DeleteFileW(zip);return FALSE;}ULONGLONG packed=FileSize64(zip);int parts=1;if(packed>DISCORD_PART_BYTES){if(!SplitArchiveForDiscord(zip,&parts)){AppendLog(L"SHARE ZIP split FAILED; verified ZIP and original .dmp kept");return FALSE;}DeleteFileW(zip);WCHAR first[MAX_PATH*2];wsprintfW(first,L"%s.%03u",zip,1u);if(outDisplay)CopyWide(outDisplay,displayCap,BaseNamePtr(first));}else if(outDisplay)CopyWide(outDisplay,displayCap,BaseNamePtr(zip));if(!DeleteFileW(dmp))AppendLog(L"SHARE ZIP created, but the original .dmp could not be removed");DWORD omb=(DWORD)(original/1048576ULL),pmb=(DWORD)(packed/1048576ULL);WCHAR line[700];if(parts>1)wsprintfW(line,L"SHARE ZIP SUCCESS full dump preserved losslessly: original=%u MB compressed=%u MB split=%d parts <=475000000 bytes; original .dmp removed",omb,pmb,parts);else wsprintfW(line,L"SHARE ZIP SUCCESS full dump preserved losslessly: original=%u MB compressed=%u MB; original .dmp removed",omb,pmb);AppendLog(line);g_lastShareCompressed=1;g_lastShareParts=parts;return TRUE;}
static BOOL IsEnhancedExe(LPCWSTR exe){return exe&&lstrcmpiW(exe,L"obs64.exe")==0;}
static void DumpStem(LPCWSTR exe,WCHAR*out,int cap){CopyWide(out,cap,exe?exe:L"process");int n=lstrlenW(out);if(n>4&&out[n-4]==L'.'&&(out[n-3]==L'e'||out[n-3]==L'E')&&(out[n-2]==L'x'||out[n-2]==L'X')&&(out[n-1]==L'e'||out[n-1]==L'E'))out[n-4]=0;}
typedef BOOL (WINAPI *PFN_MINIDUMPWRITEDUMP)(HANDLE,DWORD,HANDLE,DWORD,PVOID,PVOID,PVOID);
typedef DWORD (WINAPI *PFN_PSSCAPTURESNAPSHOT)(HANDLE,DWORD,DWORD,HANDLE*);
typedef DWORD (WINAPI *PFN_PSSFREESNAPSHOT)(HANDLE,HANDLE);
typedef DWORD (WINAPI *PFN_PSSQUERYSNAPSHOT)(HANDLE,DWORD,PVOID,DWORD);
typedef DWORD (WINAPI *PFN_GETPROCESSID)(HANDLE);
struct PSS_VA_CLONE_INFORMATION_NATIVE { HANDLE VaCloneHandle; };
#define PSS_QUERY_VA_CLONE_INFORMATION 1u
#define PSS_CAPTURE_VA_CLONE 0x00000001u
#define PSS_CAPTURE_HANDLES 0x00000004u
#define PSS_CAPTURE_HANDLE_NAME_INFORMATION 0x00000008u
#define PSS_CAPTURE_HANDLE_BASIC_INFORMATION 0x00000010u
#define PSS_CAPTURE_HANDLE_TYPE_SPECIFIC_INFORMATION 0x00000020u
#define PSS_CAPTURE_HANDLE_TRACE 0x00000040u
#define PSS_CAPTURE_THREADS 0x00000080u
#define PSS_CAPTURE_THREAD_CONTEXT 0x00000100u
#define PSS_CAPTURE_THREAD_CONTEXT_EXTENDED 0x00000200u
#define PSS_CREATE_BREAKAWAY_OPTIONAL 0x04000000u
#define PSS_CREATE_BREAKAWAY 0x08000000u
#define PSS_CREATE_USE_VM_ALLOCATIONS 0x20000000u
#define PSS_CREATE_RELEASE_SECTION 0x80000000u
#define CONTEXT_ALL_AMD64 0x0010001Fu
#define S_FALSE_HR 1L
static DWORD DumpFlagsForKind(LPCWSTR kind){
 // TEST: full diagnostic profile, same data flags as CRASH/EXITCRASH; it runs on a background worker thread.
 if(kind&&lstrcmpiW(kind,L"TEST")==0)return 0x00000002u|0x00000004u|0x00000020u|0x00000100u|0x00000800u|0x00001000u|0x00020000u|0x00040000u;
 // PRECRASH: compact handle-leak diagnostic: includes active handle data but deliberately omits MiniDumpWithFullMemory.
 if(kind&&lstrcmpiW(kind,L"PRECRASH")==0)return 0x00000004u|0x00000020u|0x00000100u|0x00000800u|0x00001000u|0x00020000u;
 // CRASH / EXITCRASH and other diagnostic captures: full memory + handles + process/thread/memory-region metadata.
 return 0x00000002u|0x00000004u|0x00000020u|0x00000100u|0x00000800u|0x00001000u|0x00020000u|0x00040000u;
}
static volatile LONG g_snapshotCallbackSeen=0;
static BOOL CALLBACK SnapshotMiniDumpCallback(PVOID,const MINIDUMP_CALLBACK_INPUT_NATIVE* in,MINIDUMP_CALLBACK_OUTPUT_NATIVE* out){if(in&&out&&in->CallbackType==16){g_snapshotCallbackSeen=1;out->Status=S_FALSE_HR;}return TRUE;}
static BOOL CaptureObsSnapshot(DWORD pid,HANDLE*outSnapshot,DWORD*outErr){
 if(outSnapshot)*outSnapshot=0;if(outErr)*outErr=0;
 HMODULE k=GetModuleHandleW(L"kernel32.dll");if(!k){if(outErr)*outErr=GetLastError();return FALSE;}
 PFN_PSSCAPTURESNAPSHOT cap=(PFN_PSSCAPTURESNAPSHOT)GetProcAddress(k,"PssCaptureSnapshot");if(!cap){if(outErr)*outErr=GetLastError();return FALSE;}
 HANDLE ph=OpenProcess(PROCESS_QUERY_INFORMATION|PROCESS_VM_READ|PROCESS_DUP_HANDLE|PROCESS_CREATE_PROCESS,FALSE,pid);if(!ph){if(outErr)*outErr=GetLastError();return FALSE;}
 DWORD flags=PSS_CAPTURE_VA_CLONE|PSS_CAPTURE_HANDLES|PSS_CAPTURE_HANDLE_NAME_INFORMATION|PSS_CAPTURE_HANDLE_BASIC_INFORMATION|PSS_CAPTURE_HANDLE_TYPE_SPECIFIC_INFORMATION|PSS_CAPTURE_HANDLE_TRACE|PSS_CAPTURE_THREADS|PSS_CAPTURE_THREAD_CONTEXT|PSS_CAPTURE_THREAD_CONTEXT_EXTENDED|PSS_CREATE_BREAKAWAY|PSS_CREATE_BREAKAWAY_OPTIONAL|PSS_CREATE_USE_VM_ALLOCATIONS|PSS_CREATE_RELEASE_SECTION;
 HANDLE snap=0;DWORD rc=cap(ph,flags,CONTEXT_ALL_AMD64,&snap);CloseHandle(ph);if(rc!=ERROR_SUCCESS||!snap){if(outErr)*outErr=rc;return FALSE;}if(outSnapshot)*outSnapshot=snap;return TRUE;
}
static BOOL QueryObsSnapshotClone(HANDLE snap,HANDLE*outClone,DWORD*outClonePid,DWORD*outErr){
 if(outClone)*outClone=0;if(outClonePid)*outClonePid=0;if(outErr)*outErr=0;if(!snap){if(outErr)*outErr=6;return FALSE;}
 HMODULE k=GetModuleHandleW(L"kernel32.dll");if(!k){if(outErr)*outErr=GetLastError();return FALSE;}
 PFN_PSSQUERYSNAPSHOT q=(PFN_PSSQUERYSNAPSHOT)GetProcAddress(k,"PssQuerySnapshot");if(!q){if(outErr)*outErr=GetLastError();return FALSE;}
 PSS_VA_CLONE_INFORMATION_NATIVE vi;ZeroMem(&vi,sizeof(vi));DWORD rc=q(snap,PSS_QUERY_VA_CLONE_INFORMATION,&vi,sizeof(vi));if(rc!=ERROR_SUCCESS||!vi.VaCloneHandle){if(outErr)*outErr=rc?rc:6;return FALSE;}
 DWORD clonePid=0;PFN_GETPROCESSID gp=(PFN_GETPROCESSID)GetProcAddress(k,"GetProcessId");if(gp)clonePid=gp(vi.VaCloneHandle);
 if(outClone)*outClone=vi.VaCloneHandle;if(outClonePid)*outClonePid=clonePid;return TRUE;
}
static void FreeObsSnapshot(HANDLE snap){if(!snap)return;HMODULE k=GetModuleHandleW(L"kernel32.dll");if(!k)return;PFN_PSSFREESNAPSHOT fre=(PFN_PSSFREESNAPSHOT)GetProcAddress(k,"PssFreeSnapshot");if(fre)fre(INVALID_HANDLE_VALUE,snap);}
static BOOL WriteSnapshotDump(HANDLE snap,DWORD pid,LPCWSTR exe,LPCWSTR kind,DWORD handles,DWORD exceptionCode,DWORD firstChance){
 AcquireSRWLockExclusive(&g_dumpWriteLock);BOOL ok=FALSE;DWORD err=0,firstErr=0;WCHAR stem[128],file[MAX_PATH*2],line[1000],newest[MAX_PATH*2];DumpStem(exe,stem,128);SYSTEMTIME st;GetLocalTime(&st);
 if(exceptionCode)wsprintfW(file,L"%s\\%s_%s_%04u%02u%02u-%02u%02u%02u_pid%u_h%u_code%08X_f%u.dmp",g_dumpRoot,stem,kind,st.wYear,st.wMonth,st.wDay,st.wHour,st.wMinute,st.wSecond,pid,handles,exceptionCode,firstChance);
 else wsprintfW(file,L"%s\\%s_%s_%04u%02u%02u-%02u%02u%02u_pid%u_h%u.dmp",g_dumpRoot,stem,kind,st.wYear,st.wMonth,st.wDay,st.wHour,st.wMinute,st.wSecond,pid,handles);
 HMODULE dbg=LoadLibraryW(L"dbghelp.dll");if(!dbg){err=GetLastError();wsprintfW(line,L"PSS DUMP %s %s pid=%u FAILED LoadLibrary dbghelp err=%u",kind,exe,pid,err);AppendLog(line);FreeObsSnapshot(snap);ReleaseSRWLockExclusive(&g_dumpWriteLock);return FALSE;}
 PFN_MINIDUMPWRITEDUMP fn=(PFN_MINIDUMPWRITEDUMP)GetProcAddress(dbg,"MiniDumpWriteDump");if(!fn){err=GetLastError();wsprintfW(line,L"PSS DUMP %s %s pid=%u FAILED MiniDumpWriteDump missing err=%u",kind,exe,pid,err);AppendLog(line);FreeLibrary(dbg);FreeObsSnapshot(snap);ReleaseSRWLockExclusive(&g_dumpWriteLock);return FALSE;}
 HANDLE fh=CreateFileW(file,GENERIC_WRITE,FILE_SHARE_READ,NULLPTR,CREATE_ALWAYS,FILE_ATTRIBUTE_NORMAL,0);if(fh==INVALID_HANDLE_VALUE){err=GetLastError();wsprintfW(line,L"PSS DUMP %s %s pid=%u FAILED CreateFile err=%u",kind,exe,pid,err);AppendLog(line);FreeLibrary(dbg);FreeObsSnapshot(snap);ReleaseSRWLockExclusive(&g_dumpWriteLock);return FALSE;}
 DWORD flags=DumpFlagsForKind(kind);MINIDUMP_CALLBACK_INFORMATION_NATIVE cb;ZeroMem(&cb,sizeof(cb));cb.CallbackRoutine=SnapshotMiniDumpCallback;cb.CallbackParam=NULLPTR;g_snapshotCallbackSeen=0;
 ok=fn(snap,pid,fh,flags,NULLPTR,NULLPTR,&cb);if(!ok)firstErr=GetLastError();else FlushFileBuffers(fh);CloseHandle(fh);
 if(!ok){
  WCHAR firstLine[900];wsprintfW(firstLine,L"PSS HPSS DUMP %s %s pid=%u failed err=%u (0x%08X) snapshotCallback=%u; trying VA-clone fallback",kind,exe,pid,firstErr,firstErr,(DWORD)g_snapshotCallbackSeen);AppendLog(firstLine);
  DeleteFileW(file);HANDLE clone=0;DWORD clonePid=0,qerr=0;
  if(QueryObsSnapshotClone(snap,&clone,&clonePid,&qerr)&&clone){
   if(!clonePid)clonePid=pid;fh=CreateFileW(file,GENERIC_WRITE,FILE_SHARE_READ,NULLPTR,CREATE_ALWAYS,FILE_ATTRIBUTE_NORMAL,0);
   if(fh!=INVALID_HANDLE_VALUE){ok=fn(clone,clonePid,fh,flags,NULLPTR,NULLPTR,NULLPTR);if(!ok)err=GetLastError();else FlushFileBuffers(fh);CloseHandle(fh);}
   else{ok=FALSE;err=GetLastError();}
   if(ok){wsprintfW(line,L"PSS CLONE DUMP %s %s pid=%u clonePid=%u SUCCESS handles=%u flags=0x%08X file=%s",kind,exe,pid,clonePid,handles,flags,BaseNamePtr(file));AppendLog(line);}
   else{DeleteFileW(file);wsprintfW(line,L"PSS CLONE DUMP %s %s pid=%u clonePid=%u FAILED err=%u (0x%08X); original HPSS err=%u",kind,exe,pid,clonePid,err,err,firstErr);AppendLog(line);}
  }else{err=qerr;wsprintfW(line,L"PSS CLONE QUERY %s %s pid=%u FAILED err=%u; original HPSS err=%u",kind,exe,pid,qerr,firstErr);AppendLog(line);ok=FALSE;}
 }
 FreeLibrary(dbg);FreeObsSnapshot(snap);
 if(!ok){ReleaseSRWLockExclusive(&g_dumpWriteLock);return FALSE;}
 if(firstErr==0){wsprintfW(line,L"PSS DUMP %s %s pid=%u SUCCESS handles=%u flags=0x%08X file=%s",kind,exe,pid,handles,flags,BaseNamePtr(file));AppendLog(line);}
 WCHAR shareName[MAX_PATH*2];CopyWide(shareName,MAX_PATH*2,BaseNamePtr(file));CompressDumpForSharing(file,shareName,MAX_PATH*2);CopyWide(g_lastCapturedFile,MAX_PATH*2,shareName);BOOL isTest=kind&&lstrcmpiW(kind,L"TEST")==0;if(IsEnhancedExe(exe)&&!isTest)CopyObsLog();g_lastDumpTime=ScanNewestDump(newest);if(g_hwnd&&!isTest)PostMessageW(g_hwnd,WM_CAPTURED,0,0);ReleaseSRWLockExclusive(&g_dumpWriteLock);return TRUE;
}
static BOOL WriteLiveDump(DWORD pid,LPCWSTR exe,LPCWSTR kind,DWORD handles,DWORD exceptionCode,DWORD firstChance){
 AcquireSRWLockExclusive(&g_dumpWriteLock);BOOL ok=FALSE;DWORD err=0;WCHAR stem[128],file[MAX_PATH*2],line[900],newest[MAX_PATH*2];DumpStem(exe,stem,128);SYSTEMTIME st;GetLocalTime(&st);
 if(exceptionCode)wsprintfW(file,L"%s\\%s_%s_%04u%02u%02u-%02u%02u%02u_pid%u_h%u_code%08X_f%u.dmp",g_dumpRoot,stem,kind,st.wYear,st.wMonth,st.wDay,st.wHour,st.wMinute,st.wSecond,pid,handles,exceptionCode,firstChance);
 else wsprintfW(file,L"%s\\%s_%s_%04u%02u%02u-%02u%02u%02u_pid%u_h%u.dmp",g_dumpRoot,stem,kind,st.wYear,st.wMonth,st.wDay,st.wHour,st.wMinute,st.wSecond,pid,handles);
 HMODULE dbg=LoadLibraryW(L"dbghelp.dll");if(!dbg){err=GetLastError();wsprintfW(line,L"DUMP %s %s pid=%u FAILED LoadLibrary dbghelp err=%u",kind,exe,pid,err);AppendLog(line);ReleaseSRWLockExclusive(&g_dumpWriteLock);return FALSE;}
 PFN_MINIDUMPWRITEDUMP fn=(PFN_MINIDUMPWRITEDUMP)GetProcAddress(dbg,"MiniDumpWriteDump");if(!fn){err=GetLastError();wsprintfW(line,L"DUMP %s %s pid=%u FAILED MiniDumpWriteDump missing err=%u",kind,exe,pid,err);AppendLog(line);FreeLibrary(dbg);ReleaseSRWLockExclusive(&g_dumpWriteLock);return FALSE;}
 HANDLE ph=OpenProcess(PROCESS_QUERY_INFORMATION|PROCESS_VM_READ|PROCESS_DUP_HANDLE,FALSE,pid);if(!ph){err=GetLastError();wsprintfW(line,L"DUMP %s %s pid=%u FAILED OpenProcess err=%u",kind,exe,pid,err);AppendLog(line);FreeLibrary(dbg);ReleaseSRWLockExclusive(&g_dumpWriteLock);return FALSE;}
 HANDLE fh=CreateFileW(file,GENERIC_WRITE,FILE_SHARE_READ,NULLPTR,CREATE_ALWAYS,FILE_ATTRIBUTE_NORMAL,0);if(fh==INVALID_HANDLE_VALUE){err=GetLastError();wsprintfW(line,L"DUMP %s %s pid=%u FAILED CreateFile err=%u",kind,exe,pid,err);AppendLog(line);CloseHandle(ph);FreeLibrary(dbg);ReleaseSRWLockExclusive(&g_dumpWriteLock);return FALSE;}
 DWORD flags=DumpFlagsForKind(kind);ok=fn(ph,pid,fh,flags,NULLPTR,NULLPTR,NULLPTR);if(!ok)err=GetLastError();else FlushFileBuffers(fh);CloseHandle(fh);CloseHandle(ph);FreeLibrary(dbg);
 if(!ok){DeleteFileW(file);wsprintfW(line,L"DUMP %s %s pid=%u FAILED MiniDumpWriteDump err=%u",kind,exe,pid,err);AppendLog(line);ReleaseSRWLockExclusive(&g_dumpWriteLock);return FALSE;}
 wsprintfW(line,L"DUMP %s %s pid=%u SUCCESS handles=%u flags=0x%08X file=%s",kind,exe,pid,handles,flags,BaseNamePtr(file));AppendLog(line);WCHAR shareName[MAX_PATH*2];CopyWide(shareName,MAX_PATH*2,BaseNamePtr(file));CompressDumpForSharing(file,shareName,MAX_PATH*2);CopyWide(g_lastCapturedFile,MAX_PATH*2,shareName);BOOL isTest=kind&&lstrcmpiW(kind,L"TEST")==0;g_lastDumpTime=ScanNewestDump(newest);if(g_hwnd&&!isTest)PostMessageW(g_hwnd,WM_CAPTURED,0,0);ReleaseSRWLockExclusive(&g_dumpWriteLock);return TRUE;
}
static BOOL WriteExternalDump(DWORD pid,LPCWSTR exe,LPCWSTR kind,DWORD handles,DWORD exceptionCode,DWORD firstChance){
 if(IsEnhancedExe(exe)){HANDLE snap=0;DWORD err=0;if(!CaptureObsSnapshot(pid,&snap,&err)){WCHAR line[512];wsprintfW(line,L"PSS SNAPSHOT %s %s pid=%u FAILED err=%u; live OBS dump skipped to avoid projector freeze",kind,exe,pid,err);AppendLog(line);return FALSE;}return WriteSnapshotDump(snap,pid,exe,kind,handles,exceptionCode,firstChance);}return WriteLiveDump(pid,exe,kind,handles,exceptionCode,firstChance);
}
static DWORD WINAPI ObsSnapshotDumpWorker(PVOID){ObsSnapshotJob job=g_obsSnapshotJob;BOOL ok=WriteSnapshotDump(job.snapshot,job.pid,job.exe,job.kind,job.handles,job.exceptionCode,job.firstChance);if(ok)g_obsCrashDumpPid=job.pid;g_obsSnapshotJobRunning=0;return 0;}
static BOOL QueueObsSnapshotDump(DWORD pid,LPCWSTR kind,DWORD handles,DWORD exceptionCode,DWORD firstChance){
 if(g_obsSnapshotJobRunning)return FALSE;HANDLE snap=0;DWORD err=0;if(!CaptureObsSnapshot(pid,&snap,&err)){WCHAR line[512];wsprintfW(line,L"PSS SNAPSHOT %s obs64.exe pid=%u FAILED err=%u; WER remains available",kind,pid,err);AppendLog(line);return FALSE;}
 ZeroMem(&g_obsSnapshotJob,sizeof(g_obsSnapshotJob));g_obsSnapshotJob.snapshot=snap;g_obsSnapshotJob.pid=pid;g_obsSnapshotJob.handles=handles;g_obsSnapshotJob.exceptionCode=exceptionCode;g_obsSnapshotJob.firstChance=firstChance;CopyWide(g_obsSnapshotJob.exe,MAX_PATH,L"obs64.exe");CopyWide(g_obsSnapshotJob.kind,32,kind);g_obsSnapshotJobRunning=1;HANDLE th=CreateThread(NULLPTR,0,ObsSnapshotDumpWorker,NULLPTR,0,0);if(!th){g_obsSnapshotJobRunning=0;FreeObsSnapshot(snap);AppendLog(L"PSS snapshot captured but dump worker could not start");return FALSE;}CloseHandle(th);return TRUE;
}
static BOOL IsSevereException(DWORD code){return code==0xC0000005u||code==0xC0000006u||code==0xC000001Du||code==0xC0000096u||code==0xC00000FDu||code==0xC0000374u||code==0xC0000409u||code==0x40000015u;}
static void CloseDebugEventHandles(DEBUG_EVENT_NATIVE&ev){if(ev.dwDebugEventCode==CREATE_THREAD_DEBUG_EVENT){if(ev.u.CreateThread.hThread)CloseHandle(ev.u.CreateThread.hThread);}else if(ev.dwDebugEventCode==CREATE_PROCESS_DEBUG_EVENT){if(ev.u.CreateProcessInfo.hFile)CloseHandle(ev.u.CreateProcessInfo.hFile);if(ev.u.CreateProcessInfo.hProcess)CloseHandle(ev.u.CreateProcessInfo.hProcess);if(ev.u.CreateProcessInfo.hThread)CloseHandle(ev.u.CreateProcessInfo.hThread);}else if(ev.dwDebugEventCode==LOAD_DLL_DEBUG_EVENT){if(ev.u.LoadDll.hFile)CloseHandle(ev.u.LoadDll.hFile);}}
static DWORD WINAPI ObsDebugThread(PVOID arg){DWORD pid=(DWORD)(ULONG_PTR)arg;WCHAR line[512];DebugSetProcessKillOnExit(FALSE);if(!DebugActiveProcess(pid)){DWORD e=GetLastError();wsprintfW(line,L"ENHANCED obs64.exe pid=%u debugger attach FAILED err=%u",pid,e);AppendLog(line);if(g_obsDebugPid==pid)g_obsDebugPid=0;return 0;}wsprintfW(line,L"ENHANCED obs64.exe pid=%u debugger attached; crash events use PSS snapshot then immediately continue",pid);AppendLog(line);BOOL done=FALSE;while(!done&&!g_exitFlag&&!g_obsDebugStop){DEBUG_EVENT_NATIVE ev;ZeroMem(&ev,sizeof(ev));if(!WaitForDebugEvent(&ev,500)){continue;}DWORD cont=DBG_CONTINUE;if(ev.dwDebugEventCode==EXCEPTION_DEBUG_EVENT){DWORD code=ev.u.Exception.ExceptionRecord.ExceptionCode;DWORD first=ev.u.Exception.dwFirstChance;cont=DBG_EXCEPTION_NOT_HANDLED;if(IsSevereException(code)&&g_obsCrashDumpPid!=pid&&!g_obsSnapshotJobRunning){HANDLE ph=OpenProcess(PROCESS_QUERY_LIMITED_INFORMATION,FALSE,pid);DWORD hc=0;if(ph){GetProcessHandleCount(ph,&hc);CloseHandle(ph);}if(QueueObsSnapshotDump(pid,L"CRASH",hc,code,first))g_obsCrashDumpPid=pid;}}
 else if(ev.dwDebugEventCode==EXIT_PROCESS_DEBUG_EVENT){DWORD exitCode=ev.u.ExitProcess.dwExitCode;if(exitCode!=0&&g_obsCrashDumpPid!=pid&&!g_obsSnapshotJobRunning){HANDLE ph=OpenProcess(PROCESS_QUERY_LIMITED_INFORMATION,FALSE,pid);DWORD hc=0;if(ph){GetProcessHandleCount(ph,&hc);CloseHandle(ph);}if(QueueObsSnapshotDump(pid,L"EXITCRASH",hc,exitCode,0))g_obsCrashDumpPid=pid;}done=TRUE;}
 CloseDebugEventHandles(ev);ContinueDebugEvent(ev.dwProcessId,ev.dwThreadId,cont);}
 if(!done)DebugActiveProcessStop(pid);wsprintfW(line,L"ENHANCED obs64.exe pid=%u debugger detached/stopped",pid);AppendLog(line);if(g_obsDebugPid==pid)g_obsDebugPid=0;g_obsDebugStop=0;return 0;}
static void StartObsDebuggerIfNeeded(DWORD pid){if(!pid)return;if(g_obsDebugThread&&WaitForSingleObject(g_obsDebugThread,0)==WAIT_OBJECT_0){CloseHandle(g_obsDebugThread);g_obsDebugThread=0;}if(g_obsDebugPid==pid&&g_obsDebugThread)return;if(g_obsDebugPid&&g_obsDebugPid!=pid)g_obsDebugStop=1;if(g_obsDebugThread)return;g_obsDebugStop=0;g_obsDebugPid=pid;g_obsCrashDumpPid=0;g_obsDebugThread=CreateThread(NULLPTR,0,ObsDebugThread,(PVOID)(ULONG_PTR)pid,0,0);if(!g_obsDebugThread)g_obsDebugPid=0;}
static void CheckDumps(){if(g_testDumpRunning||g_obsSnapshotJobRunning)return;WCHAR n[MAX_PATH*2];ULONGLONG t=ScanNewestDump(n);if(t&&t>g_lastDumpTime){g_lastDumpTime=t;CopyWide(g_lastCapturedFile,MAX_PATH*2,n);if(PrefixI(n,L"obs64.exe"))CopyObsLog();AppendLog(L"New Windows Error Reporting dump detected");if(g_hwnd)PostMessageW(g_hwnd,WM_CAPTURED,0,0);}}
static int AddRunning(DWORD pid,LPCWSTR exe,DWORD threads){for(int i=0;i<MAX_RUNNING;i++)if(!g_running[i].active){ZeroMem(&g_running[i],sizeof(RunningInfo));g_running[i].active=TRUE;g_running[i].pid=pid;CopyWide(g_running[i].exeName,MAX_PATH,exe);g_running[i].threadCount=threads;g_activeCount++;return i;}return -1;}
static void ClearRunning(){ZeroMem(g_running,sizeof(g_running));g_activeCount=0;}
static void LogResource(RunningInfo&r){HANDLE h=OpenProcess(PROCESS_QUERY_LIMITED_INFORMATION,FALSE,r.pid);if(!h)return;DWORD handles=0;GetProcessHandleCount(h,&handles);DWORD gdi=GetGuiResources(h,GR_GDIOBJECTS),user=GetGuiResources(h,GR_USEROBJECTS);WCHAR l[512];wsprintfW(l,L"RESOURCE %s pid=%u handles=%u threads=%u gdi=%u user=%u",r.exeName,r.pid,handles,r.threadCount,gdi,user);AppendLog(l);CloseHandle(h);if(IsEnhancedExe(r.exeName)&&handles>=OBS_PRECRASH_HANDLE_THRESHOLD&&g_obsPreDumpPid!=r.pid){WCHAR w[512];wsprintfW(w,L"PRECRASH threshold reached for obs64.exe pid=%u handles=%u (threshold=%u)",r.pid,handles,OBS_PRECRASH_HANDLE_THRESHOLD);AppendLog(w);if(WriteExternalDump(r.pid,r.exeName,L"PRECRASH",handles,0,0))g_obsPreDumpPid=r.pid;}}
static void ScanRunning(){ClearRunning();DWORD obsPid=0;HANDLE h=CreateToolhelp32Snapshot(TH32CS_SNAPPROCESS,0);if(h==INVALID_HANDLE_VALUE)return;PROCESSENTRY32W p;ZeroMem(&p,sizeof(p));p.dwSize=sizeof(p);if(Process32FirstW(h,&p)){do{TargetConfig m;BOOL found=FALSE;AcquireSRWLockShared(&g_lock);for(int i=0;i<g_targetCount;i++)if(TargetMatch(g_targets[i],p)){m=g_targets[i];found=TRUE;break;}ReleaseSRWLockShared(&g_lock);if(found){AddRunning(p.th32ProcessID,m.exeName,p.cntThreads);if(IsEnhancedExe(m.exeName))obsPid=p.th32ProcessID;}}while(Process32NextW(h,&p));}CloseHandle(h);if(obsPid){if(g_obsPreDumpPid!=obsPid){}StartObsDebuggerIfNeeded(obsPid);}else if(g_obsDebugPid)g_obsDebugStop=1;for(int i=0;i<MAX_RUNNING;i++)if(g_running[i].active)LogResource(g_running[i]);}
static BOOL AllEnabledWerConfigured(){BOOL ok=TRUE;AcquireSRWLockShared(&g_lock);for(int i=0;i<g_targetCount;i++)if(g_targets[i].enabled){if(!IsWerConfigured(g_targets[i].exeName)){ok=FALSE;break;}}ReleaseSRWLockShared(&g_lock);return ok;}
static DWORD WINAPI Worker(PVOID){AppendLog(L"Crash Monitor 4.2 Build 12 worker started");WCHAR n[MAX_PATH*2];g_lastDumpTime=ScanNewestDump(n);ULONGLONG lastRun=0,lastDump=0;while(!g_exitFlag){if(g_paused){if(g_obsDebugPid)g_obsDebugStop=1;if(g_hwnd)PostMessageW(g_hwnd,WM_STATE,STATE_PAUSED,0);Sleep(500);continue;}ULONGLONG now=GetTickCount64();if(g_reconfigure){g_reconfigure=0;lastRun=0;}if(now-lastRun>=60000ULL||lastRun==0){ScanRunning();BOOL configured=AllEnabledWerConfigured();if(g_hwnd)PostMessageW(g_hwnd,WM_STATE,configured?(g_activeCount?STATE_WATCHING:STATE_WAITING):STATE_NEEDS_SETUP,(LPARAM)g_activeCount);lastRun=now;}if(now-lastDump>=1200ULL){CheckDumps();lastDump=now;}Sleep(120);}AppendLog(L"Crash Monitor worker stopped");return 0;}

static void SetControlFont(HWND h,BOOL title){if(h)SendMessageW(h,WM_SETFONT,(WPARAM)(title?g_titleFont:g_font),TRUE);}
static HWND MakeControl(LPCWSTR cls,LPCWSTR text,DWORD style,int x,int y,int w,int h,HWND parent,int id,BOOL title){HWND c=CreateWindowExW(0,cls,text,WS_CHILD|WS_VISIBLE|style,x,y,w,h,parent,(HMENU)(ULONG_PTR)id,(HINSTANCE)GetModuleHandleW(0),NULLPTR);SetControlFont(c,title);return c;}
static void RefreshProgramList(){if(!g_list)return;int sel=(int)SendMessageW(g_list,LB_GETCURSEL,0,0);SendMessageW(g_list,LB_RESETCONTENT,0,0);AcquireSRWLockShared(&g_lock);for(int i=0;i<g_targetCount;i++){WCHAR s[768];WCHAR wer[96];if(!g_targets[i].enabled)lstrcpyW(wer,L"Dumps off");else if(IsEnhancedExe(g_targets[i].exeName))lstrcpyW(wer,IsWerConfigured(g_targets[i].exeName)?L"WER + enhanced ready":L"Enhanced ready / WER setup needed");else lstrcpyW(wer,IsWerConfigured(g_targets[i].exeName)?L"WER ready":L"WER setup needed");wsprintfW(s,L"%s  %s  —  %s",g_targets[i].enabled?L"[ON] ":L"[OFF]",g_targets[i].exeName,wer);SendMessageW(g_list,LB_ADDSTRING,0,(LPARAM)s);}ReleaseSRWLockShared(&g_lock);if(g_targetCount>0){if(sel<0||sel>=g_targetCount)sel=0;SendMessageW(g_list,LB_SETCURSEL,(WPARAM)sel,0);}if(g_startupBox)SendMessageW(g_startupBox,BM_SETCHECK,IsStartupEnabled()?BST_CHECKED:BST_UNCHECKED,0);if(g_pauseBox)SendMessageW(g_pauseBox,BM_SETCHECK,g_paused?BST_CHECKED:BST_UNCHECKED,0);if(g_minimizeTrayBox)SendMessageW(g_minimizeTrayBox,BM_SETCHECK,g_minimizeToTray?BST_CHECKED:BST_UNCHECKED,0);if(g_keepTrayTaskbarBox)SendMessageW(g_keepTrayTaskbarBox,BM_SETCHECK,g_keepTrayTaskbar?BST_CHECKED:BST_UNCHECKED,0);if(g_closeXTrayBox)SendMessageW(g_closeXTrayBox,BM_SETCHECK,g_closeXToTray?BST_CHECKED:BST_UNCHECKED,0);if(g_startMinimizedBox)SendMessageW(g_startMinimizedBox,BM_SETCHECK,g_startMinimized?BST_CHECKED:BST_UNCHECKED,0);if(g_startPausedBox)SendMessageW(g_startPausedBox,BM_SETCHECK,g_startPaused?BST_CHECKED:BST_UNCHECKED,0);if(g_notificationsBox)SendMessageW(g_notificationsBox,BM_SETCHECK,g_notificationsEnabled?BST_CHECKED:BST_UNCHECKED,0);if(g_displayBtn)SetWindowTextW(g_displayBtn,(g_trayOnly||g_hiddenToTray)?L"Move to Taskbar":L"Move to Tray");}
static int SelectedTarget(){if(!g_list)return -1;return (int)SendMessageW(g_list,LB_GETCURSEL,0,0);}
static BOOL FindRunningTargetPid(const TargetConfig&t,DWORD*outPid){if(outPid)*outPid=0;HANDLE h=CreateToolhelp32Snapshot(TH32CS_SNAPPROCESS,0);if(h==INVALID_HANDLE_VALUE)return FALSE;PROCESSENTRY32W p;ZeroMem(&p,sizeof(p));p.dwSize=sizeof(p);BOOL found=FALSE;if(Process32FirstW(h,&p)){do{if(TargetMatch(t,p)){if(outPid)*outPid=p.th32ProcessID;found=TRUE;break;}}while(Process32NextW(h,&p));}CloseHandle(h);return found;}
static DWORD WINAPI TestDumpWorker(PVOID){DWORD pid=g_testDumpPid;WCHAR exe[MAX_PATH];CopyWide(exe,MAX_PATH,g_testDumpExe);HANDLE ph=OpenProcess(PROCESS_QUERY_LIMITED_INFORMATION,FALSE,pid);DWORD hc=0;if(ph){GetProcessHandleCount(ph,&hc);CloseHandle(ph);}BOOL ok=WriteExternalDump(pid,exe,L"TEST",hc,0,0);g_testDumpRunning=0;if(g_hwnd)PostMessageW(g_hwnd,WM_TESTDONE,ok?1:0,0);return 0;}
static void TestSelectedDump(){int i=SelectedTarget();TargetConfig t;ZeroMem(&t,sizeof(t));AcquireSRWLockShared(&g_lock);if(i>=0&&i<g_targetCount)t=g_targets[i];ReleaseSRWLockShared(&g_lock);if(!t.exeName[0]||!t.enabled){MessageBoxW(g_hwnd,L"Select an enabled program first.",L"Crash Monitor",MB_OK|MB_ICONINFORMATION);return;}if(g_testDumpRunning){MessageBoxW(g_hwnd,L"A test dump is already being created.",L"Crash Monitor",MB_OK|MB_ICONINFORMATION);return;}DWORD pid=0;if(!FindRunningTargetPid(t,&pid)){MessageBoxW(g_hwnd,L"That program is not running right now.",L"Crash Monitor",MB_OK|MB_ICONINFORMATION);return;}if(MessageBoxW(g_hwnd,L"Create a full diagnostic test dump now?\n\nIt uses the same full data profile as a crash dump, including full process memory and handle data. After the dump is complete, Crash Monitor losslessly compresses it to ZIP and verifies the archive before removing the raw .dmp. If the ZIP is still too large for Discord Nitro, it is automatically split into sendable numbered parts. For OBS, the dump still uses the live-safe PSS snapshot / VA-clone path so projectors can keep running during file writing.",L"Crash Monitor Test Dump",MB_YESNO|MB_ICONQUESTION)!=IDYES)return;g_testDumpPid=pid;CopyWide(g_testDumpExe,MAX_PATH,t.exeName);g_lastShareCompressed=0;g_lastShareParts=0;g_testDumpRunning=1;if(g_testDumpBtn){EnableWindow(g_testDumpBtn,FALSE);SetWindowTextW(g_testDumpBtn,L"Creating Test Dump...");}HANDLE th=CreateThread(NULLPTR,0,TestDumpWorker,NULLPTR,0,0);if(!th){g_testDumpRunning=0;if(g_testDumpBtn){EnableWindow(g_testDumpBtn,TRUE);SetWindowTextW(g_testDumpBtn,L"Test Selected Dump");}MessageBoxW(g_hwnd,L"Crash Monitor could not start the test-dump worker thread.",L"Crash Monitor",MB_OK|MB_ICONERROR);return;}CloseHandle(th);}
static void UpdateSelectionDetails(){if(!g_details)return;int i=SelectedTarget();WCHAR text[1000];text[0]=0;AcquireSRWLockShared(&g_lock);if(i>=0&&i<g_targetCount){WCHAR path[MAX_PATH*2];CopyWide(path,MAX_PATH*2,g_targets[i].fullPath[0]?g_targets[i].fullPath:L"(matches this executable name anywhere)");LPCWSTR dumpState=!g_targets[i].enabled?L"Off":(IsWerConfigured(g_targets[i].exeName)?L"Ready":L"Needs setup");if(IsEnhancedExe(g_targets[i].exeName))wsprintfW(text,L"Program: %s\r\nPath: %s\r\nMonitoring: %s    WER: %s\r\nOBS enhanced: PSS live-snapshot dumps + VA-clone fallback; PRECRASH at %u handles + crash-event fallback",g_targets[i].exeName,path,g_targets[i].enabled?L"Enabled":L"Disabled",dumpState,OBS_PRECRASH_HANDLE_THRESHOLD);else wsprintfW(text,L"Program: %s\r\nPath: %s\r\nMonitoring: %s    Windows dumps: %s",g_targets[i].exeName,path,g_targets[i].enabled?L"Enabled":L"Disabled",dumpState);}ReleaseSRWLockShared(&g_lock);SetWindowTextW(g_details,text);}
static void UpdateStatusText(){if(!g_status)return;WCHAR t[512];if(g_safeSelfTestRunning){WCHAR p[420];AcquireSRWLockShared(&g_safeSelfTestProgressLock);CopyWide(p,420,g_safeSelfTestProgressText);ReleaseSRWLockShared(&g_safeSelfTestProgressLock);if(p[0]){lstrcpyW(t,L"Safe Self-Test ");lstrcatW(t,p);}else lstrcpyW(t,L"Safe Self-Test starting — waiting for the first test status...");SetWindowTextW(g_status,t);return;}BOOL anyEnabled=FALSE;AcquireSRWLockShared(&g_lock);for(int i=0;i<g_targetCount;i++)if(g_targets[i].enabled){anyEnabled=TRUE;break;}ReleaseSRWLockShared(&g_lock);if(g_currentState==STATE_NEEDS_SETUP)lstrcpyW(t,L"Crash dump setup is needed for one or more enabled programs.");else if(g_currentState==STATE_PAUSED)lstrcpyW(t,L"Monitoring is paused.");else if(g_currentState==STATE_CAPTURED)wsprintfW(t,L"Crash captured: %s",g_lastCapturedFile);else if(g_currentState==STATE_WATCHING)wsprintfW(t,L"Monitoring active — watching %u running process(es).",g_currentActive);else if(!anyEnabled)lstrcpyW(t,L"Monitoring active — all configured programs are OFF.");else lstrcpyW(t,L"Monitoring active — waiting for a configured program to run.");SetWindowTextW(g_status,t);}
static void AddTrayIcon(){if(g_trayVisible)return;g_nid.uFlags=NIF_MESSAGE|NIF_ICON|NIF_TIP;g_nid.uCallbackMessage=WM_TRAY;g_nid.hIcon=g_appIcon;if(!g_nid.szTip[0])CopyWide(g_nid.szTip,128,L"Crash Monitor");if(Shell_NotifyIconW(NIM_ADD,&g_nid))g_trayVisible=TRUE;}
static void RemoveTrayIcon(){if(!g_trayVisible)return;g_nid.uFlags=0;Shell_NotifyIconW(NIM_DELETE,&g_nid);g_trayVisible=FALSE;}
static void ShowMainWindow(){if(!g_hwnd)return;ShowWindow(g_hwnd,SW_RESTORE);ShowWindow(g_hwnd,SW_SHOW);SetForegroundWindow(g_hwnd);RefreshProgramList();UpdateSelectionDetails();UpdateStatusText();}
static void MoveToTrayMode(){if(!SaveTrayOnlySetting(TRUE)){MessageBoxW(g_hwnd,L"Crash Monitor could not save and verify tray-only mode, so the display mode was not changed.",L"Crash Monitor",MB_OK|MB_ICONERROR);return;}g_trayOnly=TRUE;g_hiddenToTray=TRUE;AddTrayIcon();RefreshProgramList();ShowWindow(g_hwnd,SW_HIDE);}
static void MoveToTaskbarMode(){if(!SaveTrayOnlySetting(FALSE)){MessageBoxW(g_hwnd,L"Crash Monitor could not save and verify taskbar mode, so the display mode was not changed.",L"Crash Monitor",MB_OK|MB_ICONERROR);return;}g_trayOnly=FALSE;g_hiddenToTray=FALSE;ShowMainWindow();if(g_keepTrayTaskbar)AddTrayIcon();else RemoveTrayIcon();RefreshProgramList();}
static void MinimizeIntoTray(){AppendLog(L"Window minimized to tray");HideMainToTray();}
static void Balloon(LPCWSTR title,LPCWSTR text,DWORD flags){if(!g_trayVisible||!g_notificationsEnabled)return;g_nid.uFlags=NIF_INFO;CopyWide(g_nid.szInfoTitle,64,title);CopyWide(g_nid.szInfo,256,text);g_nid.dwInfoFlags=flags;Shell_NotifyIconW(NIM_MODIFY,&g_nid);}
static void SetTrayState(int s,DWORD active){g_currentState=s;g_currentActive=active;WCHAR tip[128];g_nid.hIcon=g_appIcon;if(s==STATE_NEEDS_SETUP)lstrcpyW(tip,L"Crash Monitor - crash dump setup needed");else if(s==STATE_PAUSED)lstrcpyW(tip,L"Crash Monitor - paused");else if(s==STATE_WATCHING)wsprintfW(tip,L"Crash Monitor - watching %u process(es)",active);else if(s==STATE_CAPTURED)lstrcpyW(tip,L"Crash Monitor - crash dump captured");else lstrcpyW(tip,L"Crash Monitor - waiting for apps");CopyWide(g_nid.szTip,128,tip);if(g_trayVisible){g_nid.uFlags=NIF_ICON|NIF_TIP;Shell_NotifyIconW(NIM_MODIFY,&g_nid);}UpdateStatusText();}
static void BuildProgramMenus(HMENU root){HMENU en=CreatePopupMenu(),rm=CreatePopupMenu();AcquireSRWLockShared(&g_lock);for(int i=0;i<g_targetCount;i++){WCHAR label[512],status[64];if(!g_targets[i].enabled)lstrcpyW(status,L" [dumps off]");else if(IsEnhancedExe(g_targets[i].exeName))lstrcpyW(status,IsWerConfigured(g_targets[i].exeName)?L" [WER + enhanced]":L" [enhanced / WER setup]");else lstrcpyW(status,IsWerConfigured(g_targets[i].exeName)?L" [WER ready]":L" [WER setup]");lstrcpyW(label,g_targets[i].exeName);lstrcatW(label,status);AppendMenuW(en,MF_STRING|(g_targets[i].enabled?MF_CHECKED:0),CMD_TOGGLE_BASE+i,label);AppendMenuW(rm,MF_STRING,CMD_REMOVE_BASE+i,g_targets[i].exeName);}ReleaseSRWLockShared(&g_lock);AppendMenuW(root,MF_POPUP,(ULONG_PTR)en,L"Programs");AppendMenuW(root,MF_POPUP,(ULONG_PTR)rm,L"Remove Program");}
static void RemoveTargetFromUi(int i){WCHAR name[MAX_PATH];name[0]=0;AcquireSRWLockShared(&g_lock);if(i>=0&&i<g_targetCount)CopyWide(name,MAX_PATH,g_targets[i].exeName);ReleaseSRWLockShared(&g_lock);if(!name[0])return;WCHAR q[512];wsprintfW(q,L"Remove %s from Crash Monitor?",name);if(MessageBoxW(g_hwnd,q,L"Crash Monitor",MB_YESNO|MB_ICONQUESTION)!=IDYES)return;RemoveTarget(i,name);RunElevatedRemoveOne(name);RefreshProgramList();UpdateSelectionDetails();}
static void AddFromUi(){WCHAR path[MAX_PATH*2];path[0]=0;if(AddProgramDialog(g_hwnd,path,MAX_PATH*2)){LPCWSTR exe=BaseNamePtr(path);int idx=FindTargetByPath(path);if(exe&&exe[0]){if(!RunElevatedSetOne(exe,TRUE)&&idx>=0)SetTargetEnabled(idx,FALSE);}RefreshProgramList();UpdateSelectionDetails();}}
static DWORD WINAPI SafeSelfTestMonitorWorker(PVOID){LPCWSTR exe=FileExists(g_installExe)?g_installExe:g_exePath;WCHAR progressPath[MAX_PATH*2];if(BuildSafeSelfTestArtifactPath(L"CrashMonitor-SafeSelfTest-v4.2-Build12.progress",progressPath,MAX_PATH*2))DeleteFileW(progressPath);WCHAR cmd[MAX_PATH*2+96];lstrcpyW(cmd,L"\"");lstrcatW(cmd,exe);lstrcatW(cmd,L"\" --safe-self-test");STARTUPINFOW_NATIVE si;PROCESS_INFORMATION_NATIVE pi;ZeroMem(&si,sizeof(si));ZeroMem(&pi,sizeof(pi));si.cb=sizeof(si);DWORD code=CM_SELFTEST_LAUNCH_FAILED_CODE;if(CreateProcessW(exe,cmd,NULLPTR,NULLPTR,FALSE,CREATE_NO_WINDOW,NULLPTR,(LPCWSTR)0,&si,&pi)){code=0xFFFFFFFFu;ULONGLONG lastProgressTick=GetTickCount64();WCHAR last[512];last[0]=0;for(;;){DWORD wr=WaitForSingleObject(pi.hProcess,250);if(wr==WAIT_OBJECT_0){GetExitCodeProcess(pi.hProcess,&code);break;}if(wr!=WAIT_TIMEOUT){code=0xFFFFFFFFu;break;}WCHAR nowText[512];if(ReadSelfTestProgressSnapshot(nowText,512)&&lstrcmpiW(nowText,last)!=0){CopyWide(last,512,nowText);lastProgressTick=GetTickCount64();LONG idx=0,total=39;ParseSelfTestProgressNumbers(nowText,&idx,&total);AcquireSRWLockExclusive(&g_safeSelfTestProgressLock);CopyWide(g_safeSelfTestProgressText,512,nowText);g_safeSelfTestProgressIndex=idx;g_safeSelfTestProgressTotal=total;ReleaseSRWLockExclusive(&g_safeSelfTestProgressLock);if(g_hwnd)PostMessageW(g_hwnd,WM_SELFTESTPROGRESS,0,0);}if(GetTickCount64()-lastProgressTick>SELFTEST_HANG_TIMEOUT_MS){TerminateProcess(pi.hProcess,CM_SELFTEST_TIMEOUT_CODE);WaitForSingleObject(pi.hProcess,2000);code=CM_SELFTEST_TIMEOUT_CODE;break;}}CloseHandle(pi.hThread);CloseHandle(pi.hProcess);}if(g_hwnd)PostMessageW(g_hwnd,WM_SELFTESTDONE,(WPARAM)code,0);return 0;}
static void LaunchSafeSelfTest(){if(g_selfTestLaunchIntercept){g_selfTestLaunchInterceptCount++;return;}if(g_safeSelfTestRunning){MessageBoxW(g_hwnd,L"The Safe Self-Test is already running. The main status line shows the current test and progress.",L"Crash Monitor Safe Self-Test",MB_OK|MB_ICONINFORMATION);return;}AcquireSRWLockExclusive(&g_safeSelfTestProgressLock);g_safeSelfTestProgressText[0]=0;g_safeSelfTestProgressIndex=0;g_safeSelfTestProgressTotal=39;ReleaseSRWLockExclusive(&g_safeSelfTestProgressLock);g_safeSelfTestRunning=1;if(g_safeSelfTestBtn){EnableWindow(g_safeSelfTestBtn,FALSE);SetWindowTextW(g_safeSelfTestBtn,L"Self-Test starting...");}UpdateStatusText();AppendLog(L"Safe Self-Test launched with live current-test progress and bounded hang detection");g_safeSelfTestThread=CreateThread(NULLPTR,0,SafeSelfTestMonitorWorker,NULLPTR,0,0);if(!g_safeSelfTestThread){g_safeSelfTestRunning=0;if(g_safeSelfTestBtn){EnableWindow(g_safeSelfTestBtn,TRUE);SetWindowTextW(g_safeSelfTestBtn,L"Run Safe Self-Test...");}UpdateStatusText();MessageBoxW(g_hwnd,L"Crash Monitor could not start the Safe Self-Test supervisor.",L"Crash Monitor Safe Self-Test",MB_OK|MB_ICONERROR);}}
static BOOL WriteDiagnosticReportFile(LPCWSTR path){HANDLE h=CreateFileW(path,GENERIC_WRITE,FILE_SHARE_READ,NULLPTR,CREATE_ALWAYS,FILE_ATTRIBUTE_NORMAL,0);if(h==INVALID_HANDLE_VALUE)return FALSE;AppendUtf8(h,L"Crash Monitor v4.2 Build 12 - Diagnostic Report\r\n================================================\r\n");WCHAR line[1600];wsprintfW(line,L"State=%d  ActiveProcesses=%u  Paused=%d\r\nTrayOnly=%d  HiddenToTray=%d  MinimizeToTray=%d  CloseXToTray=%d  KeepTrayWithTaskbar=%d\r\nStartMinimized=%d  StartPaused=%d  Notifications=%d  StartWithWindows=%d\r\nInstallExe=%s\r\nDataDir=%s\r\nDumpDir=%s\r\nLog=%s\r\n\r\nMonitored programs:\r\n",g_currentState,g_currentActive,(int)g_paused,g_trayOnly,g_hiddenToTray,g_minimizeToTray,g_closeXToTray,g_keepTrayTaskbar,g_startMinimized,g_startPaused,g_notificationsEnabled,IsStartupEnabled(),g_installExe,g_baseDir,g_dumpRoot,g_logPath);AppendUtf8(h,line);AcquireSRWLockShared(&g_lock);for(int i=0;i<g_targetCount;i++){wsprintfW(line,L"%d. %s | enabled=%d | path=%s\r\n",i+1,g_targets[i].exeName,g_targets[i].enabled,g_targets[i].fullPath[0]?g_targets[i].fullPath:L"(name match)");AppendUtf8(h,line);}ReleaseSRWLockShared(&g_lock);AppendUtf8(h,L"\r\nPrivacy: no clipboard contents, keystrokes, private messages, passwords, tokens, or unrelated user files are collected.\r\n");CloseHandle(h);return FileExists(path)&&FileSize64(path)>0;}
static void ExportDiagnosticReport(){EnsureDir(g_baseDir);SYSTEMTIME st;GetLocalTime(&st);WCHAR path[MAX_PATH*2];wsprintfW(path,L"%s\\CrashMonitor-Diagnostic-v4.2-Build12-%04u%02u%02u-%02u%02u%02u.txt",g_baseDir,st.wYear,st.wMonth,st.wDay,st.wHour,st.wMinute,st.wSecond);if(!WriteDiagnosticReportFile(path)){MessageBoxW(g_hwnd,L"Crash Monitor could not create the diagnostic report.",L"Crash Monitor",MB_OK|MB_ICONERROR);return;}AppendLog(L"Diagnostic report exported");ShellExecuteW(g_hwnd,L"open",path,0,0,SW_SHOWNORMAL);}
static void HideMainToTray(){g_hiddenToTray=TRUE;AddTrayIcon();RefreshProgramList();ShowWindow(g_hwnd,SW_HIDE);}
static void RequestExit(HWND h){AppendLog(L"Exit App requested");SaveCurrentWindowRect();DestroyWindow(h);}
static void HandleMainClose(HWND h){if(g_closeXToTray){AppendLog(L"Main-window X -> tray");HideMainToTray();}else{AppendLog(L"Main-window X -> Exit App");RequestExit(h);}}
static void RevealExistingWindow(){if(!g_hwnd)return;g_hiddenToTray=FALSE;ShowMainWindow();if(g_trayOnly||g_keepTrayTaskbar)AddTrayIcon();}
static void HandleTrayCommand(HWND hwnd,UINT c){if(c==CMD_SHOW)RevealExistingWindow();else if(c==CMD_TASKBAR)MoveToTaskbarMode();else if(c==CMD_OPEN_CRASH)ShellExecuteW(hwnd,L"open",g_dumpRoot,0,0,SW_SHOWNORMAL);else if(c==CMD_OPEN_DATA)ShellExecuteW(hwnd,L"open",g_baseDir,0,0,SW_SHOWNORMAL);else if(c==CMD_EXPORT_REPORT)ExportDiagnosticReport();else if(c==CMD_RESET_LAYOUT)ResetWindowLayout();else if(c==CMD_TEST_DUMP)TestSelectedDump();else if(c==CMD_SAFE_SELF_TEST)LaunchSafeSelfTest();else if(c==CMD_ADD_PROGRAM)AddFromUi();else if(c==CMD_ENABLE_WER)RunElevatedHelper(TRUE);else if(c==CMD_DISABLE_WER)RunElevatedHelper(FALSE);else if(c==CMD_STARTUP){ApplyStartupSetting(!IsStartupEnabled(),TRUE);RefreshProgramList();}else if(c==CMD_PAUSE){ApplyPausedState(!g_paused);}else if(c==CMD_MINIMIZETRAY){ApplyMinimizeToTraySetting(!g_minimizeToTray,TRUE);}else if(c==CMD_CLOSEXTRAY){ApplyCloseXToTraySetting(!g_closeXToTray,TRUE);}else if(c==CMD_KEEPTRAYTASKBAR){ApplyKeepTrayTaskbarSetting(!g_keepTrayTaskbar,TRUE,TRUE);}else if(c==CMD_STARTMINIMIZED){ApplyStartMinimizedSetting(!g_startMinimized,TRUE);}else if(c==CMD_STARTPAUSED){ApplyStartPausedSetting(!g_startPaused,TRUE);}else if(c==CMD_NOTIFICATIONS){ApplyNotificationsSetting(!g_notificationsEnabled,TRUE);}else if(c==CMD_UNINSTALL)ShellExecuteW(hwnd,L"open",g_installExe,L"--uninstall",0,SW_SHOWNORMAL);else if(c>=CMD_TOGGLE_BASE&&c<CMD_TOGGLE_BASE+MAX_TARGETS){ToggleTargetWithWer((int)(c-CMD_TOGGLE_BASE));RefreshProgramList();UpdateSelectionDetails();}else if(c>=CMD_REMOVE_BASE&&c<CMD_REMOVE_BASE+MAX_TARGETS)RemoveTargetFromUi((int)(c-CMD_REMOVE_BASE));else if(c==CMD_EXIT)RequestExit(hwnd);}
static void ShowTrayMenu(HWND hwnd){HMENU m=CreatePopupMenu();AppendMenuW(m,MF_STRING,CMD_SHOW,L"Open Crash Monitor");AppendMenuW(m,MF_STRING,CMD_TASKBAR,L"Move to Taskbar");AppendMenuW(m,MF_STRING,CMD_OPEN_CRASH,L"Open Crash Dumps");AppendMenuW(m,MF_STRING,CMD_OPEN_DATA,L"Open Monitor Data Folder");AppendMenuW(m,MF_STRING,CMD_EXPORT_REPORT,L"Export Diagnostic Report");AppendMenuW(m,MF_STRING,CMD_RESET_LAYOUT,L"Reset Window Layout");AppendMenuW(m,MF_STRING,CMD_TEST_DUMP,L"Test Selected Dump...");AppendMenuW(m,MF_STRING,CMD_SAFE_SELF_TEST,L"Run Safe Self-Test...");AppendMenuW(m,MF_SEPARATOR,0,0);AppendMenuW(m,MF_STRING,CMD_ADD_PROGRAM,L"Add Program...");BuildProgramMenus(m);AppendMenuW(m,MF_SEPARATOR,0,0);AppendMenuW(m,MF_STRING,CMD_ENABLE_WER,L"Enable / Repair Crash Dumps (UAC)");AppendMenuW(m,MF_STRING,CMD_DISABLE_WER,L"Remove Crash Monitor Dump Settings (UAC)");AppendMenuW(m,MF_SEPARATOR,0,0);AppendMenuW(m,MF_STRING|(IsStartupEnabled()?MF_CHECKED:0),CMD_STARTUP,L"Start with Windows");AppendMenuW(m,MF_STRING,CMD_PAUSE,g_paused?L"Resume Monitoring":L"Pause Monitoring");AppendMenuW(m,MF_STRING|(g_minimizeToTray?MF_CHECKED:0),CMD_MINIMIZETRAY,L"Minimize to tray");AppendMenuW(m,MF_STRING|(g_closeXToTray?MF_CHECKED:0),CMD_CLOSEXTRAY,L"Close/X to tray (off = Exit App)");AppendMenuW(m,MF_STRING|(g_keepTrayTaskbar?MF_CHECKED:0),CMD_KEEPTRAYTASKBAR,L"Show tray icon with taskbar (both)");AppendMenuW(m,MF_STRING|(g_startMinimized?MF_CHECKED:0),CMD_STARTMINIMIZED,L"Start minimized on next launch");AppendMenuW(m,MF_STRING|(g_startPaused?MF_CHECKED:0),CMD_STARTPAUSED,L"Start paused on next launch");AppendMenuW(m,MF_STRING|(g_notificationsEnabled?MF_CHECKED:0),CMD_NOTIFICATIONS,L"Tray notifications");AppendMenuW(m,MF_SEPARATOR,0,0);AppendMenuW(m,MF_STRING,CMD_UNINSTALL,L"Uninstall Crash Monitor...");AppendMenuW(m,MF_STRING,CMD_EXIT,L"Exit App");POINT p;GetCursorPos(&p);SetForegroundWindow(hwnd);UINT c=TrackPopupMenu(m,TPM_RIGHTBUTTON|TPM_RETURNCMD,p.x,p.y,0,hwnd,NULLPTR);DestroyMenu(m);HandleTrayCommand(hwnd,c);}
static int ScaleMainValue(int v){return (v*g_mainScale+500)/1000;}
static void MoveMainControl(HWND c,int x,int y,int w,int h){if(c)MoveWindow(c,g_mainOffsetX+ScaleMainValue(x),g_mainOffsetY+ScaleMainValue(y),ScaleMainValue(w),ScaleMainValue(h),TRUE);}
static void ApplyMainFonts(){HWND a[]={g_header,g_subtitle,g_status,g_group,g_list,g_addBtn,g_toggleBtn,g_removeBtn,g_repairBtn,g_details,g_startupBox,g_pauseBox,g_minimizeTrayBox,g_keepTrayTaskbarBox,g_closeXTrayBox,g_startMinimizedBox,g_startPausedBox,g_notificationsBox,g_openDumpsBtn,g_openDataBtn,g_testDumpBtn,g_safeSelfTestBtn,g_exportReportBtn,g_resetLayoutBtn,g_displayBtn,g_exitBtn,g_footer};int n=(int)(sizeof(a)/sizeof(a[0]));for(int i=0;i<n;i++)if(a[i])SendMessageW(a[i],WM_SETFONT,(WPARAM)(a[i]==g_header?g_titleFont:g_font),TRUE);}
static void UpdateMainFonts(int scale){if(scale<520)scale=520;if(scale>1350)scale=1350;if(scale==g_mainFontScale)return;int normal=(16*scale+500)/1000;int title=(28*scale+500)/1000;if(normal<9)normal=9;if(title<16)title=16;HFONT nf=CreateFontW(-normal,0,0,0,FW_NORMAL,FALSE,FALSE,FALSE,DEFAULT_CHARSET,OUT_DEFAULT_PRECIS,CLIP_DEFAULT_PRECIS,CLEARTYPE_QUALITY,DEFAULT_PITCH|FF_DONTCARE,L"Segoe UI");HFONT nt=CreateFontW(-title,0,0,0,FW_SEMIBOLD,FALSE,FALSE,FALSE,DEFAULT_CHARSET,OUT_DEFAULT_PRECIS,CLIP_DEFAULT_PRECIS,CLEARTYPE_QUALITY,DEFAULT_PITCH|FF_DONTCARE,L"Segoe UI");if(!nf||!nt){if(nf)DeleteObject(nf);if(nt)DeleteObject(nt);return;}HFONT oldf=g_font,oldt=g_titleFont;g_font=nf;g_titleFont=nt;g_mainFontScale=scale;ApplyMainFonts();if(oldf)DeleteObject(oldf);if(oldt)DeleteObject(oldt);}
static void ClampDetailsHeight(){if(g_detailsHeight<70)g_detailsHeight=70;if(g_detailsHeight>270)g_detailsHeight=270;}
static void LayoutMain(HWND h){
 RECT r;if(!GetClientRect(h,&r))return;int cw=(int)(r.right-r.left),ch=(int)(r.bottom-r.top);if(cw<=0||ch<=0)return;
 const int baseW=1120,baseH=760;int sx=(cw*1000)/baseW,sy=(ch*1000)/baseH;int scale=sx<sy?sx:sy;if(scale>1350)scale=1350;if(scale<520)scale=520;g_mainScale=scale;UpdateMainFonts(scale);
 int usedW=ScaleMainValue(baseW),usedH=ScaleMainValue(baseH);g_mainOffsetX=(cw-usedW)/2;g_mainOffsetY=(ch-usedH)/2;if(g_mainOffsetX<0)g_mainOffsetX=0;if(g_mainOffsetY<0)g_mainOffsetY=0;
 int m=24,inner=baseW-2*m;int statusY=88,groupY=130;int groupH=430;int rightW=285,gap=18;int gx=m+16,gy=groupY+32;int listW=inner-rightW-gap-32;
 ClampDetailsHeight();int detailsBottom=groupY+groupH-16;int boundaryGap=10;int detailsH=g_detailsHeight;int detailsY=detailsBottom-detailsH;int listH=detailsY-gy-boundaryGap;const int minTopH=222;
 if(listH<minTopH){listH=minTopH;detailsY=gy+listH+boundaryGap;detailsH=detailsBottom-detailsY;if(detailsH<70)detailsH=70;g_detailsHeight=detailsH;}
 MoveMainControl(g_header,m,14,inner,40);MoveMainControl(g_subtitle,m,55,inner,26);MoveMainControl(g_status,m,statusY,inner,36);MoveMainControl(g_group,m,groupY,inner,groupH);
 MoveMainControl(g_list,gx,gy,listW,listH);int bx=gx+listW+gap;MoveMainControl(g_addBtn,bx,gy,rightW,36);MoveMainControl(g_toggleBtn,bx,gy+44,rightW,36);MoveMainControl(g_removeBtn,bx,gy+88,rightW,36);MoveMainControl(g_repairBtn,bx,gy+140,rightW,48);MoveMainControl(g_safeSelfTestBtn,bx,gy+196,rightW,40);
 MoveMainControl(g_details,gx,detailsY,inner-32,detailsH);
 int row1=576,row2=608,gapc=10,w1=245,w2=155,w3=180;int w4=inner-w1-w2-w3-3*gapc;MoveMainControl(g_startupBox,m,row1,w1,28);MoveMainControl(g_pauseBox,m+w1+gapc,row1,w2,28);MoveMainControl(g_minimizeTrayBox,m+w1+w2+2*gapc,row1,w3,28);MoveMainControl(g_keepTrayTaskbarBox,m+w1+w2+w3+3*gapc,row1,w4,28);
 int q1=250,q2=210,q3=200,q4=inner-q1-q2-q3-3*gapc;MoveMainControl(g_closeXTrayBox,m,row2,q1,28);MoveMainControl(g_startMinimizedBox,m+q1+gapc,row2,q2,28);MoveMainControl(g_startPausedBox,m+q1+q2+2*gapc,row2,q3,28);MoveMainControl(g_notificationsBox,m+q1+q2+q3+3*gapc,row2,q4,28);
 int by=646,bg=8,bw=(inner-6*bg)/7;MoveMainControl(g_openDumpsBtn,m,by,bw,38);MoveMainControl(g_openDataBtn,m+bw+bg,by,bw,38);MoveMainControl(g_testDumpBtn,m+2*(bw+bg),by,bw,38);MoveMainControl(g_exportReportBtn,m+3*(bw+bg),by,bw,38);MoveMainControl(g_displayBtn,m+4*(bw+bg),by,bw,38);MoveMainControl(g_resetLayoutBtn,m+5*(bw+bg),by,bw,38);MoveMainControl(g_exitBtn,m+6*(bw+bg),by,bw,38);MoveMainControl(g_footer,m,702,inner,32);
}

static void SetDetailsHeightFromDrag(int deltaPixels){if(!deltaPixels)return;int logical=(deltaPixels*1000)/g_mainScale;if(logical==0)logical=deltaPixels>0?1:-1;g_detailsHeight-=logical;ClampDetailsHeight();LayoutMain(g_hwnd);}
static LRESULT CALLBACK DetailsProc(HWND h,UINT m,WPARAM w,LPARAM l){
 if(m==WM_NCHITTEST){
  LRESULT hit=g_oldDetailsProc?CallWindowProcW(g_oldDetailsProc,h,m,w,l):DefWindowProcW(h,m,w,l);
  RECT wr;POINT p;if(GetWindowRect(h,&wr)&&GetCursorPos(&p)){int edge=ScaleMainValue(8);if(edge<4)edge=4;if(p.y>=wr.top&&p.y<=wr.top+edge)return HTTOP;}
  return hit;
 }
 if(m==WM_SETCURSOR){UINT hit=(UINT)(l&0xFFFFu);if(hit==HTTOP||g_detailsDragging){SetCursor(LoadCursorW(0,ResPtr(IDC_SIZENS)));return TRUE;}}
 if(m==WM_NCLBUTTONDOWN&&((UINT)w)==HTTOP){POINT p;if(GetCursorPos(&p)){g_detailsLastY=p.y;g_detailsDragging=TRUE;SetCapture(h);SetCursor(LoadCursorW(0,ResPtr(IDC_SIZENS)));}return 0;}
 if(m==WM_LBUTTONDOWN){POINT p;if(GetCursorPos(&p)){RECT wr;if(GetWindowRect(h,&wr)){int edge=ScaleMainValue(8);if(edge<4)edge=4;if(p.y<=wr.top+edge){g_detailsLastY=p.y;g_detailsDragging=TRUE;SetCapture(h);SetCursor(LoadCursorW(0,ResPtr(IDC_SIZENS)));return 0;}}}}
 if((m==WM_MOUSEMOVE||m==WM_NCMOUSEMOVE)&&g_detailsDragging){SetCursor(LoadCursorW(0,ResPtr(IDC_SIZENS)));POINT p;if(GetCursorPos(&p)){int dy=(int)(p.y-g_detailsLastY);if(dy){g_detailsLastY=p.y;SetDetailsHeightFromDrag(dy);}}return 0;}
 if((m==WM_LBUTTONUP||m==WM_NCLBUTTONUP)&&g_detailsDragging){g_detailsDragging=FALSE;ReleaseCapture();SaveDetailsHeightSetting();return 0;}
 if((m==WM_CANCELMODE||m==WM_CAPTURECHANGED)&&g_detailsDragging){g_detailsDragging=FALSE;SaveDetailsHeightSetting();return 0;}
 return g_oldDetailsProc?CallWindowProcW(g_oldDetailsProc,h,m,w,l):DefWindowProcW(h,m,w,l);
}
static LRESULT CALLBACK MainWndProc(HWND h,UINT m,WPARAM w,LPARAM l){if(g_taskbarCreatedMsg&&m==g_taskbarCreatedMsg){g_taskbarRecoveryCount++;BOOL needTray=g_trayOnly||g_hiddenToTray||g_keepTrayTaskbar;g_trayVisible=FALSE;if(needTray){AddTrayIcon();SetTrayState(g_currentState,g_currentActive);AppendLog(g_trayVisible?L"Tray icon restored after Explorer/taskbar restart":L"Tray icon restore after Explorer/taskbar restart FAILED; timer retry enabled");}return 0;}if(m==WM_COMMAND){UINT id=LowWord(w),code=HighWord(w);if(id==IDC_ADD&&code==BN_CLICKED)AddFromUi();else if(id==IDC_REMOVE&&code==BN_CLICKED)RemoveTargetFromUi(SelectedTarget());else if(id==IDC_TOGGLE&&code==BN_CLICKED){int i=SelectedTarget();if(i>=0){ToggleTargetWithWer(i);RefreshProgramList();UpdateSelectionDetails();}}else if(id==IDC_REPAIR&&code==BN_CLICKED)RunElevatedHelper(TRUE);else if(id==IDC_OPEN_DUMPS&&code==BN_CLICKED)ShellExecuteW(h,L"open",g_dumpRoot,0,0,SW_SHOWNORMAL);else if(id==IDC_OPEN_DATA&&code==BN_CLICKED)ShellExecuteW(h,L"open",g_baseDir,0,0,SW_SHOWNORMAL);else if(id==IDC_TEST_DUMP&&code==BN_CLICKED)TestSelectedDump();else if(id==IDC_SAFE_SELF_TEST&&code==BN_CLICKED)LaunchSafeSelfTest();else if(id==IDC_EXPORT_REPORT&&code==BN_CLICKED)ExportDiagnosticReport();else if(id==IDC_RESET_LAYOUT&&code==BN_CLICKED)ResetWindowLayout();else if(id==IDC_STARTUP&&code==BN_CLICKED){BOOL on=SendMessageW(g_startupBox,BM_GETCHECK,0,0)==BST_CHECKED;ApplyStartupSetting(on,TRUE);}else if(id==IDC_PAUSE&&code==BN_CLICKED){ApplyPausedState(SendMessageW(g_pauseBox,BM_GETCHECK,0,0)==BST_CHECKED);}else if(id==IDC_MINIMIZETRAY&&code==BN_CLICKED){ApplyMinimizeToTraySetting(SendMessageW(g_minimizeTrayBox,BM_GETCHECK,0,0)==BST_CHECKED,TRUE);}else if(id==IDC_KEEPTRAYTASKBAR&&code==BN_CLICKED){ApplyKeepTrayTaskbarSetting(SendMessageW(g_keepTrayTaskbarBox,BM_GETCHECK,0,0)==BST_CHECKED,TRUE,TRUE);}else if(id==IDC_CLOSEXTRAY&&code==BN_CLICKED){ApplyCloseXToTraySetting(SendMessageW(g_closeXTrayBox,BM_GETCHECK,0,0)==BST_CHECKED,TRUE);}else if(id==IDC_STARTMINIMIZED&&code==BN_CLICKED){ApplyStartMinimizedSetting(SendMessageW(g_startMinimizedBox,BM_GETCHECK,0,0)==BST_CHECKED,TRUE);}else if(id==IDC_STARTPAUSED&&code==BN_CLICKED){ApplyStartPausedSetting(SendMessageW(g_startPausedBox,BM_GETCHECK,0,0)==BST_CHECKED,TRUE);}else if(id==IDC_NOTIFICATIONS&&code==BN_CLICKED){ApplyNotificationsSetting(SendMessageW(g_notificationsBox,BM_GETCHECK,0,0)==BST_CHECKED,TRUE);}else if(id==IDC_DISPLAYMODE&&code==BN_CLICKED){if(g_trayOnly||g_hiddenToTray)MoveToTaskbarMode();else MoveToTrayMode();}else if(id==IDC_EXITAPP&&code==BN_CLICKED)RequestExit(h);else if(id==IDC_PROGRAMS&&(code==LBN_SELCHANGE||code==LBN_DBLCLK)){UpdateSelectionDetails();if(code==LBN_DBLCLK){int i=SelectedTarget();if(i>=0){ToggleTargetWithWer(i);RefreshProgramList();UpdateSelectionDetails();}}}return 0;}if(m==WM_SIZE){g_windowMinimized=((UINT)w==SIZE_MINIMIZED);if(g_windowMinimized&&g_minimizeToTray){MinimizeIntoTray();return 0;}LayoutMain(h);return 0;}if(m==WM_EXITSIZEMOVE){SaveCurrentWindowRect();return 0;}if(m==WM_GETMINMAXINFO){MINMAXINFO* mm=(MINMAXINFO*)l;mm->ptMinTrackSize.x=680;mm->ptMinTrackSize.y=500;return 0;}if(m==WM_TRAY){if((UINT)l==WM_RBUTTONUP||(UINT)l==WM_CONTEXTMENU)ShowTrayMenu(h);else if((UINT)l==WM_LBUTTONUP){ULONGLONG now=GetTickCount64();UINT dc=GetDoubleClickTime();if(!dc)dc=500;if(!g_lastTrayClickTick||now-g_lastTrayClickTick>dc){g_lastTrayClickTick=now;RevealExistingWindow();}}else if((UINT)l==WM_LBUTTONDBLCLK){return 0;}return 0;}if(m==WM_STATE){SetTrayState((int)w,(DWORD)l);return 0;}if(m==WM_CAPTURED){SetTrayState(STATE_CAPTURED,0);WCHAR t[256];wsprintfW(t,L"Crash Monitor saved/detected a dump: %s",g_lastCapturedFile);Balloon(L"Diagnostic dump captured",t,NIIF_ERROR);RefreshProgramList();return 0;}if(m==WM_TESTDONE){if(g_testDumpBtn){EnableWindow(g_testDumpBtn,TRUE);SetWindowTextW(g_testDumpBtn,L"Test Selected Dump");}if(w){if(g_lastShareCompressed){if(g_lastShareParts>1)MessageBoxW(h,L"Full diagnostic test dump created successfully and losslessly compressed.\n\nThe compressed archive was still over the Discord Nitro upload size, so Crash Monitor split it into numbered parts. Send all numbered parts together. The REASSEMBLE .cmd rebuilds the ZIP, which extracts back to the complete original .dmp.\n\nUse Open Crash Folder to see them.",L"Crash Monitor",MB_OK|MB_ICONINFORMATION);else MessageBoxW(h,L"Full diagnostic test dump created successfully and losslessly compressed to ZIP.\n\nExtracting the ZIP restores the complete original .dmp.\n\nUse Open Crash Folder to see it.",L"Crash Monitor",MB_OK|MB_ICONINFORMATION);}else MessageBoxW(h,L"The full diagnostic dump was created, but automatic sharing compression did not finish successfully.\n\nThe original .dmp was kept so no dump data was lost. Check monitor.log for the compression error.",L"Crash Monitor",MB_OK|MB_ICONWARNING);}else MessageBoxW(h,L"The test dump could not be created. Check monitor.log for the Windows error code.",L"Crash Monitor",MB_OK|MB_ICONERROR);return 0;}if(m==WM_SELFTESTPROGRESS){LONG idx=0,total=39;WCHAR p[420];AcquireSRWLockShared(&g_safeSelfTestProgressLock);idx=g_safeSelfTestProgressIndex;total=g_safeSelfTestProgressTotal;CopyWide(p,420,g_safeSelfTestProgressText);ReleaseSRWLockShared(&g_safeSelfTestProgressLock);if(g_safeSelfTestBtn){WCHAR bt[96];if(idx>0)wsprintfW(bt,L"Self-Test %d/%d running...",idx,total);else lstrcpyW(bt,L"Safe Self-Test running...");SetWindowTextW(g_safeSelfTestBtn,bt);}UpdateStatusText();return 0;}if(m==WM_SELFTESTDONE){DWORD code=(DWORD)w;g_safeSelfTestRunning=0;if(g_safeSelfTestThread){CloseHandle(g_safeSelfTestThread);g_safeSelfTestThread=0;}if(g_safeSelfTestBtn){EnableWindow(g_safeSelfTestBtn,TRUE);SetWindowTextW(g_safeSelfTestBtn,L"Run Safe Self-Test...");}WCHAR local[MAX_PATH*2];ZeroMem(local,sizeof(local));GetEnvironmentVariableW(L"LOCALAPPDATA",local,MAX_PATH*2);WCHAR report[MAX_PATH*2];wsprintfW(report,L"%s\\Crash Monitor\\CrashMonitor-SafeSelfTest-v4.2-Build12.txt",local);WCHAR progressFile[MAX_PATH*2];wsprintfW(progressFile,L"%s\\Crash Monitor\\CrashMonitor-SafeSelfTest-v4.2-Build12.progress",local);WCHAR msg[1000];if(code==0){lstrcpyW(msg,L"Safe Self-Test finished normally with no automated FAIL result.\n\nThe report will open now. Check the totals line for PASS / FAIL / NOT TESTED counts.");AppendLog(L"Safe Self-Test finished normally exit=0");}else if(code==1){lstrcpyW(msg,L"Safe Self-Test finished, but one or more automated checks FAILED.\n\nThe report will open now so you can see the exact failing check.");AppendLog(L"Safe Self-Test finished with FAIL result");}else if(code==CM_SELFTEST_TIMEOUT_CODE){lstrcpyW(msg,L"Safe Self-Test was stopped because it made no progress for 180 seconds.\n\nA partial report will open now. Its last RUNNING/PASS/FAIL line identifies the test that hung or timed out.");AppendLog(L"Safe Self-Test timed out after 180 seconds without progress; child terminated; partial report retained");}else if(code==CM_SELFTEST_LAUNCH_FAILED_CODE){lstrcpyW(msg,L"Safe Self-Test could not start its isolated test process.\n\nCheck monitor.log and the report folder for details.");AppendLog(L"Safe Self-Test child process launch FAILED");}else{wsprintfW(msg,L"Safe Self-Test did not finish normally.\n\nChild exit code: 0x%08X\n\nA partial report will open if one was created. Its last RUNNING/PASS/FAIL line identifies where the run stopped.",code);AppendLog(L"Safe Self-Test child ended abnormally; partial report retained");}DeleteFileW(progressFile);AcquireSRWLockExclusive(&g_safeSelfTestProgressLock);g_safeSelfTestProgressText[0]=0;g_safeSelfTestProgressIndex=0;ReleaseSRWLockExclusive(&g_safeSelfTestProgressLock);UpdateStatusText();MessageBoxW(h,msg,L"Crash Monitor Safe Self-Test",MB_OK|((code==0)?MB_ICONINFORMATION:MB_ICONERROR));if(FileExists(report))ShellExecuteW(h,L"open",report,0,0,SW_SHOWNORMAL);return 0;}if(m==WM_CONFIG_CHANGED){RefreshProgramList();UpdateSelectionDetails();return 0;}if(m==WM_TIMER){if((g_trayOnly||g_hiddenToTray||g_keepTrayTaskbar)&&!g_trayVisible){AddTrayIcon();if(g_trayVisible)SetTrayState(g_currentState,g_currentActive);}RefreshProgramList();UpdateSelectionDetails();UpdateStatusText();return 0;}if(m==WM_SHOW_EXISTING){RevealExistingWindow();return 0;}if(m==WM_CLOSE){HandleMainClose(h);return 0;}if(m==WM_DESTROY){SaveCurrentWindowRect();g_exitFlag=1;g_obsDebugStop=1;KillTimer(h,1);if(g_worker)WaitForSingleObject(g_worker,4000);if(g_obsDebugThread){WaitForSingleObject(g_obsDebugThread,2500);CloseHandle(g_obsDebugThread);g_obsDebugThread=0;}if(g_safeSelfTestThread){CloseHandle(g_safeSelfTestThread);g_safeSelfTestThread=0;}RemoveTrayIcon();PostQuitMessage(0);return 0;}return DefWindowProcW(h,m,w,l);}
static volatile LONG g_selfTestWindowTimedOut=0;
static LRESULT CALLBACK SelfTestExitWndProc(HWND h,UINT m,WPARAM w,LPARAM l){if(m==WM_TIMER&&w==99){g_selfTestWindowTimedOut=1;KillTimer(h,99);DestroyWindow(h);return 0;}return MainWndProc(h,m,w,l);}
static int RunExitBehaviorChild(BOOL viaClose){g_selfTestWindowTimedOut=0;g_closeXToTray=FALSE;g_hiddenToTray=TRUE;g_windowMinimized=FALSE;g_worker=0;g_obsDebugThread=0;g_exitFlag=0;WNDCLASSEXW wc;ZeroMem(&wc,sizeof(wc));wc.cbSize=sizeof(wc);wc.lpfnWndProc=SelfTestExitWndProc;wc.hInstance=(HINSTANCE)GetModuleHandleW(0);wc.hCursor=LoadCursorW(0,ResPtr(IDC_ARROW));wc.hbrBackground=(HANDLE)(ULONG_PTR)(COLOR_WINDOW+1);wc.lpszClassName=viaClose?L"CrashMonitorSelfTestCloseClass":L"CrashMonitorSelfTestExitClass";if(!RegisterClassExW(&wc))return 2;g_hwnd=CreateWindowExW(0,wc.lpszClassName,L"Crash Monitor isolated exit self-test",WS_OVERLAPPEDWINDOW,0,0,700,520,0,0,wc.hInstance,NULLPTR);if(!g_hwnd)return 2;SetTimer(g_hwnd,99,1500,NULLPTR);if(viaClose)PostMessageW(g_hwnd,WM_CLOSE,0,0);else PostMessageW(g_hwnd,WM_COMMAND,(WPARAM)IDC_EXITAPP,0);MSG msg;while(GetMessageW(&msg,0,0,0)>0){TranslateMessage(&msg);DispatchMessageW(&msg);}return g_selfTestWindowTimedOut?3:0;}
static void CreateMainControls(HWND h){
 g_header=MakeControl(L"STATIC",L"Crash Monitor",SS_LEFT|SS_NOPREFIX,24,18,700,40,h,IDC_HEADER,TRUE);g_subtitle=MakeControl(L"STATIC",L"WER for all apps; OBS uses live-safe process snapshots for enhanced dumps.",SS_LEFT|SS_NOPREFIX,25,60,1000,26,h,0,FALSE);g_status=MakeControl(L"STATIC",L"Starting...",SS_LEFT|SS_NOPREFIX,25,96,780,36,h,IDC_STATUS,FALSE);g_group=MakeControl(L"BUTTON",L"Monitored programs",BS_GROUPBOX,20,135,820,340,h,0,FALSE);
 g_list=CreateWindowExW(WS_EX_CLIENTEDGE,L"LISTBOX",L"",WS_CHILD|WS_VISIBLE|WS_TABSTOP|WS_VSCROLL|LBS_NOTIFY|LBS_NOINTEGRALHEIGHT,40,168,520,220,h,(HMENU)(ULONG_PTR)IDC_PROGRAMS,(HINSTANCE)GetModuleHandleW(0),NULLPTR);SetControlFont(g_list,FALSE);g_addBtn=MakeControl(L"BUTTON",L"Add Program...",BS_PUSHBUTTON|WS_TABSTOP,580,168,260,36,h,IDC_ADD,FALSE);g_toggleBtn=MakeControl(L"BUTTON",L"Enable / Disable",BS_PUSHBUTTON|WS_TABSTOP,580,212,260,36,h,IDC_TOGGLE,FALSE);g_removeBtn=MakeControl(L"BUTTON",L"Remove",BS_PUSHBUTTON|WS_TABSTOP,580,256,260,36,h,IDC_REMOVE,FALSE);g_repairBtn=MakeControl(L"BUTTON",L"Enable / Repair Crash Dumps",BS_PUSHBUTTON|WS_TABSTOP,580,308,285,48,h,IDC_REPAIR,FALSE);g_safeSelfTestBtn=MakeControl(L"BUTTON",L"Run Safe Self-Test...",BS_PUSHBUTTON|WS_TABSTOP,580,364,285,40,h,IDC_SAFE_SELF_TEST,FALSE);
 g_details=CreateWindowExW(WS_EX_CLIENTEDGE,L"EDIT",L"",WS_CHILD|WS_VISIBLE|WS_TABSTOP|WS_VSCROLL|ES_MULTILINE|ES_READONLY|ES_AUTOVSCROLL,40,416,800,130,h,(HMENU)(ULONG_PTR)IDC_DETAILS,(HINSTANCE)GetModuleHandleW(0),NULLPTR);SetControlFont(g_details,FALSE);g_oldDetailsProc=(WNDPROC)SetWindowLongPtrW(g_details,GWLP_WNDPROC,(LONG_PTR)DetailsProc);
 g_startupBox=MakeControl(L"BUTTON",L"Start with Windows",BS_AUTOCHECKBOX|WS_TABSTOP,28,500,245,30,h,IDC_STARTUP,FALSE);g_pauseBox=MakeControl(L"BUTTON",L"Pause monitoring",BS_AUTOCHECKBOX|WS_TABSTOP,360,500,180,30,h,IDC_PAUSE,FALSE);g_minimizeTrayBox=MakeControl(L"BUTTON",L"Minimize to tray",BS_AUTOCHECKBOX|WS_TABSTOP,555,500,185,30,h,IDC_MINIMIZETRAY,FALSE);g_keepTrayTaskbarBox=MakeControl(L"BUTTON",L"Show tray icon with taskbar (both)",BS_AUTOCHECKBOX|WS_TABSTOP,750,500,280,30,h,IDC_KEEPTRAYTASKBAR,FALSE);g_closeXTrayBox=MakeControl(L"BUTTON",L"Close/X to tray (off = Exit App)",BS_AUTOCHECKBOX|WS_TABSTOP,28,532,250,30,h,IDC_CLOSEXTRAY,FALSE);g_startMinimizedBox=MakeControl(L"BUTTON",L"Start minimized next launch",BS_AUTOCHECKBOX|WS_TABSTOP,290,532,210,30,h,IDC_STARTMINIMIZED,FALSE);g_startPausedBox=MakeControl(L"BUTTON",L"Start paused next launch",BS_AUTOCHECKBOX|WS_TABSTOP,510,532,200,30,h,IDC_STARTPAUSED,FALSE);g_notificationsBox=MakeControl(L"BUTTON",L"Tray notifications",BS_AUTOCHECKBOX|WS_TABSTOP,720,532,180,30,h,IDC_NOTIFICATIONS,FALSE);g_openDumpsBtn=MakeControl(L"BUTTON",L"Open Crash Folder",BS_PUSHBUTTON|WS_TABSTOP,28,548,190,38,h,IDC_OPEN_DUMPS,FALSE);g_openDataBtn=MakeControl(L"BUTTON",L"Open Data / Logs",BS_PUSHBUTTON|WS_TABSTOP,230,548,190,38,h,IDC_OPEN_DATA,FALSE);g_testDumpBtn=MakeControl(L"BUTTON",L"Test Dump",BS_PUSHBUTTON|WS_TABSTOP,432,548,190,38,h,IDC_TEST_DUMP,FALSE);g_exportReportBtn=MakeControl(L"BUTTON",L"Export Report",BS_PUSHBUTTON|WS_TABSTOP,520,548,150,38,h,IDC_EXPORT_REPORT,FALSE);g_resetLayoutBtn=MakeControl(L"BUTTON",L"Reset Layout",BS_PUSHBUTTON|WS_TABSTOP,680,548,150,38,h,IDC_RESET_LAYOUT,FALSE);g_displayBtn=MakeControl(L"BUTTON",g_trayOnly?L"Move to Taskbar":L"Move to Tray",BS_PUSHBUTTON|WS_TABSTOP,432,548,190,38,h,IDC_DISPLAYMODE,FALSE);g_exitBtn=MakeControl(L"BUTTON",L"Exit App",BS_PUSHBUTTON|WS_TABSTOP,634,548,190,38,h,IDC_EXITAPP,FALSE);g_footer=MakeControl(L"STATIC",L"v4.2 Build 12 • More automated release checks • OBS PSS + lossless ZIP",SS_LEFT|SS_NOPREFIX,28,600,1000,32,h,0,FALSE);LayoutMain(h);RefreshProgramList();UpdateSelectionDetails();UpdateStatusText();}

static BOOL DoInstall(HWND h,BOOL startup,BOOL launch,BOOL startMenu,BOOL desktop){WCHAR local[MAX_PATH*2];ZeroMem(local,sizeof(local));GetEnvironmentVariableW(L"LOCALAPPDATA",local,MAX_PATH*2);WCHAR parent[MAX_PATH*2];lstrcpyW(parent,local);lstrcatW(parent,L"\\Programs");EnsureDir(parent);EnsureDir(g_installDir);if(lstrcmpiW(g_exePath,g_installExe)!=0){if(!CopyInstallImageForUpdate(g_exePath,g_installExe)){MessageBoxW(h,L"Setup could not copy Crash Monitor to the install folder.\n\nIf an older Crash Monitor is running, exit it and try setup again.",L"Crash Monitor Setup",MB_OK|MB_ICONERROR);return FALSE;}}if(startup)SetStartupPath(g_installExe,TRUE);else SetStartupPath(g_installExe,FALSE);RegisterAppPath();if(!RegisterUninstallEntry()){MessageBoxW(h,L"Crash Monitor was copied, but Windows could not register it in Settings > Apps. Setup did not finish cleanly.",L"Crash Monitor Setup",MB_OK|MB_ICONERROR);return FALSE;}BOOL links=SetShortcuts(startMenu,desktop);if(!links)MessageBoxW(h,L"Crash Monitor installed, but Windows could not create one or more shortcuts. You can run Update / Repair again.",L"Crash Monitor Setup",MB_OK|MB_ICONWARNING);if(launch)ShellExecuteW(h,L"open",g_installExe,L"--app",0,SW_SHOWNORMAL);return TRUE;}

static void LayoutSetup(HWND h){RECT r;if(!GetClientRect(h,&r))return;int cw=(int)(r.right-r.left),ch=(int)(r.bottom-r.top);if(cw<780)cw=780;if(ch<610)ch=610;int m=30;int inner=cw-2*m;int headerX=112;MoveWindow(g_setupIcon,m+8,28,56,56,TRUE);MoveWindow(g_setupTitle,headerX,22,cw-headerX-m,44,TRUE);MoveWindow(g_setupSubtitle,headerX,68,cw-headerX-m,48,TRUE);int groupY=128;int groupH=ch-300;if(groupH<300)groupH=300;MoveWindow(g_setupGroup,m,groupY,inner,groupH,TRUE);int x=m+22,w=inner-44;MoveWindow(g_setupLocationLabel,x,groupY+30,w,24,TRUE);MoveWindow(g_setupPath,x,groupY+56,w,32,TRUE);MoveWindow(g_setupStartMenu,x,groupY+105,w,30,TRUE);MoveWindow(g_setupDesktop,x,groupY+142,w,30,TRUE);MoveWindow(g_setupStartup,x,groupY+179,w,30,TRUE);MoveWindow(g_setupLaunch,x,groupY+216,w,30,TRUE);MoveWindow(g_setupNote,x,groupY+255,w,28,TRUE);int statusY=groupY+groupH+18;MoveWindow(g_setupStatus,m+5,statusY,inner-10,54,TRUE);int by=ch-66;int cancelW=130,installW=210,gap=14;MoveWindow(g_setupCancel,cw-m-cancelW,by,cancelW,42,TRUE);MoveWindow(g_setupInstall,cw-m-cancelW-gap-installW,by,installW,42,TRUE);UpdateWindow(g_setupInstall);}
static LRESULT CALLBACK SetupWndProc(HWND h,UINT m,WPARAM w,LPARAM l){if(m==WM_COMMAND){UINT id=LowWord(w),code=HighWord(w);if(code==BN_CLICKED&&id==IDC_SETUP_CANCEL){DestroyWindow(h);return 0;}if(code==BN_CLICKED&&id==IDC_SETUP_INSTALL){BOOL s=SendMessageW(g_setupStartup,BM_GETCHECK,0,0)==BST_CHECKED;BOOL q=SendMessageW(g_setupLaunch,BM_GETCHECK,0,0)==BST_CHECKED;BOOL sm=SendMessageW(g_setupStartMenu,BM_GETCHECK,0,0)==BST_CHECKED;BOOL ds=SendMessageW(g_setupDesktop,BM_GETCHECK,0,0)==BST_CHECKED;EnableWindow(g_setupInstall,FALSE);SetWindowTextW(g_setupStatus,L"Installing Crash Monitor...");if(DoInstall(h,s,q,sm,ds)){SetWindowTextW(g_setupStatus,L"Installed successfully. Windows Apps/Search registration created.");MessageBoxW(h,L"Crash Monitor was installed successfully.\n\nIt is available in Windows Search / Start and Settings > Apps. The app window automatically scales to fit when resized. The top edge of the program-info box is the resize divider and uses the up/down cursor. Taskbar, tray, or both modes are supported.",L"Crash Monitor Setup",MB_OK|MB_ICONINFORMATION);DestroyWindow(h);}else{SetWindowTextW(g_setupStatus,L"Installation did not finish. Close any older Crash Monitor instance and try again.");EnableWindow(g_setupInstall,TRUE);}return 0;}}if(m==WM_SIZE){LayoutSetup(h);return 0;}if(m==WM_GETMINMAXINFO){MINMAXINFO* mm=(MINMAXINFO*)l;mm->ptMinTrackSize.x=860;mm->ptMinTrackSize.y=680;return 0;}if(m==WM_CLOSE){DestroyWindow(h);return 0;}if(m==WM_DESTROY){PostQuitMessage(0);return 0;}if(m==0x0001u){g_setupTitle=MakeControl(L"STATIC",L"Crash Monitor",SS_LEFT|SS_NOPREFIX,112,26,620,44,h,0,TRUE);g_setupSubtitle=MakeControl(L"STATIC",L"Reliable external crash reporting for OBS and other Windows apps.",SS_LEFT|SS_NOPREFIX,112,72,650,48,h,0,FALSE);g_setupIcon=MakeControl(L"STATIC",L"",SS_ICON,38,31,56,56,h,IDC_SETUP_ICON,FALSE);SendMessageW(g_setupIcon,STM_SETICON,(WPARAM)g_appIcon,0);g_setupGroup=MakeControl(L"BUTTON",L"Install options",BS_GROUPBOX,30,128,760,300,h,0,FALSE);g_setupLocationLabel=MakeControl(L"STATIC",L"Install location:",SS_LEFT|SS_NOPREFIX,52,158,200,24,h,0,FALSE);g_setupPath=CreateWindowExW(WS_EX_CLIENTEDGE,L"EDIT",g_installExe,WS_CHILD|WS_VISIBLE|ES_READONLY|ES_AUTOHSCROLL,52,184,710,32,h,(HMENU)(ULONG_PTR)IDC_SETUP_PATH,(HINSTANCE)GetModuleHandleW(0),NULLPTR);SetControlFont(g_setupPath,FALSE);g_setupStartMenu=MakeControl(L"BUTTON",L"Create Start Menu shortcut (makes Crash Monitor appear in Windows Search)",BS_AUTOCHECKBOX|WS_TABSTOP,52,233,710,30,h,IDC_SETUP_STARTMENU,FALSE);SendMessageW(g_setupStartMenu,BM_SETCHECK,BST_CHECKED,0);g_setupDesktop=MakeControl(L"BUTTON",L"Create Desktop shortcut",BS_AUTOCHECKBOX|WS_TABSTOP,52,270,710,30,h,IDC_SETUP_DESKTOP,FALSE);SendMessageW(g_setupDesktop,BM_SETCHECK,BST_CHECKED,0);g_setupStartup=MakeControl(L"BUTTON",L"Start Crash Monitor automatically with Windows",BS_AUTOCHECKBOX|WS_TABSTOP,52,307,710,30,h,IDC_SETUP_STARTUP,FALSE);SendMessageW(g_setupStartup,BM_SETCHECK,BST_CHECKED,0);g_setupLaunch=MakeControl(L"BUTTON",L"Launch Crash Monitor after setup",BS_AUTOCHECKBOX|WS_TABSTOP,52,344,710,30,h,IDC_SETUP_LAUNCH,FALSE);SendMessageW(g_setupLaunch,BM_SETCHECK,BST_CHECKED,0);g_setupNote=MakeControl(L"STATIC",L"Shortcuts do not assign any global keyboard hotkeys.",SS_LEFT|SS_NOPREFIX,52,383,710,28,h,0,FALSE);g_setupStatus=MakeControl(L"STATIC",L"Crash Monitor 4.2 Build 12 ready. Automated release testing now covers staged Update/Repair preservation, real Start Menu shortcut launch, and guarded Explorer/taskbar restart recovery.",SS_LEFT|SS_NOPREFIX,35,455,760,54,h,IDC_SETUP_STATUS,FALSE);g_setupInstall=MakeControl(L"BUTTON",FileExists(g_installExe)?L"Update / Repair":L"Install",BS_PUSHBUTTON|WS_TABSTOP,450,540,210,42,h,IDC_SETUP_INSTALL,FALSE);g_setupCancel=MakeControl(L"BUTTON",L"Cancel",BS_PUSHBUTTON|WS_TABSTOP,665,540,130,42,h,IDC_SETUP_CANCEL,FALSE);LayoutSetup(h);return 0;}return DefWindowProcW(h,m,w,l);}
static int RunSetup(HINSTANCE inst){WNDCLASSEXW wc;ZeroMem(&wc,sizeof(wc));wc.cbSize=sizeof(wc);wc.lpfnWndProc=SetupWndProc;wc.hInstance=inst;wc.hIcon=g_appIcon;wc.hIconSm=g_appIcon;wc.hCursor=LoadCursorW(0,ResPtr(IDC_ARROW));wc.hbrBackground=(HANDLE)(ULONG_PTR)(COLOR_WINDOW+1);wc.lpszClassName=L"CrashMonitorSetupClass411";if(!RegisterClassExW(&wc))return 1;HWND win=CreateWindowExW(WS_EX_APPWINDOW,L"CrashMonitorSetupClass411",L"Crash Monitor Setup",WS_OVERLAPPEDWINDOW|WS_VISIBLE,120,60,940,730,0,0,inst,NULLPTR);if(!win)return 1;SendMessageW(win,WM_SETICON,ICON_BIG,(LPARAM)g_appIcon);SendMessageW(win,WM_SETICON,ICON_SMALL,(LPARAM)g_appIcon);ShowWindow(win,SW_SHOW);UpdateWindow(win);MSG msg;while(GetMessageW(&msg,0,0,0)>0){TranslateMessage(&msg);DispatchMessageW(&msg);}return 0;}

static int RunApp(HINSTANCE inst){g_taskbarCreatedMsg=RegisterWindowMessageW(L"TaskbarCreated");HANDLE mutex=CreateMutexW(NULLPTR,FALSE,L"Local\\Crash_Monitor_31");if(mutex&&GetLastError()==ERROR_ALREADY_EXISTS){HWND existing=FindWindowW(L"CrashMonitorMainClass411",(LPCWSTR)0);if(existing){PostMessageW(existing,WM_SHOW_EXISTING,0,0);SetForegroundWindow(existing);}else MessageBoxW(0,L"Crash Monitor is already running.",L"Crash Monitor",MB_OK|MB_ICONINFORMATION);CloseHandle(mutex);return 0;}WNDCLASSEXW wc;ZeroMem(&wc,sizeof(wc));wc.cbSize=sizeof(wc);wc.lpfnWndProc=MainWndProc;wc.hInstance=inst;wc.hIcon=g_appIcon;wc.hIconSm=g_appIcon;wc.hCursor=LoadCursorW(0,ResPtr(IDC_ARROW));wc.hbrBackground=(HANDLE)(ULONG_PTR)(COLOR_WINDOW+1);wc.lpszClassName=L"CrashMonitorMainClass411";if(!RegisterClassExW(&wc))return 1;g_trayOnly=GetTrayOnlySetting();g_minimizeToTray=GetMinimizeToTraySetting();g_keepTrayTaskbar=GetKeepTrayTaskbarSetting();g_closeXToTray=GetCloseXToTraySetting();g_startMinimized=GetStartMinimizedSetting();g_startPaused=GetStartPausedSetting();g_notificationsEnabled=GetNotificationsSetting();g_paused=g_startPaused?1:0;g_detailsHeight=GetDetailsHeightSetting();RECT wr;if(!GetSavedWindowRectSetting(&wr))PrimaryDefaultRect(&wr);ClampRectToVisibleWorkArea(&wr);g_hwnd=CreateWindowExW(WS_EX_APPWINDOW,L"CrashMonitorMainClass411",L"Crash Monitor",WS_OVERLAPPEDWINDOW,wr.left,wr.top,wr.right-wr.left,wr.bottom-wr.top,0,0,inst,NULLPTR);if(!g_hwnd)return 1;SendMessageW(g_hwnd,WM_SETICON,ICON_BIG,(LPARAM)g_appIcon);SendMessageW(g_hwnd,WM_SETICON,ICON_SMALL,(LPARAM)g_appIcon);CreateMainControls(g_hwnd);ZeroMem(&g_nid,sizeof(g_nid));g_nid.cbSize=sizeof(g_nid);g_nid.hWnd=g_hwnd;g_nid.uID=1;g_nid.uCallbackMessage=WM_TRAY;g_nid.hIcon=g_appIcon;CopyWide(g_nid.szTip,128,L"Crash Monitor - starting");if(g_trayOnly||g_keepTrayTaskbar||g_startMinimized)AddTrayIcon();AppendLog(L"Crash Monitor 4.2 Build 12 started; Build 10 split fixes preserved; automated release test now covers staged Update/Repair preservation, actual Start Menu shortcut launch, guarded Explorer/taskbar restart recovery, live progress + hang detection, bounded logs, PSS/VA-clone OBS dumps + WER; no process injection or remote code execution.");if(!AllEnabledWerConfigured()){SetTrayState(STATE_NEEDS_SETUP,0);if(g_trayOnly||g_keepTrayTaskbar||g_startMinimized)Balloon(L"Crash Monitor",L"Open Crash Monitor and click Enable / Repair Crash Dumps. Windows will ask for UAC once.",NIIF_WARNING);}else SetTrayState(g_paused?STATE_PAUSED:STATE_WAITING,0);g_worker=CreateThread(NULLPTR,0,Worker,NULLPTR,0,0);SetTimer(g_hwnd,1,5000,NULLPTR);if(g_trayOnly){g_hiddenToTray=TRUE;ShowWindow(g_hwnd,SW_HIDE);}else if(g_startMinimized){if(g_minimizeToTray)MinimizeIntoTray();else{g_windowMinimized=TRUE;ShowWindow(g_hwnd,SW_MINIMIZE);}}else ShowMainWindow();MSG msg;while(GetMessageW(&msg,0,0,0)>0){TranslateMessage(&msg);DispatchMessageW(&msg);}if(g_worker)CloseHandle(g_worker);if(mutex)CloseHandle(mutex);return 0;}

extern "C" VOID wWinMainCRTStartup(){ZeroMem(g_baseDir,sizeof(g_baseDir));ZeroMem(g_dumpRoot,sizeof(g_dumpRoot));ZeroMem(g_logPath,sizeof(g_logPath));ZeroMem(g_configPath,sizeof(g_configPath));ZeroMem(g_exePath,sizeof(g_exePath));ZeroMem(g_installDir,sizeof(g_installDir));ZeroMem(g_installExe,sizeof(g_installExe));ZeroMem(g_lastCapturedFile,sizeof(g_lastCapturedFile));ZeroMem(g_running,sizeof(g_running));if(CommandHas(L"--selftest-close-x-exit-child")){ExitProcess((UINT)RunExitBehaviorChild(TRUE));}if(CommandHas(L"--selftest-exit-button-child")){ExitProcess((UINT)RunExitBehaviorChild(FALSE));}if(CommandHas(L"--selftest-dump-target=")){ExitProcess((UINT)RunSelfTestDumpTargetChild());}if(CommandHas(L"--selftest-shortcut-marker=")){ExitProcess((UINT)RunSelfTestShortcutMarkerChild());}if(CommandHas(L"--safe-self-test")){int st=RunSafeSelfTest();ExitProcess((UINT)st);}BuildPaths();LoadTargets();HINSTANCE inst=(HINSTANCE)GetModuleHandleW(0);g_appIcon=BuildAppIcon(inst);g_font=CreateFontW(-16,0,0,0,FW_NORMAL,FALSE,FALSE,FALSE,DEFAULT_CHARSET,OUT_DEFAULT_PRECIS,CLIP_DEFAULT_PRECIS,CLEARTYPE_QUALITY,DEFAULT_PITCH|FF_DONTCARE,L"Segoe UI");g_titleFont=CreateFontW(-28,0,0,0,FW_SEMIBOLD,FALSE,FALSE,FALSE,DEFAULT_CHARSET,OUT_DEFAULT_PRECIS,CLIP_DEFAULT_PRECIS,CLEARTYPE_QUALITY,DEFAULT_PITCH|FF_DONTCARE,L"Segoe UI");if(CommandHas(L"--uninstall-admin-quiet")){DoUninstallAdmin(TRUE);ExitProcess(0);}if(CommandHas(L"--uninstall-admin")){DoUninstallAdmin(FALSE);ExitProcess(0);}if(CommandHas(L"--uninstall-quiet")){BeginUninstall(TRUE);ExitProcess(0);}if(CommandHas(L"--uninstall")){BeginUninstall(FALSE);ExitProcess(0);}if(CommandHas(L"--wer-enable-all")){DoWerHelper(TRUE);ExitProcess(0);}if(CommandHas(L"--wer-disable-all")){DoWerHelper(FALSE);ExitProcess(0);}WCHAR one[MAX_PATH];if(CommandValue(L"--wer-enable-one=",one,MAX_PATH)){DoWerOne(one,TRUE);ExitProcess(0);}if(CommandValue(L"--wer-remove-one=",one,MAX_PATH)){DoWerOne(one,FALSE);ExitProcess(0);}BOOL appMode=CommandHas(L"--app")||lstrcmpiW(g_exePath,g_installExe)==0;int rc=appMode?RunApp(inst):RunSetup(inst);if(g_font)DeleteObject(g_font);if(g_titleFont)DeleteObject(g_titleFont);if(g_appIcon)DestroyIcon(g_appIcon);ExitProcess((UINT)rc);}
