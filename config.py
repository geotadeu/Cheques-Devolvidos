import locale

class Config:
    CoopAtual = -1
    DirRelatorios = None
    ListaCoop = []
    ListaPA = []

    def __init__(self):
        locale.setlocale(locale.LC_ALL, 'pt_BR.utf8')
        Config.load('.\\Config')

    @classmethod
    def load(cls, directory):
        configs = open(directory + '\\configs.txt').readlines()
        cls.CoopAtual = int(configs[0].replace('\n', ''))
        cls.DirRelatorios = configs[1].replace('\n', '')
        cls.ListaCoop = open(directory + '\\lista_coop.txt').readlines()
        cls.ListaPA = open(directory + '\\lista_pa.txt').readlines()
        cls.ListaPA = [w.replace('\n', '') for w in cls.ListaPA]