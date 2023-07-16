#%%
from str_convert import SceneAnalyzer
from dotenv import load_dotenv
import os

API_KEY = os.getenv("OPENAI_API_KEY")

analyzer = SceneAnalyzer(API_KEY, '내가죽던날_자막.srt')  
events = analyzer.process_subtitle()

events
# %%
