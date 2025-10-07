# src/services/openai_service.py

import openai
import json
import os
from dotenv import load_dotenv

load_dotenv()

def gerar_analise_e_prompt(api_key: str, transcricao_completa: str, info_cliente: dict, contexto_documentos: str = "") -> dict:
    openai.api_key = api_key
    
    prompt_mestre = f"""
    Sua tarefa é analisar a transcrição de uma reunião e o conteúdo de documentos de apoio para o cliente '{info_cliente.get('nome', 'N/A')}'.
    Os DOCUMENTOS DE APOIO são a fonte principal de verdade. A TRANSCRIÇÃO serve como contexto adicional.

    Gere um objeto JSON com duas chaves: "pre_analise" e "prompt_lovable".

    1.  **"pre_analise" (string, em português):**
        * Um documento de pré-análise detalhado. Comece com "Documento de Pré-Análise" e "Cliente: {info_cliente.get('nome', 'N/A')}".
        * Use o conteúdo dos documentos e da transcrição para preencher as seções: "Objetivo Principal:", "Público-Alvo:", "Funcionalidades Essenciais Detalhadas:" e "Requisitos Não-Funcionais e Observações:". Seja o mais específico possível.

    2.  **"prompt_lovable" (string, em inglês):**
        * Um prompt de UI detalhado para o Lovable.ai, baseado em todas as informações.
        * **Overview:** [Descrição da aplicação em 1 frase.]
        * **Style:** [Estilo visual, usando as cores primárias {info_cliente.get('cores', 'N/A')}.]
        * **Main Components:** [Descrição detalhada dos componentes da UI.]
        * **UI Language:** All UI text must be in Portuguese.

    **--- DOCUMENTOS DE APOIO ---**
    {contexto_documentos}
    **--- FIM DOS DOCUMENTOS ---**

    **--- TRANSCRIÇÃO DA REUNIÃO ---**
    {transcricao_completa}
    **--- FIM DA TRANSCRIÇÃO ---**

    Retorne APENAS o objeto JSON.
    """
    
    try:
        response = openai.chat.completions.create(
            model="gpt-4-turbo", 
            messages=[
                {"role": "system", "content": "Você é uma IA especialista em análise de negócios e requisitos de software. Sua saída deve ser um objeto JSON estruturado."},
                {"role": "user", "content": prompt_mestre}
            ],
            response_format={"type": "json_object"},
            temperature=0.2,
        )
        resultado_json = json.loads(response.choices[0].message.content)
        return resultado_json
    except Exception as e:
        print(f"Erro ao chamar a API da OpenAI: {e}")
        return {"pre_analise": "Ocorreu um erro ao gerar a análise.", "prompt_lovable": "Error generating prompt."}