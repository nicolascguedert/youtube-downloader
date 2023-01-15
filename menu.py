from funções import *
#pip install PySimpleGUI
import PySimpleGUI as sg


sg.theme("DarkTanBlue") #determina o tema do GUI
layout = [[sg.Text('Origin URL:', size = (12, 0)), sg.InputText(size = (60,30)),], #primeira linha
        [sg.Text('Folder Path:', size = (12, 0)), sg.InputText(size = (60,30)), sg.FolderBrowse()], #segunda linha
        [sg.Button('Download Video'), sg.Button('Download Audio'), sg.Button('Cancel')]] #terceira linha
janela = sg.Window("MEDIA DOWNLOADER", layout=layout, finalize=True) #atribui o GUI
janela2 = None #desativa


while True:
    window, event, values = sg.read_all_windows() #lê os dados da janela
    
    # TRATAMENTO DE SAíDA #
    if event == sg.WIN_CLOSED or event == 'Cancel': # fecha o programa se o usuário fechar a janela ou pressionar cancel
        break
    #---------------------#
    
    # TRATAMENTO DE VIDEO #
    if window==janela: #escolhe a primeira janela

        elink = Validators(values[0], values[1]).validator_link() #tratamento de link
        epath = Validators(values[0], values[1]).validator_path() #tratamento de path
        
        audio=False  #desatribui/começa desatribuido o dowload do audio
        video=False  #desatribui/começa desatribuido o dowload do video

        match event: #funciona igual um swith case, quando o event da janela 1 for igual a x
            case 'Download Video': #executa o download video
                if epath == True and elink == True: #somente se o link e path forem válidos
                    if "playlist" in values[0]: #se for uma playlist
                        link = values[0] #atribui os links da playlist para a variável link a ser usada na seleção
                        path= values[1] #atribui o caminho de download para a variável path a ser usada na seleção
                        janela2 = PlaylistDownload(values[0], values[1]).setJanela() #abre a segunda janela para seleção
                        janela.hide() #esconde a primeira janela
                        video=True #atribui o download video
                    else:
                        IndividualDownload(values[0], values[1]).downloadVideo() #se não for uma playlist, o download ocorre de forma direta
                        sg.PopupAutoClose('Download completed successfully!!') #mostra na tela que o download foi um sucesso
    #---------------------#
            
    # TRATAMENTO DE AUDIO #
            case'Download Audio': #executa o download audio
                if epath == True and elink == True: #somente se o link e path forem válidos
                    if "playlist" in values[0]: #se for uma playlist
                        link = values[0] #atribui os links da playlist para a variável link a ser usada na seleção
                        path=values[1] #atribui o caminho de download para a variável path a ser usada na seleção
                        janela2 = PlaylistDownload(values[0], values[1]).setJanela() #abre a segunda janela para seleção
                        janela.hide() #esconde a primeira janela
                        audio=True #atribui o download audio
                    else:
                        IndividualDownload(values[0], values[1]).downloadAudio() #se não for uma playlist, o download ocorre de forma direta
                        sg.PopupAutoClose('Download completed successfully!!') #mostra na tela que o download foi um sucesso
    #---------------------#

    # JANELA DE SELEÇÃO #
    if window==janela2: #escolhe a segunda janela chamada no download da playlist
        match event: #funciona igual um swith case, quando o event da janela 2 for igual a x
            case 'Back': #se o usuário decidir voltar
                janela2.hide() #esconde a janela 2
                janela2=None #desativa
                audio=False #desatribui o download audio
                video=False #desatribui o download video
                janela.un_hide() #retorna/reabre a janela 1

            case 'Ok': #se o usuário prosseguir
                selecionados=[] #cria a lista de selecionados vazia
                for chave, valor in values.items(): #percorre a lista de valores padrão
                    if valor==True: #se estiver selecionado
                        selecionados.append("https://www.youtube.com/watch?v="+chave) #adiciona na lista
                if audio: #se for audio faz/chama o download dos audios
                    PlaylistDownload(link, path).downloadAllTracks(selecionados)
                elif video: #se for video faz/chama o download dos videos
                    PlaylistDownload(link, path).downloadAllVideos(selecionados)
                janela2.hide() #esconde a janela 2
                janela2=None #desativa
                audio=False #desatribui o download audio
                video=False #desatribui o download video
                sg.PopupAutoClose('Download completed successfully!!') #mostra na tela que o download foi um sucesso
                janela.un_hide() #retorna/reabre a janela 1
    #--------------------#
    values[0], values[1] = '', '' #exclui os values para executar novamente
janela.close() #finaliza/fecha o programa