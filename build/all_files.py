from os import listdir

print(*[
	file
	for file in (listdir('Dist'))
	if file.endswith('.dll')
],sep='\n')