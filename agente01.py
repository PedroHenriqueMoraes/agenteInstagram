from crewai import LLM, Agent, Task, Crew
import os
from crewai_tools import SerperDevTool
from dotenv import load_dotenv
from datetime import datetime, timedelta
from pydantic import BaseModel

load_dotenv()

llm = LLM(
    model= 'gpt-3.5-turbo'
)


class Image_output(BaseModel):
    prompt : str
class Nome_arquivo(BaseModel):
    nome_img : str
class Descricao_instagram(BaseModel):
    descricao_post : str

class CrewAgents:
    def __init__(self):
     
        self.tool = SerperDevTool()

        # Calculate yesterday's date for news filtering
        self.yesterday = datetime.now() - timedelta(days=1)
        self.yesterday_str = self.yesterday.strftime('%Y-%m-%d')

#------------------------------------------AGENTS---------------------------------------------------
    
    def _initialize_agents(self):
        # Viral News Discovery Agent
        self.viral_news_analyst = Agent(
            role='''You are an expert social media analyst specializing in tracking viral news across 
            multiple platforms including Twitter, LinkedIn, Facebook, and Reddit''',
            goal=f'''Identify the most viral news stories from the previous day {self.yesterday_str} across all major 
            social media platforms, focusing on engagement metrics and reach''',
            backstory='''You are a veteran social media analyst with extensive experience in 
            tracking viral content. You use advanced analytics tools to monitor engagement 
            rates, share counts, and discussion volume across platforms''',
            #tools=[self.tool]
            llm= llm
        )

        # Hashtag Analysis Agent
        self.hashtag_analyst = Agent(
            role='''You are a hashtag and trending topics specialist who analyzes social media 
            trends related to current news stories''',
            goal='''Track and analyze hashtags associated with viral news stories, identifying 
            patterns and measuring their impact''',
            backstory='''You have developed sophisticated methods for tracking hashtag 
            performance and understanding their relationship to news virality''',
            #tools=[self.tool]
            llm= llm
        )

        # Viral Content Selection Agent
        self.viral_selector = Agent(
            role='''You are a viral content curator who specializes in identifying the single 
            most impactful news story of the day''',
            goal='''Analyze multiple viral stories and their associated metrics to select the 
            most significant and engaging story''',
            backstory='''You have years of experience in content curation and understand what 
            makes a story truly viral and meaningful''',
            #tools=[self.tool]
            llm= llm
        )

        # Story Update Tracker
        self.update_tracker = Agent(
            role='''You are a news development specialist who tracks updates and new information 
            about viral stories''',
            goal='''Monitor and collect all updates, developments, and new information about 
            the selected viral story from the previous day''',
            backstory='''You are meticulous in tracking news developments and have expertise 
            in finding verified updates from reliable sources''',
            #tools=[self.tool]
            llm= llm
        )

        # News Creation Specialist
        self.news_writer = Agent(
            role='''You are an expert news writer specializing in creating comprehensive, 
            well-researched articles''',
            goal='''Create engaging, accurate, and professionally written news articles that 
            incorporate all relevant information and updates''',
            backstory='''You have extensive journalism experience and excel at crafting 
            compelling narratives while maintaining journalistic integrity''',
            tools=[self.tool],
            llm= llm
        )

        self.description_agent = Agent(
            role= '''Você é um social media no instagram de uma página de notícias, seu papel é fonercer as melhores descrições para o instagram''',
            goal= '''seu obijetivo é tornar notícias em uma descrição amigavel no instagram''',
            backstory= '''voce faz parte de uma agencia de social media e esta operando uma conta de notícia no instagram''',
            llm= llm
        )

        self.search_photos_agent = Agent(
            role='''vocé é um engenheiro de prompt de geração de imagens''',
            goal= '''seu objetivo é criar prompts resumidos de imagem''',
            backstory='''voce faz parte de uma agencia de social media e esta operando uma conta de notícia no instagram''',
            tools= [self.tool],
            llm= llm
        )

#------------------------------------------TASKS----------------------------------------------------

    def _initialize_taks(self):
        # Task Definitions
        self.find_viral_news = Task(
            description=f'''
            Find the most viral news stories from {self.yesterday_str}. Analyze:
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
            agent=self.viral_news_analyst
        )

        self.analyze_hashtags = Task(
            description=f'''
            Analyze hashtags associated with viral news from {self.yesterday_str}. Focus on:
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
            agent=self.hashtag_analyst,
            context=[self.find_viral_news]
        )

        self.select_top_story = Task(
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
            agent=self.viral_selector,
            context=[self.find_viral_news, self.analyze_hashtags]
        )

        self.track_updates = Task(
            description=f'''
            Research all updates and new developments about the selected story from {self.yesterday_str}.
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
            agent=self.update_tracker,
            context=[self.select_top_story]
        )

        self.create_article = Task(
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
            agent=self.news_writer,
            context=[self.select_top_story, self.track_updates],
            output_file= 'noticia.md'
        )


        self.search_images_task = Task(
            description='''
            você cria um prompt para gerar uma imagem de acordo com a notícia''',
            expected_output= '''
            voce deve criar um prompt de imagens ultra realista para uma IA que gera imagem, esse prompt tem que ter relação com a notícia e nunca violar as diretrizes da openai, não site nome de politicos ou pessoas reais''',
            agent = self.search_photos_agent,
            context= [self.create_article],
            output_pydantic= Image_output
        )

        self.criador_de_arquivo = Task(
            description= '''crie um nome arquivo de acordo com a noticia''',
            expected_output= '''devolva somente um nome curto para um arquivo de foto referente a notícia''',
            context= [self.create_article],
            agent= self.news_writer,
            output_pydantic= Nome_arquivo

        )

        self.generate_description = Task(
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
            agent= self.description_agent,
            context= [self.create_article],
            output_pydantic = Descricao_instagram
        )

#-----------------------------------------------CREW-SETUP------------------------------------------

    def createCrew(self):
        self.crew = Crew(
            agents=[
                self.viral_news_analyst,
                self.hashtag_analyst,
                self.viral_selector,
                self.update_tracker,
                self.news_writer,
                self.search_photos_agent,
                self.description_agent

            ],
            tasks=[
                self.find_viral_news,
                self.analyze_hashtags,
                self.select_top_story,
                self.track_updates,
                self.create_article,
                self.search_images_task,
                self.generate_description,
                self.criador_de_arquivo
            ],
            verbose=True
        )



        # Execute the crew
        result = self.crew.kickoff()
#---------------------------------------------OBJECTS-PYDANTIC--------------------------------------

    def formatted_output(self):

        taskOutputPompt = self.search_images_task.output
        taskOutputName = self.criador_de_arquivo.output
        saidaDescricao = self.generate_description.output

        #-----------------------------------------------------------------------------------------#
        
        outputPydanticPrompt = taskOutputPompt.pydantic
        outputPydanticName = taskOutputName.pydantic
        pydanticDescricao = saidaDescricao.pydantic

        self.promptImg = outputPydanticPrompt.prompt
        self.nomeArquivo = outputPydanticName.nome_img
        self.descricaoPost = pydanticDescricao.descricao_post

        return {
            "prompt": self.promptImg,
            "nome_arquivo": self.nomeArquivo,
            "descricao": self.descricaoPost
        }
        





