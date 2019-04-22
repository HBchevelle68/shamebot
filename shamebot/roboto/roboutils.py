
cmdlist = [
'$help',
'$hello',
'$shamemedaddy'
]
desclist = [
'Displays this message',
'Greet shamebot and it will greet you back',
'A hardcoded shame'
]

helpstr = '''
	Shamebot Interactive Commands
	{:<36} {:>20}
	{:<36} {:>20}
	{:<21} {:>20}
	'''.format(
		cmdlist[0], desclist[0],
		cmdlist[1], desclist[1],
		cmdlist[2], desclist[2]
		)
