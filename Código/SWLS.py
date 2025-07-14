import tkinter as tk
from tkinter import ttk, messagebox
from fpdf import FPDF
import os
import platform
import subprocess
import sys


def caminho_recurso(rel_path):
    if hasattr(sys, '_MEIPASS'):
        return os.path.join(sys._MEIPASS, rel_path)
    return os.path.join(os.path.abspath("."), rel_path)


def configurar_estilo():
    estilo = ttk.Style()
    estilo.theme_use('default')
    estilo.configure('.', font=('Helvetica', 11), background='#f9f9f9')
    estilo.configure('TButton', font=('Helvetica', 11), padding=6)
    estilo.configure('TLabel', background='#f9f9f9')
    estilo.configure('TRadiobutton', background='#f9f9f9', font=('Helvetica', 11))


PERGUNTAS = [
    "1. Em muitos aspetos, a minha vida aproxima-se dos meus ideais.",
    "2. As minhas condições de vida são excelentes.",
    "3. Estou satisfeito com a minha vida.",
    "4. Até agora, consegui obter aquilo que era importante na vida.",
    "5. Se pudesse viver a minha vida de novo, não alteraria praticamente nada."
]

OPCOES = [
    "1 - Totalmente em desacordo",
    "2 - Em desacordo",
    "3 - Mais ou menos em desacordo",
    "4 - Nem de acordo nem em desacordo",
    "5 - Mais ou menos de acordo",
    "6 - De acordo",
    "7 - Totalmente de acordo"
]


def interpretar_swls(score):
    if score >= 30:
        return "Muito satisfeito com a vida."
    elif score >= 25:
        return "Altamente satisfeito com a vida."
    elif score >= 20:
        return "Satisfação média com a vida."
    elif score >= 15:
        return "Satisfação ligeiramente abaixo da média."
    elif score >= 10:
        return "Insatisfação significativa com a vida."
    else:
        return "Extremamente insatisfeito com a vida."


class PDFSWLS(FPDF):
    def header(self):
        self.set_font("Helvetica", 'B', 12)
        self.cell(0, 10, "Escala de Satisfação com a Vida (SWLS) - Resultados", 0, 1, 'C')

    def add_dados(self, dados):
        self.set_font("Helvetica", '', 11)
        for k, v in dados.items():
            self.cell(0, 10, f"{k}: {v}", 0, 1)

    def add_respostas(self, respostas):
        self.set_font("Helvetica", '', 10)
        self.cell(0, 10, "Respostas ao Questionário:", 0, 1)
        for i, r in enumerate(respostas, 1):
            self.cell(0, 8, f"{i}. {r}", 0, 1)

    def add_score(self, score):
        self.ln(5)
        self.set_font("Helvetica", 'B', 11)
        self.cell(0, 10, "Resultado Total SWLS:", 0, 1)
        self.set_font("Helvetica", '', 11)
        self.cell(0, 8, f"Pontuação Total: {score}", 0, 1)

    def add_interpretacao(self, texto):
        self.ln(5)
        self.set_font("Helvetica", 'I', 10)
        self.multi_cell(0, 8, f"Interpretação: {texto}")
        self.ln(10)
        self.set_font("Helvetica", 'I', 9)
        self.multi_cell(0, 8, "Referência: Simões, A. (1992). Ulterior validação de uma escala de satisfação com a vida (SWLS). Revista Portuguesa de Pedagogia, 26(3), 503-515.")


class AplicacaoSWLS(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Escala de Satisfação com a Vida (SWLS)")
        self.geometry("820x600")
        self.configure(bg="#f9f9f9")
        self.iconbitmap(caminho_recurso("swls.ico"))  
        configurar_estilo()

        
        titulo = tk.Label(self, text="Escala de Satisfação com a Vida (SWLS)",
                          font=("Helvetica", 20, "bold"), bg="#f9f9f9", fg="#2c3e50")
        titulo.pack(pady=(20, 5))

        
        nota = tk.Label(self, text="Nota: Esta escala foi adaptada e validada para a população portuguesa.",
                        font=("Helvetica", 11, "italic"), bg="#f9f9f9", fg="#34495e")
        nota.pack(pady=(0, 15))

        
        desenvol_frame = tk.Frame(self, bg="#f9f9f9")
        desenvol_frame.pack(fill="x", padx=20, pady=(0, 30))

        lbl_desenvolvimento = tk.Label(desenvol_frame,
            text="Desenvolvimento de Software: Ruben Baptista (2025)",
            font=("Helvetica", 11),  
            bg="#f9f9f9",
            fg="#2c3e50",
            justify="center")
        lbl_desenvolvimento.pack(fill="x")

        lbl_referencia = tk.Label(desenvol_frame,
            text="Referência: Simões, A. (1992). Ulterior validação de uma escala de satisfação com a vida (SWLS). Revista Portuguesa de Pedagogia, 26(3), 503-515.",
            font=("Helvetica", 10, "italic"),
            bg="#f9f9f9",
            fg="#34495e",
            wraplength=780,
            justify="center")
        lbl_referencia.pack(fill="x", pady=(2, 0))

        
        ttk.Button(self, text="Iniciar", command=self.abrir_dados).pack(pady=(0, 30))

    def abrir_dados(self):
        self.withdraw()
        JanelaDados(self)


class JanelaDados(tk.Toplevel):
    def __init__(self, master):
        super().__init__(master)
        self.title("Dados do/a Participante")
        self.geometry("400x400")
        self.iconbitmap(caminho_recurso("swls.ico"))  
        self.master = master
        self.campos = {}

        for campo in ["Nome", "Idade", "Sexo", "Aplicado por", "Cédula profissional (OPP)", "Data de Aplicação"]:
            tk.Label(self, text=campo).pack(pady=(10, 0))
            entry = tk.Entry(self)
            entry.pack()
            self.campos[campo] = entry

        ttk.Button(self, text="Iniciar Questionário", command=self.iniciar_questionario).pack(pady=20)

    def iniciar_questionario(self):
        dados = {k: v.get().strip() for k, v in self.campos.items()}
        if not all(dados.values()):
            messagebox.showwarning("Campos obrigatórios", "Por favor, preencha todos os campos.")
            return
        self.withdraw()
        JanelaQuestionario(self.master, dados)


class JanelaQuestionario(tk.Toplevel):
    def __init__(self, master, dados):
        super().__init__(master)
        self.title("Questionário SWLS")
        self.geometry("820x720")
        self.iconbitmap(caminho_recurso("swls.ico"))  
        self.dados = dados
        self.respostas = []

        container = ttk.Frame(self)
        container.pack(fill="both", expand=True)

        self.canvas = tk.Canvas(container, bg="white", highlightthickness=0)
        self.canvas.pack(side="left", fill="both", expand=True)

        scrollbar = ttk.Scrollbar(container, orient="vertical", command=self.canvas.yview)
        scrollbar.pack(side="right", fill="y")

        self.canvas.configure(yscrollcommand=scrollbar.set)

        self.scrollable_frame = ttk.Frame(self.canvas)
        self.canvas_frame = self.canvas.create_window((0, 0), window=self.scrollable_frame, anchor="nw")

        self.scrollable_frame.bind("<Configure>", self._on_frame_configure)
        self.canvas.bind("<Configure>", self._on_canvas_configure)

        
        self.canvas.bind_all("<MouseWheel>", self._on_mousewheel)  
        self.canvas.bind_all("<Button-4>", self._on_mousewheel)    
        self.canvas.bind_all("<Button-5>", self._on_mousewheel)    

        self._preencher_questionario()

    def _preencher_questionario(self):
        for idx, pergunta in enumerate(PERGUNTAS):
            ttk.Label(self.scrollable_frame, text=pergunta, wraplength=760, anchor="w",
                      font=("Helvetica", 13, "bold")).pack(anchor="w", pady=(20, 8), padx=10)

            var = tk.IntVar()
            self.respostas.append(var)

            radios_frame = ttk.Frame(self.scrollable_frame)
            radios_frame.pack(anchor="w", padx=20, pady=(0, 20))

            for val in range(1, 8):
                ttk.Radiobutton(radios_frame, text=OPCOES[val - 1], variable=var, value=val).pack(anchor="w", pady=2)

        btn_frame = ttk.Frame(self.scrollable_frame)
        btn_frame.pack(fill="x", pady=20)
        ttk.Button(btn_frame, text="Submeter", command=self.submeter).pack(ipadx=15, ipady=6)

    def _on_frame_configure(self, event):
        self.canvas.configure(scrollregion=self.canvas.bbox("all"))

    def _on_canvas_configure(self, event):
        largura = event.width
        self.canvas.itemconfig(self.canvas_frame, width=largura)

    def _on_mousewheel(self, event):
        if event.num == 4:  
            self.canvas.yview_scroll(-1, "units")
        elif event.num == 5:  
            self.canvas.yview_scroll(1, "units")
        else:  
            self.canvas.yview_scroll(int(-1*(event.delta/120)), "units")

    def submeter(self):
        respostas = [v.get() for v in self.respostas]
        if not all(respostas):
            messagebox.showwarning("Incompleto", "Por favor, responda a todas as questões.")
            return

        score = sum(respostas)
        interpretacao = interpretar_swls(score)

        nome = self.dados.get("Nome", "participante").replace(" ", "_")
        nome_ficheiro = f"SWLS_{nome}.pdf"

        pdf = PDFSWLS()
        pdf.add_page()
        pdf.add_dados(self.dados)
        pdf.add_respostas(respostas)
        pdf.add_score(score)
        pdf.add_interpretacao(interpretacao)

        try:
            pdf.output(nome_ficheiro)
        except Exception as e:
            messagebox.showerror("Erro ao gerar PDF", str(e))
            return

        self.mostrar_resultado(nome_ficheiro, score, interpretacao)

    def mostrar_resultado(self, ficheiro, score, texto):
        janela = tk.Toplevel(self)
        janela.title("Resultados SWLS")
        janela.geometry("600x400")
        janela.configure(bg="white")
        janela.iconbitmap(caminho_recurso("swls.ico")) 

        tk.Label(janela, text="Resumo dos Resultados", font=("Helvetica", 14, "bold"), bg="white", fg="#2c3e50").pack(pady=10)

        texto_final = (f"Pontuação Total: {score}\n\n"
                       f"Interpretação: {texto}\n\n"
                       f"O PDF foi guardado como: {ficheiro}\n")

        caixa = tk.Text(janela, wrap="word", bg="white", font=("Helvetica", 11), height=10, borderwidth=0)
        caixa.insert("1.0", texto_final)
        caixa.configure(state="disabled")
        caixa.pack(padx=20, pady=10, fill="both", expand=True)

        def abrir_pdf():
            caminho = os.path.abspath(ficheiro)
            try:
                if platform.system() == "Windows":
                    os.startfile(caminho)
                elif platform.system() == "Darwin":
                    subprocess.run(["open", caminho])
                else:
                    subprocess.run(["xdg-open", caminho])
            except Exception as e:
                messagebox.showerror("Erro", f"Não foi possível abrir o PDF.\n{e}")

        ttk.Button(janela, text="Ver PDF", command=abrir_pdf).pack(pady=10)

        botoes_frame = ttk.Frame(janela)
        botoes_frame.pack(pady=10)

        ttk.Button(botoes_frame, text="Aplicar de novo", command=self.reiniciar).pack(side="left", padx=10)
        ttk.Button(botoes_frame, text="Sair", command=self.master.quit).pack(side="left", padx=10)

    def reiniciar(self):
        self.destroy()
        self.master.deiconify()


if __name__ == "__main__":
    app = AplicacaoSWLS()
    app.mainloop()