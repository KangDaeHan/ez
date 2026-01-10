# 맥 바탕화면 위젯 가이드

## 개요

맥 바탕화면에 EZ Calendar를 위젯으로 추가하려면 Electron 기반의 데스크톱 앱이 필요합니다.

## 구현 방법

### 1. Electron 앱 생성

```bash
# 별도의 desktop 폴더에서 Electron 프로젝트 생성
npx create-electron-app ez-calendar-desktop --template=vite
```

### 2. 주요 기능

1. **시스템 트레이 통합**
   - 메뉴바에 아이콘 추가
   - 빠른 일정 확인

2. **위젯 모드**
   - 항상 최상위 창 (Always on top)
   - 프레임 없는 투명 창
   - 드래그로 위치 조정

3. **알림**
   - 네이티브 macOS 알림
   - 일정 리마인더

### 3. 예제 코드

```javascript
// main.js (Electron 메인 프로세스)
const { app, BrowserWindow, Tray, Menu, nativeImage } = require('electron')
const path = require('path')

let mainWindow
let widgetWindow
let tray

function createWidgetWindow() {
  widgetWindow = new BrowserWindow({
    width: 300,
    height: 400,
    frame: false,
    transparent: true,
    alwaysOnTop: true,
    skipTaskbar: true,
    resizable: false,
    webPreferences: {
      nodeIntegration: true,
      contextIsolation: false,
    },
  })

  widgetWindow.loadURL('http://localhost:3000/widget')
  
  // 드래그 가능하도록 설정
  widgetWindow.setMovable(true)
}

function createTray() {
  const icon = nativeImage.createFromPath(path.join(__dirname, 'icon.png'))
  tray = new Tray(icon.resize({ width: 16, height: 16 }))
  
  const contextMenu = Menu.buildFromTemplate([
    { label: '위젯 표시', click: () => widgetWindow.show() },
    { label: '위젯 숨기기', click: () => widgetWindow.hide() },
    { type: 'separator' },
    { label: '설정', click: () => mainWindow.show() },
    { type: 'separator' },
    { label: '종료', click: () => app.quit() },
  ])
  
  tray.setToolTip('EZ Calendar')
  tray.setContextMenu(contextMenu)
}

app.whenReady().then(() => {
  createWidgetWindow()
  createTray()
})
```

### 4. 위젯 전용 페이지 추가

프론트엔드에 위젯 전용 라우트 추가:

```typescript
// frontend/src/app/router/index.ts
{
  path: '/widget',
  name: 'Widget',
  component: () => import('@pages/widget/ui/WidgetPage.vue'),
  meta: { title: '위젯' },
}
```

### 5. 빌드 및 배포

```bash
# macOS 앱으로 빌드
npm run make -- --platform darwin

# DMG 파일 생성
npm run make -- --platform darwin --targets @electron-forge/maker-dmg
```

## 대안: 웹 기반 위젯

macOS Sonoma 이후 버전에서는 Safari에서 웹 앱을 독에 추가할 수 있습니다:

1. Safari에서 EZ Calendar 웹앱 열기
2. 파일 > 독에 추가
3. 바탕화면에 위젯처럼 사용

## 참고 자료

- [Electron 공식 문서](https://www.electronjs.org/docs)
- [electron-forge](https://www.electronforge.io/)
- [electron-builder](https://www.electron.build/)

