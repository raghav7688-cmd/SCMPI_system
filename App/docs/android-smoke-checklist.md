# Android Smoke Checklist

Use this checklist after dependency or navigation changes to quickly validate core app behavior.

## Preconditions
- Backend API is reachable from emulator at `http://10.0.2.2:8000/`.
- App installs on a debug device/emulator.
- Build variant is `debug`.

## 1) Authentication Flow
- Launch app and confirm `LoginScreen` is shown first.
- Tap **Login** with empty fields and verify validation message appears.
- Tap **Register** and verify navigation to `RegisterScreen`.
- On register, verify:
  - empty fields -> validation message
  - short password -> validation message
  - mismatched passwords -> validation message
- Register with valid values and verify navigation to `HomeScreen`.
- From top-bar logout icon, verify return to `LoginScreen` and back stack is cleared.

## 2) Home Tabs + API Calls
- Open each tab in `HomeScreen`: Recommend, Mandi, Production, Predict.
- Recommend tab:
  - empty submit shows validation
  - valid input returns result card
- Mandi tab:
  - valid input returns result card
  - API/network failure shows error text
- Production tab:
  - valid state shows result card
- Predict tab:
  - non-numeric area shows `Invalid area`
  - valid input shows prediction result card

## 3) Navigation Integrity
- Kill/relaunch app after login/logout and verify start destination is still login.
- Verify no crashes when switching tabs repeatedly.
- Verify no crash when toggling password visibility on Login/Register.

## 4) Build/Quality Gates
Run these before merge:

```powershell
.\gradlew.bat :app:assembleDebug --stacktrace --no-daemon
.\gradlew.bat :app:testDebugUnitTest --stacktrace --no-daemon
.\gradlew.bat :app:lintDebug --stacktrace --no-daemon
.\gradlew.bat :app:connectedDebugAndroidTest --stacktrace --no-daemon
```

If `connectedDebugAndroidTest` fails with "No connected devices", start an emulator/device and rerun only that command.

