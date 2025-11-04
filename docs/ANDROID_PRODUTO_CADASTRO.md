# 📱 Cadastramento de Produto com Foto - Android Java

Este guia mostra como implementar o cadastramento de produtos com upload de fotos em um app Android Java, consumindo a API Flask com JWT.

## 🏗️ Estrutura do Projeto

```
app/src/main/java/com/exemplo/app/
├── models/
│   └── Produto.java
├── api/
│   ├── ApiClient.java
│   ├── ApiService.java
│   └── AuthInterceptor.java
├── activities/
│   └── CadastrarProdutoActivity.java
└── utils/
    └── ImageUtils.java
```

## 📋 1. Dependências no build.gradle (Module: app)

```gradle
dependencies {
    // Retrofit para API calls
    implementation 'com.squareup.retrofit2:retrofit:2.9.0'
    implementation 'com.squareup.retrofit2:converter-gson:2.9.0'
    implementation 'com.squareup.okhttp3:logging-interceptor:4.11.0'
    
    // Glide para carregamento de imagens
    implementation 'com.github.bumptech.glide:glide:4.15.1'
    
    // Material Design
    implementation 'com.google.android.material:material:1.9.0'
    
    // Para seleção de imagens
    implementation 'androidx.activity:activity:1.7.2'
    implementation 'androidx.fragment:fragment:1.6.1'
}
```

## 🔐 2. Configuração da API com JWT

### ApiClient.java
```java
package com.exemplo.app.api;

import okhttp3.OkHttpClient;
import okhttp3.logging.HttpLoggingInterceptor;
import retrofit2.Retrofit;
import retrofit2.converter.gson.GsonConverterFactory;

public class ApiClient {
    private static final String BASE_URL = "http://10.175.101.30:5001/"; // IP da sua rede
    private static Retrofit retrofit = null;
    private static String authToken = null;

    public static Retrofit getClient() {
        if (retrofit == null) {
            HttpLoggingInterceptor logging = new HttpLoggingInterceptor();
            logging.setLevel(HttpLoggingInterceptor.Level.BODY);

            OkHttpClient.Builder httpClient = new OkHttpClient.Builder();
            httpClient.addInterceptor(logging);
            
            // Adicionar interceptor de autenticação
            httpClient.addInterceptor(new AuthInterceptor());

            retrofit = new Retrofit.Builder()
                    .baseUrl(BASE_URL)
                    .addConverterFactory(GsonConverterFactory.create())
                    .client(httpClient.build())
                    .build();
        }
        return retrofit;
    }

    public static void setAuthToken(String token) {
        authToken = token;
    }

    public static String getAuthToken() {
        return authToken;
    }
}
```

### AuthInterceptor.java
```java
package com.exemplo.app.api;

import java.io.IOException;
import okhttp3.Interceptor;
import okhttp3.Request;
import okhttp3.Response;

public class AuthInterceptor implements Interceptor {
    @Override
    public Response intercept(Chain chain) throws IOException {
        Request originalRequest = chain.request();
        
        String token = ApiClient.getAuthToken();
        if (token != null) {
            Request.Builder builder = originalRequest.newBuilder()
                    .header("Authorization", "Bearer " + token);
            
            Request newRequest = builder.build();
            return chain.proceed(newRequest);
        }
        
        return chain.proceed(originalRequest);
    }
}
```

### ApiService.java
```java
package com.exemplo.app.api;

import com.exemplo.app.models.Produto;
import com.exemplo.app.models.LoginRequest;
import com.exemplo.app.models.LoginResponse;
import com.exemplo.app.models.UploadResponse;

import java.util.List;

import okhttp3.MultipartBody;
import okhttp3.RequestBody;
import retrofit2.Call;
import retrofit2.http.*;

public interface ApiService {
    
    @POST("login")
    Call<LoginResponse> login(@Body LoginRequest loginRequest);
    
    @GET("produtos")
    Call<List<Produto>> listarProdutos();
    
    @POST("produtos")
    Call<Produto> criarProduto(@Body Produto produto);
    
    @Multipart
    @POST("produtos/{id}/upload-image")
    Call<UploadResponse> uploadImagem(
        @Path("id") int produtoId,
        @Part MultipartBody.Part image
    );
    
    @DELETE("produtos/{id}/delete-image")
    Call<Void> deletarImagem(@Path("id") int produtoId);
}
```

## 📦 3. Modelos de Dados

### Produto.java
```java
package com.exemplo.app.models;

import com.google.gson.annotations.SerializedName;
import java.util.Map;

public class Produto {
    @SerializedName("id_produto")
    private int idProduto;
    
    private String nome;
    private double preco;
    private int estoque;
    private String descricao;
    private String url;
    
    @SerializedName("urls_imagem")
    private Map<String, String> urlsImagem;

    // Construtores
    public Produto() {}

    public Produto(String nome, double preco, int estoque, String descricao) {
        this.nome = nome;
        this.preco = preco;
        this.estoque = estoque;
        this.descricao = descricao;
    }

    // Getters e Setters
    public int getIdProduto() { return idProduto; }
    public void setIdProduto(int idProduto) { this.idProduto = idProduto; }

    public String getNome() { return nome; }
    public void setNome(String nome) { this.nome = nome; }

    public double getPreco() { return preco; }
    public void setPreco(double preco) { this.preco = preco; }

    public int getEstoque() { return estoque; }
    public void setEstoque(int estoque) { this.estoque = estoque; }

    public String getDescricao() { return descricao; }
    public void setDescricao(String descricao) { this.descricao = descricao; }

    public String getUrl() { return url; }
    public void setUrl(String url) { this.url = url; }

    public Map<String, String> getUrlsImagem() { return urlsImagem; }
    public void setUrlsImagem(Map<String, String> urlsImagem) { this.urlsImagem = urlsImagem; }

    // Métodos utilitários para imagens
    public String getThumbnailUrl() {
        return urlsImagem != null ? urlsImagem.get("thumbnail") : null;
    }

    public String getMediumUrl() {
        return urlsImagem != null ? urlsImagem.get("medium") : null;
    }

    public String getLargeUrl() {
        return urlsImagem != null ? urlsImagem.get("large") : null;
    }
}
```

### LoginRequest.java
```java
package com.exemplo.app.models;

public class LoginRequest {
    private String usuario;
    private String senha;

    public LoginRequest(String usuario, String senha) {
        this.usuario = usuario;
        this.senha = senha;
    }

    // Getters e Setters
    public String getUsuario() { return usuario; }
    public void setUsuario(String usuario) { this.usuario = usuario; }

    public String getSenha() { return senha; }
    public void setSenha(String senha) { this.senha = senha; }
}
```

### LoginResponse.java
```java
package com.exemplo.app.models;

public class LoginResponse {
    private String mensagem;
    private String token;

    // Getters e Setters
    public String getMensagem() { return mensagem; }
    public void setMensagem(String mensagem) { this.mensagem = mensagem; }

    public String getToken() { return token; }
    public void setToken(String token) { this.token = token; }
}
```

### UploadResponse.java
```java
package com.exemplo.app.models;

import java.util.Map;

public class UploadResponse {
    private String mensagem;
    private Map<String, String> urls;

    // Getters e Setters
    public String getMensagem() { return mensagem; }
    public void setMensagem(String mensagem) { this.mensagem = mensagem; }

    public Map<String, String> getUrls() { return urls; }
    public void setUrls(Map<String, String> urls) { this.urls = urls; }
}
```

## 🎨 4. Layout da Activity

### activity_cadastrar_produto.xml
```xml
<?xml version="1.0" encoding="utf-8"?>
<ScrollView xmlns:android="http://schemas.android.com/apk/res/android"
    xmlns:app="http://schemas.android.com/apk/res-auto"
    android:layout_width="match_parent"
    android:layout_height="match_parent"
    android:padding="16dp">

    <LinearLayout
        android:layout_width="match_parent"
        android:layout_height="wrap_content"
        android:orientation="vertical">

        <!-- Header -->
        <TextView
            android:layout_width="match_parent"
            android:layout_height="wrap_content"
            android:text="Cadastrar Produto"
            android:textSize="24sp"
            android:textStyle="bold"
            android:gravity="center"
            android:layout_marginBottom="24dp" />

        <!-- Imagem do Produto -->
        <com.google.android.material.card.MaterialCardView
            android:layout_width="200dp"
            android:layout_height="200dp"
            android:layout_gravity="center_horizontal"
            android:layout_marginBottom="16dp"
            app:cardCornerRadius="8dp"
            app:cardElevation="4dp">

            <ImageView
                android:id="@+id/ivProdutoImagem"
                android:layout_width="match_parent"
                android:layout_height="match_parent"
                android:scaleType="centerCrop"
                android:src="@drawable/ic_image_placeholder"
                android:background="@color/grey_200" />

        </com.google.android.material.card.MaterialCardView>

        <!-- Botões de Imagem -->
        <LinearLayout
            android:layout_width="match_parent"
            android:layout_height="wrap_content"
            android:orientation="horizontal"
            android:layout_marginBottom="24dp">

            <Button
                android:id="@+id/btnSelecionarImagem"
                android:layout_width="0dp"
                android:layout_height="wrap_content"
                android:layout_weight="1"
                android:layout_marginEnd="8dp"
                android:text="Selecionar Foto"
                style="@style/Widget.Material3.Button.OutlinedButton" />

            <Button
                android:id="@+id/btnRemoverImagem"
                android:layout_width="0dp"
                android:layout_height="wrap_content"
                android:layout_weight="1"
                android:layout_marginStart="8dp"
                android:text="Remover Foto"
                android:enabled="false"
                style="@style/Widget.Material3.Button.OutlinedButton" />

        </LinearLayout>

        <!-- Campos do Produto -->
        <com.google.android.material.textfield.TextInputLayout
            android:layout_width="match_parent"
            android:layout_height="wrap_content"
            android:layout_marginBottom="16dp"
            style="@style/Widget.Material3.TextInputLayout.OutlinedBox">

            <com.google.android.material.textfield.TextInputEditText
                android:id="@+id/etNome"
                android:layout_width="match_parent"
                android:layout_height="wrap_content"
                android:hint="Nome do Produto"
                android:inputType="textCapWords" />

        </com.google.android.material.textfield.TextInputLayout>

        <com.google.android.material.textfield.TextInputLayout
            android:layout_width="match_parent"
            android:layout_height="wrap_content"
            android:layout_marginBottom="16dp"
            style="@style/Widget.Material3.TextInputLayout.OutlinedBox">

            <com.google.android.material.textfield.TextInputEditText
                android:id="@+id/etPreco"
                android:layout_width="match_parent"
                android:layout_height="wrap_content"
                android:hint="Preço (R$)"
                android:inputType="numberDecimal" />

        </com.google.android.material.textfield.TextInputLayout>

        <com.google.android.material.textfield.TextInputLayout
            android:layout_width="match_parent"
            android:layout_height="wrap_content"
            android:layout_marginBottom="16dp"
            style="@style/Widget.Material3.TextInputLayout.OutlinedBox">

            <com.google.android.material.textfield.TextInputEditText
                android:id="@+id/etEstoque"
                android:layout_width="match_parent"
                android:layout_height="wrap_content"
                android:hint="Quantidade em Estoque"
                android:inputType="number" />

        </com.google.android.material.textfield.TextInputLayout>

        <com.google.android.material.textfield.TextInputLayout
            android:layout_width="match_parent"
            android:layout_height="wrap_content"
            android:layout_marginBottom="24dp"
            style="@style/Widget.Material3.TextInputLayout.OutlinedBox">

            <com.google.android.material.textfield.TextInputEditText
                android:id="@+id/etDescricao"
                android:layout_width="match_parent"
                android:layout_height="wrap_content"
                android:hint="Descrição"
                android:inputType="textMultiLine"
                android:lines="3"
                android:gravity="top" />

        </com.google.android.material.textfield.TextInputLayout>

        <!-- Botão Salvar -->
        <Button
            android:id="@+id/btnSalvar"
            android:layout_width="match_parent"
            android:layout_height="wrap_content"
            android:text="Cadastrar Produto"
            android:textSize="16sp"
            style="@style/Widget.Material3.Button" />

        <!-- Loading -->
        <ProgressBar
            android:id="@+id/progressBar"
            android:layout_width="wrap_content"
            android:layout_height="wrap_content"
            android:layout_gravity="center_horizontal"
            android:layout_marginTop="16dp"
            android:visibility="gone" />

    </LinearLayout>

</ScrollView>
```

## 📱 5. Activity Principal

### CadastrarProdutoActivity.java
```java
package com.exemplo.app.activities;

import android.content.Intent;
import android.net.Uri;
import android.os.Bundle;
import android.provider.MediaStore;
import android.util.Log;
import android.view.View;
import android.widget.Button;
import android.widget.EditText;
import android.widget.ImageView;
import android.widget.ProgressBar;
import android.widget.Toast;

import androidx.activity.result.ActivityResultLauncher;
import androidx.activity.result.contract.ActivityResultContracts;
import androidx.appcompat.app.AppCompatActivity;

import com.bumptech.glide.Glide;
import com.exemplo.app.R;
import com.exemplo.app.api.ApiClient;
import com.exemplo.app.api.ApiService;
import com.exemplo.app.models.LoginRequest;
import com.exemplo.app.models.LoginResponse;
import com.exemplo.app.models.Produto;
import com.exemplo.app.models.UploadResponse;
import com.exemplo.app.utils.ImageUtils;

import java.io.File;

import okhttp3.MediaType;
import okhttp3.MultipartBody;
import okhttp3.RequestBody;
import retrofit2.Call;
import retrofit2.Callback;
import retrofit2.Response;

public class CadastrarProdutoActivity extends AppCompatActivity {
    
    private static final String TAG = "CadastrarProduto";
    
    // Views
    private ImageView ivProdutoImagem;
    private EditText etNome, etPreco, etEstoque, etDescricao;
    private Button btnSelecionarImagem, btnRemoverImagem, btnSalvar;
    private ProgressBar progressBar;
    
    // Data
    private ApiService apiService;
    private Uri imagemSelecionada;
    private int produtoIdCriado = -1;
    
    // Launcher para seleção de imagem
    private ActivityResultLauncher<Intent> selecionarImagemLauncher;
    
    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_cadastrar_produto);
        
        initViews();
        setupApi();
        setupImagePicker();
        setupListeners();
        
        // Fazer login automático (em produção, implementar tela de login)
        fazerLogin();
    }
    
    private void initViews() {
        ivProdutoImagem = findViewById(R.id.ivProdutoImagem);
        etNome = findViewById(R.id.etNome);
        etPreco = findViewById(R.id.etPreco);
        etEstoque = findViewById(R.id.etEstoque);
        etDescricao = findViewById(R.id.etDescricao);
        btnSelecionarImagem = findViewById(R.id.btnSelecionarImagem);
        btnRemoverImagem = findViewById(R.id.btnRemoverImagem);
        btnSalvar = findViewById(R.id.btnSalvar);
        progressBar = findViewById(R.id.progressBar);
    }
    
    private void setupApi() {
        apiService = ApiClient.getClient().create(ApiService.class);
    }
    
    private void setupImagePicker() {
        selecionarImagemLauncher = registerForActivityResult(
            new ActivityResultContracts.StartActivityForResult(),
            result -> {
                if (result.getResultCode() == RESULT_OK && result.getData() != null) {
                    imagemSelecionada = result.getData().getData();
                    
                    // Mostrar preview da imagem
                    Glide.with(this)
                        .load(imagemSelecionada)
                        .centerCrop()
                        .into(ivProdutoImagem);
                    
                    btnRemoverImagem.setEnabled(true);
                }
            }
        );
    }
    
    private void setupListeners() {
        btnSelecionarImagem.setOnClickListener(v -> selecionarImagem());
        btnRemoverImagem.setOnClickListener(v -> removerImagem());
        btnSalvar.setOnClickListener(v -> salvarProduto());
    }
    
    private void fazerLogin() {
        LoginRequest loginRequest = new LoginRequest("admin", "admin");
        
        apiService.login(loginRequest).enqueue(new Callback<LoginResponse>() {
            @Override
            public void onResponse(Call<LoginResponse> call, Response<LoginResponse> response) {
                if (response.isSuccessful() && response.body() != null) {
                    String token = response.body().getToken();
                    ApiClient.setAuthToken(token);
                    Log.d(TAG, "Login realizado com sucesso");
                } else {
                    Log.e(TAG, "Erro no login: " + response.code());
                    Toast.makeText(CadastrarProdutoActivity.this, 
                        "Erro na autenticação", Toast.LENGTH_SHORT).show();
                }
            }
            
            @Override
            public void onFailure(Call<LoginResponse> call, Throwable t) {
                Log.e(TAG, "Falha no login", t);
                Toast.makeText(CadastrarProdutoActivity.this, 
                    "Erro de conexão", Toast.LENGTH_SHORT).show();
            }
        });
    }
    
    private void selecionarImagem() {
        Intent intent = new Intent(Intent.ACTION_PICK, MediaStore.Images.Media.EXTERNAL_CONTENT_URI);
        intent.setType("image/*");
        selecionarImagemLauncher.launch(intent);
    }
    
    private void removerImagem() {
        imagemSelecionada = null;
        ivProdutoImagem.setImageResource(R.drawable.ic_image_placeholder);
        btnRemoverImagem.setEnabled(false);
    }
    
    private void salvarProduto() {
        if (!validarCampos()) return;
        
        mostrarLoading(true);
        
        // Criar objeto produto
        Produto produto = new Produto(
            etNome.getText().toString().trim(),
            Double.parseDouble(etPreco.getText().toString().trim()),
            Integer.parseInt(etEstoque.getText().toString().trim()),
            etDescricao.getText().toString().trim()
        );
        
        // Primeiro criar o produto
        apiService.criarProduto(produto).enqueue(new Callback<Produto>() {
            @Override
            public void onResponse(Call<Produto> call, Response<Produto> response) {
                if (response.isSuccessful() && response.body() != null) {
                    produtoIdCriado = response.body().getIdProduto();
                    Log.d(TAG, "Produto criado com ID: " + produtoIdCriado);
                    
                    // Se há imagem selecionada, fazer upload
                    if (imagemSelecionada != null) {
                        uploadImagem();
                    } else {
                        mostrarLoading(false);
                        mostrarSucesso();
                    }
                } else {
                    mostrarLoading(false);
                    Log.e(TAG, "Erro ao criar produto: " + response.code());
                    Toast.makeText(CadastrarProdutoActivity.this, 
                        "Erro ao cadastrar produto", Toast.LENGTH_SHORT).show();
                }
            }
            
            @Override
            public void onFailure(Call<Produto> call, Throwable t) {
                mostrarLoading(false);
                Log.e(TAG, "Falha ao criar produto", t);
                Toast.makeText(CadastrarProdutoActivity.this, 
                    "Erro de conexão", Toast.LENGTH_SHORT).show();
            }
        });
    }
    
    private void uploadImagem() {
        try {
            File imageFile = ImageUtils.getFileFromUri(this, imagemSelecionada);
            
            RequestBody requestFile = RequestBody.create(
                MediaType.parse("image/*"), 
                imageFile
            );
            
            MultipartBody.Part imagePart = MultipartBody.Part.createFormData(
                "image", 
                imageFile.getName(), 
                requestFile
            );
            
            apiService.uploadImagem(produtoIdCriado, imagePart).enqueue(new Callback<UploadResponse>() {
                @Override
                public void onResponse(Call<UploadResponse> call, Response<UploadResponse> response) {
                    mostrarLoading(false);
                    
                    if (response.isSuccessful()) {
                        Log.d(TAG, "Upload realizado com sucesso");
                        mostrarSucesso();
                    } else {
                        Log.e(TAG, "Erro no upload: " + response.code());
                        Toast.makeText(CadastrarProdutoActivity.this, 
                            "Produto criado, mas erro no upload da imagem", 
                            Toast.LENGTH_LONG).show();
                    }
                }
                
                @Override
                public void onFailure(Call<UploadResponse> call, Throwable t) {
                    mostrarLoading(false);
                    Log.e(TAG, "Falha no upload", t);
                    Toast.makeText(CadastrarProdutoActivity.this, 
                        "Produto criado, mas erro no upload da imagem", 
                        Toast.LENGTH_LONG).show();
                }
            });
            
        } catch (Exception e) {
            mostrarLoading(false);
            Log.e(TAG, "Erro ao preparar imagem", e);
            Toast.makeText(this, "Erro ao processar imagem", Toast.LENGTH_SHORT).show();
        }
    }
    
    private boolean validarCampos() {
        String nome = etNome.getText().toString().trim();
        String preco = etPreco.getText().toString().trim();
        String estoque = etEstoque.getText().toString().trim();
        
        if (nome.isEmpty()) {
            etNome.setError("Nome é obrigatório");
            return false;
        }
        
        if (preco.isEmpty()) {
            etPreco.setError("Preço é obrigatório");
            return false;
        }
        
        try {
            Double.parseDouble(preco);
        } catch (NumberFormatException e) {
            etPreco.setError("Preço inválido");
            return false;
        }
        
        if (estoque.isEmpty()) {
            etEstoque.setError("Estoque é obrigatório");
            return false;
        }
        
        try {
            Integer.parseInt(estoque);
        } catch (NumberFormatException e) {
            etEstoque.setError("Estoque inválido");
            return false;
        }
        
        return true;
    }
    
    private void mostrarLoading(boolean mostrar) {
        progressBar.setVisibility(mostrar ? View.VISIBLE : View.GONE);
        btnSalvar.setEnabled(!mostrar);
        btnSelecionarImagem.setEnabled(!mostrar);
        btnRemoverImagem.setEnabled(!mostrar && imagemSelecionada != null);
    }
    
    private void mostrarSucesso() {
        Toast.makeText(this, "Produto cadastrado com sucesso!", Toast.LENGTH_LONG).show();
        
        // Limpar formulário ou voltar para tela anterior
        finish(); // ou implementar limpeza dos campos
    }
}
```

## 🛠️ 6. Utilitários para Imagem

### ImageUtils.java
```java
package com.exemplo.app.utils;

import android.content.Context;
import android.database.Cursor;
import android.net.Uri;
import android.provider.MediaStore;

import java.io.File;
import java.io.FileOutputStream;
import java.io.InputStream;

public class ImageUtils {
    
    public static File getFileFromUri(Context context, Uri uri) throws Exception {
        InputStream inputStream = context.getContentResolver().openInputStream(uri);
        
        // Criar arquivo temporário
        File tempFile = File.createTempFile("upload", ".jpg", context.getCacheDir());
        
        FileOutputStream outputStream = new FileOutputStream(tempFile);
        
        byte[] buffer = new byte[1024];
        int length;
        while ((length = inputStream.read(buffer)) > 0) {
            outputStream.write(buffer, 0, length);
        }
        
        outputStream.close();
        inputStream.close();
        
        return tempFile;
    }
    
    public static String getRealPathFromURI(Context context, Uri uri) {
        String[] projection = {MediaStore.Images.Media.DATA};
        Cursor cursor = context.getContentResolver().query(uri, projection, null, null, null);
        
        if (cursor == null) return null;
        
        int columnIndex = cursor.getColumnIndexOrThrow(MediaStore.Images.Media.DATA);
        cursor.moveToFirst();
        String path = cursor.getString(columnIndex);
        cursor.close();
        
        return path;
    }
}
```

## 📝 7. Permissões no AndroidManifest.xml

```xml
<uses-permission android:name="android.permission.INTERNET" />
<uses-permission android:name="android.permission.READ_EXTERNAL_STORAGE" />
<uses-permission android:name="android.permission.CAMERA" />

<!-- Para Android 9+ permitir HTTP -->
<application
    android:usesCleartextTraffic="true"
    ... >
    
    <activity 
        android:name=".activities.CadastrarProdutoActivity"
        android:exported="false" />
        
</application>
```

## 🚀 8. Como Usar

1. **Configure o IP do servidor** em `ApiClient.java`
2. **Execute o app Flask** na porta 5001
3. **Abra a activity** de cadastro no Android
4. **Preencha os dados** do produto
5. **Selecione uma foto** (opcional)
6. **Clique em "Cadastrar Produto"**

O sistema irá:
- ✅ Criar o produto via API
- ✅ Upload da foto em múltiplas resoluções
- ✅ Retornar URLs para thumbnail, medium e large
- ✅ Mostrar feedback ao usuário

## 🔍 Logs para Debug

```java
// No Android Studio, filtre por:
adb logcat | grep CadastrarProduto
```

## 📚 Próximos Passos

- Implementar tela de login separada
- Adicionar validação de rede
- Implementar cache de imagens
- Adicionar funcionalidade de edição
- Implementar retry automático em falhas