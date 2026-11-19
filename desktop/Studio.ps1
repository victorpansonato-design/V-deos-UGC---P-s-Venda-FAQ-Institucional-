# Estúdio UniAnchieta • Windows PowerShell 5.1 / WPF
$ErrorActionPreference = 'Stop'
Add-Type -AssemblyName PresentationFramework, PresentationCore, WindowsBase
$invariant = [Globalization.CultureInfo]::InvariantCulture
$rootDir = $PSScriptRoot
$paths = @{}
$presenters = @{}
$job = $null
$progressTimer = New-Object Windows.Threading.DispatcherTimer
$progressTimer.Interval = [TimeSpan]::FromMilliseconds(400)

[xml]$view = @'
<Window xmlns="http://schemas.microsoft.com/winfx/2006/xaml/presentation" xmlns:x="http://schemas.microsoft.com/winfx/2006/xaml"
 Title="Estúdio UniAnchieta" Width="1080" Height="800" MinWidth="680" MinHeight="540" Background="#F3F6FA" FontFamily="Segoe UI" WindowStartupLocation="CenterScreen">
<Window.Resources>
 <Style TargetType="TextBlock"><Setter Property="Foreground" Value="#152A42"/></Style>
 <Style TargetType="Button"><Setter Property="Padding" Value="14,8"/><Setter Property="Margin" Value="0,3,8,5"/><Setter Property="Background" Value="#FFFFFF"/><Setter Property="BorderBrush" Value="#B9C8D8"/><Setter Property="Foreground" Value="#173C68"/><Setter Property="Cursor" Value="Hand"/></Style>
 <Style TargetType="ComboBox"><Setter Property="Padding" Value="8,5"/><Setter Property="Margin" Value="0,3,12,8"/><Setter Property="MinWidth" Value="126"/></Style>
 <Style x:Key="section" TargetType="TextBlock"><Setter Property="Foreground" Value="#122A45"/><Setter Property="FontSize" Value="18"/><Setter Property="FontWeight" Value="SemiBold"/><Setter Property="Margin" Value="0,8,0,8"/></Style>
</Window.Resources>
<Grid Margin="20"><Grid.RowDefinitions><RowDefinition Height="Auto"/><RowDefinition/><RowDefinition Height="Auto"/></Grid.RowDefinitions>
 <Border x:Name="Hero" CornerRadius="15" Padding="24,16" Margin="0,0,0,14" ClipToBounds="True">
  <Border.Background><LinearGradientBrush StartPoint="0,0" EndPoint="1,1"><GradientStop Color="#061D39"/><GradientStop Color="#0051A0" Offset=".67"/><GradientStop Color="#2976B5" Offset="1"/></LinearGradientBrush></Border.Background>
  <DockPanel><Image x:Name="Marca" DockPanel.Dock="Right" Width="110" MaxHeight="48" Stretch="Uniform"/><StackPanel><TextBlock Foreground="#C9DEEF" Text="GRUPO ANCHIETA  /  CX" FontWeight="SemiBold" FontSize="11"/><TextBlock Foreground="White" Text="Estúdio de vídeo" FontSize="29" FontWeight="SemiBold"/></StackPanel></DockPanel>
 </Border>
 <Grid Grid.Row="1"><Grid.ColumnDefinitions><ColumnDefinition Width="5*"/><ColumnDefinition Width="14"/><ColumnDefinition Width="4*"/></Grid.ColumnDefinitions>
 <Border Background="White" CornerRadius="14" Padding="17"><ScrollViewer VerticalScrollBarVisibility="Auto"><StackPanel x:Name="Inputs">
 <TextBlock Text="Material de origem" Style="{StaticResource section}"/>
 <WrapPanel><StackPanel><TextBlock Text="Origem"/><ComboBox x:Name="Origin" SelectedIndex="0"><ComboBoxItem>Filmagem do Marketing</ComboBoxItem><ComboBoxItem>Avatar gerado</ComboBoxItem></ComboBox></StackPanel><StackPanel x:Name="People" Visibility="Collapsed"><TextBlock Text="Perfil"/><ComboBox x:Name="Person" SelectedIndex="0"><ComboBoxItem>Apresentadora</ComboBoxItem><ComboBoxItem>Apresentador</ComboBoxItem></ComboBox></StackPanel></WrapPanel>
 <WrapPanel><Button x:Name="Video" Content="Escolher vídeo principal"/><TextBlock x:Name="VideoName" VerticalAlignment="Center" TextWrapping="Wrap"/></WrapPanel>
 <WrapPanel><Button x:Name="Audio" Content="Escolher locução"/><Button x:Name="ClearAudio" Content="Usar áudio do vídeo"/></WrapPanel><TextBlock x:Name="AudioName" Text="Áudio do vídeo" TextWrapping="Wrap"/>
 <CheckBox x:Name="Sync" Margin="0,7,0,4" Visibility="Collapsed"><TextBlock Text="A locução selecionada é a mesma usada no lip-sync, ou a pessoa não fala em quadro." TextWrapping="Wrap"/></CheckBox>
 <TextBlock Text="Direção" Style="{StaticResource section}"/>
 <WrapPanel><StackPanel><TextBlock Text="Formato"/><ComboBox x:Name="Format" SelectedIndex="0"><ComboBoxItem>Vertical · 9:16</ComboBoxItem><ComboBoxItem>Horizontal · 16:9</ComboBoxItem></ComboBox></StackPanel><StackPanel><TextBlock Text="Acabamento da legenda"/><ComboBox x:Name="Look" SelectedIndex="0"><ComboBoxItem>Editorial · azul</ComboBoxItem><ComboBoxItem>Cinema · claro</ComboBoxItem></ComboBox></StackPanel></WrapPanel>
 <WrapPanel><Button x:Name="Captions" Content="Escolher legenda SRT"/><Button x:Name="ClearCaptions" Content="Remover"/><TextBlock x:Name="CaptionsName" TextWrapping="Wrap" VerticalAlignment="Center"/></WrapPanel>
 <TextBlock Text="Use um SRT em português, com até duas linhas por fala." TextWrapping="Wrap" Foreground="#50647B"/>
 <WrapPanel><Button x:Name="Outro" Content="Escolher vinheta oficial"/><TextBlock x:Name="OutroName" TextWrapping="Wrap" VerticalAlignment="Center"/></WrapPanel>
 </StackPanel></ScrollViewer></Border>
 <Border Grid.Column="2" Background="#0B1C30" CornerRadius="14" Padding="16"><Grid><Grid.RowDefinitions><RowDefinition Height="Auto"/><RowDefinition/><RowDefinition Height="Auto"/></Grid.RowDefinitions>
 <TextBlock x:Name="PreviewTitle" Text="Prévia do material" Foreground="#DCEBFA" FontSize="15" Margin="0,0,0,8"/>
 <MediaElement x:Name="Player" Grid.Row="1" Stretch="Uniform" LoadedBehavior="Manual" UnloadedBehavior="Manual" ScrubbingEnabled="True"/>
 <WrapPanel Grid.Row="2"><Button x:Name="Play" Content="Reproduzir"/><Button x:Name="Pause" Content="Pausar"/></WrapPanel>
 </Grid></Border></Grid>
 <Border Grid.Row="2" Background="White" CornerRadius="14" Margin="0,12,0,0" Padding="15"><StackPanel>
 <ProgressBar x:Name="Progress" Height="5" Minimum="0" Maximum="100" Foreground="#0051A0" Background="#D7E5F2"/>
 <DockPanel Margin="0,6,0,0"><WrapPanel DockPanel.Dock="Right"><Button x:Name="Cancel" Content="Cancelar" Visibility="Collapsed"/><Button x:Name="Render" Content="Exportar MP4" Background="#0051A0" Foreground="White"/></WrapPanel><TextBlock x:Name="Status" VerticalAlignment="Center" Text="Escolha o material e a vinheta do formato." TextWrapping="Wrap"/></DockPanel>
 </StackPanel></Border>
</Grid></Window>
'@
$window = [Windows.Markup.XamlReader]::Load((New-Object Xml.XmlNodeReader $view))
$ui = @{}
$ns = New-Object Xml.XmlNamespaceManager $view.NameTable
$ns.AddNamespace('x','http://schemas.microsoft.com/winfx/2006/xaml')
foreach ($item in $view.SelectNodes('//*[@x:Name]',$ns)) {
    $name = $item.GetAttribute('Name','http://schemas.microsoft.com/winfx/2006/xaml')
    $ui[$name] = $window.FindName($name)
}
function Show-Problem($text) {
    [void][Windows.MessageBox]::Show($window,[string]$text,'Estúdio UniAnchieta','OK','Warning')
}
function Select-Media($filter) {
    $dialog = New-Object Microsoft.Win32.OpenFileDialog
    $dialog.Filter = $filter
    if ($dialog.ShowDialog($window)) { return $dialog.FileName }
}
function Open-Preview($path, $label) {
    $ui.Player.Stop()
    $ui.Player.Source = $null
    $ui.PreviewTitle.Text = $label
    if ($path) {
        $ui.Player.Source = New-Object Uri($path)
        $ui.Player.Position = [TimeSpan]::Zero
        $ui.Player.Play()
    }
}
function Profile-Key {
    if ($ui.Origin.SelectedIndex -eq 0) { return 'marketing' }
    return ('avatar' + $ui.Person.SelectedIndex)
}
function Update-Person {
    $key = Profile-Key
    $ui.People.Visibility = if ($key -eq 'marketing') {'Collapsed'} else {'Visible'}
    $paths.Video = $presenters[$key]
    $ui.VideoName.Text = [IO.Path]::GetFileName($paths.Video)
    Open-Preview $paths.Video 'Prévia do material'
}
function Find-Tool($name) {
    $near = Join-Path (Join-Path $rootDir 'ffmpeg') ($name+'.exe')
    if (Test-Path -LiteralPath $near -PathType Leaf) { return $near }
    $found = Get-Command ($name+'.exe') -CommandType Application -ErrorAction SilentlyContinue | Select-Object -First 1
    if (!$found) { throw "O estúdio precisa de $name.exe. Instale FFmpeg no PATH ou na pasta ffmpeg ao lado do estúdio." }
    return $found.Source
}
function Probe($path) {
    $extension = [IO.Path]::GetExtension($path)
    $format = switch ($extension.ToLowerInvariant()) {
        '.mp4' {'mov'}
        '.mov' {'mov'}
        '.mkv' {'matroska'}
        '.mp3' {'mp3'}
        '.wav' {'wav'}
        default { throw "Formato de arquivo não aceito. Escolha um vídeo MP4, MOV ou MKV, ou áudio WAV ou MP3." }
    }
    $result = & $script:ffprobe -v error -show_streams -show_format -of json -protocol_whitelist 'file,pipe' -f $format -i $path
    if ($LASTEXITCODE -ne 0) { throw 'Mídia ilegível pelo FFprobe.' }
    $data = $result -join [Environment]::NewLine | ConvertFrom-Json
    $data | Add-Member -NotePropertyName InputFormat -NotePropertyValue $format
    return $data
}
function Seconds($info) {
    $duration = [double]::Parse([string]$info.format.duration,$invariant)
    if ($duration -le 0 -or [double]::IsInfinity($duration) -or [double]::IsNaN($duration)) { throw 'A mídia precisa ter duração definida.' }
    return $duration
}
function Fmt($value) { return ([double]$value).ToString('0.######',$invariant) }
function Video-Stream($info) { return ($info.streams | Where-Object codec_type -eq 'video' | Select-Object -First 1) }
function Audio-Stream($info) { return ($info.streams | Where-Object codec_type -eq 'audio' | Select-Object -First 1) }
function Parse-SrtTime($value) {
    return [TimeSpan]::ParseExact(($value.Replace(',','.')),'hh\:mm\:ss\.fff',$invariant).TotalSeconds
}
function Ass-Time($value) {
    $t = [int][math]::Floor($value * 100 + .00001)
    return '{0}:{1:00}:{2:00}.{3:00}' -f [int][math]::Floor($t/360000),[int][math]::Floor(($t/6000)%60),[int][math]::Floor(($t/100)%60),($t%100)
}
function Write-Captions($file, $destination, $duration, $width, $height, $look) {
    $blocks = ([IO.File]::ReadAllText($file).Trim() -replace "\r\n?", "`n") -split "\n\s*\n"
    $body = New-Object 'System.Collections.Generic.List[string]'
    $scale = if ($width -lt $height) {52} else {48}
    $style = if ($look -eq 0) {'3,4,0,2'} else {'1,2,2,2'}
    $margin = [int]($height*.12)
    $header = @"
[Script Info]
ScriptType: v4.00+
PlayResX: $width
PlayResY: $height
WrapStyle: 0
ScaledBorderAndShadow: yes
[V4+ Styles]
Format: Name,Fontname,Fontsize,PrimaryColour,SecondaryColour,OutlineColour,BackColour,Bold,Italic,Underline,StrikeOut,ScaleX,ScaleY,Spacing,Angle,BorderStyle,Outline,Shadow,Alignment,MarginL,MarginR,MarginV,Encoding
Style: Fala,Segoe UI,$scale,&H00FFFFFF,&H00FFFFFF,&H003A200C,&H80000000,-1,0,0,0,100,100,0,0,$style,88,88,$margin,1
[Events]
Format: Layer,Start,End,Style,Name,MarginL,MarginR,MarginV,Effect,Text
"@
    $last = 0.0
    foreach ($block in $blocks) {
        $lines = @($block -split "\n")
        if ($lines.Count -lt 3 -or $lines.Count -gt 4 -or $lines[1] -notmatch '^(\d{2}:\d{2}:\d{2},\d{3}) --> (\d{2}:\d{2}:\d{2},\d{3})$') {
            throw 'SRT inválido. Use número, linha de tempos e uma ou duas linhas de legenda.'
        }
        $start = Parse-SrtTime $Matches[1]
        $end = Parse-SrtTime $Matches[2]
        if ($start -lt $last -or $end -le $start -or $end -gt ($duration+.002)) { throw 'Legenda fora da duração do vídeo ou com sobreposição.' }
        $last = $end
        $caption = @($lines[2..($lines.Count-1)] | ForEach-Object {
            if ($_.Contains('{') -or $_.Contains('}') -or $_.Contains('\')) { throw 'Use texto simples no SRT, sem chaves ou comandos.' }
            $_.Trim()
        }) -join '\N'
        $middle = [int]($width/2); $baseline = $height - $margin
        $anim = if ($look -eq 0) { '{\fad(90,70)\move('+$middle+','+($baseline+8)+','+$middle+','+$baseline+',0,130)}' } else { '{\fad(130,90)}' }
        $body.Add(('Dialogue: 0,'+(Ass-Time $start)+','+(Ass-Time $end)+',Fala,,0,0,0,,'+$anim+$caption))
    }
    [IO.File]::WriteAllText($destination, ($header+"`r`n"+($body -join "`r`n")), (New-Object Text.UTF8Encoding($false)))
}
function Release-Job {
    $progressTimer.Stop()
    if ($script:job) {
        if ($script:job.proc) { $script:job.proc.Dispose() }
        if (Test-Path -LiteralPath $script:job.temp) { [IO.Directory]::Delete($script:job.temp,$true) }
        if (Test-Path -LiteralPath $script:job.partial) { [IO.File]::Delete($script:job.partial) }
    }
    $script:job = $null
    $ui.Inputs.IsEnabled = $true
    $ui.Render.IsEnabled = $true
    $ui.Cancel.Visibility = 'Collapsed'
}
function New-ExportArguments($videoPath, $outroPath, $audioPath, $captionsPath,
    $base, $outro, $narr, $body, $ending, $width, $height, $look, $temp, $partial) {
    $read = @('-hide_banner','-nostdin','-loglevel','error','-progress','progress.txt','-stats_period','0.4','-protocol_whitelist','file,pipe','-f',$base.InputFormat,'-i',$videoPath,'-protocol_whitelist','file,pipe','-f',$outro.InputFormat,'-i',$outroPath)
    $bodyAudio = '0:a:0'
    if ($audioPath) { $read += @('-protocol_whitelist','file,pipe','-f',$narr.InputFormat,'-i',$audioPath); $bodyAudio='2:a:0' }
    $sub = ''
    if ($captionsPath) { Write-Captions $captionsPath (Join-Path $temp 'captions.ass') $body $width $height $look; $sub=',subtitles=captions.ass' }
    $normalize = "scale=${width}:${height}:force_original_aspect_ratio=decrease:force_divisible_by=2,pad=${width}:${height}:(ow-iw)/2:(oh-ih)/2:color=0x081727,setsar=1,fps=30,format=yuv420p"
    $videoFilter = "[0:v:0]$normalize$sub,setpts=PTS-STARTPTS[v0];[1:v:0]$normalize,setpts=PTS-STARTPTS[v1]"
    $baseAudio = "[${bodyAudio}]aresample=48000,aformat=channel_layouts=stereo,apad,atrim=duration=$(Fmt $body),asetpts=PTS-STARTPTS[a0]"
    $lastAudio = if (Audio-Stream $outro) { '[1:a:0]aresample=48000,aformat=channel_layouts=stereo,apad' } else { 'anullsrc=r=48000:cl=stereo' }
    $mix = "$videoFilter;$baseAudio;$lastAudio,atrim=duration=$(Fmt $ending),asetpts=PTS-STARTPTS[a1];[v0][a0][v1][a1]concat=n=2:v=1:a=1[outv][outa]"
    $encode = @('-filter_complex',$mix,'-map','[outv]','-map','[outa]','-c:v','libx264','-preset','medium','-crf','17','-c:a','aac','-b:a','192k','-movflags','+faststart','-n',$partial)
    return ($read+$encode)
}

function Start-Export {
    if ($script:job) {return}
    if (!$paths.Video -or !$paths.Outro) { throw 'Escolha o vídeo principal e a vinheta oficial.' }
    if ($paths.Audio -and !$ui.Sync.IsChecked) { throw 'Confirme o uso e a sincronia da faixa selecionada.' }
    $script:ffprobe = Find-Tool 'ffprobe'
    $executable = Find-Tool 'ffmpeg'
    $base = Probe $paths.Video
    $outro = Probe $paths.Outro
    $v = Video-Stream $base; $endV = Video-Stream $outro
    if (!$v -or !$endV) { throw 'O vídeo principal e a vinheta precisam conter imagem.' }
    $body = Seconds $base; $ending = Seconds $outro
    $width = 1080; $height = 1920
    if ($ui.Format.SelectedIndex -eq 1) { $width=1920; $height=1080 }
    if ([math]::Abs(($endV.width / $endV.height) / ($width / $height) - 1) -gt .03) { throw 'A proporção da vinheta difere do formato escolhido.' }
    if (!$paths.Audio -and !(Audio-Stream $base)) { throw 'Escolha uma locução. O vídeo principal está sem áudio.' }
    $narr = $null
    if ($paths.Audio) {
        $narr = Probe $paths.Audio
        if (!(Audio-Stream $narr) -or [math]::Abs((Seconds $narr)-$body) -gt .15) {throw 'A locução deve ter a mesma duração do vídeo principal (tolerância de 0,15 s).'}
    }
    $duration = ([math]::Ceiling($body*30-.000001)+[math]::Ceiling($ending*30-.000001))/30
    if ($duration -gt 60) { throw "A duração com a vinheta é $(Fmt $duration) s. Reduza o corpo para caber em um minuto." }
    $save = New-Object Microsoft.Win32.SaveFileDialog
    $save.Filter = 'Vídeo MP4|*.mp4'; $save.FileName='FAQ-UniAnchieta.mp4'
    if (!$save.ShowDialog($window)) { return }
    if ([IO.File]::Exists($save.FileName)) { throw 'Escolha um nome novo para preservar as exportações anteriores.' }
    $id = [guid]::NewGuid().ToString('N')
    $temp = Join-Path ([IO.Path]::GetTempPath()) ('anchieta-'+$id)
    [void][IO.Directory]::CreateDirectory($temp)
    $partial = Join-Path ([IO.Path]::GetDirectoryName($save.FileName)) ('.anchieta-'+$id+'.mp4')
    $script:job = @{temp=$temp;partial=$partial;target=$save.FileName;duration=$duration;width=$width;height=$height;proc=$null;stopped=$false;start=[DateTime]::UtcNow}
    $read = New-ExportArguments $paths.Video $paths.Outro $paths.Audio $paths.Captions $base $outro $narr $body $ending $width $height $ui.Look.SelectedIndex $temp $partial
    # Windows files reject double quotes. All argv values here end in a filename or a trusted filter/literal.
    $info = New-Object Diagnostics.ProcessStartInfo
    $info.FileName = $executable; $info.WorkingDirectory=$temp
    $info.Arguments = (@($read | ForEach-Object { '"'+$_+'"' }) -join ' ')
    $info.UseShellExecute=$false; $info.CreateNoWindow=$true; $info.RedirectStandardError=$true
    $proc = New-Object Diagnostics.Process
    $proc.StartInfo=$info
    [void]$proc.Start()
    $job.proc=$proc; $job.errors=$proc.StandardError.ReadToEndAsync()
    $ui.Render.IsEnabled=$false; $ui.Inputs.IsEnabled=$false; $ui.Progress.Value=0; $ui.Cancel.Visibility='Visible'
    $ui.Status.Text='Compondo vídeo, legenda e vinheta…'; $progressTimer.Start()
}

function Stop-Export {
    if (!$script:job) { return }
    $script:job.stopped = $true
    if ($script:job.proc -and !$script:job.proc.HasExited) {
        $script:job.proc.Kill()
        [void]$script:job.proc.WaitForExit(3000)
    }
    Release-Job
    $ui.Status.Text = 'Exportação cancelada.'
    $ui.Progress.Value = 0
}

function Confirm-Export {
    $result = Probe $script:job.partial
    $video = Video-Stream $result
    $audio = Audio-Stream $result
    $seconds = Seconds $result
    if ($video.codec_name -ne 'h264' -or $audio.codec_name -ne 'aac' -or
        $video.width -ne $script:job.width -or $video.height -ne $script:job.height -or
        $seconds -gt 60.001 -or [math]::Abs($seconds-$script:job.duration) -gt .10) {
        throw 'A exportação não passou pela conferência de formato, codecs ou duração.'
    }
    $target = $script:job.target
    [IO.File]::Move($script:job.partial,$target)
    Release-Job
    $ui.Progress.Value = 100
    $ui.Status.Text = 'MP4 salvo. Revise a fala, a legenda e a vinheta na prévia.'
    Open-Preview $target 'Prévia do MP4 exportado'
}

function Update-Export {
    if (!$script:job) { return }
    try {
        $proc = $script:job.proc
        if ($proc.HasExited) {
            $proc.WaitForExit()
            if ($proc.ExitCode -ne 0) {
                $details = $script:job.errors.GetAwaiter().GetResult().Trim()
                if ($details.Length -gt 900) { $details = $details.Substring($details.Length-900) }
                throw "FFmpeg não concluiu a exportação. $details"
            }
            $ui.Status.Text = 'Conferindo o MP4…'
            Confirm-Export
            return
        }
        $report = Join-Path $script:job.temp 'progress.txt'
        if (![IO.File]::Exists($report)) { return }
        try { $lines = [IO.File]::ReadAllLines($report) }
        catch [IO.IOException] { return }
        $last = $lines | Where-Object { $_ -match '^out_time_us=\d+$' } | Select-Object -Last 1
        if (!$last) { return }
        $done = [double]::Parse($last.Substring(12),$invariant)/1000000
        $elapsed = ([DateTime]::UtcNow-$script:job.start).TotalSeconds
        $fraction = [math]::Min(.99,$done/$script:job.duration)
        $ui.Progress.Value = $fraction * 100
        if ($elapsed -lt 2 -or $fraction -lt .05) { return }
        $eta = [TimeSpan]::FromSeconds([math]::Ceiling($elapsed*(1/$fraction-1)))
        $stage = if ($fraction -lt .88) {'Compondo vídeo, legenda e vinheta'} else {'Finalizando o MP4'}
        $ui.Status.Text = "$stage • $([int]($fraction*100))% • faltam cerca de $($eta.ToString('mm\:ss'))"
    } catch {
        Release-Job
        $ui.Status.Text = 'Falha na exportação.'
        Show-Problem $_.Exception.Message
    }
}

$videoFilter = 'Vídeos MP4, MOV e MKV|*.mp4;*.mov;*.mkv'
$ui.Video.Add_Click({
    $file = Select-Media $videoFilter
    if ($file) {
        $presenters[(Profile-Key)] = $file
        Update-Person
    }
})
$ui.Audio.Add_Click({
    $file = Select-Media 'Áudio MP3 ou WAV|*.mp3;*.wav'
    if ($file) {
        $paths.Audio = $file
        $ui.AudioName.Text = [IO.Path]::GetFileName($file)
        $ui.Sync.Visibility = 'Visible'
        $ui.Sync.IsChecked = $false
        Open-Preview $file 'Prévia da locução'
    }
})
$ui.ClearAudio.Add_Click({
    $paths.Remove('Audio')
    $ui.AudioName.Text = 'Áudio do vídeo'
    $ui.Sync.Visibility = 'Collapsed'
    $ui.Sync.IsChecked = $false
    Open-Preview $paths.Video 'Prévia do material'
})
$ui.Captions.Add_Click({
    $file = Select-Media 'Legendas SRT|*.srt'
    if ($file) {
        $paths.Captions = $file
        $ui.CaptionsName.Text = [IO.Path]::GetFileName($file)
    }
})
$ui.ClearCaptions.Add_Click({
    $paths.Remove('Captions')
    $ui.CaptionsName.Text = ''
})
$ui.Outro.Add_Click({
    $file = Select-Media $videoFilter
    if ($file) {
        $paths.Outro = $file
        $ui.OutroName.Text = [IO.Path]::GetFileName($file)
        Open-Preview $file 'Prévia da vinheta'
    }
})
$ui.Origin.Add_SelectionChanged({ Update-Person })
$ui.Person.Add_SelectionChanged({ Update-Person })
$ui.Format.Add_SelectionChanged({
    $paths.Remove('Outro')
    $ui.OutroName.Text = ''
    $ui.Status.Text = 'Selecione a vinheta oficial para o formato escolhido.'
})
$ui.Play.Add_Click({ if ($ui.Player.Source) { $ui.Player.Play() } })
$ui.Pause.Add_Click({ if ($ui.Player.Source) { $ui.Player.Pause() } })
$ui.Player.Add_MediaFailed({
    $ui.Status.Text = 'O Windows não reproduziu a prévia. Confira o codec do material.'
})
$ui.Render.Add_Click({
    try { Start-Export }
    catch {
        Release-Job
        $ui.Status.Text = 'Confira os materiais antes de exportar.'
        Show-Problem $_.Exception.Message
    }
})
$ui.Cancel.Add_Click({ Stop-Export })
$progressTimer.Add_Tick({ Update-Export })
$window.Add_Closing({
    param($sender,$eventArgs)
    if ($script:job) {
        $answer = [Windows.MessageBox]::Show($window,'Cancelar a exportação e fechar o estúdio?','Estúdio UniAnchieta','YesNo','Question')
        if ($answer -ne 'Yes') { $eventArgs.Cancel = $true; return }
        Stop-Export
    }
    $ui.Player.Close()
})
$ui.Hero.Add_MouseMove({
    param($sender,$eventArgs)
    if (![Windows.SystemParameters]::ClientAreaAnimation -or $sender.ActualWidth -le 0) { return }
    $x = $eventArgs.GetPosition($sender).X/$sender.ActualWidth
    $sender.Background.EndPoint = [Windows.Point]::new((.9+.15*$x),1)
})
$ui.Hero.Add_MouseLeave({
    param($sender,$eventArgs)
    $sender.Background.EndPoint = [Windows.Point]::new(1,1)
})
$logo = Join-Path $rootDir 'marca.png'
if ([IO.File]::Exists($logo)) {
    try {
        $bitmap = New-Object Windows.Media.Imaging.BitmapImage
        $bitmap.BeginInit()
        $bitmap.CacheOption = 'OnLoad'
        $bitmap.UriSource = New-Object Uri($logo)
        $bitmap.EndInit()
        $ui.Marca.Source = $bitmap
    } catch {
        $ui.Status.Text = 'A marca local não abriu. As exportações usam a vinheta selecionada.'
    }
}
[void]$window.ShowDialog()
