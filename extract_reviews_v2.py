deix"""
Script para extrair depoimentos do Google Maps do Professor Ricardo Semerene
Usando requests e BeautifulSoup
"""

import requests
import json
import re
import time

def extract_reviews():
    """
    Extrai reviews do Google Maps usando a API interna.
    O Google Maps carrega dados via JSON embutido na página.
    """
    
    # URL do Google Maps
    url = "https://www.google.com/maps/place/Ricardo+Semerene+%7C+Matem%C3%A1tica:+Concursos+e+Vestibulares/@-14.4095261,-51.31668,4z/data=!4m8!3m7!1s0x935ef1648bd3c255:0x3579eb3d26ddd7a8!8m2!3d-14.4095262!4d-51.31668!9m1!1b1!16s%2Fg%2F11z3l82rck?hl=pt-BR"
    
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
        'Accept-Language': 'pt-BR,pt;q=0.9,en-US;q=0.8,en;q=0.7',
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,*/*;q=0.8',
    }
    
    print("Fazendo requisição ao Google Maps...")
    session = requests.Session()
    session.headers.update(headers)
    
    try:
        response = session.get(url, timeout=30)
        response.raise_for_status()
        print(f"Status da resposta: {response.status_code}")
        
        html_content = response.text
        
        # O Google Maps embute dados em scripts
        # Procurar por dados de reviews no JSON embutido
        reviews = []
        
        # Padrão para encontrar dados de reviews no JSON
        # O Google usa um formato específico com arrays aninhados
        
        # Tentar encontrar o bloco de dados de reviews
        # Padrões comuns no HTML do Google Maps
        patterns = [
            r'\["https://localservice.*?"\s*,\s*\d+\s*,\s*\[.*?\]\s*,\s*\[(.*?)\]\s*,',
            r'"reviewContent":"(.*?)"',
            r'"text":"(.*?)"',
            r'role="article".*?<span[^>]*>(.*?)</span>',
        ]
        
        # Método 1: Procurar por dados estruturados
        # O Google Maps geralmente tem dados em formato JSON-LD
        json_ld_pattern = r'<script type="application/ld\+json">(.*?)</script>'
        json_ld_matches = re.findall(json_ld_pattern, html_content, re.DOTALL)
        
        if json_ld_matches:
            print("Encontrados dados JSON-LD!")
            for match in json_ld_matches:
                try:
                    data = json.loads(match)
                    if 'aggregateRating' in data:
                        rating = data['aggregateRating']
                        print(f"  Nota média: {rating.get('ratingValue', 'N/A')}")
                        print(f"  Total de avaliações: {rating.get('reviewCount', 'N/A')}")
                    
                    if 'review' in data:
                        for review in data['review']:
                            reviews.append({
                                'nome': review.get('author', {}).get('name', 'Anônimo'),
                                'nota': review.get('reviewRating', {}).get('ratingValue'),
                                'texto': review.get('reviewBody', ''),
                                'data': review.get('datePublished', 'Não identificada')
                            })
                except json.JSONDecodeError:
                    continue
        
        # Método 2: Procurar por reviews no HTML renderizado
        if not reviews:
            print("\nProcurando reviews no HTML...")
            
            # Padrão para encontrar blocos de review
            # O Google Maps usa classes específicas
            review_pattern = r'<div[^>]*class="[^"]*jftiEf[^"]*"[^>]*>(.*?)</div>\s*</div>\s*</div>'
            
            # Tentar encontrar seções de review
            section_pattern = r'<section[^>]*>.*?</section>'
            sections = re.findall(section_pattern, html_content, re.DOTALL)
            
            for section in sections:
                if 'review' in section.lower() or 'avalia' in section.lower():
                    print("Encontrada seção de reviews!")
                    # Extrair informações
                    name_matches = re.findall(r'<span[^>]*>([^<]+)</span>', section)
                    text_matches = re.findall(r'<span[^>]*class="[^"]*MyEned[^"]*"[^>]*>([^<]*)</span>', section)
                    
                    for name in name_matches[:10]:
                        if name.strip() and len(name) > 2:
                            reviews.append({
                                'nome': name.strip(),
                                'nota': None,
                                'texto': '',
                                'data': None
                            })
        
        # Método 3: Extrair do data atributo ou script
        if not reviews:
            print("\nTentando extrair de scripts inline...")
            
            # Procurar por dados em scripts
            script_pattern = r'window\._APP_INITIALIZATION_.*?=\s*(\{.*?\});'
            script_matches = re.findall(script_pattern, html_content, re.DOTALL)
            
            # Outro padrão comum
            if not script_matches:
                script_pattern = r'AF_initDataCallback\(\{[^}]*data:\s*(\[.*?\])'
                script_matches = re.findall(script_pattern, html_content, re.DOTALL)
            
            for match in script_matches:
                try:
                    # Tentar parsear como JSON/Python literal
                    import ast
                    data = ast.literal_eval(match[:50000])  # Limitar tamanho
                    print(f"Encontrados dados no script: {type(data)}")
                except:
                    continue
        
        return reviews
        
    except requests.RequestException as e:
        print(f"Erro na requisição: {e}")
        return []

def save_reviews(reviews, filename="depoimentos.json"):
    """Salva os reviews em um arquivo JSON"""
    with open(filename, 'w', encoding='utf-8') as f:
        json.dump(reviews, f, ensure_ascii=False, indent=2)
    print(f"\n{len(reviews)} depoimentos salvos em '{filename}'")

def main():
    print("=" * 60)
    print("Extrator de Depoimentos - Google Maps")
    print("Professor Ricardo Semerene")
    print("=" * 60)
    
    reviews = extract_reviews()
    
    if reviews:
        print(f"\nTotal de depoimentos encontrados: {len(reviews)}")
        save_reviews(reviews)
        
        # Salvar também em CSV
        import csv
        with open("depoimentos.csv", 'w', encoding='utf-8', newline='') as f:
            writer = csv.DictWriter(f, fieldnames=['nome', 'nota', 'texto', 'data'])
            writer.writeheader()
            writer.writerows(reviews)
        print("Depoimentos também salvos em 'depoimentos.csv'")
        
        # Exibir resumo
        print("\n" + "=" * 60)
        print("RESUMO DOS DEPOIMENTOS")
        print("=" * 60)
        for i, review in enumerate(reviews, 1):
            print(f"\n{i}. {review['nome']}")
            if review.get('nota'):
                print(f"   Nota: {review['nota']} estrelas")
            if review.get('texto'):
                print(f"   Texto: {review['texto'][:100]}...")
            if review.get('data'):
                print(f"   Data: {review['data']}")
    else:
        print("\nNenhum depoimento foi extraído via requests.")
        print("O Google Maps pode estar bloqueando requisições diretas.")
        print("\nAlternativas:")
        print("1. Usar Selenium com navegador visível (modo não-headless)")
        print("2. Usar a API oficial do Google Places (requer API key)")
        print("3. Copiar manualmente os depoimentos da página")

if __name__ == "__main__":
    main()