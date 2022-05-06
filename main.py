# importa pacote dnspython
import dns.resolver
import os


# seta o servidor de DNS utilizado
buscador = dns.resolver.Resolver()
# buscador.nameservers = ['208.67.220.220']  # OpenDNS
buscador.nameservers = ['8.8.8.8']  # Google
# buscador.nameservers = ['1.1.1.1']  # Cloudflare


# funcao que verifica se o domínio tem algum registro
def tem_registros(dominio, tipo):
    try:
        buscador.resolve(dominio, tipo)
        return True
    except Exception:
        return False


def getRegistros(dominio, tipo):
    consulta = buscador.resolve(dominio, tipo)
    return consulta


class bcolors:
    RESET = '\033[0m'  #RESET COLOR
    BLUE = '\033[1;34m'
    YELLOW = '\033[1;33m'
    GREEN = '\033[1;32m'
    GRAY = '\033[1;37m'

def main():
    print(f"{bcolors.BLUE}Digite o domínio: {bcolors.RESET}")
    dominio = input()
    print()


    # lista de possíveis subdomínios
    subdominios = ['atacado', 'firebird', 'webmail', 'pop', 'pop3', 'smtp', 'imap', 'pda', 'calendario', 'autodiscover',
                   'relatorio', 'relatorios','painel', 'autoconfig', 'sip', 'cpcalendars', 'cpcontacts', 'cpanel',
                   'ftp', 'webdisk', 'whm', 'e-mail', 'www', 'default._domainkey', 'mail._domainkey', 'mail', 'mail2',
                   'emailmkt', 'mkt', 's1._domainkey', 's2._domainkey', 'email', 'blog', 'sac', 'correio', 'mailserver',
                   'google._domainkey', 'admin', 'app', 'newsletter', 'news', 'mssql', 'pgsql', 'mysql',
                   'zmail._domainkey', 'websvn', 'intranet', 'mx', '_amazonses', 'amazonses', 'webmail2', 'loja',
                   'interno', 'servidor', 'ssh', 'phpmyadmin', 'hostingermail-a._domainkey',
                   'hostingermail-b._domainkey', 'hostingermail-c._domainkey', 'backup', 'www2', 'local', 'websvn',
                   'sistema', 'wap', "materiais", "clickmailmkt", "catalogo", "api"]

    registros_srv = ['_sipfederationtls._tcp', '_SIP._tls', '_autodiscover._tcp', '_imap._tcp', '_pop3._tcp',
                     '_submission._tcp', '_smtp._tcp']

    registrosPrincipais = []
    registrosSecundarios = []
    registrosSRV = []


    # mostra o registro A da raiz
    if tem_registros(dominio, 'A'):

        # exibe o registro A
        consultaA = getRegistros(dominio, 'A')
        for dadoA in consultaA:
            registrosPrincipais.append(' 3600s A ' + str(dadoA))
#    else:
#        print('Nenhum registro A encontrado na raiz do domínio.')

    # se tem registros MX
    if tem_registros(dominio, 'MX'):
        # exibe registros MX
        consultaMX = getRegistros(dominio, 'MX')
        for dadoMX in consultaMX:
            if str(dadoMX).find('mail.' + dominio) == -1:
                # se não há registro do tipo mail.dominio.com.br:
                registrosPrincipais.append(' 14400s MX ' + str(dadoMX))
            else:
                # se existir mx com mail.com.br
                registrosPrincipais.append(' 14400s MX ' + str(dadoMX))
                mailMX = getRegistros('mail.' + dominio, 'A')
                for dadoMX2 in mailMX:
                    registrosSecundarios.append('mail 14400s A ' + str(dadoMX2))
                #subdominios.remove('mail')
#    else:
#        print('Não há registros MX')

    # se tem registro TXT
    if tem_registros(dominio, 'TXT'):
        consultaTXT = getRegistros(dominio, 'TXT')
        for dadoTXT in consultaTXT:
            registrosPrincipais.append(' 14400s TXT ' + str(dadoTXT))
#    else:
#        print('Não há registros TXT.')

    # se tem registros CNAME dos subdominios
    for subdominio in subdominios:
        if tem_registros(subdominio + '.' + dominio, 'CNAME'):
            consultaCNAME = getRegistros(subdominio + '.' + dominio, 'CNAME')
            for dadoCNAME in consultaCNAME:
                registrosSecundarios.append(subdominio + ' 14400s CNAME ' + str(dadoCNAME))
            subdominios.remove(subdominio)

    # se tem registros A dos subdominios
    for subdominio in subdominios:
        if tem_registros(subdominio + '.' + dominio, 'A'):
            consultaASec = getRegistros(subdominio + '.' + dominio, 'A')
            for dadoASec in consultaASec:
                registrosSecundarios.append(subdominio + ' 14400s A ' + str(dadoASec))
            subdominios.remove(subdominio)

    # se tem registros TXT dos subdomínio
    for subdominio in subdominios:
        if tem_registros(subdominio + '.' + dominio, 'TXT'):
            consultaTXTSec = getRegistros(subdominio + '.' + dominio, 'TXT')
            for dadoTXTSec in consultaTXTSec:
                registrosSecundarios.append(subdominio + ' 14400s TXT ' + str(dadoTXTSec))
            subdominios.remove(subdominio)

    # se tem registros SRV dos subdomínios
    for registro in registros_srv:
        if tem_registros(registro + "." + dominio, 'SRV'):
            consultaSRVSec = getRegistros(registro + "." + dominio, 'SRV')
            for dadoSRVSec in consultaSRVSec:
                registrosSRV.append(registro + ' 14400s SRV ' + str(dadoSRVSec))

    # imprime a lista com os itens
    print()
    print()
    if registrosPrincipais:
        for item in registrosPrincipais:
            print(item)
    else:
        print('Sem registros na raíz.')

    if registrosSecundarios:
        for item2 in registrosSecundarios:
            print(item2)
    else:
        print('Sem registros dos subdomínios.')

    if registrosSRV:
        for item3 in registrosSRV:
            print(item3)
    else:
        print('Sem registros SRV.')

    print()
    print(f'{bcolors.GREEN}Quantidade de registros: {bcolors.RESET}' + str(len(registrosPrincipais) + len(registrosSecundarios)))
    print()
    print(f'{bcolors.GRAY}Registros não localizados:{bcolors.RESET}')
    print(subdominios)
    print()

    print(f'{bcolors.YELLOW}Registros NS:{bcolors.RESET}')
    # mostra o registro NS da raiz
    if tem_registros(dominio, 'NS'):

        # exibe o registro NS
        consultaNS = getRegistros(dominio, 'ns')
        for dadoNS in consultaNS:
            print(dadoNS)


def check_domains():
    global dominios
    print(f'{bcolors.BLUE}Informe o nome do arquivo:{bcolors.RESET}')
    nome_arquivo = input()
    if os.path.isfile(nome_arquivo + '.txt'):
        try:
            dominios = open(nome_arquivo + '.txt', 'r')
            for dominio in dominios:
                dominio = dominio.rstrip('\n')
                print(dominio + ':')
                if tem_registros(dominio, 'NS'):
                    # exibe o registro NS
                    consultaNS = getRegistros(dominio, 'ns')
                    for dadoNS in consultaNS:
                        print(dadoNS)
                else:
                    print('Nenhum registro NS encontrado.')
                print('----------------------------------')
        except:
            print("Erro ao abrir a lista de domínios.")
        finally:
            dominios.close()
    else:
        print('O arquivo não existe!')


def verificar_registro():
    input_registro = ""
    print(f"{bcolors.BLUE}Digite o domínio:{bcolors.RESET}")
    input_dominio = input()
    print()
    print(f"{bcolors.BLUE}Digite o registro a ser verificado: (Ex.: mail, webmail){bcolors.RESET}")
    input_registro = input()
    print()
    print(f"{bcolors.BLUE}Digite o tipo do Registro: (Ex.: mx, txt, ns, a, cname){bcolors.RESET}")
    input_tipo = input()
    print()

    if input_registro == "":
        endereco_buscado = input_dominio
    else:
        endereco_buscado = input_registro + '.' + input_dominio

    if tem_registros(endereco_buscado, input_tipo):
        consulta_tipo = getRegistros(endereco_buscado, input_tipo)
        for dado in consulta_tipo:
            print(input_registro + ' 14400s ' + input_tipo.upper() + ' ' + str(dado))
    else:
        print('O registro informado não existe.')

while True:
    print('----------------------------------')
    print(f"{bcolors.BLUE}1 - Analisar um domínio. {bcolors.RESET}")
    print(f"{bcolors.BLUE}2 - Verificar um registro.{bcolors.RESET}")
    print(f"{bcolors.BLUE}3 - Checar domínios do arquivo .txt{bcolors.RESET}")
    print(f"{bcolors.BLUE}0 - Sair.{bcolors.RESET}")
    escolha = input()
    if escolha.isnumeric():
        escolha = int(escolha)
        if escolha == 1:
            main()
        elif escolha == 2:
            verificar_registro()
        elif escolha == 3:
            check_domains()
        elif escolha == 0:
            break
        else:
            print("Digite um valor válido!")
    else:
        print("Digite apenas números!")
