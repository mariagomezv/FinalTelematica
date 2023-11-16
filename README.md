# FinalTelematica
## IMAGEN ASTRONOMICA DEL DIA
## Pasos:

 1. Crear una isntancia en aws ubuntu, de t3 small y que tenga
    habilitado el puerto 8000/tcp desde cualquier parte, ademas del ssh
  2. Ingresa a la instancia, preferiblemente por ssh y ajecuta el script:

   
	 

		    sudo apt update
            sudo apt install snap docker-compose -y
            sudo snap install terraform --classic
            git clone https://github.com/mariagomezv/FinalTelematica.git
            cd FinalTelematica/logic/
            terraform init
            sudo terraform apply -auto-approve

 2. Acceder a la ip publica desde google, por ej puerto 8000.    
		 ej: http://54.167.199.98:8000/
  4. Registrarse e iniciar sesion
  5. Deleitarse con la imagen del dia de la NASA
  
