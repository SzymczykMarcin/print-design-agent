<# Load bundled fonts, outline the composed type and export a reopened Corel master. #>
param([string]$ProjectPath = (Join-Path $PSScriptRoot '..'))
$ErrorActionPreference = 'Stop'
$ProjectPath = (Resolve-Path $ProjectPath).Path
New-Item -ItemType Directory -Force -Path (Join-Path $ProjectPath 'working/print-candidates') | Out-Null
Add-Type @"
using System;
using System.Runtime.InteropServices;
public class DesignFonts {
 [DllImport("gdi32.dll", CharSet=CharSet.Unicode)] public static extern int AddFontResourceEx(string path, uint flags, IntPtr reserved);
 [DllImport("user32.dll", CharSet=CharSet.Unicode)] public static extern IntPtr SendMessage(IntPtr hwnd, uint msg, IntPtr wparam, IntPtr lparam);
}
"@
Get-ChildItem (Join-Path $ProjectPath 'inputs/fonts') -Recurse -Filter '*.ttf' | ForEach-Object {
 if ([DesignFonts]::AddFontResourceEx($_.FullName, 0, [IntPtr]::Zero) -eq 0) { throw "Cannot load font: $($_.Name)" }
}
[void][DesignFonts]::SendMessage([IntPtr]0xffff, 0x001D, [IntPtr]::Zero, [IntPtr]::Zero)
$app = New-Object -ComObject CorelDRAW.Application
$doc = $app.OpenDocument((Join-Path $ProjectPath 'working/assembly.svg'))
try {
 $doc.Unit = 3
 $context = $doc.ColorContext.GetCopy()
 if ($context.ColorProfileNameList -notmatch 'ISO Coated v2 \(ECI\)') { throw 'This recipe requires the ISO Coated v2 (ECI) document profile.' }
 $context.RenderingIntent = 2
 $doc.AssignColorContext($context)
 $doc.ActivePage.SetSize(152,214)
 # The full-page cream rectangle anchors the SVG import to the page.
 $all = $doc.ActivePage.Shapes.All()
 $anchor = @($doc.ActivePage.Shapes | Where-Object { $_.Name -eq 'cream-paper' })[0]
 $offsetX = -$anchor.LeftX
 $offsetY = 214 - $anchor.TopY
 $all.Move($offsetX, $offsetY)
 $texts = @($doc.ActivePage.Shapes | Where-Object { [int]$_.Type -eq 6 })
 $evidence = @()
 foreach ($shape in $texts) {
   $font = $shape.Text.Story.Font
   if ($font -notin @('Lato','Lato Regular','Pacifico','Bebas Neue')) { throw "Unexpected font: $font" }
   $evidence += [pscustomobject]@{Text=$shape.Text.Story.Text; Font=$font; Left=$shape.LeftX; Top=$shape.TopY; Width=$shape.SizeWidth; Height=$shape.SizeHeight}
 }
 $doc.PDFSettings.Reset()
 $doc.PDFSettings.pdfVersion = 8
 $doc.PDFSettings.ColorMode = 0
 $doc.PDFSettings.DownsampleColor = $false
 $doc.PDFSettings.DownsampleGray = $false
 $doc.PublishToPDF((Join-Path $ProjectPath 'working/before-outline.pdf'))
 foreach ($shape in $texts) { $shape.ConvertToCurves() }
 if (@($doc.ActivePage.Shapes | Where-Object { [int]$_.Type -eq 6 }).Count -ne 0) { throw 'Live text remains.' }
 $evidence | ConvertTo-Json -Depth 4 | Set-Content (Join-Path $ProjectPath 'reports/typography-v02.json') -Encoding utf8
 $cdr = Join-Path $ProjectPath 'working/flyer-a5-front-v02.cdr'
 $doc.SaveAs($cdr,$app.CreateStructSaveAsOptions())
 $doc.Export((Join-Path $ProjectPath 'working/flyer-a5-front-v02.svg'),1345,0,$app.CreateStructExportOptions(),$app.CreateStructPaletteOptions())
 $doc.Close()
 $doc=$app.OpenDocument($cdr)
 if (@($doc.ActivePage.Shapes | Where-Object { [int]$_.Type -eq 6 }).Count -ne 0) { throw 'Reopened master has live text.' }
 $doc.PDFSettings.Reset()
 $doc.PDFSettings.pdfVersion = 8
 $doc.PDFSettings.DownsampleColor = $false
 $doc.PDFSettings.DownsampleGray = $false
 $doc.PDFSettings.ColorMode=0
 $doc.PublishToPDF((Join-Path $ProjectPath 'working/outlined-rgb.pdf'))
 $doc.PDFSettings.ColorMode=1
 $doc.PublishToPDF((Join-Path $ProjectPath 'working/print-candidates/flyer-a5-front-v02.pdf'))
 Write-Output ('Corel version: ' + $app.Version + '; text blocks outlined: ' + $texts.Count + '; context: ' + $doc.ColorContext.ToString())
} finally { if ($doc) { $doc.Close() } }
