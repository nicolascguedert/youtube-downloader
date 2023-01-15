#pip install pytube and moviepy
from pytube import YouTube, Playlist
import os, re, moviepy.editor as mp, PySimpleGUI as sg
class IndividualVideo(): #constrói a classe IndividualVideo atribuindo self.objYT na função da API
    def __init__(self, link):
        self.link=link
        self.objYT = YouTube(link)


class PlaylistVideo(): #constrói a classe PlaylistVideo atribuindo self.objYTPL na função da API
    def __init__(self,link):
        self.link = link
        self.objYTPL = Playlist(link)


class IndividualDownload(IndividualVideo): #constrói a classe herdando a superclasse IndividualVideo
    def __init__(self, link, path):
        super().__init__(link)
        self.path = path
    
    def downloadVideo(self): #busca e faz o download do video
        self.objYT.streams.get_highest_resolution().download(self.path, filename_prefix="video_", skip_existing= True)
    
    def downloadAudio(self): #busca o video e faz o download somente do audio
        self.objYT.streams.filter(only_audio = True).first().download(self.path, filename_prefix="audio_", skip_existing= True)
        conversor(self.path)


class PlaylistDownload(PlaylistVideo, IndividualDownload): #constrói a classe herdando outras classes/polimorfismo
    def __init__(self, link, path): # continua a construir a classe entrando o link e o path
        super().__init__(link) #chama a superclasse Playlist video e atribui o valor do link
        self.name = self.objYTPL.title
        self.path = path+'/'+self.name

    def downloadAudio(self, url): #busca o video de acordo com o link fornecido e faz o download do audio, sendo usado dentro do for do AllTracks e AllVideos
        YouTube(url).streams.filter(only_audio = True).first().download(self.path, filename_prefix="audio_", skip_existing= True) #removi o conversos para quando for chamar o download audio não chamar a função muitas vezes desnecessariamente
        
    def downloadAllVideos(self, selecionados): #faz somente o download de todos os video selecionados na playlist
        self.selecionados = selecionados
        for url in self.objYTPL.video_urls:
            if url in self.selecionados:
                IndividualDownload(url, self.path).downloadVideo()
    
    def downloadAllTracks(self, selecionados): #faz somente o download de todos os audios selecionados na playlist
        self.selecionados = selecionados
        for url in self.objYTPL.video_urls:
            if url in self.selecionados:
                self.downloadAudio(url)
        conversor(self.path)

    def setJanela(self): #permite a possibilidade de alterar a lista de objetos referentes a playlist
        layout = [[sg.Text(self.objYTPL.title)]]
        for video in self.objYTPL.videos:
            layout.append([sg.Checkbox(video.title, key=video.video_id, default=True)],)
        layout.append([sg.Button('Back'), sg.Button('Ok')])
        return sg.Window("Select medias", layout=layout, finalize=True)

        
class Validators(): #constrói a classe entrando o link e path
    def __init__(self,link,path):
        self.link = link
        self.path = path

    def validator_link(self): #confere se o link é válido
        if "playlist" not in self.link:
            try:
                YouTube(self.link)
            except:
                sg.PopupAutoClose("Invalid Link! Enter again!!")
            else:
                return True
        else:
            try:
                Playlist(self.link)
            except:
                sg.PopupAutoClose("Invalid Link! Enter again!!")
            else:
                return True
                    
        
    def validator_path(self): #busca se o caminho existe no sistema e retorna o status
        status = os.path.lexists(self.path)
        if status == False:
            sg.PopupOK("Invalid Path! Enter again!!")
        else:
            return status


def conversor(path): #converte os arquivos de mp4 para mp3, não constítui uma classe, def solitária para uso dentro das classes de Download
    for file in os.listdir(path):                      #For para percorrer dentro da pasta passada anteriormente
            if re.search('mp4', file) and "audio_"in file:                 #If verificando se o arquivo e .MP4                    
                mp4_path = os.path.join (path, file)   #Cria uma variavel para armazenar o arquivo .MP4
                mp3_path = os.path.join (path, os.path.splitext(file)[0] + ".mp3") # Variavel que cria o nome do arquivo e adiciona .MP3 ao final
                new_file = mp.AudioFileClip(mp4_path)  #Cria o arquivo de acordo com o tipo
                new_file.write_audiofile(mp3_path)     #Renomeia o arquivo, setando o nome criado anteriormente
                os.remove(mp4_path)                    #Remove o arquivo .MP4; desetivar linha permite salvar o audio e video do mesmo video ao mesmo tempo