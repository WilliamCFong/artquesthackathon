# Requirements
- docker
- docker-compose
- npm

## Installation
1. Run `docker-compose up --build` to construct project images
2. For first instantiation also run
   1. `docker-compose exec server migrate` to setup database schema
3. To load data from CABQ resources run
   - `docker-compose exec server python manage.py ingest_public_art`
 
