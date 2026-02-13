# PyInstallerビルドスクリプト
# 管理者権限は不要（ビルド自体には管理者権限は必要ない）

Write-Host "=== ネットワークアダプター切り替えツール ビルドスクリプト ===" -ForegroundColor Cyan
Write-Host ""

# 仮想環境の確認
if (-not (Test-Path "venv\Scripts\Activate.ps1")) {
    Write-Host "エラー: 仮想環境が見つかりません" -ForegroundColor Red
    Write-Host "先に 'python -m venv venv' を実行してください"
    exit 1
}

# 仮想環境を有効化
Write-Host "仮想環境を有効化..." -ForegroundColor Yellow
& .\venv\Scripts\Activate.ps1

# PyInstallerのインストール確認
Write-Host "PyInstallerのバージョン確認..." -ForegroundColor Yellow
$pyinstallerVersion = & python -c "import PyInstaller; print(PyInstaller.__version__)" 2>$null

if ($LASTEXITCODE -ne 0) {
    Write-Host "PyInstallerがインストールされていません。インストールします..." -ForegroundColor Yellow
    pip install pyinstaller
} else {
    Write-Host "PyInstaller バージョン: $pyinstallerVersion" -ForegroundColor Green
}

# 古いビルドファイルを削除
Write-Host "`n古いビルドファイルを削除..." -ForegroundColor Yellow
if (Test-Path "dist") {
    Remove-Item -Recurse -Force "dist"
}
if (Test-Path "build") {
    Remove-Item -Recurse -Force "build"
}
if (Test-Path "NetworkAdapterSwitcher.spec") {
    Remove-Item -Force "NetworkAdapterSwitcher.spec"
}

# ビルド実行
Write-Host "`nPyInstallerでビルドを開始..." -ForegroundColor Yellow
Write-Host "================================================" -ForegroundColor Cyan

pyinstaller `
    --name=NetworkAdapterSwitcher `
    --onefile `
    --windowed `
    --clean `
    --add-data="src;src" `
    --hidden-import=tkinter `
    --hidden-import=tkinter.ttk `
    --hidden-import=tkinter.messagebox `
    --manifest=app.manifest `
    src\main.py

if ($LASTEXITCODE -eq 0) {
    Write-Host "`n================================================" -ForegroundColor Cyan
    Write-Host "✓ ビルド成功!" -ForegroundColor Green
    Write-Host ""
    Write-Host "実行ファイル: $(Resolve-Path 'dist\NetworkAdapterSwitcher.exe')" -ForegroundColor Green
    Write-Host ""
    Write-Host "注意: このアプリケーションは管理者権限で実行する必要があります" -ForegroundColor Yellow
    Write-Host "実行ファイルを右クリック → '管理者として実行' を選択してください" -ForegroundColor Yellow
    Write-Host ""
    
    # ファイルサイズを表示
    $exeSize = (Get-Item "dist\NetworkAdapterSwitcher.exe").Length
    $exeSizeMB = [math]::Round($exeSize / 1MB, 2)
    Write-Host "ファイルサイズ: $exeSizeMB MB" -ForegroundColor Cyan
} else {
    Write-Host "`n✗ ビルド失敗" -ForegroundColor Red
    exit 1
}
