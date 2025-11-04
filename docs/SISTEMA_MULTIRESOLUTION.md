# Sistema de Múltiplas Resoluções de Imagem

## 📋 Visão Geral

O sistema foi implementado para automaticamente gerar três resoluções diferentes de cada imagem de produto carregada na API. Isso permite que o frontend Android escolha a resolução mais adequada para cada contexto de uso.

## 🎯 Resoluções Configuradas

| Resolução | Tamanho | Uso Recomendado |
|-----------|---------|-----------------|
| **thumbnail** | 150x150px | Listas, RecyclerView, miniaturas |
| **medium** | 400x400px | Cards de produto, tela de detalhes |
| **large** | 800x800px | Visualização ampliada, zoom |

## 🔄 Fluxo de Funcionamento

### 1. Upload de Imagem
```
POST /produtos/{id}/upload-image
Content-Type: multipart/form-data
Body: image=[arquivo]
```

**Processo automático:**
1. Recebe a imagem original
2. Gera automaticamente as 3 resoluções
3. Salva cada resolução como arquivo separado
4. Retorna URLs para todas as resoluções
5. Armazena as URLs no banco como JSON

### 2. Resposta do Upload
```json
{
    "mensagem": "Imagem enviada com sucesso",
    "resolutions": {
        "thumbnail": "http://localhost:5000/images/produtos/produto_1_abc123_thumbnail.jpg",
        "medium": "http://localhost:5000/images/produtos/produto_1_abc123_medium.jpg",
        "large": "http://localhost:5000/images/produtos/produto_1_abc123_large.jpg"
    },
    "filenames": {
        "thumbnail": "produto_1_abc123_thumbnail.jpg",
        "medium": "produto_1_abc123_medium.jpg", 
        "large": "produto_1_abc123_large.jpg"
    }
}
```

### 3. Consulta de Produtos

**GET /produtos** ou **GET /produtos/{id}**

```json
{
    "id_produto": 1,
    "nome": "Smartphone XYZ",
    "preco": 899.99,
    "estoque": 50,
    "descricao": "Smartphone com tela de 6.1 polegadas",
    "images": {
        "thumbnail": "http://localhost:5000/images/produtos/produto_1_abc123_thumbnail.jpg",
        "medium": "http://localhost:5000/images/produtos/produto_1_abc123_medium.jpg",
        "large": "http://localhost:5000/images/produtos/produto_1_abc123_large.jpg"
    }
}
```

## 📱 Implementação no Android

### RecyclerView Adapter
```java
public class ProductAdapter extends RecyclerView.Adapter<ProductAdapter.ViewHolder> {
    
    @Override
    public void onBindViewHolder(@NonNull ViewHolder holder, int position) {
        Product product = products.get(position);
        
        // Para RecyclerView, use thumbnail para performance
        String thumbnailUrl = product.getImages().get("thumbnail");
        
        Glide.with(context)
            .load(thumbnailUrl)
            .placeholder(R.drawable.placeholder_product)
            .error(R.drawable.error_image)
            .into(holder.productImage);
    }
}
```

### Tela de Detalhes
```java
public class ProductDetailActivity extends AppCompatActivity {
    
    private void loadProductImage(Product product) {
        // Para tela de detalhes, use medium
        String mediumUrl = product.getImages().get("medium");
        
        Glide.with(this)
            .load(mediumUrl)
            .placeholder(R.drawable.placeholder_detail)
            .into(productDetailImage);
    }
    
    private void showFullScreenImage(Product product) {
        // Para visualização ampliada, use large
        String largeUrl = product.getImages().get("large");
        
        // Implementar visualização em tela cheia
        Intent intent = new Intent(this, FullScreenImageActivity.class);
        intent.putExtra("image_url", largeUrl);
        startActivity(intent);
    }
}
```

### Modelo de Dados
```java
public class Product {
    private int idProduto;
    private String nome;
    private double preco;
    private int estoque;
    private String descricao;
    private Map<String, String> images;
    
    // Métodos de conveniência
    public String getThumbnailUrl() {
        return images != null ? images.get("thumbnail") : null;
    }
    
    public String getMediumUrl() {
        return images != null ? images.get("medium") : null;
    }
    
    public String getLargeUrl() {
        return images != null ? images.get("large") : null;
    }
}
```

## 🛠️ Configuração e Manutenção

### Alterando Resoluções
Para modificar as resoluções, edite a configuração em `app.py`:

```python
IMAGE_RESOLUTIONS = {
    'thumbnail': (150, 150),   # Altere conforme necessário
    'medium': (400, 400),      # Altere conforme necessário
    'large': (800, 800)        # Altere conforme necessário
}
```

### Limpeza de Arquivos
- O sistema automaticamente remove imagens antigas quando uma nova é carregada
- Use `DELETE /produtos/{id}/remove-image` para remover todas as resoluções

### Compatibilidade
- O sistema mantém compatibilidade com URLs antigas (string simples)
- URLs antigas são automaticamente convertidas para o novo formato

## 🔍 Testes

Execute o script de teste:
```bash
python test_multiresolution.py
```

Teste manual com curl:
```bash
# Upload de imagem
curl -X POST -F "image=@exemplo.jpg" http://localhost:5000/produtos/1/upload-image

# Consultar produto
curl http://localhost:5000/produtos/1

# Remover imagem
curl -X DELETE http://localhost:5000/produtos/1/remove-image
```

## ⚠️ Considerações

1. **Performance**: Use thumbnail para listas e medium para detalhes
2. **Armazenamento**: Cada imagem gera 3 arquivos - considere isso no planejamento de espaço
3. **Qualidade**: As imagens são otimizadas com qualidade 85% e compressão
4. **Formato**: Sistema converte automaticamente para RGB quando necessário
5. **Fallback**: Sempre implemente placeholders para casos de erro de carregamento