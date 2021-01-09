$output = $(docker images --format "{{.Repository}}:{{.ID}}") | select-string "bdb" | ConvertFrom-String -Delimiter ":" | Select -Property P2
$output | foreach-object {
	$str = $_ | Select -First 1 | Select-Object -ExpandProperty P2 
	docker rmi $str
}
