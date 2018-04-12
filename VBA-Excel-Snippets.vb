' this is a comment

' Loop through all files in a folder using Dir to get names and prefilter
Sub LoopThroughFiles()
    Dim MyObj As Object, MySource As Object, file As Variant
   file = Dir("c:\testfolder\*test*")
   While (file <> "")
      If InStr(file, "test") > 0 Then
         MsgBox "found " & file
         Exit Sub
      End If
     file = Dir
  Wend
End Sub
