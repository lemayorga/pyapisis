Demo project which implement the following :
  
![My Skills](https://skillicons.dev/icons?i=py,fastapi,postgres,&theme=dark)

Lanzamos el comando para crear el entorno virtual:
# python -m venv venv
Y después lo activamos:

# Windows
.\venv\Scripts\activate
# Mac/linux
source venv/bin/activate


#database-migration-scripts
## create env
conda env create -f environment.yml

Instalar los modulos requerios al entorno virtual
# pip install -r requirements.txt 


Ejecutar el api rest
# kill $(pgrep -P $uvicorn_pid) src.main:app --reload 

Ejecutar el api rest, especificando el puerto
# cd src
# uvicorn src.main:app --reload  --port 8500



## directory structure
database-migration -----> postgresdb1 ---->mar7schema
-----> mar7table
## alembic init
alembic init <schemaname>
## create revision
alembic revision -m "-message"
## for local revision
export postgresdb=postgresql://postgres:my
