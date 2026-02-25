$env:HEADLESS="true"

Write-Host "Running smoke tests..."
pytest -m smoke -n auto
