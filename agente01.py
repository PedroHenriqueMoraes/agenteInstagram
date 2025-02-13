from crewai import LLM, Agent, Task, Crew
import os
from crewai_tools import SerperDevTool
from dotenv import load_dotenv
from datetime import datetime, timedelta
from pydantic import BaseModel

load_dotenv()


class Image_output(BaseModel):
    prompt : str
class Nome_arquivo(BaseModel):
    nome_img : str
class Descricao_instagram(BaseModel):
    descricao_post : str


llm = LLM(
    model='gpt-4',
    api_key=os.getenv('OPENAI_API_KEY')
)

search_tool = SerperDevTool()

# Calculate yesterday's date for news filtering
yesterday = datetime.now() - timedelta(days=1)
yesterday_str = yesterday.strftime('%Y-%m-%d')


# Viral News Discovery Agent
viral_news_analyst = Agent(
    role='''You are an expert social media analyst specializing in tracking viral news across 
    multiple platforms including Twitter, LinkedIn, Facebook, and Reddit''',
    goal='''Identify the most viral news stories from the previous day across all major 
    social media platforms, focusing on engagement metrics and reach''',
    backstory='''You are a veteran social media analyst with extensive experience in 
    tracking viral content. You use advanced analytics tools to monitor engagement 
    rates, share counts, and discussion volume across platforms''',
    # tools=[search_tool]
)

# Hashtag Analysis Agent
hashtag_analyst = Agent(
    role='''You are a hashtag and trending topics specialist who analyzes social media 
    trends related to current news stories''',
    goal='''Track and analyze hashtags associated with viral news stories, identifying 
    patterns and measuring their impact''',
    backstory='''You have developed sophisticated methods for tracking hashtag 
    performance and understanding their relationship to news virality''',
    # tools=[search_tool]
)

# Viral Content Selection Agent
viral_selector = Agent(
    role='''You are a viral content curator who specializes in identifying the single 
    most impactful news story of the day''',
    goal='''Analyze multiple viral stories and their associated metrics to select the 
    most significant and engaging story''',
    backstory='''You have years of experience in content curation and understand what 
    makes a story truly viral and meaningful''',
    # tools=[search_tool]
)

# Story Update Tracker
update_tracker = Agent(
    role='''You are a news development specialist who tracks updates and new information 
    about viral stories''',
    goal='''Monitor and collect all updates, developments, and new information about 
    the selected viral story from the previous day''',
    backstory='''You are meticulous in tracking news developments and have expertise 
    in finding verified updates from reliable sources''',
    # tools=[search_tool]
)

# News Creation Specialist
news_writer = Agent(
    role='''You are an expert news writer specializing in creating comprehensive, 
    well-researched articles''',
    goal='''Create engaging, accurate, and professionally written news articles that 
    incorporate all relevant information and updates''',
    backstory='''You have extensive journalism experience and excel at crafting 
    compelling narratives while maintaining journalistic integrity''',
    # tools=[search_tool]
)

description_agent = Agent(
    role= '''Você é um social media no instagram de uma página de notícias, seu papel é fonercer as melhores descrições para o instagram''',
    goal= '''seu obijetivo é tornar notícias em uma descrição amigavel no instagram''',
    backstory= '''voce faz parte de uma agencia de social media e esta operando uma conta de notícia no instagram'''
)

search_photos_agent = Agent(
    role='''vocé é um engenheiro de prompt de geração de imagens''',
    goal= '''seu objetivo é criar prompts resumidos de imagem''',
    backstory='''voce faz parte de uma agencia de social media e esta operando uma conta de notícia no instagram''',
    tools= [search_tool]
)

# Task Definitions
find_viral_news = Task(
    description=f'''
    Find the most viral news stories from {yesterday_str}. Analyze:
    - Social media engagement metrics
    - Share counts across platforms
    - Comment volumes and discussion intensity
    - Cross-platform presence
    ''',
    expected_output='''
    Provide in Portuguese:
    1. Top 5 most viral stories from yesterday
    2. Engagement metrics for each story
    3. Platforms where each story had the most impact
    ''',
    agent=viral_news_analyst
)

analyze_hashtags = Task(
    description=f'''
    Analyze hashtags associated with viral news from {yesterday_str}. Focus on:
    - Trending hashtags related to viral stories
    - Hashtag engagement metrics
    - Cross-platform hashtag performance
    ''',
    expected_output='''
    Provide in Portuguese:
    1. Most impactful hashtags for each viral story
    2. Hashtag engagement statistics
    3. Platform-specific hashtag performance
    ''',
    agent=hashtag_analyst,
    context=[find_viral_news]
)

select_top_story = Task(
    description='''
    Analyze the viral stories and hashtag data to select the single most impactful 
    story of the day. Consider:
    - Total engagement across platforms
    - Story significance and relevance
    - Hashtag performance
    - Potential for ongoing development
    ''',
    expected_output='''
    Provide in Portuguese:
    1. Selected top story with justification
    2. Comprehensive engagement metrics
    3. Associated trending hashtags
    ''',
    agent=viral_selector,
    context=[find_viral_news, analyze_hashtags]
)

track_updates = Task(
    description=f'''
    Research all updates and new developments about the selected story from {yesterday_str}.
    Focus on:
    - New information and developments
    - Official statements and reactions
    - Expert analyses and perspectives
    - Fact-checking and verification
    ''',
    expected_output='''
    Provide in Portuguese:
    1. All verified updates about the story
    2. New developments and information
    3. Expert insights and reactions
    ''',
    agent=update_tracker,
    context=[select_top_story]
)

create_article = Task(
    description='''
    Create a comprehensive news article about the selected viral story. Include:
    - Main story details and context
    - Latest developments and updates
    - Social media impact and reactions
    - Expert perspectives and analysis
    ''',
    expected_output='''
    Provide in Portuguese:
    A complete, professional news article including:
    1. Headline and subheadline
    2. Main story content
    3. Latest updates and developments
    4. Social media context and impact
    5. Expert quotes and analysis
    6. At the end, create a section citing headlines from three current trending news stories
    ''',
    agent=news_writer,
    context=[select_top_story, track_updates],
    output_file= 'notícia.md'
    
)


search_images_task = Task(
    description='''
    você cria um prompt para gerar uma imagem de acordo com a notícia''',
    expected_output= '''
    voce deve criar um prompt bem elaborado para uma IA que gera imagem, esse prompt tem que ter relação com a notícia''',
    agent = search_photos_agent,
    context= [create_article],
    output_pydantic= Image_output
)

criador_de_arquivo = Task(
    description= '''crie um nome arquivo de acordo com a noticia''',
    expected_output= '''devolva somente um nome curto para um arquivo de foto referente a notícia''',
    context= [create_article],
    agent= news_writer,
    output_pydantic= Nome_arquivo

)

generate_description = Task(
    description='''
        Com base na seguinte notícia, crie uma legenda chamativa e envolvente para um post no Instagram.

    A legenda deve:
    - Resumir a notícia de forma clara e interessante.
    - Usar um tom apropriado ao tema (informativo, curioso, motivacional ou crítico).
    - Incluir emojis.
    - Ter entre 150 e 300 caracteres para melhor engajamento.
    - Incentivar a interação com perguntas ou chamadas para ação (ex: "O que você acha disso?", 
      "Comente sua opinião!", "Compartilhe com um amigo que precisa saber disso!").
    ''',
    expected_output= '''
    Uma única legenda no estilo de um post no Instagram, com emojis e chamada para ação (CTA).''',
    agent= description_agent,
    context= [create_article],
    output_pydantic = Descricao_instagram
)

# Crew Setup
crew = Crew(
    agents=[
        viral_news_analyst,
        hashtag_analyst,
        viral_selector,
        update_tracker,
        news_writer,
        search_photos_agent,
        description_agent

    ],
    tasks=[
        find_viral_news,
        analyze_hashtags,
        select_top_story,
        track_updates,
        create_article,
        search_images_task,
        generate_description,
        criador_de_arquivo
    ],
    verbose=True
)

# Execute the crew
result = crew.kickoff()

taskOutputPompt = search_images_task.output

taskOutputName = criador_de_arquivo.output

saidaDescricao = generate_description.output

#---------------------------------------------------------------

outputPydanticPrompt = taskOutputPompt.pydantic

outputPydanticName = taskOutputName.pydantic

pydanticDescricao = saidaDescricao.pydantic

promptImg = outputPydanticPrompt.prompt
print(promptImg)

nomeArquivo = outputPydanticName.nome_img
print(nomeArquivo)

descricaoPost = pydanticDescricao.descricao_post
print(descricaoPost)





