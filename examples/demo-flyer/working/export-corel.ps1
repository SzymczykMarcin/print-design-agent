<# Rebuild outlined CDR/SVG sources and PDFs through the installed CorelDRAW COM server. #>
param([Parameter(Mandatory=$true)][string]$ProjectPath, [Parameter(Mandatory=$true)][string]$InputPath)
$ErrorActionPreference = 'Stop'
$app = New-Object -ComObject CorelDRAW.Application
foreach ($name in @('flyer-a5-front-v01','social-feed-v01','social-story-v01')) {
    $doc = $app.OpenDocument((Join-Path $InputPath ($name + '.svg')))
    try {
        $doc.Unit = 3
        $width = if ($name -like 'flyer*') { 154.0 } else { 1080.0 * 25.4 / 96 }
        $height = if ($name -like 'flyer*') { 216.0 } elseif ($name -like '*feed*') { 1350.0 * 25.4 / 96 } else { 1920.0 * 25.4 / 96 }
        $doc.ActivePage.SetSize($width, $height)
        $all = $doc.ActivePage.Shapes.All()
        $all.Move(-$all.LeftX, $height - $all.TopY)
        $texts = $doc.ActivePage.Shapes.FindShapes('', 6, $true)
        Write-Output ($name + ': text objects=' + $texts.Count)
        foreach ($shape in $texts) {
            if ($shape.Text.Story.Font -notlike 'Lato*') { throw 'Unexpected font substitution.' }
        }
        $doc.PDFSettings.Reset()
        $doc.PDFSettings.pdfVersion = 8
        $doc.PDFSettings.ColorMode = 0

        $doc.PDFSettings.DownsampleColor = $false
        $doc.PDFSettings.DownsampleGray = $false
        $doc.PDFSettings.TextAsCurves = $false
        $doc.PublishToPDF((Join-Path $InputPath ($name + '-before.pdf')))
        foreach ($shape in $texts) { $shape.ConvertToCurves() }
        if ($doc.ActivePage.Shapes.FindShapes('', 6, $true).Count -ne 0) { throw 'Live text remains.' }
        $cdr = Join-Path $ProjectPath ('working/' + $name + '.cdr')
        $saveOptions = $app.CreateStructSaveAsOptions()
        $doc.SaveAs([string]$cdr, $saveOptions)
        $doc.Export((Join-Path $ProjectPath ('working/' + $name + '.svg')), 1345, 0, $app.CreateStructExportOptions(), $app.CreateStructPaletteOptions())
        $doc.Close()
        $doc = $app.OpenDocument($cdr)
        if ($doc.ActivePage.Shapes.FindShapes('', 6, $true).Count -ne 0) { throw 'Reopened CDR contains live text.' }
        $doc.PDFSettings.pdfVersion = 8
        $doc.PDFSettings.ColorMode = 0

        $doc.PDFSettings.DownsampleColor = $false
        $folder = if ($name -like 'flyer*') { 'exports/print/' } else { 'previews/' }
        $pdf = Join-Path $ProjectPath ($folder + $name + '.pdf')
        $doc.PublishToPDF($pdf)
        Copy-Item (Join-Path $InputPath ($name + '-before.pdf')) (Join-Path $ProjectPath ('reports/' + $name + '-before-outline.pdf'))
        Write-Output ('Saved and reopened: ' + $name)
    } finally { if ($doc) { $doc.Close() } }
}
