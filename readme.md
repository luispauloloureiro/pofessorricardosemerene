# Professor Ricardo Semerene - Landing Page

Landing page profissional para aulas particulares de matemática.

## 📁 Estrutura de Arquivos

```
├── index.html          # Página principal
├── styles.css          # Estilos CSS
├── discloud.config     # Configuração para deploy no Discloud
└── README.md           # Este arquivo
```

## 🚀 Deploy no Discloud

1. **Preparar os arquivos:**
   - Certifique-se de que `index.html`, `styles.css` e `discloud.config` estão na mesma pasta

2. **Fazer upload:**
   - Acesse [Discloud](https://discloud.com.br/)
   - Faça login ou crie uma conta
   - Clique em "Aplicações" → "Nova Aplicação"
   - Faça upload da pasta completa (zip) ou conecte seu repositório GitHub

3. **Configurar:**
   - A aplicação detectará automaticamente o `discloud.config`
   - Tipo: `web`
   - Main: `index.html`
   - Escolha o plano (gratuito disponível)

4. **Deploy:**
   - Clique em "Deploy"
   - Aguarde a conclusão
   - Seu site estará disponível em: `https://seuapp.discloud.app`

## 📝 Personalizações Importantes

### 1. Número do WhatsApp
No arquivo `index.html`, linha ~1415, substitua:
```
https://wa.me/5500000000000
```
Pelo seu número real no formato: `5500000000000` (DDD + número sem espaços)

### 2. Foto do Professor
Substitua o emoji `👨‍🏫` por uma foto real:
- Adicione uma imagem (ex: `professor.jpg`) na pasta
- No `index.html`, substitua:
```html
<span class="about-image-icon">👨‍🏫</span>
```
Por:
```html
<img src="professor.jpg" alt="Professor Ricardo Semerene" class="about-image-photo">
```

### 3. Cores (opcional)
Edite `styles.css` nas variáveis CSS `:root`:
```css
--primary: #1a365d;      /* Azul principal */
--accent: #e8a838;       /* Dourado */
```

## ✨ Funcionalidades

- ✅ Design responsivo (mobile, tablet, desktop)
- ✅ Navegação suave entre seções
- ✅ Menu mobile (hamburguer)
- ✅ Animações de entrada no scroll
- ✅ Botão "voltar ao topo"
- ✅ Integração com WhatsApp
- ✅ SEO otimizado (meta tags)

## 📱 Seções

1. **Hero** - Primeira dobra com headline e CTAs
2. **Quem Sou** - Sobre o professor e credenciais
3. **Crenças** - Filosofia de ensino
4. **Planos** - 4 opções de investimento
5. **Diferenciais** - O que diferencia o serviço
6. **Abordagem** - Metodologia em 5 passos
7. **Agendamento** - CTA final
8. **Footer** - Informações de contato

## 🛠️ Tecnologias

- HTML5 semântico
- CSS3 moderno (Flexbox, Grid, CSS Variables)
- JavaScript vanilla (sem frameworks)
- Google Fonts (Inter, Playfair Display)

## 📄 Licença

Todos os direitos reservados © 2026 Professor Ricardo Semerene.