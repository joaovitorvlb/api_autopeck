import os
import uuid
import json
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import secrets
from datetime import datetime, timedelta
import re
from werkzeug.utils import secure_filename
from PIL import Image

# Compatibilidade com versões antigas e novas do Pillow
try:
    # Pillow >= 9.1.0
    RESAMPLE_FILTER = Image.Resampling.LANCZOS
except AttributeError:
    # Pillow < 9.1.0
    RESAMPLE_FILTER = Image.LANCZOS

from flask import Flask, request, jsonify, g, send_from_directory, render_template, render_template_string
from flask_jwt_extended import (
    JWTManager, jwt_required, create_access_token,
    get_jwt_identity
)
from flasgger import Swagger, swag_from
from dao_mysql.funcionario_dao import FuncionarioDAO
from dao_mysql.produto_dao import ProdutoDAO
from dao_mysql.db import init_db
from dao_mysql.venda_dao import VendaDAO
from dao_mysql.item_venda_dao import ItemVendaDAO
from dao_mysql.cliente_dao import ClienteDAO
from dao_mysql.usuario_dao import UsuarioDAO
from dao_mysql.nivel_acesso_dao import NivelAcessoDAO



from datetime import date

# Inicializa o pool de conexões ao importar o app (se as variáveis de ambiente estiverem configuradas)
try:
    init_db()
except Exception:
    # Se não for possível inicializar agora (ex.: envs não configuradas), deixamos para inicializar
    # no primeiro request ou via scripts de teste que chamam init_db() explicitamente.
    pass

app = Flask(__name__)
app.config["JWT_ISSUER"] = "Flask_PyJWT" # Issuer of tokens
app.config["JWT_AUTHTYPE"] = "HS256" # HS256, HS512, RS256, or RS512
app.config["JWT_SECRET"] = "SECRETKEY" # string for HS256/HS512, bytes (RSA Private Key) for RS256/RS512
app.config["JWT_AUTHMAXAGE"] = 3600
app.config["JWT_REFRESHMAXAGE"] = 604800

# Configuração para upload de arquivos
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024  # 16MB máximo

# Usar caminho absoluto para funcionar em produção (PythonAnywhere)
BASE_DIR = os.path.abspath(os.path.dirname(__file__))
app.config['UPLOAD_FOLDER'] = os.path.join(BASE_DIR, 'static', 'images', 'produtos')

# Criar diretório de upload se não existir
os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)

ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif', 'webp'}

# Configuração das resoluções de imagem
IMAGE_RESOLUTIONS = {
    'thumbnail': (150, 150),   # Para listas/miniaturas
    'medium': (400, 400),      # Para detalhes/cards
    'large': (800, 800)        # Para visualização ampliada
}

# Setup the Flask-JWT-Extended extension
app.config['JWT_SECRET_KEY'] = 'super-secret'  # Change this!
jwt = JWTManager(app)

swagger = Swagger(app)

# Instancia o DAO
dao_funcionario = FuncionarioDAO()

# ---------------------------
# 🧍‍♂️ CLIENTE
# ---------------------------
@app.route("/clientes", methods=["POST"])
@swag_from("swagger_docs/clientes.yml")
def criar_cliente():
    # TODO: Adicionar lógica para cadastrar cliente
    try:
        dados = request.get_json()
        dao_cliente = ClienteDAO()
        cliente = dao_cliente.criar_cliente(dados)
        return jsonify(cliente), 201
    except Exception as erro:
        return jsonify({
            "erro": "Erro ao cadastrar cliente",
            "mensagem": str(erro)
        }), 500

@app.route("/clientes", methods=["GET"])
def listar_clientes():
    # TODO: Lógica para listar clientes
    try:
        dao_cliente = ClienteDAO()
        clientes = dao_cliente.listar_clientes()
        return jsonify(clientes), 200
    except Exception as erro:
        return jsonify({
            "erro": "Erro ao listar clientes",
            "mensagem": str(erro)
        }), 500

@app.route("/clientes/<int:id>", methods=["GET"])
def obter_cliente(id):
    # TODO: Buscar cliente por ID
    try:
        dao_cliente = ClienteDAO()
        cliente = dao_cliente.buscar_cliente(id)
        if not cliente:
            return jsonify({"erro": f"Cliente com ID {id} não encontrado"}), 404
        return jsonify(cliente), 200
    except Exception as erro:
        return jsonify({
            "erro": "Erro ao buscar cliente",
            "mensagem": str(erro)
        }), 500

@app.route("/clientes/<int:id>", methods=["PUT"])
def atualizar_cliente(id):
    # TODO: Atualizar cliente existente
    try:
        dados = request.get_json()
        dao_cliente = ClienteDAO()
        cliente = dao_cliente.atualizar_cliente(id, dados)
        if not cliente:
            return jsonify({"erro": f"Cliente com ID {id} não encontrado"}), 404
        return jsonify({"mensagem": f"Cliente com ID {id} atualizado com sucesso", "cliente": cliente}), 200
    except Exception as erro:
        return jsonify({
            "erro": "Erro ao atualizar cliente",
            "mensagem": str(erro)
        }), 500

@app.route("/clientes/<int:id>", methods=["DELETE"])
def excluir_cliente(id):
    # TODO: Excluir cliente
    try:
        dao_cliente = ClienteDAO()
        resultado = dao_cliente.excluir_cliente(id)
        if not resultado:
            return jsonify({"erro": f"Cliente com ID {id} não encontrado"}), 404
        return jsonify({"mensagem": f"Cliente com ID {id} excluído com sucesso"}), 200
    except Exception as erro:
        return jsonify({
            "erro": "Erro ao excluir cliente",
            "mensagem": str(erro)
        }), 500


# ---------------------------
# 🧑‍💼 FUNCIONARIO
# ---------------------------
@app.route("/funcionarios", methods=["POST"])
def criar_funcionario():
    try:
        dados = request.get_json()
        
        # Validar dados obrigatórios
        campos_obrigatorios = ['id_funcionario', 'nome']
        for campo in campos_obrigatorios:
            if campo not in dados:
                return jsonify({
                    "erro": f"O campo '{campo}' é obrigatório"
                }), 400
        
        # Criar objeto funcionário com os dados recebidos
        funcionario = {
            'id_funcionario': dados['id_funcionario'],
            'nome': dados['nome'],
            'cargo': dados.get('cargo'),  # campos opcionais usam .get()
            'salario': dados.get('salario'),
            'data_contratacao': dados.get('data_contratacao')
        }
        
        # Chamar o DAO para salvar
        novo_funcionario = dao_funcionario.criar(funcionario)
        
        return jsonify({
            "mensagem": "Funcionário cadastrado com sucesso",
            "funcionario": novo_funcionario
        }), 201
        
    except Exception as erro:
        return jsonify({
            "erro": "Erro ao cadastrar funcionário",
            "mensagem": str(erro)
        }), 500

@app.route("/funcionarios", methods=["GET"])
def listar_funcionarios():
    try:
        dao_funcionario = FuncionarioDAO()
        funcionarios = dao_funcionario.listar_funcionarios()
        return jsonify(funcionarios), 200
    except Exception as erro:
        return jsonify({
            "erro": "Erro ao listar funcionários",
            "mensagem": str(erro)
        }), 500

@app.route("/funcionarios/<int:id>", methods=["GET"])
def obter_funcionario(id):
    # TODO: Buscar funcionário por ID
    try:
        dao_funcionario = FuncionarioDAO()
        funcionario = dao_funcionario.buscar_funcionario(id)
        if not funcionario:
            return jsonify({"erro": f"Funcionário com ID {id} não encontrado"}), 404
        return jsonify(funcionario), 200
    except Exception as erro:
        return jsonify({
            "erro": "Erro ao buscar funcionário",
            "mensagem": str(erro)
        }), 500

@app.route("/funcionarios/<int:id>", methods=["PUT"])
def atualizar_funcionario(id):
    # TODO: Atualizar funcionário
    try:
        dados = request.get_json()
        dao_funcionario = FuncionarioDAO()
        funcionario = dao_funcionario.atualizar_funcionario(id, dados)
        if not funcionario:
            return jsonify({"erro": f"Funcionário com ID {id} não encontrado"}), 404
        return jsonify({"mensagem": f"Funcionário com ID {id} atualizado com sucesso", "funcionario": funcionario}), 200
    except Exception as erro:
        return jsonify({
            "erro": "Erro ao atualizar funcionário",
            "mensagem": str(erro)
        }), 500

@app.route("/funcionarios/<int:id>", methods=["DELETE"])
def excluir_funcionario(id):
    # TODO: Excluir funcionário
    try:
        dao_funcionario = FuncionarioDAO()
        resultado = dao_funcionario.excluir_funcionario(id)
        if not resultado:
            return jsonify({"erro": f"Funcionário com ID {id} não encontrado"}), 404
        return jsonify({"mensagem": f"Funcionário com ID {id} excluído com sucesso"}), 200
    except Exception as erro:
        return jsonify({
            "erro": "Erro ao excluir funcionário",
            "mensagem": str(erro)
        }), 500


# ---------------------------
# 📦 PRODUTO - Inserir novo produto
# ---------------------------
@app.route("/produtos", methods=["POST"])
def criar_produto():
    print("🚀 [DEBUG] Rota POST /produtos iniciada")
    
    try:
        print("📥 [DEBUG] Verificando dados recebidos...")
        dados = request.get_json()
        print(f"📦 [DEBUG] Dados JSON recebidos: {dados}")
        print(f"📦 [DEBUG] Tipo dos dados: {type(dados)}")
        
        if not dados:
            print("❌ [DEBUG] Nenhum JSON recebido")
            return jsonify({"erro": "JSON do corpo da requisição é obrigatório"}), 400

        print("✅ [DEBUG] JSON válido recebido")
        
        campos_obrigatorios = ["nome", "preco", "estoque"]
        print(f"🔍 [DEBUG] Verificando campos obrigatórios: {campos_obrigatorios}")
        
        for campo in campos_obrigatorios:
            if campo not in dados:
                print(f"❌ [DEBUG] Campo obrigatório ausente: {campo}")
                print(f"📋 [DEBUG] Campos presentes: {list(dados.keys())}")
                return jsonify({"erro": f"O campo '{campo}' é obrigatório"}), 400
            else:
                print(f"✅ [DEBUG] Campo '{campo}' presente: {dados[campo]}")

        print("🔢 [DEBUG] Validando e convertendo tipos...")
        
        # Conversões e validações básicas
        try:
            preco = float(dados["preco"])
            print(f"✅ [DEBUG] Preço convertido: {preco}")
        except Exception as e:
            print(f"❌ [DEBUG] Erro ao converter preço: {e}")
            print(f"📦 [DEBUG] Valor do preço recebido: {dados['preco']} (tipo: {type(dados['preco'])})")
            return jsonify({"erro": "Campo 'preco' deve ser numérico"}), 400

        try:
            estoque = int(dados["estoque"])
            print(f"✅ [DEBUG] Estoque convertido: {estoque}")
        except Exception as e:
            print(f"❌ [DEBUG] Erro ao converter estoque: {e}")
            print(f"📦 [DEBUG] Valor do estoque recebido: {dados['estoque']} (tipo: {type(dados['estoque'])})")
            return jsonify({"erro": "Campo 'estoque' deve ser inteiro"}), 400

        nome = dados["nome"]
        descricao = dados.get("descricao", "")
        
        print(f"📝 [DEBUG] Dados processados:")
        print(f"   - Nome: {nome}")
        print(f"   - Descrição: {descricao}")
        print(f"   - Preço: {preco}")
        print(f"   - Estoque: {estoque}")

        print("🗄️ [DEBUG] Criando DAO de produto...")
        dao_produto = ProdutoDAO()

        print("💾 [DEBUG] Chamando criar_produto no DAO...")
        produto_data = {
            'nome': nome,
            'descricao': descricao,
            'preco': preco,
            'estoque': estoque
        }
        print(f"📦 [DEBUG] Dados para o DAO: {produto_data}")
        
        produto_criado = dao_produto.criar_produto(produto_data)
        print(f"✅ [DEBUG] Produto criado pelo DAO: {produto_criado}")

        if produto_criado:
            # Aplicar processamento dinâmico de imagens
            produto_processado = process_product_images(produto_criado)
            
            # Adicionar apenas a mensagem de sucesso ao produto processado
            produto_processado['mensagem'] = "Produto cadastrado com sucesso"
            
            print(f"📤 [DEBUG] Resposta de sucesso: {produto_processado}")
            return jsonify(produto_processado), 201
        else:
            print("❌ [DEBUG] DAO retornou None/False")
            return jsonify({"erro": "Erro ao criar produto"}), 500

    except Exception as erro:
        print(f"💥 [ERROR] Exceção na criação de produto: {erro}")
        import traceback
        print("📊 [ERROR] Stack trace completo:")
        traceback.print_exc()
        return jsonify({
            "erro": "Erro ao cadastrar produto",
            "mensagem": str(erro)
        }), 500


def generate_dynamic_image_urls(produto_id, base_url=None):
    """
    Gera URLs dinâmicas para as imagens de um produto baseado no padrão de nomenclatura
    Padrão: produto_{id}_{uuid}_{resolucao}.{extensao}
    
    Args:
        produto_id (int): ID do produto
        base_url (str): URL base da aplicação (opcional)
    
    Returns:
        dict: URLs para cada resolução se as imagens existirem, None caso contrário
    """
    if base_url is None:
        base_url = request.url_root.rstrip('/') if request else 'http://localhost:5001'
    
    # Padrão de busca: produto_{id}_*_{resolucao}.*
    upload_folder = app.config['UPLOAD_FOLDER']
    found_images = {}
    
    try:
        # Verificar se pasta existe
        if not os.path.exists(upload_folder):
            return None
            
        # Listar todos os arquivos da pasta
        for filename in os.listdir(upload_folder):
            # Verificar se o arquivo segue o padrão do produto
            if filename.startswith(f'produto_{produto_id}_'):
                # Extrair resolução do nome do arquivo
                # Formato esperado: produto_1_uuid_thumbnail.jpg
                parts = filename.split('_')
                if len(parts) >= 4:
                    # A resolução está antes da extensão
                    resolution_with_ext = parts[-1]  # "thumbnail.jpg"
                    resolution = resolution_with_ext.split('.')[0]  # "thumbnail"
                    
                    # Verificar se é uma resolução válida
                    if resolution in IMAGE_RESOLUTIONS:
                        found_images[resolution] = f"{base_url}/images/produtos/{filename}"
        
        return found_images if found_images else None
        
    except Exception as e:
        print(f"❌ [ERROR] Erro ao gerar URLs dinâmicas: {e}")
        return None

def process_product_images(produto):
    """
    Processa produto para adicionar URLs dinâmicas das imagens
    Retorna apenas os campos essenciais: id_produto, nome, descricao, preco, estoque, urls_imagem
    """
    if not produto:
        return produto
    
    produto_id = produto.get('id_produto')
    if not produto_id:
        return produto
    
    # Gerar URLs dinâmicas
    dynamic_urls = generate_dynamic_image_urls(produto_id)
    
    # Criar resposta simplificada com apenas os campos necessários
    produto_simplificado = {
        'id_produto': produto.get('id_produto'),
        'nome': produto.get('nome'),
        'descricao': produto.get('descricao', ''),
        'preco': produto.get('preco'),
        'estoque': produto.get('estoque'),
        'urls_imagem': dynamic_urls
    }
    
    return produto_simplificado
@app.route("/test", methods=["GET"])
def test_route():
    """Rota de teste simples para verificar se servidor responde"""
    return jsonify({
        "message": "Servidor está funcionando",
        "timestamp": str(date.today()),
        "status": "OK"
    }), 200

@app.route("/test-db", methods=["GET"])
@jwt_required()
def test_db():
    """Testa conexão com banco de dados"""
    try:
        dao_produto = ProdutoDAO()
        produtos = dao_produto.listar_produtos()
        return jsonify({
            "message": "Banco de dados funcionando",
            "total_produtos": len(produtos),
            "status": "OK"
        }), 200
    except Exception as e:
        return jsonify({
            "message": "Erro no banco de dados",
            "error": str(e),
            "status": "ERROR"
        }), 500

@app.route("/produtos", methods=["GET"])
@jwt_required()
def listar_produtos():
    try:
        print("📋 [DEBUG] Iniciando listagem de produtos...")
        
        dao_produto = ProdutoDAO()
        print("📋 [DEBUG] DAO criado, consultando banco...")
        
        produtos = dao_produto.listar_produtos()
        print(f"📋 [DEBUG] Consulta concluída. {len(produtos)} produtos encontrados")
        
        # Processar cada produto para adicionar URLs dinâmicas
        produtos_processados = []
        for produto in produtos:
            produto_dict = dict(produto) if hasattr(produto, 'keys') else produto
            
            # Aplicar processamento dinâmico de imagens
            produto_processado = process_product_images(produto_dict)
            produtos_processados.append(produto_processado)
        
        #print(f"📋 [DEBUG] Processamento concluído. Retornando {len(produtos_processados)} produtos")
        #print(f"📦 [DEBUG] Array de produtos processados: {produtos_processados}")
        return jsonify(produtos_processados), 200
        
    except Exception as erro:
        print(f"❌ [ERROR] Erro na listagem: {erro}")
        import traceback
        traceback.print_exc()
        return jsonify({
            "erro": "Erro ao listar produtos",
            "mensagem": str(erro)
        }), 500

@app.route("/produtos/<int:id>", methods=["GET"])
def obter_produto(id):
    # TODO: Buscar produto por ID
    try:
        dao_produto = ProdutoDAO()
        produto = dao_produto.buscar_produto(id)
        if not produto:
            return jsonify({"erro": f"Produto com ID {id} não encontrado"}), 404
        if hasattr(produto, "to_dict"):
            produto = produto.to_dict()

        # Processar imagens do produto
        produto_processado = process_product_images(produto)
        
        return jsonify(produto_processado), 200
    except Exception as erro:
        return jsonify({
            "erro": "Erro ao buscar produto",
            "mensagem": str(erro)
        }), 500

@app.route("/produtos/<int:id>", methods=["PUT"])
@jwt_required()
def atualizar_produto(id):
    try:
        dados = request.get_json()
        
        # Validar que pelo menos um campo foi enviado
        if not dados:
            return jsonify({"erro": "Nenhum dado fornecido para atualização"}), 400
        
        dao_produto = ProdutoDAO()
        
        # Buscar o produto existente
        produto_atual = dao_produto.buscar_produto(id)
        if not produto_atual:
            return jsonify({"erro": f"Produto com ID {id} não encontrado"}), 404
        
        # Atualizar os campos (mantém os valores atuais se não forem enviados)
        nome = dados.get('nome', produto_atual['nome'])
        descricao = dados.get('descricao', produto_atual['descricao'])
        preco = dados.get('preco', produto_atual['preco'])
        estoque = dados.get('estoque', produto_atual['estoque'])
        nome_imagem = dados.get('nome_imagem', produto_atual['nome_imagem'])
        
        # Executar a atualização
        dao_produto.atualizar_produto(id, nome, descricao, preco, estoque, nome_imagem)
        
        # Buscar o produto atualizado para retornar
        produto_atualizado = dao_produto.buscar_produto(id)
        
        # Aplicar processamento dinâmico de imagens
        produto_processado = process_product_images(produto_atualizado)
        
        return jsonify({
            "mensagem": "Produto atualizado com sucesso",
            "produto": produto_processado
        }), 200
        
    except Exception as erro:
        return jsonify({
            "erro": "Erro ao atualizar produto",
            "mensagem": str(erro)
        }), 500

@app.route("/produtos/<int:id>", methods=["DELETE"])
@jwt_required()
def excluir_produto(id):
    try:
        dao_produto = ProdutoDAO()
        
        # Verificar se o produto existe
        produto = dao_produto.buscar_produto(id)
        if not produto:
            return jsonify({"erro": f"Produto com ID {id} não encontrado"}), 404
        
        # Executar a exclusão
        dao_produto.deletar_produto(id)
        
        return jsonify({
            "mensagem": "Produto excluído com sucesso",
            "produto_excluido": produto
        }), 200
        
    except Exception as erro:
        return jsonify({
            "erro": "Erro ao excluir produto",
            "mensagem": str(erro)
        }), 500


# ---------------------------
# 🖼️ GESTÃO DE IMAGENS
# ---------------------------

def allowed_file(filename):
    """Verifica se o arquivo tem extensão permitida"""
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

def create_image_resolutions(image_path, base_filename):
    """
    Cria múltiplas resoluções de uma imagem e retorna os caminhos dos arquivos criados
    """
    created_files = {}
    
    try:
        with Image.open(image_path) as img:
            # Converter para RGB se necessário (para JPEG)
            if img.mode in ('RGBA', 'LA', 'P'):
                img = img.convert('RGB')
            
            for resolution_name, (width, height) in IMAGE_RESOLUTIONS.items():
                # Calcular novo tamanho mantendo proporção
                img_copy = img.copy()
                img_copy.thumbnail((width, height), RESAMPLE_FILTER)
                
                # Criar nome do arquivo para esta resolução
                name_parts = base_filename.rsplit('.', 1)
                if len(name_parts) == 2:
                    name, ext = name_parts
                    resolution_filename = f"{name}_{resolution_name}.{ext}"
                else:
                    resolution_filename = f"{base_filename}_{resolution_name}"
                
                resolution_path = os.path.join(app.config['UPLOAD_FOLDER'], resolution_filename)
                
                # Salvar imagem redimensionada
                img_copy.save(resolution_path, quality=85, optimize=True)
                created_files[resolution_name] = resolution_filename
                
    except Exception as e:
        # Se houver erro, limpar arquivos já criados
        for filename in created_files.values():
            file_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
            if os.path.exists(file_path):
                os.remove(file_path)
        raise e
    
    return created_files

def generate_image_urls(base_url, filenames_dict):
    """
    Gera URLs para todas as resoluções de imagem
    """
    urls = {}
    for resolution, filename in filenames_dict.items():
        urls[resolution] = f"{base_url}/images/produtos/{filename}"
    return urls

def cleanup_product_images(produto_url_data):
    """
    Remove arquivos de imagem de um produto baseado nos dados da URL
    """
    if not produto_url_data:
        return
    
    try:
        # Se é string JSON, parse
        if isinstance(produto_url_data, str):
            url_data = json.loads(produto_url_data)
        else:
            url_data = produto_url_data
        
        # Remover cada arquivo de resolução
        for resolution, url in url_data.items():
            if url:
                filename = url.split('/')[-1]
                filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
                if os.path.exists(filepath):
                    os.remove(filepath)
    except Exception:
        pass  # Ignorar erros de limpeza

@app.route("/images/produtos/<filename>", methods=["GET"])
def get_product_image(filename):
    """Serve imagens de produtos estaticamente"""
    try:
        return send_from_directory(app.config['UPLOAD_FOLDER'], filename)
    except FileNotFoundError:
        return jsonify({"erro": "Imagem não encontrada"}), 404

@app.route("/produtos/<int:id>/images", methods=["GET"])
@jwt_required()
def get_product_images_urls(id):
    """
    Retorna todas as URLs de imagens disponíveis para um produto específico
    Geração dinâmica baseada nos arquivos existentes
    """
    try:
        dao_produto = ProdutoDAO()
        
        # Verificar se produto existe
        produto = dao_produto.buscar_produto(id)
        if not produto:
            return jsonify({"erro": f"Produto com ID {id} não encontrado"}), 404
        
        # Gerar URLs dinâmicas
        image_urls = generate_dynamic_image_urls(id)
        
        if image_urls:
            return jsonify({
                "id_produto": id,
                "nome_produto": produto.get('nome'),
                "imagens_disponiveis": len(image_urls),
                "urls": image_urls,
                "resoluções_disponiveis": list(image_urls.keys())
            }), 200
        else:
            return jsonify({
                "id_produto": id,
                "nome_produto": produto.get('nome'),
                "imagens_disponiveis": 0,
                "urls": None,
                "mensagem": "Nenhuma imagem encontrada para este produto"
            }), 200
            
    except Exception as erro:
        return jsonify({
            "erro": "Erro ao buscar imagens do produto",
            "mensagem": str(erro)
        }), 500

@app.route("/admin/images/scan", methods=["GET"])
def scan_all_product_images():
    """
    Faz um scan de todas as imagens disponíveis no sistema
    Útil para debug e verificação de integridade
    """
    try:
        upload_folder = app.config['UPLOAD_FOLDER']
        
        if not os.path.exists(upload_folder):
            return jsonify({
                "erro": "Pasta de upload não encontrada",
                "caminho": upload_folder
            }), 404
        
        # Escanear todos os arquivos
        arquivos_encontrados = []
        produtos_com_imagens = {}
        
        for filename in os.listdir(upload_folder):
            if filename.startswith('produto_'):
                # Extrair ID do produto do nome do arquivo
                try:
                    parts = filename.split('_')
                    if len(parts) >= 3:
                        produto_id = int(parts[1])
                        
                        if produto_id not in produtos_com_imagens:
                            produtos_com_imagens[produto_id] = []
                        
                        produtos_com_imagens[produto_id].append(filename)
                        arquivos_encontrados.append(filename)
                        
                except ValueError:
                    continue
        
        # Gerar URLs para cada produto
        produtos_urls = {}
        for produto_id in produtos_com_imagens:
            produtos_urls[produto_id] = generate_dynamic_image_urls(produto_id)
        
        return jsonify({
            "total_arquivos": len(arquivos_encontrados),
            "produtos_com_imagens": len(produtos_com_imagens),
            "arquivos": arquivos_encontrados,
            "produtos_urls": produtos_urls,
            "resumo_por_produto": {
                produto_id: len(arquivos) 
                for produto_id, arquivos in produtos_com_imagens.items()
            }
        }), 200
        
    except Exception as erro:
        return jsonify({
            "erro": "Erro ao escanear imagens",
            "mensagem": str(erro)
        }), 500

@app.route("/produtos/<int:id>/upload-image", methods=["POST"])
def upload_product_image(id):
    """Upload de imagem para um produto específico com múltiplas resoluções"""
    try:
        dao_produto = ProdutoDAO()
        
        # Verificar se produto existe
        produto = dao_produto.buscar_produto(id)
        if not produto:
            return jsonify({"erro": f"Produto com ID {id} não encontrado"}), 404
        
        # Verificar se arquivo foi enviado
        if 'image' not in request.files:
            return jsonify({"erro": "Nenhum arquivo de imagem enviado"}), 400
        
        file = request.files['image']
        if file.filename == '':
            return jsonify({"erro": "Nenhum arquivo selecionado"}), 400
        
        if file and allowed_file(file.filename):
            # Limpar imagens anteriores se existirem
            if produto['nome_imagem']:
                cleanup_product_images(produto['nome_imagem'])
            
            # Gerar nome base único para o arquivo
            file_extension = file.filename.rsplit('.', 1)[1].lower()
            base_filename = f"produto_{id}_{uuid.uuid4().hex}.{file_extension}"
            
            # Salvar arquivo original temporariamente
            temp_filepath = os.path.join(app.config['UPLOAD_FOLDER'], base_filename)
            file.save(temp_filepath)
            
            try:
                # Criar múltiplas resoluções
                resolution_filenames = create_image_resolutions(temp_filepath, base_filename)
                
                # Remover arquivo original temporário
                os.remove(temp_filepath)
                
                # Gerar URLs para todas as resoluções (método dinâmico)
                base_url = request.url_root.rstrip('/')
                
                # Agora não precisamos salvar URLs no banco, elas são geradas dinamicamente
                # Apenas salvamos um indicador de que o produto tem imagens
                dao_produto.atualizar_produto(
                    id, 
                    produto['nome'], 
                    produto['descricao'], 
                    produto['preco'], 
                    produto['estoque'], 
                    "has_images"  # Indicador simples de que existem imagens
                )
                
                # Gerar URLs dinâmicas para retorno
                image_urls = generate_dynamic_image_urls(id, base_url)
                
                return jsonify({
                    "mensagem": "Imagem enviada com sucesso",
                    "resolutions": image_urls,
                    "filenames": resolution_filenames,
                    "total_arquivos": len(resolution_filenames)
                }), 200
                
            except Exception as e:
                # Limpar arquivo temporário em caso de erro
                if os.path.exists(temp_filepath):
                    os.remove(temp_filepath)
                raise e
                
        else:
            return jsonify({"erro": "Tipo de arquivo não permitido. Use: png, jpg, jpeg, gif, webp"}), 400
            
    except Exception as erro:
        return jsonify({
            "erro": "Erro ao fazer upload da imagem",
            "mensagem": str(erro)
        }), 500

@app.route("/produtos/<int:id>/remove-image", methods=["DELETE"])
def remove_product_image(id):
    """Remove todas as resoluções de imagem de um produto usando sistema dinâmico"""
    try:
        dao_produto = ProdutoDAO()
        
        # Verificar se produto existe
        produto = dao_produto.buscar_produto(id)
        if not produto:
            return jsonify({"erro": f"Produto com ID {id} não encontrado"}), 404
        
        # Encontrar e remover todos os arquivos do produto dinamicamente
        upload_folder = app.config['UPLOAD_FOLDER']
        arquivos_removidos = []
        
        if os.path.exists(upload_folder):
            for filename in os.listdir(upload_folder):
                # Verificar se o arquivo pertence ao produto
                if filename.startswith(f'produto_{id}_'):
                    filepath = os.path.join(upload_folder, filename)
                    try:
                        os.remove(filepath)
                        arquivos_removidos.append(filename)
                        print(f"🗑️ [DEBUG] Arquivo removido: {filename}")
                    except Exception as e:
                        print(f"❌ [ERROR] Erro ao remover {filename}: {e}")
        
        # Atualizar produto removendo indicador de imagens
        dao_produto.atualizar_produto(
            id, 
            produto['nome'], 
            produto['descricao'], 
            produto['preco'], 
            produto['estoque'], 
            None
        )
        
        return jsonify({
            "mensagem": f"Imagens do produto removidas com sucesso",
            "arquivos_removidos": arquivos_removidos,
            "total_removidos": len(arquivos_removidos)
        }), 200
        
    except Exception as erro:
        return jsonify({
            "erro": "Erro ao remover imagem",
            "mensagem": str(erro)
        }), 500


# ---------------------------
# 🧾 VENDA
# ---------------------------
@app.route("/vendas", methods=["POST"])
def criar_venda():
    try:

        
        dados = request.get_json()
        
        # Validar campos obrigatórios
        campos_obrigatorios = ['id_venda', 'id_cliente', 'id_funcionario']
        for campo in campos_obrigatorios:
            if campo not in dados:
                return jsonify({"erro": f"O campo '{campo}' é obrigatório"}), 400
        
        dao_venda = VendaDAO()
        dao_cliente = ClienteDAO()
        dao_funcionario = FuncionarioDAO()
        
        # Verificar se cliente existe
        cliente = dao_cliente.buscar_cliente(dados['id_cliente'])
        if not cliente:
            return jsonify({"erro": f"Cliente com ID {dados['id_cliente']} não encontrado"}), 404
        
        # Verificar se funcionário existe
        funcionario = dao_funcionario.buscar_funcionario(dados['id_funcionario'])
        if not funcionario:
            return jsonify({"erro": f"Funcionário com ID {dados['id_funcionario']} não encontrado"}), 404
        
        # Preparar dados da venda
        id_venda = dados['id_venda']
        id_cliente = dados['id_cliente']
        id_funcionario = dados['id_funcionario']
        data_venda = dados.get('data_venda', str(date.today()))
        total = dados.get('total', 0.0)
        
        # Inserir venda
        dao_venda.inserir_venda(id_venda, id_cliente, id_funcionario, data_venda, total)
        
        # Inserir itens da venda se fornecidos
        itens = dados.get('itens', [])
        if itens:
            dao_item = ItemVendaDAO()
            dao_produto = ProdutoDAO()
            
            total_calculado = 0.0
            for item in itens:
                # Verificar se produto existe
                produto = dao_produto.buscar_produto(item['id_produto'])
                if not produto:
                    return jsonify({"erro": f"Produto com ID {item['id_produto']} não encontrado"}), 404
                
                # Verificar estoque
                if produto['estoque'] < item['quantidade']:
                    return jsonify({
                        "erro": f"Estoque insuficiente para produto {produto['nome']}. Disponível: {produto['estoque']}"
                    }), 400
                
                # Inserir item
                id_item = item.get('id_item')
                preco_unitario = item.get('preco_unitario', produto['preco'])
                dao_item.inserir_item(id_item, id_venda, item['id_produto'], item['quantidade'], preco_unitario)
                
                # Atualizar estoque
                novo_estoque = produto['estoque'] - item['quantidade']
                dao_produto.atualizar_produto(
                    item['id_produto'],
                    produto['nome'],
                    produto['descricao'],
                    produto['preco'],
                    novo_estoque
                )
                
                total_calculado += preco_unitario * item['quantidade']
            
            # Atualizar total da venda se foi calculado
            if total == 0.0 and total_calculado > 0.0:
                dao_venda.atualizar_venda(id_venda, id_cliente, id_funcionario, data_venda, total_calculado)
        
        # Buscar venda criada
        venda_criada = dao_venda.buscar_venda(id_venda)
        
        return jsonify({
            "mensagem": "Venda criada com sucesso",
            "venda": venda_criada
        }), 201
        
    except Exception as erro:
        return jsonify({
            "erro": "Erro ao criar venda",
            "mensagem": str(erro)
        }), 500

@app.route("/vendas", methods=["GET"])
def listar_vendas():
    # TODO: Listar todas as vendas
    try:
        dao_venda = VendaDAO()
        vendas = dao_venda.listar_vendas()
        return jsonify(vendas), 200
    except Exception as erro:
        return jsonify({
            "erro": "Erro ao listar vendas",
            "mensagem": str(erro)
        }), 500

@app.route("/vendas/<int:id>", methods=["GET"])
def obter_venda(id):
    # TODO: Obter detalhes da venda (com itens)
    try:
        dao_venda = VendaDAO()
        venda = dao_venda.buscar_venda(id)
        if not venda:
            return jsonify({"erro": f"Venda com ID {id} não encontrada"}), 404
        return jsonify(venda), 200
    except Exception as erro:
        return jsonify({
            "erro": "Erro ao buscar venda",
            "mensagem": str(erro)
        }), 500

@app.route("/vendas/<int:id>", methods=["DELETE"])
def excluir_venda(id):
    # TODO: Excluir venda
    try:
        dao_venda = VendaDAO()
        resultado = dao_venda.excluir_venda(id)
        if not resultado:
            return jsonify({"erro": f"Venda com ID {id} não encontrada"}), 404
        return jsonify({"mensagem": f"Venda com ID {id} excluída com sucesso"}), 200
    except Exception as erro:
        return jsonify({
            "erro": "Erro ao excluir venda",
            "mensagem": str(erro)
        }), 500


# ---------------------------
# 🧮 ITEM VENDA
# ---------------------------
@app.route("/itens_venda", methods=["GET"])
def listar_itens_venda():
    # TODO: Listar todos os itens de venda
    try:
        dao_item = ItemVendaDAO()
        itens = dao_item.listar_itens()
        return jsonify(itens), 200
    except Exception as erro:
        return jsonify({
            "erro": "Erro ao listar itens de venda",
            "mensagem": str(erro)
        }), 500

@app.route("/itens_venda/<int:id>", methods=["GET"])
def obter_item_venda(id):
    # TODO: Obter item de venda por ID
    try:
        dao_item = ItemVendaDAO()
        item = dao_item.buscar_item(id)
        if not item:
            return jsonify({"erro": f"Item de venda com ID {id} não encontrado"}), 404
        return jsonify(item), 200
    except Exception as erro:
        return jsonify({
            "erro": "Erro ao buscar item de venda",
            "mensagem": str(erro)
        }), 500

@app.route("/vendas/<int:id_venda>/itens", methods=["GET"])
def listar_itens_de_venda(id_venda):
    # TODO: Listar itens de uma venda específica
    try:
        dao_item = ItemVendaDAO()
        itens = dao_item.listar_itens_por_venda(id_venda)
        return jsonify(itens), 200
    except Exception as erro:
        return jsonify({
            "erro": "Erro ao listar itens de venda",
            "mensagem": str(erro)
        }), 500


# ---------------------------
# 🔒 LOGIN (JWT) E RECUPERAÇÃO DE SENHA
# ---------------------------

import secrets
import hashlib
from datetime import datetime, timedelta

# Simple in-memory user store for demo. Prefer storing hashed passwords in DB.
# You can override by setting an env var `AUTH_USERS` with JSON like: '{"maria":"1234"}'
import json

try:
    default_users = json.loads(os.environ.get("AUTH_USERS", "{}"))
except Exception:
    default_users = {}

# Provide a small demo user if none configured (helps local testing)
if not default_users:
    default_users = {"joaovitorvlb@hotmail.com": "1234", "admin": "admin"}

# Store para tokens de recuperação de senha (em produção, usar banco de dados)
recovery_tokens = {}  # {token: {"email": str, "expiry": datetime, "used": bool}}

def generate_recovery_token():
    """Gera um token seguro para recuperação de senha"""
    return secrets.token_urlsafe(32)

def send_recovery_email(email, token):
    """
    Envia email de recuperação usando SMTP do Outlook/Hotmail
    """
    try:
        # Configurações para Outlook/Hotmail
        smtp_server = "smtp-mail.outlook.com"
        smtp_port = 587
        
        # CONFIGURE AQUI SUAS CREDENCIAIS
        # Crie variáveis de ambiente ou coloque temporariamente aqui para testar
        sender_email = os.getenv('EMAIL_USER', 'seu_email@hotmail.com')  # Substitua pelo seu email
        sender_password = os.getenv('EMAIL_PASSWORD', 'sua_senha')  # Substitua pela sua senha
        
        recovery_link = f"http://localhost:5001/redefinir-senha?token={token}"
        
        # Criando a mensagem
        msg = MIMEMultipart()
        msg['From'] = sender_email
        msg['To'] = email
        msg['Subject'] = "🔐 Recuperação de Senha - Sistema de Vendas"
        
        # Corpo do email em HTML (mais bonito)
        body = f"""
        <html>
        <body>
            <h2>🔐 Recuperação de Senha</h2>
            <p>Olá!</p>
            <p>Você solicitou a recuperação de sua senha para o sistema.</p>
            <p><strong>Clique no link abaixo para redefinir sua senha:</strong></p>
            <p><a href="{recovery_link}" style="background-color: #4CAF50; color: white; padding: 10px 20px; text-decoration: none; border-radius: 5px;">Redefinir Senha</a></p>
            <p><em>Ou copie e cole este link no seu navegador:</em><br>
            {recovery_link}</p>
            <hr>
            <p><strong>⚠️ Este link é válido por 30 minutos.</strong></p>
            <p><strong>⚠️ Se você não solicitou esta recuperação, ignore este email.</strong></p>
            <br>
            <p>Atenciosamente,<br>Equipe de Suporte</p>
        </body>
        </html>
        """
        
        msg.attach(MIMEText(body, 'html'))
        
        # Conectando e enviando
        server = smtplib.SMTP(smtp_server, smtp_port)
        server.starttls()  # Habilita criptografia
        server.login(sender_email, sender_password)
        server.send_message(msg)
        server.quit()
        
        print(f"✅ [EMAIL] Email enviado com sucesso para: {email}")
        return True
        
    except Exception as e:
        print(f"❌ [EMAIL] Erro ao enviar email: {e}")
        # Fallback: exibe no console se falhar
        print("📧 [EMAIL] Simulando envio de email de recuperação:")
        print(f"📧 [EMAIL] Para: {email}")
        print(f"📧 [EMAIL] Link: {recovery_link}")
        return False
    print("📧 [EMAIL] Email enviado com sucesso (simulação)")
    
    return True

@app.route("/esqueci-senha", methods=["POST"])
def esqueci_senha():
    """
    Endpoint para solicitar recuperação de senha
    Recebe email do usuário e envia link de recuperação
    """
    try:
        data = request.get_json()
        
        if not data or 'email' not in data:
            return jsonify({
                "erro": "Email é obrigatório",
                "exemplo": {"email": "usuario@exemplo.com"}
            }), 400
        
        email = data['email'].strip().lower()
        
        # Validar formato de email básico
        if '@' not in email or '.' not in email:
            return jsonify({"erro": "Formato de email inválido"}), 400
        
        # Verificar se usuário existe
        if email not in default_users:
            # Por segurança, não revelar se email existe ou não
            return jsonify({
                "mensagem": "Se o email estiver cadastrado, você receberá instruções de recuperação.",
                "status": "processado"
            }), 200
        
        # Gerar token de recuperação
        recovery_token = generate_recovery_token()
        
        # Armazenar token com expiração de 30 minutos
        recovery_tokens[recovery_token] = {
            "email": email,
            "expiry": datetime.now() + timedelta(minutes=30),
            "used": False
        }
        
        # Enviar email de recuperação
        email_sent = send_recovery_email(email, recovery_token)
        
        if email_sent:
            return jsonify({
                "mensagem": "Instruções de recuperação enviadas para seu email.",
                "status": "enviado",
                "validade": "30 minutos",
                "token_debug": recovery_token  # Remover em produção
            }), 200
        else:
            return jsonify({
                "erro": "Erro ao enviar email de recuperação",
                "status": "erro_envio"
            }), 500
            
    except Exception as e:
        return jsonify({
            "erro": "Erro interno do servidor",
            "mensagem": str(e)
        }), 500

@app.route("/validar-token-recuperacao", methods=["POST"])
def validar_token_recuperacao():
    """
    Endpoint para validar se um token de recuperação é válido
    Útil para frontend verificar antes de exibir formulário
    """
    try:
        data = request.get_json()
        
        if not data or 'token' not in data:
            return jsonify({"erro": "Token é obrigatório"}), 400
        
        token = data['token']
        
        # Verificar se token existe
        if token not in recovery_tokens:
            return jsonify({
                "valido": False,
                "erro": "Token inválido ou expirado"
            }), 400
        
        token_data = recovery_tokens[token]
        
        # Verificar se token já foi usado
        if token_data['used']:
            return jsonify({
                "valido": False,
                "erro": "Token já foi utilizado"
            }), 400
        
        # Verificar se token expirou
        if datetime.now() > token_data['expiry']:
            # Remover token expirado
            del recovery_tokens[token]
            return jsonify({
                "valido": False,
                "erro": "Token expirado"
            }), 400
        
        # Token válido
        remaining_time = token_data['expiry'] - datetime.now()
        minutes_left = int(remaining_time.total_seconds() / 60)
        
        return jsonify({
            "valido": True,
            "email": token_data['email'],
            "tempo_restante": f"{minutes_left} minutos"
        }), 200
        
    except Exception as e:
        return jsonify({
            "erro": "Erro interno do servidor",
            "mensagem": str(e)
        }), 500

@app.route("/redefinir-senha", methods=["POST"])
def redefinir_senha():
    """
    Endpoint para redefinir senha usando token de recuperação
    """
    try:
        data = request.get_json()
        
        # Validar campos obrigatórios
        required_fields = ['token', 'nova_senha']
        for field in required_fields:
            if not data or field not in data:
                return jsonify({
                    "erro": f"Campo '{field}' é obrigatório",
                    "exemplo": {
                        "token": "token_de_recuperacao",
                        "nova_senha": "nova_senha_123"
                    }
                }), 400
        
        token = data['token']
        nova_senha = data['nova_senha']
        
        # Validar nova senha
        if len(nova_senha) < 4:
            return jsonify({
                "erro": "Nova senha deve ter pelo menos 4 caracteres"
            }), 400
        
        # Verificar se token existe e é válido
        if token not in recovery_tokens:
            return jsonify({
                "erro": "Token inválido ou expirado"
            }), 400
        
        token_data = recovery_tokens[token]
        
        # Verificar se token já foi usado
        if token_data['used']:
            return jsonify({
                "erro": "Token já foi utilizado"
            }), 400
        
        # Verificar se token expirou
        if datetime.now() > token_data['expiry']:
            del recovery_tokens[token]
            return jsonify({
                "erro": "Token expirado"
            }), 400
        
        # Atualizar senha do usuário
        email = token_data['email']
        default_users[email] = nova_senha
        
        # Marcar token como usado
        recovery_tokens[token]['used'] = True
        
        # Log da alteração
        print(f"🔐 [SECURITY] Senha alterada para usuário: {email}")
        
        return jsonify({
            "mensagem": "Senha redefinida com sucesso!",
            "status": "sucesso",
            "email": email
        }), 200
        
    except Exception as e:
        return jsonify({
            "erro": "Erro interno do servidor",
            "mensagem": str(e)
        }), 500

@app.route("/redefinir-senha", methods=["GET"])
def form_redefinir_senha():
    """
    Página HTML para redefinir senha usando template
    """
    token = request.args.get('token')
    
    if not token:
        return render_template_string("""
        <div style="text-align: center; margin-top: 50px; font-family: Arial;">
            <h2>🔐 Recuperação de Senha</h2>
            <p>❌ Token não fornecido.</p>
            <a href="/esqueci-senha" style="color: #007bff;">Solicitar nova recuperação</a>
        </div>
        """), 400
    
    # Verificar se token é válido
    if token not in recovery_tokens:
        return render_template_string("""
        <div style="text-align: center; margin-top: 50px; font-family: Arial;">
            <h2>🔐 Recuperação de Senha</h2>
            <p>❌ Token inválido ou expirado.</p>
            <a href="#" onclick="solicitarRecuperacao()" style="color: #007bff;">Solicitar nova recuperação</a>
            <script>
            function solicitarRecuperacao() {
                var email = prompt("Digite seu email:");
                if (email) {
                    fetch('/esqueci-senha', {
                        method: 'POST',
                        headers: {'Content-Type': 'application/json'},
                        body: JSON.stringify({email: email})
                    }).then(r => r.json()).then(d => alert(d.mensagem));
                }
            }
            </script>
        </div>
        """), 400
    
    token_data = recovery_tokens[token]
    
    if token_data['used']:
        return render_template_string("""
        <div style="text-align: center; margin-top: 50px; font-family: Arial;">
            <h2>🔐 Recuperação de Senha</h2>
            <p>❌ Token já foi utilizado.</p>
        </div>
        """), 400
    
    if datetime.now() > token_data['expiry']:
        return render_template_string("""
        <div style="text-align: center; margin-top: 50px; font-family: Arial;">
            <h2>🔐 Recuperação de Senha</h2>
            <p>❌ Token expirado.</p>
        </div>
        """), 400
    
    # Renderizar template com o email do usuário
    return render_template('redefinir_senha.html', email=token_data['email'])

@app.route("/teste-recuperacao", methods=["GET"])
def teste_recuperacao():
    """
    Página de teste para o sistema de recuperação de senha
    """
    return render_template('teste_recuperacao.html')

@app.route("/recovery-status", methods=["GET"])
def recovery_status():
    """
    Endpoint para administradores verificarem tokens ativos (debug)
    Remover em produção ou adicionar autenticação admin
    """
    try:
        # Limpar tokens expirados
        current_time = datetime.now()
        expired_tokens = [
            token for token, data in recovery_tokens.items() 
            if current_time > data['expiry']
        ]
        
        for token in expired_tokens:
            del recovery_tokens[token]
        
        # Preparar dados para exibição
        active_tokens = []
        for token, data in recovery_tokens.items():
            remaining_time = data['expiry'] - current_time
            active_tokens.append({
                "token": token[:10] + "...",  # Mostrar apenas início do token
                "email": data['email'],
                "tempo_restante": str(remaining_time).split('.')[0],
                "usado": data['used'],
                "expira_em": data['expiry'].strftime("%Y-%m-%d %H:%M:%S")
            })
        
        return jsonify({
            "tokens_ativos": len(active_tokens),
            "tokens_expirados_removidos": len(expired_tokens),
            "detalhes": active_tokens
        }), 200
        
    except Exception as e:
        return jsonify({
            "erro": "Erro interno do servidor",
            "mensagem": str(e)
        }), 500


@app.route("/login", methods=["POST"])
def login():
    body = request.get_json(force=True)
    usuario = body.get("usuario")
    senha = body.get("senha")

    # Validação básica
    if not usuario or not senha:
        return jsonify({"erro": "Campos 'usuario' e 'senha' são obrigatórios"}), 400
    
    # cria o token JWT
    
    # Identity can be any data that is json serializable
    access_token = create_access_token(identity=usuario)

    # retorna o token junto com a mensagem
    if default_users.get(usuario) == senha:
        return jsonify({
        "mensagem": f"Login bem-sucedido. Bem-vindo, {usuario}!",
        "token": access_token
    }), 200
    else:
        return jsonify({"erro": "Credenciais inválidas"}), 401


@app.route("/logout", methods=["POST"])
def logout():
    # Stateless JWTs cannot be "destroyed" server-side unless you keep a revocation list.
    # For now just let the client discard the token.

    return jsonify({"mensagem": "Logout realizado (descartar token no cliente)"}), 200


# ---------------------------
# 👥 ROTAS DE USUÁRIOS (PROTEGIDAS POR JWT)
# ---------------------------

@app.route("/usuarios", methods=["GET"])
@jwt_required()
def listar_usuarios():
    """Lista todos os usuários (protegida por JWT)"""
    if not MYSQL_AVAILABLE:
        return jsonify({"erro": "DAO MySQL não disponível"}), 503
    
    try:
        dao_usuario = UsuarioDAO()
        usuarios = dao_usuario.listar_usuarios()
        return jsonify(usuarios), 200
    except Exception as e:
        return jsonify({"erro": "Erro ao listar usuários", "mensagem": str(e)}), 500


@app.route("/usuarios/<int:id>", methods=["GET"])
@jwt_required()
def buscar_usuario(id):
    """Busca um usuário específico por ID (protegida por JWT)"""
    if not MYSQL_AVAILABLE:
        return jsonify({"erro": "DAO MySQL não disponível"}), 503
    
    try:
        dao_usuario = UsuarioDAO()
        usuario = dao_usuario.buscar_usuario(id)
        
        if usuario:
            return jsonify(usuario), 200
        else:
            return jsonify({"erro": "Usuário não encontrado"}), 404
    except Exception as e:
        return jsonify({"erro": "Erro ao buscar usuário", "mensagem": str(e)}), 500


@app.route("/usuarios/email/<email>", methods=["GET"])
@jwt_required()
def buscar_usuario_por_email(email):
    """Busca um usuário específico por email (protegida por JWT)"""
    if not MYSQL_AVAILABLE:
        return jsonify({"erro": "DAO MySQL não disponível"}), 503
    
    try:
        dao_usuario = UsuarioDAO()
        usuario = dao_usuario.buscar_usuario_por_email(email)
        
        if usuario:
            return jsonify(usuario), 200
        else:
            return jsonify({"erro": "Usuário não encontrado"}), 404
    except Exception as e:
        return jsonify({"erro": "Erro ao buscar usuário", "mensagem": str(e)}), 500


@app.route("/usuarios/nivel/<int:id_nivel>", methods=["GET"])
@jwt_required()
def listar_usuarios_por_nivel(id_nivel):
    """Lista usuários de um nível de acesso específico (protegida por JWT)"""
    if not MYSQL_AVAILABLE:
        return jsonify({"erro": "DAO MySQL não disponível"}), 503
    
    try:
        dao_usuario = UsuarioDAO()
        usuarios = dao_usuario.listar_usuarios_por_nivel(id_nivel)
        return jsonify(usuarios), 200
    except Exception as e:
        return jsonify({"erro": "Erro ao listar usuários", "mensagem": str(e)}), 500


@app.route("/usuarios/ativos", methods=["GET"])
@jwt_required()
def listar_usuarios_ativos():
    """Lista apenas usuários ativos (protegida por JWT)"""
    if not MYSQL_AVAILABLE:
        return jsonify({"erro": "DAO MySQL não disponível"}), 503
    
    try:
        dao_usuario = UsuarioDAO()
        usuarios = dao_usuario.listar_usuarios_ativos()
        return jsonify(usuarios), 200
    except Exception as e:
        return jsonify({"erro": "Erro ao listar usuários ativos", "mensagem": str(e)}), 500


# ---------------------------
# 🔐 ROTAS DE NÍVEIS DE ACESSO (PROTEGIDAS POR JWT)
# ---------------------------

@app.route("/niveis-acesso", methods=["GET"])
@jwt_required()
def listar_niveis_acesso():
    """Lista todos os níveis de acesso (protegida por JWT)"""
    if not MYSQL_AVAILABLE:
        return jsonify({"erro": "DAO MySQL não disponível"}), 503
    
    try:
        dao_nivel = NivelAcessoDAO()
        niveis = dao_nivel.listar_niveis_acesso()
        return jsonify(niveis), 200
    except Exception as e:
        return jsonify({"erro": "Erro ao listar níveis de acesso", "mensagem": str(e)}), 500


# ---------------------------
# 🚀 EXECUÇÃO
# ---------------------------
if __name__ == "__main__":
    # Para responder em toda a rede (não apenas localhost):
    # host='0.0.0.0' - permite acesso de qualquer IP da rede
    # port=5000 - porta padrão (pode ser alterada)
    app.run(host='0.0.0.0', port=5001, debug=True)
