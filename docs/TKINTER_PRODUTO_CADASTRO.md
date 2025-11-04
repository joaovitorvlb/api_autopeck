# 🖥️ Cadastramento de Produto com Foto - Python Tkinter

Este guia mostra como criar uma aplicação desktop em Python Tkinter para cadastrar produtos com upload de fotos, consumindo a API Flask com JWT.

## 🏗️ Estrutura do Projeto

```
tkinter_app/
├── main.py
├── api/
│   └── api_client.py
├── models/
│   └── produto.py
├── views/
│   ├── login_window.py
│   ├── main_window.py
│   └── cadastro_produto_window.py
├── utils/
│   └── image_utils.py
└── requirements.txt
```

## 📦 1. Dependências (requirements.txt)

```txt
requests==2.31.0
Pillow==10.0.0
```

## 🔐 2. Cliente da API

### api/api_client.py
```python
import requests
import json
from typing import Optional, Dict, Any

class ApiClient:
    def __init__(self, base_url: str = "http://localhost:5001"):
        self.base_url = base_url.rstrip('/')
        self.token: Optional[str] = None
        self.session = requests.Session()
    
    def set_token(self, token: str):
        """Define o token JWT para autenticação"""
        self.token = token
        self.session.headers.update({
            'Authorization': f'Bearer {token}'
        })
    
    def clear_token(self):
        """Remove o token de autenticação"""
        self.token = None
        if 'Authorization' in self.session.headers:
            del self.session.headers['Authorization']
    
    def login(self, usuario: str, senha: str) -> Dict[str, Any]:
        """Faz login e retorna a resposta"""
        url = f"{self.base_url}/login"
        data = {
            "usuario": usuario,
            "senha": senha
        }
        
        try:
            response = self.session.post(url, json=data)
            result = response.json()
            
            if response.status_code == 200 and 'token' in result:
                self.set_token(result['token'])
                return {"success": True, "data": result}
            else:
                return {"success": False, "error": result.get('erro', 'Erro desconhecido')}
                
        except requests.exceptions.RequestException as e:
            return {"success": False, "error": f"Erro de conexão: {str(e)}"}
        except json.JSONDecodeError:
            return {"success": False, "error": "Resposta inválida do servidor"}
    
    def listar_produtos(self) -> Dict[str, Any]:
        """Lista todos os produtos"""
        url = f"{self.base_url}/produtos"
        
        try:
            # Timeout maior para evitar problemas de conexão
            response = self.session.get(url, timeout=60)
            
            if response.status_code == 200:
                return {"success": True, "data": response.json()}
            else:
                return {"success": False, "error": f"Erro {response.status_code}"}
                
        except requests.exceptions.Timeout:
            return {"success": False, "error": "Timeout na conexão - servidor demorou para responder"}
        except requests.exceptions.RequestException as e:
            return {"success": False, "error": f"Erro de conexão: {str(e)}"}
    
    def criar_produto(self, produto_data: Dict[str, Any]) -> Dict[str, Any]:
        """Cria um novo produto"""
        url = f"{self.base_url}/produtos"
        
        try:
            # Timeout maior para operações de criação
            response = self.session.post(url, json=produto_data, timeout=60)
            
            if response.status_code == 201:
                return {"success": True, "data": response.json()}
            else:
                result = response.json() if response.headers.get('content-type', '').startswith('application/json') else {}
                return {"success": False, "error": result.get('erro', f'Erro {response.status_code}')}
                
        except requests.exceptions.Timeout:
            return {"success": False, "error": "Timeout na criação - servidor demorou para responder"}
        except requests.exceptions.RequestException as e:
            return {"success": False, "error": f"Erro de conexão: {str(e)}"}
        except json.JSONDecodeError:
            return {"success": False, "error": "Resposta inválida do servidor"}
    
    def upload_imagem(self, produto_id: int, image_path: str) -> Dict[str, Any]:
        """Faz upload de imagem para um produto"""
        url = f"{self.base_url}/produtos/{produto_id}/upload-image"
        
        try:
            with open(image_path, 'rb') as image_file:
                files = {'image': image_file}
                
                # Para upload, não usar JSON headers
                headers = {}
                if self.token:
                    headers['Authorization'] = f'Bearer {self.token}'
                
                response = requests.post(url, files=files, headers=headers)
            
            if response.status_code == 200:
                return {"success": True, "data": response.json()}
            else:
                result = response.json() if response.headers.get('content-type', '').startswith('application/json') else {}
                return {"success": False, "error": result.get('erro', f'Erro {response.status_code}')}
                
        except FileNotFoundError:
            return {"success": False, "error": "Arquivo de imagem não encontrado"}
        except requests.exceptions.RequestException as e:
            return {"success": False, "error": f"Erro de conexão: {str(e)}"}
        except Exception as e:
            return {"success": False, "error": f"Erro no upload: {str(e)}"}
    
    def deletar_imagem(self, produto_id: int) -> Dict[str, Any]:
        """Deleta a imagem de um produto"""
        url = f"{self.base_url}/produtos/{produto_id}/delete-image"
        
        try:
            response = self.session.delete(url)
            
            if response.status_code == 200:
                return {"success": True, "data": response.json()}
            else:
                result = response.json() if response.headers.get('content-type', '').startswith('application/json') else {}
                return {"success": False, "error": result.get('erro', f'Erro {response.status_code}')}
                
        except requests.exceptions.RequestException as e:
            return {"success": False, "error": f"Erro de conexão: {str(e)}"}
```

## 📦 3. Modelo de Dados

### models/produto.py
```python
from dataclasses import dataclass
from typing import Optional, Dict

@dataclass
class Produto:
    nome: str
    preco: float
    estoque: int
    descricao: str = ""
    id_produto: Optional[int] = None
    url: Optional[str] = None
    urls_imagem: Optional[Dict[str, str]] = None
    
    def to_dict(self) -> Dict:
        """Converte o produto para dicionário para envio à API"""
        return {
            "nome": self.nome,
            "preco": self.preco,
            "estoque": self.estoque,
            "descricao": self.descricao
        }
    
    @classmethod
    def from_dict(cls, data: Dict):
        """Cria produto a partir de dicionário da API"""
        return cls(
            id_produto=data.get('id_produto'),
            nome=data.get('nome', ''),
            preco=data.get('preco', 0.0),
            estoque=data.get('estoque', 0),
            descricao=data.get('descricao', ''),
            url=data.get('url'),
            urls_imagem=data.get('urls_imagem')
        )
    
    def get_thumbnail_url(self) -> Optional[str]:
        """Retorna URL da thumbnail"""
        if self.urls_imagem:
            return self.urls_imagem.get('thumbnail')
        return self.url
    
    def get_medium_url(self) -> Optional[str]:
        """Retorna URL da imagem média"""
        if self.urls_imagem:
            return self.urls_imagem.get('medium')
        return self.url
    
    def get_large_url(self) -> Optional[str]:
        """Retorna URL da imagem grande"""
        if self.urls_imagem:
            return self.urls_imagem.get('large')
        return self.url
```

## 🔐 4. Janela de Login

### views/login_window.py
```python
import tkinter as tk
from tkinter import ttk, messagebox
from api.api_client import ApiClient

class LoginWindow:
    def __init__(self, on_login_success=None):
        self.api_client = ApiClient()
        self.on_login_success = on_login_success
        
        self.root = tk.Tk()
        self.root.title("Login - Sistema de Produtos")
        self.root.geometry("400x300")
        self.root.resizable(False, False)
        
        # Centralizar janela
        self.center_window()
        
        self.setup_ui()
    
    def center_window(self):
        """Centraliza a janela na tela"""
        self.root.update_idletasks()
        x = (self.root.winfo_screenwidth() // 2) - (400 // 2)
        y = (self.root.winfo_screenheight() // 2) - (300 // 2)
        self.root.geometry(f"400x300+{x}+{y}")
    
    def setup_ui(self):
        """Configura a interface do usuário"""
        # Frame principal
        main_frame = ttk.Frame(self.root, padding="40")
        main_frame.pack(fill=tk.BOTH, expand=True)
        
        # Título
        title_label = ttk.Label(main_frame, text="Sistema de Produtos", 
                               font=("Arial", 18, "bold"))
        title_label.pack(pady=(0, 30))
        
        # Campo usuário
        ttk.Label(main_frame, text="Usuário:").pack(anchor=tk.W, pady=(0, 5))
        self.usuario_entry = ttk.Entry(main_frame, width=30, font=("Arial", 12))
        self.usuario_entry.pack(pady=(0, 15))
        self.usuario_entry.insert(0, "admin")  # Valor padrão
        
        # Campo senha
        ttk.Label(main_frame, text="Senha:").pack(anchor=tk.W, pady=(0, 5))
        self.senha_entry = ttk.Entry(main_frame, width=30, font=("Arial", 12), show="*")
        self.senha_entry.pack(pady=(0, 20))
        self.senha_entry.insert(0, "admin")  # Valor padrão
        
        # Botão login
        self.login_button = ttk.Button(main_frame, text="Entrar", 
                                      command=self.fazer_login)
        self.login_button.pack(pady=(0, 10))
        
        # Status
        self.status_label = ttk.Label(main_frame, text="", foreground="red")
        self.status_label.pack()
        
        # Bind Enter key
        self.root.bind('<Return>', lambda e: self.fazer_login())
        
        # Focar no campo usuário
        self.usuario_entry.focus()
    
    def fazer_login(self):
        """Realiza o login"""
        usuario = self.usuario_entry.get().strip()
        senha = self.senha_entry.get().strip()
        
        if not usuario or not senha:
            self.status_label.config(text="Preencha todos os campos")
            return
        
        # Desabilitar botão
        self.login_button.config(state="disabled")
        self.status_label.config(text="Fazendo login...", foreground="blue")
        
        # Atualizar interface
        self.root.update()
        
        # Fazer login
        resultado = self.api_client.login(usuario, senha)
        
        if resultado["success"]:
            self.status_label.config(text="Login realizado com sucesso!", 
                                   foreground="green")
            
            # Chamar callback se fornecido
            if self.on_login_success:
                self.on_login_success(self.api_client)
            
            # Fechar janela após delay
            self.root.after(1000, self.root.destroy)
        else:
            self.status_label.config(text=f"Erro: {resultado['error']}", 
                                   foreground="red")
            self.login_button.config(state="normal")
    
    def show(self):
        """Mostra a janela"""
        self.root.mainloop()
        return self.api_client if self.api_client.token else None
```

## 🖼️ 5. Utilitários de Imagem

### utils/image_utils.py
```python
import os
import tempfile
from PIL import Image
import tkinter as tk
from tkinter import filedialog

class ImageUtils:
    
    @staticmethod
    def selecionar_imagem(parent=None):
        """Abre diálogo para seleção de imagem"""
        filetypes = [
            ("Imagens", "*.jpg *.jpeg *.png *.gif *.bmp"),
            ("JPEG", "*.jpg *.jpeg"),
            ("PNG", "*.png"),
            ("Todos os arquivos", "*.*")
        ]
        
        return filedialog.askopenfilename(
            parent=parent,
            title="Selecionar Imagem",
            filetypes=filetypes
        )
    
    @staticmethod
    def redimensionar_imagem(image_path: str, max_size: tuple = (800, 800)) -> str:
        """Redimensiona imagem mantendo proporção"""
        try:
            with Image.open(image_path) as img:
                # Converter para RGB se necessário
                if img.mode in ('RGBA', 'LA', 'P'):
                    img = img.convert('RGB')
                
                # Redimensionar mantendo proporção
                img.thumbnail(max_size, Image.Resampling.LANCZOS)
                
                # Salvar em arquivo temporário
                temp_file = tempfile.NamedTemporaryFile(
                    delete=False, 
                    suffix='.jpg'
                )
                img.save(temp_file.name, 'JPEG', quality=85)
                
                return temp_file.name
                
        except Exception as e:
            raise Exception(f"Erro ao processar imagem: {str(e)}")
    
    @staticmethod
    def criar_thumbnail(image_path: str, size: tuple = (150, 150)) -> str:
        """Cria thumbnail da imagem"""
        try:
            with Image.open(image_path) as img:
                # Converter para RGB se necessário
                if img.mode in ('RGBA', 'LA', 'P'):
                    img = img.convert('RGB')
                
                # Criar thumbnail
                img.thumbnail(size, Image.Resampling.LANCZOS)
                
                # Salvar em arquivo temporário
                temp_file = tempfile.NamedTemporaryFile(
                    delete=False, 
                    suffix='_thumb.jpg'
                )
                img.save(temp_file.name, 'JPEG', quality=80)
                
                return temp_file.name
                
        except Exception as e:
            raise Exception(f"Erro ao criar thumbnail: {str(e)}")
    
    @staticmethod
    def validar_imagem(image_path: str) -> bool:
        """Valida se o arquivo é uma imagem válida"""
        try:
            with Image.open(image_path) as img:
                img.verify()
            return True
        except:
            return False
    
    @staticmethod
    def obter_info_imagem(image_path: str) -> dict:
        """Obtém informações da imagem"""
        try:
            with Image.open(image_path) as img:
                return {
                    "formato": img.format,
                    "modo": img.mode,
                    "tamanho": img.size,
                    "tamanho_arquivo": os.path.getsize(image_path)
                }
        except Exception as e:
            return {"erro": str(e)}
```

## 📝 6. Janela de Cadastro de Produto

### views/cadastro_produto_window.py
```python
import tkinter as tk
from tkinter import ttk, messagebox, filedialog
import os
from PIL import Image, ImageTk
from models.produto import Produto
from utils.image_utils import ImageUtils

class CadastroProdutoWindow:
    def __init__(self, api_client, parent=None, on_produto_criado=None):
        self.api_client = api_client
        self.on_produto_criado = on_produto_criado
        self.imagem_selecionada = None
        self.thumbnail_path = None
        
        # Criar janela
        if parent:
            self.root = tk.Toplevel(parent)
        else:
            self.root = tk.Tk()
        
        self.root.title("Cadastrar Produto")
        self.root.geometry("600x700")
        self.root.resizable(True, False)
        
        # Centralizar janela
        self.center_window()
        
        self.setup_ui()
    
    def center_window(self):
        """Centraliza a janela na tela"""
        self.root.update_idletasks()
        x = (self.root.winfo_screenwidth() // 2) - (600 // 2)
        y = (self.root.winfo_screenheight() // 2) - (700 // 2)
        self.root.geometry(f"600x700+{x}+{y}")
    
    def setup_ui(self):
        """Configura a interface do usuário"""
        # Frame principal com scroll
        canvas = tk.Canvas(self.root)
        scrollbar = ttk.Scrollbar(self.root, orient="vertical", command=canvas.yview)
        scrollable_frame = ttk.Frame(canvas)
        
        scrollable_frame.bind(
            "<Configure>",
            lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
        )
        
        canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
        canvas.configure(yscrollcommand=scrollbar.set)
        
        # Pack canvas e scrollbar
        canvas.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")
        
        # Frame de conteúdo
        main_frame = ttk.Frame(scrollable_frame, padding="20")
        main_frame.pack(fill=tk.BOTH, expand=True)
        
        # Título
        title_label = ttk.Label(main_frame, text="Cadastrar Produto", 
                               font=("Arial", 16, "bold"))
        title_label.pack(pady=(0, 20))
        
        # Frame para imagem
        image_frame = ttk.LabelFrame(main_frame, text="Imagem do Produto", padding="10")
        image_frame.pack(fill=tk.X, pady=(0, 20))
        
        # Canvas para imagem
        self.image_canvas = tk.Canvas(image_frame, width=200, height=200, 
                                     bg="lightgray", relief="sunken", bd=2)
        self.image_canvas.pack(pady=(0, 10))
        
        # Texto placeholder
        self.image_canvas.create_text(100, 100, text="Nenhuma imagem\nselecionada", 
                                     justify=tk.CENTER, fill="gray")
        
        # Botões de imagem
        image_buttons_frame = ttk.Frame(image_frame)
        image_buttons_frame.pack()
        
        self.btn_selecionar = ttk.Button(image_buttons_frame, text="Selecionar Imagem", 
                                        command=self.selecionar_imagem)
        self.btn_selecionar.pack(side=tk.LEFT, padx=(0, 10))
        
        self.btn_remover = ttk.Button(image_buttons_frame, text="Remover Imagem", 
                                     command=self.remover_imagem, state="disabled")
        self.btn_remover.pack(side=tk.LEFT)
        
        # Frame para dados do produto
        dados_frame = ttk.LabelFrame(main_frame, text="Dados do Produto", padding="10")
        dados_frame.pack(fill=tk.X, pady=(0, 20))
        
        # Campo Nome
        ttk.Label(dados_frame, text="Nome:*").pack(anchor=tk.W, pady=(0, 5))
        self.nome_entry = ttk.Entry(dados_frame, width=50, font=("Arial", 11))
        self.nome_entry.pack(fill=tk.X, pady=(0, 10))
        
        # Frame para preço e estoque
        preco_estoque_frame = ttk.Frame(dados_frame)
        preco_estoque_frame.pack(fill=tk.X, pady=(0, 10))
        
        # Campo Preço
        preco_frame = ttk.Frame(preco_estoque_frame)
        preco_frame.pack(side=tk.LEFT, fill=tk.X, expand=True, padx=(0, 10))
        ttk.Label(preco_frame, text="Preço (R$):*").pack(anchor=tk.W, pady=(0, 5))
        self.preco_entry = ttk.Entry(preco_frame, font=("Arial", 11))
        self.preco_entry.pack(fill=tk.X)
        
        # Campo Estoque
        estoque_frame = ttk.Frame(preco_estoque_frame)
        estoque_frame.pack(side=tk.LEFT, fill=tk.X, expand=True)
        ttk.Label(estoque_frame, text="Estoque:*").pack(anchor=tk.W, pady=(0, 5))
        self.estoque_entry = ttk.Entry(estoque_frame, font=("Arial", 11))
        self.estoque_entry.pack(fill=tk.X)
        
        # Campo Descrição
        ttk.Label(dados_frame, text="Descrição:").pack(anchor=tk.W, pady=(10, 5))
        self.descricao_text = tk.Text(dados_frame, height=4, font=("Arial", 11))
        self.descricao_text.pack(fill=tk.X)
        
        # Scrollbar para descrição
        desc_scrollbar = ttk.Scrollbar(dados_frame, command=self.descricao_text.yview)
        self.descricao_text.config(yscrollcommand=desc_scrollbar.set)
        
        # Frame para botões
        buttons_frame = ttk.Frame(main_frame)
        buttons_frame.pack(fill=tk.X, pady=(20, 0))
        
        # Botão Cancelar
        self.btn_cancelar = ttk.Button(buttons_frame, text="Cancelar", 
                                      command=self.cancelar)
        self.btn_cancelar.pack(side=tk.LEFT)
        
        # Botão Salvar
        self.btn_salvar = ttk.Button(buttons_frame, text="Cadastrar Produto", 
                                    command=self.salvar_produto)
        self.btn_salvar.pack(side=tk.RIGHT)
        
        # Barra de progresso
        self.progress_frame = ttk.Frame(main_frame)
        self.progress_frame.pack(fill=tk.X, pady=(10, 0))
        
        self.progress_label = ttk.Label(self.progress_frame, text="")
        self.progress_label.pack()
        
        self.progress_bar = ttk.Progressbar(self.progress_frame, mode='indeterminate')
        self.progress_bar.pack(fill=tk.X, pady=(5, 0))
        
        # Inicialmente ocultar progresso
        self.progress_frame.pack_forget()
        
        # Focar no campo nome
        self.nome_entry.focus()
    
    def selecionar_imagem(self):
        """Seleciona uma imagem"""
        file_path = ImageUtils.selecionar_imagem(self.root)
        
        if file_path:
            try:
                # Validar imagem
                if not ImageUtils.validar_imagem(file_path):
                    messagebox.showerror("Erro", "Arquivo selecionado não é uma imagem válida")
                    return
                
                # Obter informações da imagem
                info = ImageUtils.obter_info_imagem(file_path)
                
                # Verificar tamanho do arquivo (max 16MB)
                max_size = 16 * 1024 * 1024  # 16MB
                if info.get("tamanho_arquivo", 0) > max_size:
                    messagebox.showerror("Erro", "Imagem muito grande. Máximo 16MB.")
                    return
                
                self.imagem_selecionada = file_path
                
                # Criar thumbnail para preview
                self.thumbnail_path = ImageUtils.criar_thumbnail(file_path, (180, 180))
                
                # Mostrar preview
                self.mostrar_preview()
                
                # Habilitar botão remover
                self.btn_remover.config(state="normal")
                
            except Exception as e:
                messagebox.showerror("Erro", f"Erro ao processar imagem: {str(e)}")
    
    def mostrar_preview(self):
        """Mostra preview da imagem selecionada"""
        if self.thumbnail_path and os.path.exists(self.thumbnail_path):
            try:
                # Carregar e mostrar imagem
                pil_image = Image.open(self.thumbnail_path)
                photo = ImageTk.PhotoImage(pil_image)
                
                # Limpar canvas
                self.image_canvas.delete("all")
                
                # Mostrar imagem no centro
                self.image_canvas.create_image(100, 100, image=photo)
                
                # Manter referência da imagem
                self.image_canvas.image = photo
                
            except Exception as e:
                print(f"Erro ao mostrar preview: {e}")
    
    def remover_imagem(self):
        """Remove a imagem selecionada"""
        self.imagem_selecionada = None
        
        # Limpar thumbnail
        if self.thumbnail_path and os.path.exists(self.thumbnail_path):
            try:
                os.unlink(self.thumbnail_path)
            except:
                pass
        self.thumbnail_path = None
        
        # Limpar canvas
        self.image_canvas.delete("all")
        self.image_canvas.create_text(100, 100, text="Nenhuma imagem\nselecionada", 
                                     justify=tk.CENTER, fill="gray")
        
        # Desabilitar botão remover
        self.btn_remover.config(state="disabled")
    
    def validar_campos(self):
        """Valida os campos do formulário"""
        nome = self.nome_entry.get().strip()
        preco_str = self.preco_entry.get().strip()
        estoque_str = self.estoque_entry.get().strip()
        
        if not nome:
            messagebox.showerror("Erro", "Nome é obrigatório")
            self.nome_entry.focus()
            return False
        
        if not preco_str:
            messagebox.showerror("Erro", "Preço é obrigatório")
            self.preco_entry.focus()
            return False
        
        try:
            preco = float(preco_str.replace(',', '.'))
            if preco <= 0:
                raise ValueError()
        except ValueError:
            messagebox.showerror("Erro", "Preço deve ser um número válido maior que zero")
            self.preco_entry.focus()
            return False
        
        if not estoque_str:
            messagebox.showerror("Erro", "Estoque é obrigatório")
            self.estoque_entry.focus()
            return False
        
        try:
            estoque = int(estoque_str)
            if estoque < 0:
                raise ValueError()
        except ValueError:
            messagebox.showerror("Erro", "Estoque deve ser um número inteiro válido")
            self.estoque_entry.focus()
            return False
        
        return True
    
    def mostrar_progresso(self, texto="Processando..."):
        """Mostra barra de progresso"""
        self.progress_label.config(text=texto)
        self.progress_frame.pack(fill=tk.X, pady=(10, 0))
        self.progress_bar.start()
        
        # Desabilitar botões
        self.btn_salvar.config(state="disabled")
        self.btn_cancelar.config(state="disabled")
        self.btn_selecionar.config(state="disabled")
        self.btn_remover.config(state="disabled")
        
        self.root.update()
    
    def ocultar_progresso(self):
        """Oculta barra de progresso"""
        self.progress_bar.stop()
        self.progress_frame.pack_forget()
        
        # Reabilitar botões
        self.btn_salvar.config(state="normal")
        self.btn_cancelar.config(state="normal")
        self.btn_selecionar.config(state="normal")
        if self.imagem_selecionada:
            self.btn_remover.config(state="normal")
    
    def salvar_produto(self):
        """Salva o produto"""
        if not self.validar_campos():
            return
        
        # Mostrar progresso
        self.mostrar_progresso("Criando produto...")
        
        # Coletar dados
        nome = self.nome_entry.get().strip()
        preco = float(self.preco_entry.get().strip().replace(',', '.'))
        estoque = int(self.estoque_entry.get().strip())
        descricao = self.descricao_text.get("1.0", tk.END).strip()
        
        # Criar produto
        produto = Produto(nome=nome, preco=preco, estoque=estoque, descricao=descricao)
        
        # Enviar para API
        resultado = self.api_client.criar_produto(produto.to_dict())
        
        if resultado["success"]:
            produto_criado = Produto.from_dict(resultado["data"])
            
            # Se há imagem, fazer upload
            if self.imagem_selecionada:
                self.progress_label.config(text="Enviando imagem...")
                self.root.update()
                
                try:
                    # Redimensionar imagem antes do upload
                    imagem_otimizada = ImageUtils.redimensionar_imagem(
                        self.imagem_selecionada, 
                        (1200, 1200)
                    )
                    
                    resultado_upload = self.api_client.upload_imagem(
                        produto_criado.id_produto, 
                        imagem_otimizada
                    )
                    
                    # Limpar arquivo temporário
                    try:
                        os.unlink(imagem_otimizada)
                    except:
                        pass
                    
                    if not resultado_upload["success"]:
                        messagebox.showwarning(
                            "Aviso", 
                            f"Produto criado, mas erro no upload da imagem:\n{resultado_upload['error']}"
                        )
                
                except Exception as e:
                    messagebox.showwarning(
                        "Aviso", 
                        f"Produto criado, mas erro no upload da imagem:\n{str(e)}"
                    )
            
            self.ocultar_progresso()
            
            # Mostrar sucesso
            messagebox.showinfo("Sucesso", "Produto cadastrado com sucesso!")
            
            # Chamar callback se fornecido
            if self.on_produto_criado:
                self.on_produto_criado(produto_criado)
            
            # Fechar janela
            self.cancelar()
            
        else:
            self.ocultar_progresso()
            messagebox.showerror("Erro", f"Erro ao criar produto:\n{resultado['error']}")
    
    def cancelar(self):
        """Cancela o cadastro"""
        # Limpar arquivos temporários
        if self.thumbnail_path and os.path.exists(self.thumbnail_path):
            try:
                os.unlink(self.thumbnail_path)
            except:
                pass
        
        self.root.destroy()
    
    def show(self):
        """Mostra a janela"""
        self.root.mainloop()
```

## 🏠 7. Janela Principal

### views/main_window.py
```python
import tkinter as tk
from tkinter import ttk, messagebox
from views.cadastro_produto_window import CadastroProdutoWindow
from models.produto import Produto

class MainWindow:
    def __init__(self, api_client):
        self.api_client = api_client
        self.produtos = []
        
        self.root = tk.Tk()
        self.root.title("Sistema de Produtos")
        self.root.geometry("800x600")
        
        self.setup_ui()
        self.carregar_produtos()
    
    def setup_ui(self):
        """Configura a interface do usuário"""
        # Menu
        menubar = tk.Menu(self.root)
        self.root.config(menu=menubar)
        
        # Menu Produto
        produto_menu = tk.Menu(menubar, tearoff=0)
        menubar.add_cascade(label="Produto", menu=produto_menu)
        produto_menu.add_command(label="Novo Produto", command=self.novo_produto)
        produto_menu.add_separator()
        produto_menu.add_command(label="Atualizar Lista", command=self.carregar_produtos)
        
        # Toolbar
        toolbar = ttk.Frame(self.root)
        toolbar.pack(fill=tk.X, padx=5, pady=5)
        
        ttk.Button(toolbar, text="Novo Produto", command=self.novo_produto).pack(side=tk.LEFT, padx=(0, 10))
        ttk.Button(toolbar, text="Atualizar", command=self.carregar_produtos).pack(side=tk.LEFT)
        
        # Frame principal
        main_frame = ttk.Frame(self.root)
        main_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=5)
        
        # Treeview para produtos
        columns = ("ID", "Nome", "Preço", "Estoque", "Imagem")
        self.tree = ttk.Treeview(main_frame, columns=columns, show="headings", height=15)
        
        # Configurar colunas
        self.tree.heading("ID", text="ID")
        self.tree.heading("Nome", text="Nome")
        self.tree.heading("Preço", text="Preço (R$)")
        self.tree.heading("Estoque", text="Estoque")
        self.tree.heading("Imagem", text="Tem Imagem")
        
        self.tree.column("ID", width=60, anchor=tk.CENTER)
        self.tree.column("Nome", width=250)
        self.tree.column("Preço", width=100, anchor=tk.E)
        self.tree.column("Estoque", width=80, anchor=tk.CENTER)
        self.tree.column("Imagem", width=100, anchor=tk.CENTER)
        
        # Scrollbar para treeview
        scrollbar = ttk.Scrollbar(main_frame, orient=tk.VERTICAL, command=self.tree.yview)
        self.tree.configure(yscrollcommand=scrollbar.set)
        
        # Pack treeview e scrollbar
        self.tree.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        
        # Status bar
        self.status_var = tk.StringVar()
        self.status_var.set("Pronto")
        status_bar = ttk.Label(self.root, textvariable=self.status_var, relief=tk.SUNKEN)
        status_bar.pack(fill=tk.X, side=tk.BOTTOM)
    
    def carregar_produtos(self):
        """Carrega lista de produtos da API"""
        self.status_var.set("Carregando produtos...")
        self.root.update()
        
        resultado = self.api_client.listar_produtos()
        
        if resultado["success"]:
            self.produtos = [Produto.from_dict(p) for p in resultado["data"]]
            self.atualizar_tree()
            self.status_var.set(f"Carregados {len(self.produtos)} produtos")
        else:
            messagebox.showerror("Erro", f"Erro ao carregar produtos:\n{resultado['error']}")
            self.status_var.set("Erro ao carregar produtos")
    
    def atualizar_tree(self):
        """Atualiza a TreeView com os produtos"""
        # Limpar tree
        for item in self.tree.get_children():
            self.tree.delete(item)
        
        # Adicionar produtos
        for produto in self.produtos:
            tem_imagem = "Sim" if produto.urls_imagem or produto.url else "Não"
            
            self.tree.insert("", tk.END, values=(
                produto.id_produto,
                produto.nome,
                f"R$ {produto.preco:.2f}",
                produto.estoque,
                tem_imagem
            ))
    
    def novo_produto(self):
        """Abre janela para cadastrar novo produto"""
        cadastro_window = CadastroProdutoWindow(
            api_client=self.api_client,
            parent=self.root,
            on_produto_criado=self.on_produto_criado
        )
        cadastro_window.show()
    
    def on_produto_criado(self, produto):
        """Callback chamado quando um produto é criado"""
        self.carregar_produtos()  # Recarregar lista
    
    def show(self):
        """Mostra a janela"""
        self.root.mainloop()
```

## 🚀 8. Arquivo Principal

### main.py
```python
#!/usr/bin/env python3
"""
Sistema de Produtos - Desktop (Tkinter)
Aplicação para cadastrar produtos com imagens via API Flask
"""

from views.login_window import LoginWindow
from views.main_window import MainWindow

def main():
    """Função principal"""
    print("🚀 Iniciando Sistema de Produtos...")
    
    # Janela de login
    login_window = LoginWindow()
    api_client = login_window.show()
    
    if api_client and api_client.token:
        print("✅ Login realizado com sucesso!")
        
        # Janela principal
        main_window = MainWindow(api_client)
        main_window.show()
    else:
        print("❌ Login cancelado ou falhou")

if __name__ == "__main__":
    main()
```

## 📋 9. Como Executar

### Instalação:
```bash
# Criar ambiente virtual
python -m venv venv

# Ativar ambiente (Linux/Mac)
source venv/bin/activate

# Ativar ambiente (Windows)
venv\Scripts\activate

# Instalar dependências
pip install -r requirements.txt
```

### Execução:
```bash
# Certificar que a API Flask está rodando
# Em outro terminal:
cd app_flask
source venv/bin/activate
python app.py

# Executar aplicação Tkinter
python main.py
```

## 🎯 10. Funcionalidades

- ✅ **Login com JWT** - Autenticação automática
- ✅ **Lista de produtos** - Visualização em tabela
- ✅ **Cadastro de produtos** - Formulário completo
- ✅ **Upload de imagens** - Com redimensionamento automático
- ✅ **Preview de imagem** - Visualização antes do envio
- ✅ **Validação de campos** - Verificação completa
- ✅ **Feedback visual** - Barra de progresso e status
- ✅ **Interface responsiva** - Redimensionável

## 🔧 11. Customizações

### Alterar servidor:
```python
# Em api/api_client.py
def __init__(self, base_url: str = "http://SEU_IP:5001"):
```

### Alterar credenciais:
```python
# Em views/login_window.py
self.usuario_entry.insert(0, "seu_usuario")
self.senha_entry.insert(0, "sua_senha")
```

### Personalizar interface:
- Modificar cores e fontes nos arquivos de view
- Adicionar novos campos no formulário
- Implementar funcionalidades extras

## 📚 Próximos Passos

- Implementar edição de produtos
- Adicionar cache de imagens
- Implementar busca e filtros
- Adicionar relatórios
- Melhorar tratamento de erros