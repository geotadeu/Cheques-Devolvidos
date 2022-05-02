import pandas as pd
from config import *
from tkinter import messagebox

class Exportador:
    def exportar(self, tipo, cooperativa, pa, caminho1, caminho2, caminho3):
        self.cooperativa = int(cooperativa)
        self.pa = str(pa)
        self.pac_cliente = int(''.join([n for n in self.pa if n.isdigit()]))
        self.geral = False

        pd.set_option('display.max_rows', 500)
        pd.set_option('display.max_columns', 500)
        pd.set_option('display.width', 1000)

        self.df_cc = self.carregar_arquivo(caminho1, 'csv', ['Com', 'Banco', 'Agencia', 'Conta Dest.', 'Cod Dev', 'Lote', 'Pos.', 'n0', 'n1', 'Ban', 'Ag Dest', 'Ag Dep', 'Conta', 'Nº CH', 'TD', 'Valor', 'Ocorrencia', 'Data', 'n2', 'n3', 'n4', 'n5', 'Valor1', 'Valor2', 'PAC Cliente', 'PA Dep', 'PAC Cliente1', 'n6', 'Canal'], ['Data'])
        self.df_ic = self.carregar_arquivo(caminho2, 'txt', ['temp0', 'temp1', 'Ag Dest', 'Conta', 'PA Dep', 'temp2', 'Banco', 'Agencia', 'temp3', 'Nº CH', 'temp4', 'Cod Dev', 'temp5', 'temp6', 'temp7', 'temp8', 'temp9', 'Valor', 'temp10', 'temp11', 'temp12', 'temp13'])
        self.df_cp = self.carregar_arquivo(caminho3, 'csv', ['temp', 'Ag Dest', 'Conta', 'temp1', 'Data', 'Banco', 'Agencia', 'temp3', 'Nº CH', 'Valor', 'temp4', 'PAC Cliente', 'temp5', 'Cod Dev', 'Ag Dep', 'Info', 'temp6'])
        
        if ((self.df_cc is None) or (self.df_ic is None)):
            messagebox.showwarning('Aviso', 'Selecione arquivos válidos para exportar')
            return

        self.data = self.df_cc.iloc[0]['Data']

        self.tratar_cc()
        self.tratar_ic()
        self.tratar_cp()

        prefix = pd.to_datetime(self.data, format='%d/%m/%Y %H:%M:%S').strftime("%Y-%m-%d") + ' - Cheques devolvidos - '

        if tipo == 'Compensação geral':
            self.geral = True
            self.salvar_arquivo(prefix + 'Compensação Geral.xlsx', self.obter_dados_compensacao())
        elif tipo == 'PA selecionado':
            self.salvar_arquivo(prefix + 'Compensação Individual - ' + str(self.cooperativa) +' - ' + self.pa + '.xlsx', self.obter_dados_pa())
        elif tipo == 'Todos PAs':
            for p in Config.ListaPA:
                self.pa = p
                self.pac_cliente = int(''.join([n for n in p if n.isdigit()]))
                self.salvar_arquivo(prefix + 'Compensação de Agencia - ' + str(self.cooperativa) +' - ' + self.pa + '.xlsx', self.obter_dados_pa())
        elif tipo == 'Resumo de ocorrências':
            self.salvar_arquivo(prefix + 'Resumo de ocorrências.xlsx', self.obter_resumo_ocorrencias())
        else:
            messagebox.showerror('Erro', 'Tipo de relatório inválido')
            return

        messagebox.showinfo('Sucesso', 'O arquivo foi exportado para a pasta de Relatórios!')

    def carregar_arquivo(self, caminho, tipo, colunas, datas=None):
        dados = None
        if not caminho:
            return None
        file = open(caminho, 'r', encoding='UTF-8')
        if not file:
            return None
        if tipo == 'csv':
            dados = pd.read_csv(file, encoding='UTF-8', sep=',', names=colunas)
        elif tipo == 'txt':
            dados = pd.read_fwf(file, names=colunas)
        if dados.empty:
            dados = None
        else:
            if datas:
                for data in datas:
                    pd.to_datetime(dados[data], format='%d/%m/%Y %H:%M:%S')
        return dados

    def salvar_arquivo(self, nome, df):
        df.to_excel(Config.DirRelatorios + '\\' + nome, index=False)

    def tratar_cc(self):
        self.df_cc = self.df_cc.drop(columns=['Com', 'Conta Dest.', 'Lote', 'Pos.', 'n0', 'n1', 'Ban', 'TD', 'n2', 'n3', 'n4', 'n5', 'Valor1', 'Valor2', 'PAC Cliente1', 'n6', 'Canal'])

        # Passar a coluna de ocorrências pro final
        self.df_cc = self.df_cc[['Banco', 'Agencia', 'Cod Dev', 'Ag Dep', 'Conta', 'Ag Dest', 'Nº CH', 'Valor', 'Data', 'PAC Cliente', 'PA Dep', 'Ocorrencia']]

        # Converter a conta
        self.df_cc['Conta'] = self.df_cc['Conta'].str.replace('.', '', regex=True)
        self.df_cc['Conta'] = self.df_cc['Conta'].str.replace('-', '', regex=True)
        self.df_cc['Conta'] = self.df_cc['Conta'].astype(float)

    def tratar_ic(self):
        self.df_ic = self.df_ic.drop(columns=['temp0', 'temp1', 'temp2', 'temp3', 'temp4', 'temp5', 'temp6', 'temp7', 'temp8', 'temp9', 'temp10', 'temp11', 'temp12', 'temp13'])
        self.df_ic = self.df_ic.reindex(columns=self.df_ic.columns.tolist() + ['Ocorrencia', 'Data', 'PAC Cliente', 'Ag Dep', 'Tratativa'])

        # Passar a coluna de ocorrências pro final
        self.df_ic = self.df_ic[['Banco', 'Agencia', 'Cod Dev', 'Ag Dep', 'Conta', 'Ag Dest', 'Nº CH', 'Valor', 'Data', 'PAC Cliente', 'PA Dep', 'Tratativa', 'Ocorrencia']]

        # Converter a agência destino               
        self.df_ic['Ag Dest'] = self.df_ic['Ag Dest']*1000
        self.df_ic['Ag Dest'] = self.df_ic['Ag Dest'].mask(self.df_ic['Ag Dest'] == 1000, 1)
        self.df_ic['Ag Dest'] = self.df_ic['Ag Dest'].astype(float)

        # Converter o valor
        self.df_ic['Valor'] = self.df_ic['Valor'].str.replace(',', '-', regex=True)
        self.df_ic['Valor'] = self.df_ic['Valor'].str.replace('.', '', regex=True)
        self.df_ic['Valor'] = self.df_ic['Valor'].str.replace('-', '.', regex=True)
        self.df_ic['Valor'] = self.df_ic['Valor'].astype(float)

        # Converter a conta
        self.df_ic['Conta'] = self.df_ic['Conta'].str.replace('.', '', regex=True)
        self.df_ic['Conta'] = self.df_ic['Conta'].str.replace('-', '', regex=True)
        self.df_ic['Conta'] = self.df_ic['Conta'].astype(float)

    def tratar_cp(self):
        self.df_cp = self.df_cp.drop(columns=['temp', 'temp1', 'temp3', 'temp4', 'temp5', 'temp6'])
        self.df_cp = self.df_cp.reindex(columns=self.df_cp.columns.tolist() + ["PA Dep", 'Ocorrencia'])
        
        # Passar a coluna de ocorrências pro final
        self.df_cp = self.df_cp[['Banco', 'Agencia', 'Cod Dev', 'Ag Dep', 'Conta', 'Ag Dest', 'Nº CH', 'Valor', 'Data', 'PAC Cliente', 'PA Dep', 'Info', 'Ocorrencia']]
        
        # Converter a conta
        self.df_cp['Conta'] = self.df_cp['Conta'].astype(float)
        
        # Mesclar relatório de poupança com intercredis
        self.df_cp = pd.merge(self.df_cp, self.df_ic[["Banco", "Agencia", "Conta", "Nº CH", "Valor", "PA Dep"]], on=["Banco", "Agencia", "Conta", "Nº CH", "Valor"], how="left")
        self.df_cp = self.df_cp.drop(columns=["PA Dep_x"]).rename(columns={'PA Dep_y': 'PA Dep'})
        self.df_cp = self.df_cp[['Banco', 'Agencia', 'Cod Dev', 'Ag Dep', 'Conta', 'Ag Dest', 'Nº CH', 'Valor', 'Data', 'PAC Cliente', 'PA Dep', 'Info', 'Ocorrencia']]

    def obter_resumo_ocorrencias(self):
        df_todos = pd.DataFrame(self.df_cc.sort_values(by=['Ocorrencia'], inplace=True))
        df_todos.loc[df_todos['Ocorrencia'].notnull()]
        df_todos['Data'] = self.data
        df_todos['Data'] = pd.to_datetime(df_todos['Data'], format='%d/%m/%Y %H:%M:%S').apply(lambda x: x.date())
        return df_todos

    def obter_dados_ocorrencias(self, ocorrencias):
        # Tratar e obter dados C/C
        df_cc = pd.DataFrame(self.df_cc)

        # Tratar e obter dados C/P
        df_cp = pd.DataFrame(self.df_cp)

        # Tratar e obter dados InterCredi
        df_ic = pd.DataFrame(self.df_ic)
        
        # Tratamento e concatenação da base
        df_todos = pd.concat([
            ocorrencias,
            self.tratativa_cc_pa_proprio(df_cc),
            self.tratativa_cp_pa_proprio(df_cp),
            self.tratativa_cc_pa_receber(df_cc),
            self.tratativa_cc_pa_enviar(df_cc),
            self.tratativa_cp_pa_receber(df_cp),
            self.tratativa_cp_pa_enviar(df_cp),
            self.tratativa_cc_ic_receber(df_cc),
            self.tratativa_cc_ic_enviar(df_ic),
            self.tratativa_cp_ic_receber(df_cp),
            self.tratativa_cp_ic_enviar(df_cp)
            ])
        
        df_todos['Data'] = self.data
        df_todos['Data'] = pd.to_datetime(df_todos['Data'], format='%d/%m/%Y %H:%M:%S').apply(lambda x: x.date())
        return df_todos[['Banco', 'Agencia', 'Cod Dev', 'Ag Dep', 'Conta', 'Ag Dest', 'Nº CH', 'Valor', 'Data', 'PAC Cliente', 'PA Dep', 'Tratativa', 'Ocorrencia']] 

    def obter_dados_compensacao(self):
        ocorrencias = self.df_cc.loc[
            (self.df_cc['Ocorrencia'].notnull()) &
            (self.df_cc['Ocorrencia'].ne('CHEQUE DEPOSITADO VIA CELULAR')) &
            (self.df_cc['Ocorrencia'].ne('EFETUAR NOVO DEPÓSITO'))]
        ocorrencias.insert(len(ocorrencias.columns), 'Tratativa', 'Ocorrencia')

        return self.obter_dados_ocorrencias(ocorrencias)

    def obter_dados_pa(self):
        ocorrencias = self.df_cc.loc[
            (self.df_cc['Ocorrencia'].notnull()) &
            (self.df_cc['Ocorrencia'].ne('CHEQUE DEPOSITADO VIA CELULAR')) &
            (self.df_cc['Ocorrencia'].ne('EFETUAR NOVO DEPÓSITO')) &
            (self.df_cc['PA Dep'].eq(self.pa) | self.df_cc['PAC Cliente'].eq(self.pac_cliente))]
        ocorrencias.insert(len(ocorrencias.columns), 'Tratativa', 'Ocorrencia')

        return self.obter_dados_ocorrencias(ocorrencias)

    def tratativa_cc_pa_proprio(self, df):
        df_saida = pd.DataFrame(df.loc[
            (df['Ag Dep'].eq(self.cooperativa) | self.busca_geral()) & 
            (df['PA Dep'].eq(self.pa)) & 
            (df['PAC Cliente'].eq(self.pac_cliente) | self.busca_geral()) & 
            (df['Ocorrencia'].ne('CHEQUE C/ TRATAMENTO P/ TD'))])
        df_saida.insert(len(df_saida.columns), 'Tratativa', 'Conta-Corrente - Meu PA')
        return df_saida.sort_values(by=['Ag Dest','Conta'], ascending=True)

    def tratativa_cc_pa_receber(self, df):
        df_saida = pd.DataFrame(df.loc[
            (df['Ag Dep'].eq(self.cooperativa) | self.busca_geral()) &
            (df['PA Dep'].ne(self.pa) & ((not self.busca_geral()) | df['PA Dep'].eq(self.pa))) &
            (df['PAC Cliente'].eq(self.pac_cliente) | self.busca_geral())])
        df_saida.insert(len(df_saida.columns), 'Tratativa', 'Conta-Corrente - InterPA Receber')
        return df_saida.sort_values(by=['Ag Dest','Conta'], ascending=True)

    def tratativa_cc_pa_enviar(self, df):
        df_saida = pd.DataFrame(df.loc[
            (df['Ag Dep'].eq(self.cooperativa) | self.busca_geral()) &
            (df['PA Dep'].eq(self.pa) | self.busca_geral()) & 
            (df['PAC Cliente'].ne(self.pac_cliente) & (not self.busca_geral()))])
        df_saida.insert(len(df_saida.columns), 'Tratativa', 'Conta-Corrente - InterPA Enviar')
        return df_saida.sort_values(by=['Ag Dest','Conta'], ascending=True)

    def tratativa_cc_ic_receber(self, df):
        df_saida = pd.DataFrame(df.loc[
            (df['Ocorrencia'].isnull()) &
            (df['Ag Dep'].ne(self.cooperativa)) & 
            (df['PAC Cliente'].eq(self.pac_cliente) | self.busca_geral())])
        df_saida.insert(len(df_saida.columns), 'Tratativa', 'Conta-Corrente - InterCredi Receber')
        return df_saida.sort_values(by=['Ag Dest','Conta'], ascending=True)

    def tratativa_cc_ic_enviar(self, df):
        df_saida = pd.DataFrame(df.loc[
            (~(df['Ag Dest'] == 1)) & 
            (df['Ag Dep'].eq(self.cooperativa) | self.busca_geral()) &
            (df['PA Dep'].eq(self.pa) | self.busca_geral())])
        df_saida = df_saida.drop(columns=['Tratativa', 'Ag Dep'])
        df_saida.insert(4, 'Ag Dep', Config.CoopAtual)
        df_saida['Ag Dep'] = df_saida['Ag Dep'].astype(float)
        df_saida.insert(len(df_saida.columns), 'Tratativa', 'Conta-Corrente - InterCredi Enviar')
        return df_saida.sort_values(by=['Ag Dest','Conta'], ascending=True)

    def tratativa_cp_pa_proprio(self, df):
        df_saida = pd.DataFrame(df.loc[
            (df['Ag Dep'].eq(self.cooperativa) | self.busca_geral()) &
            (df['Ag Dest'].eq(self.cooperativa) | self.busca_geral()) &
            (df['PA Dep'].eq(self.pa)) &
            (df['PAC Cliente'].eq(self.pac_cliente) | self.busca_geral())])
        df_saida.insert(len(df_saida.columns), 'Tratativa', 'Conta-Poupança - Meu PA')
        return df_saida.sort_values(by=['Ag Dest','Conta'], ascending=True)

    def tratativa_cp_pa_receber(self, df):
        df_saida = pd.DataFrame(df.loc[
            (df['Ag Dep'].eq(self.cooperativa) | self.busca_geral()) &
            (df['PA Dep'].ne(self.pa) & ((not self.busca_geral()) | df['PA Dep'].eq(self.pa))) &
            (df['PAC Cliente'].eq(self.pac_cliente) | self.busca_geral())])
        df_saida.insert(len(df_saida.columns), 'Tratativa', 'Conta-Poupança - InterPA Receber')
        return df_saida.sort_values(by=['Ag Dest','Conta'], ascending=True)

    def tratativa_cp_pa_enviar(self, df):        
        df_saida = pd.DataFrame(df.loc[
            (df['Ag Dep'].eq(self.cooperativa) | self.busca_geral()) &
            (df['PA Dep'].eq(self.pa)) &
            (df['PAC Cliente'].ne(self.pac_cliente) & (not self.busca_geral()))])
        df_saida.insert(len(df_saida.columns), 'Tratativa', 'Conta-Poupança - InterPA Enviar')
        return df_saida.sort_values(by=['Ag Dest','Conta'], ascending=True)

    def tratativa_cp_ic_receber(self, df):        
        df_saida = pd.DataFrame(df.loc[
            (df['Ag Dep'].ne(self.cooperativa) | self.busca_geral()) &
            (df['Info'].eq('RECEBEDORA'))])
        df_saida.insert(len(df_saida.columns), 'Tratativa', 'Conta-Poupança - InterCredi Receber')
        return df_saida.sort_values(by=['Ag Dest','Conta'], ascending=True)

    def tratativa_cp_ic_enviar(self, df):
        df_saida = pd.DataFrame(df.loc[
            (df['Ag Dep'].eq(self.cooperativa) | self.busca_geral()) &
            (df['PA Dep'].eq(self.pa) | self.busca_geral()) &
            (df['Info'].eq('DESTINATARIA'))])
        df_saida.insert(len(df_saida.columns), 'Tratativa', 'Conta-Poupança - InterCredi Enviar')
        return df_saida.sort_values(by=['Ag Dest','Conta'], ascending=True)

    def busca_geral(self):
        return self.geral