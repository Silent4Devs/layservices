from dynaconf import Dynaconf

settings = Dynaconf(
    envvar_prefix=False,  
    settings_files=[".env"], 
    load_dotenv=True,  
    environments=False,  
)