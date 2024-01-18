import plotly.express as px
from vizro_ai import VizroAI
from dotenv import load_dotenv
load_dotenv()
vizro_ai = VizroAI()
df = px.data.gapminder()
vizro_ai.plot(df, "describe the composition of gdp in continent, and add horizontal line for avg gdp", explain=True)