Fitness:
	Composto de cliente e servidor ftp:
	O cliente envia uma string com diretório, aquivo e flags 
	do gcc para o servidor que compila o arquivo especificado
	e testa sua performance com o Gprof.
	A string é enviada com a a seguinte sintaxe via ftp:
	diretorio(tab)arquivo(tab)flag1 flag2...
	Ex.:"/home/foo/\tbar.c\t-g -pthread"

	Endreço padrão: 127.0.0.1:4242
