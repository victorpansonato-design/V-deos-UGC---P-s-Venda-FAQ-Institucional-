# Exercises the exact media arguments used by the desktop without loading WPF.
$ErrorActionPreference = 'Stop'
$source = Join-Path $PSScriptRoot 'Studio.ps1'
$tokens = $null
$errors = $null
$parsed = [System.Management.Automation.Language.Parser]::ParseFile($source,[ref]$tokens,[ref]$errors)
if ($errors) { throw ($errors -join [Environment]::NewLine) }

$helpers = @('Probe','Seconds','Fmt','Video-Stream','Audio-Stream','Parse-SrtTime','Ass-Time','Write-Captions','New-ExportArguments')
$definitions = $parsed.FindAll({param($node)
    $node -is [System.Management.Automation.Language.FunctionDefinitionAst] -and $helpers -contains $node.Name
}, $false)
foreach ($definition in $definitions) { . ([scriptblock]::Create($definition.Extent.Text)) }
if ($definitions.Count -ne $helpers.Count) { throw 'Não foram encontradas todas as funções de exportação.' }

$action = {
    $invariant = [Globalization.CultureInfo]::InvariantCulture
    $script:ffprobe = (Get-Command ffprobe -CommandType Application | Select-Object -First 1).Source
    $ffmpeg = (Get-Command ffmpeg -CommandType Application | Select-Object -First 1).Source
    $bodyFile = Join-Path $work 'corpo vídeo.mp4'
    $outroFile = Join-Path $work 'vinheta-teste.mp4'
    $srt = Join-Path $work 'teste.srt'
    $mp3 = Join-Path $work 'fala externa.mp3'
    $output = Join-Path $work 'saída.mp4'
    [IO.File]::WriteAllLines($srt, @('1','00:00:00,100 --> 00:00:01,800','Ação, atenção e coração.'))

    & $ffmpeg -v error -f lavfi -i 'testsrc2=size=144x256:rate=30:duration=2' -f lavfi -i 'sine=frequency=440:duration=2' -c:v libx264 -c:a aac -pix_fmt yuv420p $bodyFile
    if ($LASTEXITCODE) { throw 'Falha criando o corpo de teste.' }
    & $ffmpeg -v error -f lavfi -i 'sine=frequency=260:duration=2' -c:a libmp3lame $mp3
    if ($LASTEXITCODE) { throw 'Falha criando o áudio MP3 de teste.' }
    $profile = Probe $bodyFile
    $narration = Probe $mp3
    $cases = @(
        @{name='Vertical com voz original'; width=1080; height=1920; size='144x256'; look=0; audio=$null; narr=$null},
        @{name='Horizontal com MP3'; width=1920; height=1080; size='256x144'; look=1; audio=$mp3; narr=$narration}
    )
    foreach ($case in $cases) {
        & $ffmpeg -v error -y -f lavfi -i "color=blue:size=$($case.size):rate=24:duration=1" -f lavfi -i 'sine=frequency=880:duration=1' -c:v libx264 -c:a aac -pix_fmt yuv420p $outroFile
        if ($LASTEXITCODE) { throw 'Falha criando a vinheta de teste.' }
        if ([IO.File]::Exists($output)) { [IO.File]::Delete($output) }
        $outro = Probe $outroFile
        $arguments = New-ExportArguments $bodyFile $outroFile $case.audio $srt $profile $outro $case.narr (Seconds $profile) (Seconds $outro) $case.width $case.height $case.look $work $output
        & $ffmpeg @arguments
        if ($LASTEXITCODE) { throw 'Falha na exportação.' }
        $delivery = Probe $output
        $video = Video-Stream $delivery
        $audio = Audio-Stream $delivery
        $duration = Seconds $delivery
        if ($video.width -ne $case.width -or $video.height -ne $case.height -or $video.codec_name -ne 'h264' -or
            $audio.codec_name -ne 'aac' -or [math]::Abs($duration - 3) -gt .10) { throw 'Perfil do MP4 incorreto.' }
        if (!(Select-String -LiteralPath 'progress.txt' -Pattern '^progress=end$')) { throw 'Progresso sem conclusão.' }
        Write-Output "$($case.name) · $($video.width)×$($video.height), $(Fmt $duration) s, H.264/AAC"
    }
}

$work = Join-Path ([IO.Path]::GetTempPath()) ('anchieta-smoke-'+[guid]::NewGuid().ToString('N'))
[void][IO.Directory]::CreateDirectory($work)
Push-Location $work
try {
    & $action
} finally {
    Pop-Location
    [IO.Directory]::Delete($work,$true)
}
