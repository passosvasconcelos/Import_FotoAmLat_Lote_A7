from tkinter import * #Tkinter é a interface gráfica utilizada pelo python
#Programa utiliza 3 funções que são executadas por 3 botões: primeiro botão lê o anasete, segundo botão lê as fotos e terceiro botão processa a transferência dos arquivos


from PIL import ImageTk, Image #bibliotecas do python utilizadas para manipular arquivos .jpg
import os #Bibliotecas do python utilizadas para manipular e buscar arquivos em geral no pc:
root=Tk()
class lote:
    def __init__(self,root): #a função __init__ é sempre a primeira função a ser iniciada pela classe Lote quando a executar-mos
        #define variáveis:
        self.root=root
        self.a7original=StringVar()
        self.fotos=StringVar()
        self.fotos.set("nenhuma foto carregada")
        self.listafotos=[]
        self.nomedoarquivo=StringVar()
        self.nomedoarquivo.set("Nenhum arquivo selecionado")
        self.destino=StringVar()
        self.tipoDeAmostra=StringVar()
        self.tipoDeAmostra.set("lateral")
        self.andamento=StringVar()
        self.testos=[]

        #Interface grafica:
        frameprincipal=Frame(self.root)
        frameprincipal.pack(side=TOP)
        frameOpcoes=Frame(frameprincipal)
        frameOpcoes.pack(side=TOP)
        opcao1=Radiobutton(frameOpcoes, text="Amostra lateral", value="lateral", variable=self.tipoDeAmostra)
        opcao2=Radiobutton(frameOpcoes, text="Lâmina", value="lamina", variable=self.tipoDeAmostra)
        opcao3=Radiobutton(frameOpcoes, text="LaminaTesto", value="laminatesto", variable=self.tipoDeAmostra)
        opcao1.pack(side=LEFT, fill=X)
        opcao2.pack(side=LEFT, fill=X)
        opcao3.pack(side=LEFT, fill=X)
        
        frame1=Frame(frameprincipal)
        frame1.pack(side=LEFT, anchor="nw")
        dica1=Label(frame1, text="1- selecione o Anasete-->", font="arial 12 bold")
        dica1.pack(side=TOP, anchor="e")
        dica2=Label(frame1, text="2- selecione as fotos-->", font="arial 12 bold")
        dica2.pack(side=TOP, anchor="e")
        dica3=Label(frame1, text="3- copie as fotos-->", font="arial 12 bold")
        dica3.pack(side=TOP, anchor="e")

        frame2=Frame(frameprincipal)
        frame2.pack(side=LEFT, anchor="nw")
        b1=Button(frame2, text="selecionar", command=self.lendoa7)
        b1.pack(side=TOP, anchor="w", fill=X)
        b2=Button(frame2, text="selecionar", command=self.lendofotos)
        b2.pack(side=TOP, anchor="w", fill=X)
        b3=Button(frame2, text="copiar fotos", command=self.geralote)
        b3.pack(side=TOP, anchor="w", fill=X)

        frame3=Frame(frameprincipal)
        frame3.pack(side=LEFT)        
        self.arquivoselecionado=Label(frame3, text="anasete selecionado: "+self.nomedoarquivo.get(), font="12")
        self.arquivoselecionado.pack(side=TOP)                
        self.LabelFotos=Label(frame3, text="nenhuma foto carregada", font="12")
        self.LabelFotos.pack(side=TOP)        
        self.labelStatus=Label(frame3, text="nenhuma foto copiada!", font="12")
        self.labelStatus.pack(side=TOP)
    def lendoa7(self): #função lê o arquivo anasete
        ftypes = [('Anasete', '*.a7')]
        dlg = filedialog.Open(root, filetypes = ftypes)
        fl=dlg.show() #dlg.show() retorna o endereço do arquivo selecionado e salva na variável fl
        num_testemunhos=0
        a7dados=""
        if fl != '':            
            a7=open(fl, "r")
            a7.seek(0,2)
            tamanho=a7.tell()
            a7.seek(0)
            while a7.tell()<tamanho:
                print (str(int((a7.tell()*1.0/tamanho)*100))+"%" )
                
                a7dados+=a7.read(524288)
                
            print (str(int((a7.tell()*1.0/tamanho)*100))+"% carregado com êxito!")
            a7.seek(0)
            print (a7dados.find("25 12~Nome do poço\n"))
            print (a7dados[a7dados.find("25 12~Nome do poço\n")+20:a7dados.find("25 12~Nome do poço\n")+25])
            for linha in a7:
                
                if linha=="25 12~Nome do poço\n":
                    break
                
            for linha in a7:
                
                num_testemunhos=int(linha.strip("\n"))
                break
            for linha in a7:
                
                if num_testemunhos>0:
                    self.testos.append(linha.split())
                    num_testemunhos-=1
                else:
                    break
            if self.testos!=[]:
                for i in range(len(self.testos)):
                    self.testos[i].append(float(self.testos[i][0]) - float(self.testos[i][2]))
                print ("testemunhos -->", self.testos)
            else:
                print ("Anasete sem testemunhos")
            
            l=fl.split("/")
            caminho=l[:-1]
            self.destino.set("/".join(caminho))
            
            self.nomedoarquivo.set(l[-1])
            self.a7original.set(fl)
            self.arquivoselecionado.configure(text="anasete selecionado: "+self.nomedoarquivo.get(), font="arial 10 bold")
        return 0
    def lendofotos(self):
        ftypes = [('jpg files', '*.jpg')]
        dlg = tkFileDialog.askopenfilenames(filetypes=[('imagem jpeg', '*.jpg')])
        
        if dlg[0]=="{":
            dlg=dlg.replace("} {","$")
            dlg=dlg.strip("{")
            dlg=dlg.strip("}")
            self.listafotos=dlg.split("$")
        else:
            self.listafotos=dlg.split(" ")
        
        self.listafotos.sort()    
        self.LabelFotos.configure(text="Fotos carregadas!!!", font="arial 10 bold")
        
        return 0
    
    def geralote(self):
        if self.listafotos==[]:
            print ("comando inválido: nenhuma foto selecionada para carregar no anasete")
            return 0
        elif self.nomedoarquivo.get()=="Nenhum arquivo selecionado":
            print ("comando inválido: nenhum anasete foi selecionado")
            return 0
        if self.tipoDeAmostra.get()=="lateral":
            a7=open(self.a7original.get(), "r")
            novoa7=open(self.a7original.get().strip(".a7")+"_temp.a7", "a")
            trilhaanterior=""
            escreveu_conteudo=False
            l_edit=""
            amlat_edit=""
            amostraAnterior=0000,00
            indiceAmLat=0
            totaldefotos=len(self.listafotos)
            contador=0
            for i in self.listafotos:
                contador+=1
                subindice=0
                amostraDupla=False
                im=Image.open(i)
                l=i.split("/")
                foto=l[-1]
                
                self.andamento.set("Transferindo: "+foto+" andamento: "+str(contador)+"/"+str(totaldefotos))
                if foto[:foto.find("m")]==amostraAnterior:
                    amlat_edit=amlat_edit.replace("\n   1.0000000 "+foto[:foto.find("m")], "\n   2.0000000 "+foto[:foto.find("m")])
                
                    n_caracteres=len(foto.strip(".jpg"))
                    l_edit=l_edit.replace(foto[:foto.find("m")]+"000 2\n   0\n   0\n   1", foto[:foto.find("m")]+"000 2\n   0\n   0\n   2")
                    l_edit+="\n    "+str(n_caracteres)+"~"+foto[:n_caracteres]
                    subindice=1
                    amostraDupla=True
                    indiceAmLat-=1

                if amostraDupla==False:
                    amostraAnterior=foto[:foto.find("m")]
                
                    n_caracteres=len(foto.strip(".jpg"))
                    amlat_edit+="\n   1.0000000 "+foto[:foto.find("m")]
                
                    l_edit+="\n  "+str(indiceAmLat)+" "+foto[:foto.find("m")]+"000 2\n   0\n   0\n   1\n    "+str(n_caracteres)+"~"+foto[:n_caracteres]
                
                
                
                fotosa7=str(self.nomedoarquivo.get().strip(".a7")+".DL"+str(indiceAmLat)+"#"+str(subindice))
                im.save(self.destino.get()+"/"+foto)
                os.rename(self.destino.get()+"/"+foto, self.destino.get()+"/"+fotosa7)
                print ("foto original: ", foto, "foto no anasete: ", fotosa7)
                print (self.andamento.get())
                indiceAmLat+=1
                
                
            
        
            l_edit=l_edit.replace(",",".")

            lin=0
            leu=False
            for linha in a7:
                if linha!="\n":
                
                    l=linha.split()
                    if l[0]=="nome" and escreveu_conteudo==False:
                        trilhaanterior=linha.strip("nome = ")
                        trilhaanterior=trilhaanterior.strip(",\n")
                    if linha=="TipoConteudo:cria {\n" and escreveu_conteudo==False or linha=="TipoCurvaXY:cria {\n" and escreveu_conteudo==False or linha=="TipoIntervaloValor:cria {\n" and escreveu_conteudo==False:
                        novoa7.write("TipoTrilha:cria {\n  anterior = TipoTrilha.objeto[ "+trilhaanterior+" ],\n  largura = 80,\n  nome = 'Foto AmLat',\n  cabecalho = 1,\n}\n\n")
                        novoa7.write("TipoConteudo:cria {\n  grid_tick_h = 0,\n  trilha = TipoTrilha.objeto[ 'Foto AmLat' ],\n  min = 0,\n  max = 100,\n  cor = '255 255 255',\n  estilo = 0,\n  grid = 0,\n  nome = 'Amostra Lateral',\n  grid_tick_v = 1,\n  espessura = 1,\n}\n\n")
                        novoa7.write("TipoCurvaXY:cria {\n  grid = 0,\n  tam_marca = 2,\n  cor = '255 125 0',\n  colorir = 0,\n  cor_colorir = '255 255 255',\n  min = 0,\n  max = 2,\n  nome = 'Amlat',\n  cab_texto = 'Amlat',\n  cab_valores = 0,\n  marca = 3,\n  estilo = 0,\n  escala = 0,\n  grid_tick_v = 1,\n  preencher = 0,\n  trilha = TipoTrilha.objeto[ 'AmLat' ],\n  espessura = 1,\n  ligapontos = 'sem_conexao',\n  cab_ticks = 0,\n  invalido = 'ignora',\n  grid_tick_h = 0,\n}\n\n")
                    
                        escreveu_conteudo=True
                    if linha=="$if nil\n":
                        lin=0
                        leu=True
                    
                    if lin==4 and leu==True:
                        amlat_edit=amlat_edit.replace(",",".")
                        total_dados=linha.strip("\n")
                        novo_total_dados=int(total_dados)+2
                        novoa7.write(str(novo_total_dados)+"\n")
                        novoa7.write("22 15~Amostra Lateral\n "+str(indiceAmLat)+l_edit+"\n")
                        novoa7.write("2 5~Amlat\n "+str(indiceAmLat)+amlat_edit+"\n")
                    
                    
                        break
                    
                lin+=1        
                novoa7.write(linha)
            for linha in a7:
                novoa7.write(linha)
        
            novoa7.close()
            a7.close()
            os.remove(self.a7original.get())
            os.rename(self.a7original.get().strip(".a7")+"_temp.a7",self.a7original.get())
                
        
            self.labelStatus.configure(text="Processo concluído com sucesso!", font="arial 12 bold", foreground="blue")
            return "amostras laterais transferidas com sucesso!"
    

        elif self.tipoDeAmostra.get()=="laminatesto":
            a7=open(self.a7original.get(), "r")
            novoa7=open(self.a7original.get().strip(".a7")+"_temp.a7", "a")
            trilhaanterior=""
            escreveu_conteudo=False
            l_edit=""
            amlat_edit=""
            amostraAnterior=0000,00
            indiceAmLat=0
            totaldefotos=len(self.listafotos)
            contador=0
            t=0
            prof_lamina_movimentada=""
            for i in self.listafotos:
                contador+=1
                subindice=0
                amostraDupla=False
                im=Image.open(i)
                l=i.split("/")
                foto=l[-1]
                foto=foto.replace(",",".")
                
                self.andamento.set("Transferindo: "+foto+" andamento: "+str(contador)+"/"+str(totaldefotos))
                if foto[:foto.find("m")]==amostraAnterior:
                                   
                    n_caracteres=len(foto.strip(".jpg"))
                    l_edit=l_edit.replace(prof_lamina_movimentada+" 0\n   0\n   1\n    ", prof_lamina_movimentada+" 0\n   0\n   2\n    ")
                    
                    l_edit+=str(n_caracteres)+"~"+foto[:n_caracteres]
                    l_edit=l_edit.replace("\n   0"+str(n_caracteres)+"~"+foto[:n_caracteres], "\n    "+str(n_caracteres)+"~"+foto[:n_caracteres]+"\n   0")
                    subindice=1
                    amostraDupla=True
                    indiceAmLat-=1

                if amostraDupla==False:
                    amostraAnterior=foto[:foto.find("m")]
                    
                    n_caracteres=len(foto.strip(".jpg"))
                    if (float(foto[:foto.find("m")])) > (float(self.testos[t][1]) - float(self.testos[t][3])):
                        t+=1
                    if (float(self.testos[t][2])) <= (float(foto[:foto.find("m")])) <= (float(self.testos[t][1]) - float(self.testos[t][3])):
                        print ("testemunho ", t)
                        print ("base sondador: ", (float(self.testos[t][1]) - float(self.testos[t][3])))
                        prof_lamina_movimentada=str(float(foto[:foto.find("m")])+self.testos[t][3])
                        l_edit+="\n  "+str(indiceAmLat)+" "+prof_lamina_movimentada+" 0\n   0\n   1\n    "+str(n_caracteres)+"~"+foto[:n_caracteres]+"\n   0"

                    
                
                
                
                fotosa7=str(self.nomedoarquivo.get().strip(".a7")+".LT"+str(indiceAmLat)+"#"+str(subindice))
                im.save(self.destino.get()+"/"+foto)
                os.rename(self.destino.get()+"/"+foto, self.destino.get()+"/"+fotosa7)
                print ("foto original: ", foto, "foto no anasete: ", fotosa7)
                print (self.andamento.get())
                indiceAmLat+=1
                
                
            
        
            l_edit=l_edit.replace(",",".")

            lin=0
            leu=False
            for linha in a7:
                if linha!="\n":
                
                    l=linha.split()
                    if l[0]=="nome" and escreveu_conteudo==False:
                        trilhaanterior=linha.strip("nome = ")
                        trilhaanterior=trilhaanterior.strip(",\n")
                    if linha=="TipoConteudo:cria {\n" and escreveu_conteudo==False or linha=="TipoCurvaXY:cria {\n" and escreveu_conteudo==False or linha=="TipoIntervaloValor:cria {\n" and escreveu_conteudo==False:
                        novoa7.write("TipoTrilha:cria {\n  anterior = TipoTrilha.objeto[ "+trilhaanterior+" ],\n  largura = 80,\n  nome = 'Fotos de Detalhe',\n  cabecalho = 1,\n}\n\n")
                        novoa7.write("TipoConteudo:cria {\n  grid_tick_h = 0,\n  trilha = TipoTrilha.objeto[ 'Fotos de Detalhe' ],\n  min = 0,\n  max = 100,\n  cor = '255 255 255',\n  estilo = 0,\n  grid = 0,\n  nome = 'Fotos de Detalhe',\n  grid_tick_v = 1,\n  espessura = 1,\n}\n\n")
                        
                        escreveu_conteudo=True
                    if linha=="$if nil\n":
                        lin=0
                        leu=True
                    
                    if lin==4 and leu==True:
                        amlat_edit=amlat_edit.replace(",",".")
                        total_dados=linha.strip("\n")
                        novo_total_dados=int(total_dados)+1
                        novoa7.write(str(novo_total_dados)+"\n")
                        novoa7.write("22 16~Fotos de Detalhe\n "+str(indiceAmLat)+l_edit+"\n")
                    
                    
                        break
                    
                lin+=1        
                novoa7.write(linha)
            for linha in a7:
                novoa7.write(linha)
        
            novoa7.close()
            a7.close()
            os.remove(self.a7original.get())
            os.rename(self.a7original.get().strip(".a7")+"_temp.a7",self.a7original.get())
                
        
            self.labelStatus.configure(text="Processo concluído com sucesso!", font="arial 12 bold", foreground="blue")
            return "amostras laterais transferidas com sucesso!"
    




        elif self.tipoDeAmostra.get()=="lamina":
            print ("não disponível... (Ainda)")
            return 0
app = lote(root)
root.title("Importação de fotos de amostra lateral - Grupo A7")
root.geometry("700x100")
root.mainloop()
