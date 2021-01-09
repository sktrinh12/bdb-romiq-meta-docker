$output = $(docker ps -a --format '{{.Image}}:{{.ID}}') | select-string -pattern "romiq" | ConvertFrom-String -Delimiter ":" | Select -Property P2
$output | foreach-object {
	$str = $_ | Select -First 1 | Select-Object -ExpandProperty P2 
	docker stop $str
	docker rm $str
}


$output = $(docker images --format "{{.Repository}}:{{.ID}}") | select-string -pattern "bdb|_romiq" -NotMatch | ConvertFrom-String -Delimiter ":" | Select -Property P2
$output | foreach-object {
	$str = $_ | Select -First 1 | Select-Object -ExpandProperty P2 
	docker rmi $str
}
